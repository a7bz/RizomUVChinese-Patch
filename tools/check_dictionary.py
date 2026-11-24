"""词典自检：格式、空值、编码问题、可疑译文。

用法：
    python tools/check_dictionary.py

错误（error）会让脚本以非零状态退出，用于发布前守门；
提示（note）只是信息，不影响退出码。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "translations" / "dictionary_zh.json"

# 译文里不该出现的字符
BAD_CHARS = {
    "\ufffd": "替换字符（编码损坏）",
    "\t": "制表符（界面里会被当作普通字符绘制）",
    "\r": "回车符",
    "\n": "换行符（单行控件会显示异常）",
}

CJK = re.compile(r"[\u4e00-\u9fff]")

# 保持原样的品牌名与单位：译文与原文相同是预期行为
SAME_OK = {
    "RGB", "HSL", "HSV", "UV", "UDIM", "3D", "XY", "YZ", "ZX",
    "px/cm", "px/mm", "tx/cm", "tx/dm", "tx/ft", "tx/in", "tx/km",
    "tx/m", "tx/mi", "tx/mm", "tx/yd", "px", "mm", "cm", "km", "dm",
    "in", "ft", "yd", "mi", "dpi", "1:1",
}


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []

    if not DICT.exists():
        print(f"找不到词典文件：{DICT}")
        return 1

    raw = DICT.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append("文件带 UTF-8 BOM；运行时解析器不接受，请保存为无 BOM 的 UTF-8")

    try:
        data = json.loads(raw.decode("utf-8-sig"))
    except json.JSONDecodeError as exc:
        print(f"JSON 解析失败：{exc}")
        return 1

    if not isinstance(data, dict):
        print("顶层必须是对象")
        return 1

    if data.get("version") != 1:
        errors.append(f"version 应为 1，实际为 {data.get('version')!r}")

    table = data.get("translations")
    if not isinstance(table, dict):
        print("缺少 translations 对象")
        return 1
    if not table:
        errors.append("translations 为空")

    for en, zh in table.items():
        if not isinstance(en, str) or not isinstance(zh, str):
            errors.append(f"键值必须是字符串：{en!r} -> {zh!r}")
            continue
        if not en.strip():
            errors.append("存在空的英文键")
            continue
        if en != en.strip():
            # 宿主里确实存在带尾随空格的条目（如 "Grow "），保留但提示
            notes.append(f"英文键首尾有空白：{en!r}")
        if not zh.strip():
            errors.append(f"译文为空：{en!r}")
            continue
        if en == zh and not CJK.search(zh) and en not in SAME_OK:
            notes.append(f"译文与原文相同：{en!r}")

        for ch, why in BAD_CHARS.items():
            if ch in zh:
                errors.append(f"译文含{why}：{en!r} -> {zh!r}")

    total_chars = sum(
        len(k) + len(v) for k, v in table.items()
        if isinstance(k, str) and isinstance(v, str)
    )

    print(f"词典文件 : {DICT.name}")
    print(f"词条数量 : {len(table)}")
    print(f"字符总量 : {total_chars}")

    if notes:
        print(f"\n提示 {len(notes)} 条：")
        for n in notes[:20]:
            print(f"  - {n}")
        if len(notes) > 20:
            print(f"  ... 还有 {len(notes) - 20} 条")

    if errors:
        print(f"\n错误 {len(errors)} 个：")
        for e in errors[:50]:
            print(f"  - {e}")
        if len(errors) > 50:
            print(f"  ... 还有 {len(errors) - 50} 个")
        return 1

    print("\n自检通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
