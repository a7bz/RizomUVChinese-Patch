"""覆盖率检查：对比「运行时采集到的界面字符串」与「词典已翻译条目」。

用法：
    python tools/check_coverage.py [--log 采集日志] [--misses 诊断文件] [--all]

两种数据来源：

* 采集日志（完整清单）：`%TEMP%\\rizomuv_collect_*.log`，每行 `标签<TAB>原文`。
  用它统计覆盖率——它记录了宿主调用过的**全部**字符串。

* 运行时诊断（未命中清单）：安装目录下的 `missing_strings.txt`，
  每行 `标签<TAB>次数<TAB>原文`（UTF-16LE，由 `RIZOMUV_ZH_DEBUG=1` 触发）。
  用它补齐最近一次运行里仍显示英文的条目。

未命中里有两类不算翻译缺失：

* 长段落片段：宿主把长帮助文本按行拆开后逐行绘制，采集到的单行只是
  某个词典键的一部分。运行时的 `lookup_fragment` 会按比例切出译文。
* 自绘文本：只在测量路径出现、从不经过绘制路径的字符串。宿主用自带的
  字形图集渲染它们（不调用 GDI 文字输出），钩子层无法替换；强行替换反而
  会让测量宽度与实际绘制不一致，导致排版错乱。
"""

from __future__ import annotations

import argparse
import glob
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "translations" / "dictionary_zh.json"

# 这些前缀/形状不是界面文本，不需要翻译
SKIP_PREFIX = (
    "Zom", "PREVIEW_", "wxWidgets", "Unofficial", "DISCLAIMER",
    "Current Directory", "RizomUV 2020", "On line Lua", "Can run releases",
    "This release build", "U...1...", "C:\\Users", "no data",
    "ZomLoad", "ZomSet", "ZomGenerate",
)

# 品牌名、单位、轴标记、鼠标按键缩写：保持原样
SKIP_EXACT = {
    "RizomUV", "RizomUV Legacy", "Maya", "3DSMax", "Softimage", "Rhino",
    "Rhino3D", "C4D", "Blender", "ZBrush", "Modo", "CUSTOMIZE",
    "Saved Custom", "RMB Orbit", "UV Mapping Application",
    "LMB", "RMB", "MMB", "DLMB", "Shift", "PAN", "ZOOM", "ORBIT",
    "SELECT", "DESELECT", "PELT", "Ed",
    "1:1", "bmp", "png", "jpg", "tiff", "ps", "px", "cm", "mm", "km",
    "dm", "in", "ft", "yd", "mi", "dpi", "Px",
    "default", "deviation", "edge", "enable", "Status: OK",
    "_999999", "_u_v", "S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
    "2014/2015", "2017/2018",
    # 轴标记：变换面板的坐标轴缩写，保持原样
    "U & V", "Tu", "Tv", "Su", "Sv", "Rw", "In",
}

DRAW_TAGS = {"ExtTextOutW", "TextOutW", "DrawTextW", "DrawStateW"}


def load_dict() -> dict[str, str]:
    data = json.loads(DICT.read_text(encoding="utf-8"))
    return data.get("translations", {})


def read_inventory(path: str) -> dict[str, set[str]]:
    """读采集日志，返回 {原文: {来源标签}}。"""
    text = Path(path).read_bytes().decode("utf-8", errors="replace")
    out: dict[str, set[str]] = {}
    for line in text.splitlines():
        if "\t" not in line:
            continue
        tag, body = line.split("\t", 1)
        if body:
            out.setdefault(body, set()).add(tag)
    return out


def read_misses(path: str) -> dict[str, int]:
    """读运行时诊断文件（UTF-16LE），返回 {原文: 调用次数}。"""
    raw = Path(path).read_bytes()
    text = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") \
        else raw.decode("utf-8", errors="replace")

    out: dict[str, int] = {}
    for line in text.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        try:
            count = int(parts[1])
        except ValueError:
            count = 1
        out[parts[-1]] = count
    return out


def find_inventory() -> list[str]:
    pattern = os.path.join(os.environ.get("TEMP", "."), "rizomuv_collect_*.log")
    return sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)


def find_misses() -> list[str]:
    found: list[str] = []
    for root in (Path(os.environ.get("TEMP", ".")), ROOT):
        found += glob.glob(str(root / "**" / "missing_strings.txt"), recursive=True)
    return sorted(found, key=os.path.getmtime, reverse=True)


def is_skip(t: str) -> bool:
    if len(t.strip()) <= 1:
        return True
    # 首尾空白是宿主的排版手段，运行时会去掉空白再查表，不算缺失
    t = t.strip()
    if all(c in "0123456789.+-°" for c in t):
        return True
    if t in SKIP_EXACT:
        return True
    # 鼠标组合键（LMB-Ctrl-Space 等）与轴标记（X+Y+、Box X-Y-）
    if t.startswith(("LMB", "RMB", "MMB", "DLMB")):
        return True
    if "X+" in t or "X-" in t or "Y+" in t or "Y-" in t:
        return True
    for p in SKIP_PREFIX:
        if t.startswith(p):
            return True
    if t.isupper() and len(t) > 16:
        return True
    if t.replace("_", "").isupper() and "_" in t:
        return True
    if any("\u4e00" <= c <= "\u9fff" for c in t):
        return True
    return False


def classify(missing: list[str], table: dict[str, str],
             tags: dict[str, set[str]]) -> tuple[list[str], list[str], list[str]]:
    """把未命中的条目分成：长段落片段 / 自绘文本 / 真正缺失。"""
    long_keys = [k for k in table if len(k) >= 60]

    def is_fragment(t: str) -> bool:
        if any(k.startswith(t) and len(k) > len(t) for k in table):
            return True
        return any(t in k for k in long_keys)

    def measure_only(t: str) -> bool:
        seen = tags.get(t, set())
        return bool(seen) and not (seen & DRAW_TAGS)

    fragments = [t for t in missing if is_fragment(t)]
    rest = [t for t in missing if t not in set(fragments)]
    measure = [t for t in rest if measure_only(t)]
    real = [t for t in rest if t not in set(measure)]
    return fragments, measure, real


def report_real(real: list[str], limit: int) -> None:
    if not real:
        return
    print(f"\n-- 缺失（前 {min(limit, len(real))} 条）--")
    for t in real[:limit]:
        print(f"  {t!r}")
    if len(real) > limit:
        print(f"  ... 还有 {len(real) - limit} 条，用 --all 查看")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", help="指定采集日志；省略则用 %TEMP% 下最新的")
    ap.add_argument("--misses", help="指定运行时诊断文件；省略则自动查找")
    ap.add_argument("--all", action="store_true", help="列出全部缺失项")
    args = ap.parse_args()

    table = load_dict()

    # ---- 完整清单：统计覆盖率
    logs = [args.log] if args.log else find_inventory()
    inventory: dict[str, set[str]] = {}
    for p in logs[:3]:
        for text, tags in read_inventory(p).items():
            inventory.setdefault(text, set()).update(tags)

    if inventory:
        candidates = sorted(t for t in inventory if not is_skip(t))
        missing = [t for t in candidates if t not in table]
        covered = len(candidates) - len(missing)
        fragments, measure, real = classify(missing, table, inventory)

        total = len(candidates)
        denom = total - len(fragments) - len(measure)
        pct = (covered * 100.0 / denom) if denom else 0.0

        print(f"界面字符串   : {total}")
        print(f"已翻译       : {covered}")
        print(f"长段落片段   : {len(fragments)}（按行拆分，运行时按比例切译文）")
        print(f"自绘文本     : {len(measure)}（宿主字形图集渲染，钩子无法介入）")
        print(f"真正缺失     : {len(real)}")
        print(f"覆盖率       : {pct:.1f}%")
        print(f"词典总条目   : {len(table)}")
        report_real(real, len(real) if args.all else 40)
        return 0

    # ---- 只有诊断文件：报告本次运行仍显示英文的条目
    misses = [args.misses] if args.misses else find_misses()
    if not misses:
        print("找不到采集日志或诊断文件。")
        print("采集：按 docs/development.md 运行 tools/collect_strings 采集一次。")
        print("诊断：设置 RIZOMUV_ZH_DEBUG=1 启动，正常退出后会写出 missing_strings.txt。")
        return 1

    observed: dict[str, int] = {}
    for p in misses[:3]:
        for text, count in read_misses(p).items():
            observed[text] = observed.get(text, 0) + count

    missing = sorted(t for t in observed if not is_skip(t) and t not in table)
    tags = {t: set() for t in observed}   # 诊断文件不带绘制/测量区分
    fragments, _, real = classify(missing, table, tags)

    print(f"诊断条目     : {len(observed)}")
    print(f"未命中       : {len(missing)}")
    print(f"长段落片段   : {len(fragments)}")
    print(f"真正缺失     : {len(real)}")
    print(f"词典总条目   : {len(table)}")
    print("\n提示：诊断文件只记录未命中项，无法据此算覆盖率。")
    print("      要统计覆盖率，请运行 tools/collect_strings 生成完整清单。")
    report_real(real, len(real) if args.all else 40)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
