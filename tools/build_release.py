"""打包发布产物。

产出到 release/ 目录：
  RizomUVChinese-Patch-vX.Y.Z.exe            单文件安装包（载荷已嵌入）
  RizomUVChinese-Patch-vX.Y.Z-Portable.zip   绿色版
  README-zh.txt                              使用说明
  manifest.json                              体积与 SHA-256

前提：
  * 运行 source/build.bat 得到 build/out 下的启动器与运行时（脚本会自动调用）；
  * csc.exe 可用（脚本会尝试自动定位，也可用环境变量 CSC_PATH 指定）。

用法：
    python tools/build_release.py [--version v1.0.0] [--skip-build]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD_OUT = BUILD / "out"
BUILD_SETUP = BUILD / "setup"
RELEASE = ROOT / "release"
GREEN = ROOT / "green"
TRANSLATIONS = ROOT / "translations"
INSTALLER = ROOT / "installer"

RUNTIME_DLL = "RizomUVChineseRuntime.dll"
LAUNCHER_EXE = "RizomUVChineseLauncher.exe"
DICTIONARY = "dictionary_zh.json"

GREEN_SCRIPTS = ["安装.bat", "卸载.bat", "查看状态.bat", "创建快捷方式.bat", "patch.ps1"]

CSC_CANDIDATES = [
    r"%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\Roslyn\csc.exe",
    r"%ProgramFiles%\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\Roslyn\csc.exe",
    r"%ProgramFiles%\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\Roslyn\csc.exe",
    r"%ProgramFiles%\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\Roslyn\csc.exe",
    r"%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\Roslyn\csc.exe",
    r"%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
]


def log(msg: str) -> None:
    print(msg, flush=True)


def expand(path: str) -> Path:
    return Path(os.path.expandvars(path))


def find_csc() -> Path | None:
    override = os.environ.get("CSC_PATH")
    if override:
        p = Path(override)
        if p.exists():
            return p
    for c in CSC_CANDIDATES:
        p = expand(c)
        if p.exists():
            return p
    return None


def run(cmd: list[str] | str) -> None:
    log(f"  $ {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
    result = subprocess.run(cmd, shell=isinstance(cmd, str))
    if result.returncode != 0:
        raise SystemExit(f"命令失败（{result.returncode}）")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------ 构建


def build_runtime() -> None:
    log("[1/3] 编译运行时与启动器")
    bat = ROOT / "source" / "build.bat"
    if not bat.exists():
        raise SystemExit(f"找不到 {bat}")
    run(f'cmd /c "{bat}"')
    for name in (RUNTIME_DLL, LAUNCHER_EXE):
        if not (BUILD_OUT / name).exists():
            raise SystemExit(f"编译后缺少 {name}")


def build_setup() -> None:
    log("[2/3] 编译安装器（嵌入载荷）")
    csc = find_csc()
    if csc is None:
        raise SystemExit("找不到 csc.exe，无法编译安装器。可用环境变量 CSC_PATH 指定。")

    BUILD_SETUP.mkdir(parents=True, exist_ok=True)
    out = BUILD_SETUP / "Setup.exe"

    # /resource: 把三个文件作为嵌入资源打进 Setup.exe，安装包因此是单文件
    resources = [
        f"/resource:{BUILD_OUT / LAUNCHER_EXE},{LAUNCHER_EXE}",
        f"/resource:{BUILD_OUT / RUNTIME_DLL},{RUNTIME_DLL}",
        f"/resource:{TRANSLATIONS / DICTIONARY},{DICTIONARY}",
    ]

    run([
        str(csc), "/nologo", "/target:winexe", f"/out:{out}",
        f"/win32manifest:{INSTALLER / 'app.manifest'}",
        "/r:System.dll", "/r:System.Drawing.dll", "/r:System.Windows.Forms.dll",
        *resources,
        str(INSTALLER / "Setup.cs"),
    ])
    if not out.exists():
        raise SystemExit("安装器编译失败")


# ------------------------------------------------------------------ 打包


def readme_text(version: str) -> str:
    return f"""RizomUV 简体中文补丁 v{version}
====================================

适用版本：RizomUV VS / RS 2020.1（rizomuv.exe）
汉化范围：菜单栏、面板标题、按钮、下拉选项、工具提示与说明文字

安装
----
双击 RizomUVChinese-Patch-v{version}.exe，选择 RizomUV 安装目录即可。
安装后请用桌面上的「RizomUV 中文版」启动；直接运行 rizomuv.exe 仍是英文。

静默安装：
    RizomUVChinese-Patch-v{version}.exe /S /dir="E:\\Program Files\\Rizom Lab\\RizomUV 2020.1"

卸载
----
安装包版：运行 RizomUVChinese-Patch-v{version}.exe /uninstall
绿色版：  运行「卸载.bat」

绿色版
------
Portable.zip 解压到任意位置，运行「安装.bat」，脚本会自动查找 RizomUV 安装目录。
其余脚本：
    卸载.bat          卸载并还原英文
    查看状态.bat      显示安装位置与词典词条数
    创建快捷方式.bat  重建桌面快捷方式

实现方式
--------
补丁不修改 rizomuv.exe，而是用一个启动器注入运行时 DLL，
在 IAT 层接管文字绘制与测量函数，把英文原文换成中文译文。
因此：
  * 原程序文件保持完整，卸载后即恢复英文；
  * 不需要改系统区域设置或代码页；
  * 直接运行 rizomuv.exe 不受任何影响。

本项目只分发界面翻译与加载工具，不包含 RizomUV 的任何程序文件，
请先自行安装正版软件。
"""


def stage_payload(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BUILD_OUT / RUNTIME_DLL, dest / RUNTIME_DLL)
    shutil.copy2(BUILD_OUT / LAUNCHER_EXE, dest / LAUNCHER_EXE)
    shutil.copy2(TRANSLATIONS / DICTIONARY, dest / DICTIONARY)


def package(version: str) -> list[Path]:
    log("[3/3] 打包")
    if RELEASE.exists():
        shutil.rmtree(RELEASE)
    RELEASE.mkdir(parents=True)

    readme = RELEASE / "README-zh.txt"
    readme.write_text(readme_text(version), encoding="utf-8-sig")

    # ---- 单文件安装包
    installer = RELEASE / f"RizomUVChinese-Patch-v{version}.exe"
    shutil.copy2(BUILD_SETUP / "Setup.exe", installer)

    # ---- 绿色版
    green_stage = BUILD / "green"
    if green_stage.exists():
        shutil.rmtree(green_stage)
    green_stage.mkdir(parents=True)

    for name in GREEN_SCRIPTS:
        src = GREEN / name
        if not src.exists():
            raise SystemExit(f"缺少绿色版脚本：{src}")
        shutil.copy2(src, green_stage / name)
    stage_payload(green_stage / "payload")

    portable = RELEASE / f"RizomUVChinese-Patch-v{version}-Portable.zip"
    entries = [(green_stage / n, n) for n in GREEN_SCRIPTS]
    entries += [
        (green_stage / "payload" / RUNTIME_DLL, f"payload/{RUNTIME_DLL}"),
        (green_stage / "payload" / LAUNCHER_EXE, f"payload/{LAUNCHER_EXE}"),
        (green_stage / "payload" / DICTIONARY, f"payload/{DICTIONARY}"),
        (readme, "README-zh.txt"),
    ]
    with zipfile.ZipFile(portable, "w", zipfile.ZIP_DEFLATED) as z:
        for src, arcname in entries:
            z.write(src, arcname)

    outputs = sorted(p for p in RELEASE.iterdir() if p.is_file())
    manifest = {
        "version": f"v{version}",
        "files": [
            {"name": p.name, "size": p.stat().st_size, "sha256": sha256(p)}
            for p in outputs
        ],
    }
    (RELEASE / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return outputs + [RELEASE / "manifest.json"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="1.0.0", help="版本号（不带 v 前缀）")
    ap.add_argument("--skip-build", action="store_true", help="跳过编译，用现有产物打包")
    args = ap.parse_args()

    version = args.version.lstrip("v")
    log(f"版本：v{version}")

    if not args.skip_build:
        build_runtime()
        build_setup()
    else:
        for p in (BUILD_OUT / RUNTIME_DLL, BUILD_OUT / LAUNCHER_EXE,
                  BUILD_SETUP / "Setup.exe", TRANSLATIONS / DICTIONARY):
            if not p.exists():
                raise SystemExit(f"缺少编译产物：{p}")

    outputs = package(version)

    log("")
    log("发布产物：")
    for p in outputs:
        log(f"  {p.name:<48} {p.stat().st_size:>12,} 字节")
    return 0


if __name__ == "__main__":
    sys.exit(main())
