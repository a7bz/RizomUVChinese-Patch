<#
.SYNOPSIS
    RizomUV 简体中文补丁 —— 绿色版脚本。

.DESCRIPTION
    只往 RizomUV 安装目录新增三个文件（启动器、运行时 DLL、词典），
    不修改 rizomuv.exe，不写注册表。
    卸载时按状态文件删除这些文件；若安装前已存在同名文件则还原备份。

    由同目录的 .bat 调用，一般不需要直接运行。
#>
[CmdletBinding()]
param(
    [ValidateSet('install', 'uninstall', 'status', 'shortcut')]
    [string]$Action = 'install',

    [string]$Target = '',

    [switch]$Silent
)

$ErrorActionPreference = 'Stop'

$Script:PayloadNames = @(
    'RizomUVChineseLauncher.exe',
    'RizomUVChineseRuntime.dll',
    'dictionary_zh.json'
)
$Script:StateFile = 'chinese_patch.json'
$Script:BackupDir = 'chinese_patch_backup'
$Script:HostExe = 'rizomuv.exe'
$Script:ShortcutName = 'RizomUV 中文版.lnk'

# ------------------------------------------------------------------ 输出

function Write-Title([string]$Text) {
    Write-Host ''
    Write-Host "  $Text" -ForegroundColor Cyan
    Write-Host ('  ' + ('-' * ($Text.Length + 2))) -ForegroundColor DarkGray
}

function Write-Ok([string]$Text) { Write-Host "  [完成] $Text" -ForegroundColor Green }
function Write-Info([string]$Text) { Write-Host "  $Text" }
function Write-Warn([string]$Text) { Write-Host "  [注意] $Text" -ForegroundColor Yellow }
function Write-Err([string]$Text) { Write-Host "  [错误] $Text" -ForegroundColor Red }

function Pause-IfInteractive {
    if (-not $Silent) {
        Write-Host ''
        Read-Host '  按回车键退出' | Out-Null
    }
}

# ------------------------------------------------------------------ 定位安装目录

function Get-CandidateDirs {
    $seen = New-Object System.Collections.Generic.HashSet[string]
    $out = New-Object System.Collections.Generic.List[string]

    function Add-Candidate([string]$dir) {
        if ([string]::IsNullOrWhiteSpace($dir)) { return }
        $full = $dir.TrimEnd('\', '/')
        if (-not $seen.Add($full.ToLowerInvariant())) { return }
        if (Test-Path (Join-Path $full $Script:HostExe)) { $out.Add($full) }
    }

    # 1. 注册表里的卸载信息
    $uninstallRoots = @(
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
        'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
        'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    )
    foreach ($root in $uninstallRoots) {
        if (-not (Test-Path $root)) { continue }
        Get-ChildItem $root -ErrorAction SilentlyContinue | ForEach-Object {
            $props = Get-ItemProperty $_.PSPath -ErrorAction SilentlyContinue
            if (-not $props) { return }
            if ($props.DisplayName -notlike '*RizomUV*') { return }
            if ($props.InstallLocation) { Add-Candidate $props.InstallLocation }
            if ($props.DisplayIcon) {
                $icon = $props.DisplayIcon -replace '^"', '' -replace '",.*$', ''
                Add-Candidate (Split-Path -Parent $icon)
            }
        }
    }

    # 2. Program Files 下的常见布局
    foreach ($base in @($env:ProgramFiles, ${env:ProgramFiles(x86)})) {
        if (-not $base) { continue }
        foreach ($vendor in @('Rizom Lab', 'Rizom-Lab', 'RizomUV')) {
            $root = Join-Path $base $vendor
            if (-not (Test-Path $root)) { continue }
            Add-Candidate $root
            Get-ChildItem $root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
                Add-Candidate $_.FullName
            }
        }
    }

    return $out
}

function Resolve-Target {
    if ($Target) {
        $p = $Target.Trim('"').TrimEnd('\', '/')
        if (Test-Path (Join-Path $p $Script:HostExe)) { return $p }
        throw "指定的目录里没有 $($Script:HostExe)：$p"
    }

    $candidates = @(Get-CandidateDirs)
    if ($candidates.Count -eq 1) { return $candidates[0] }
    if ($candidates.Count -gt 1) {
        Write-Info '找到多个可能的安装目录：'
        for ($i = 0; $i -lt $candidates.Count; $i++) {
            Write-Info ("    [{0}] {1}" -f ($i + 1), $candidates[$i])
        }
        if ($Silent) { return $candidates[0] }
        $pick = Read-Host "  请选择 [1-$($candidates.Count)]，直接回车使用第 1 个"
        if ([string]::IsNullOrWhiteSpace($pick)) { return $candidates[0] }
        $n = 0
        if ([int]::TryParse($pick, [ref]$n) -and $n -ge 1 -and $n -le $candidates.Count) {
            return $candidates[$n - 1]
        }
        return $candidates[0]
    }

    if ($Silent) { throw "没有找到 RizomUV 安装目录。" }

    Write-Warn '没有自动找到 RizomUV 安装目录。'
    $manual = Read-Host '  请粘贴安装目录路径（包含 rizomuv.exe）'
    $manual = $manual.Trim('"').TrimEnd('\', '/')
    if (-not (Test-Path (Join-Path $manual $Script:HostExe))) {
        throw "该目录里没有 $($Script:HostExe)：$manual"
    }
    return $manual
}

function Get-InstalledTargets {
    $found = New-Object System.Collections.Generic.List[string]
    foreach ($dir in @(Get-CandidateDirs)) {
        if (Test-Path (Join-Path $dir $Script:StateFile)) { $found.Add($dir) }
    }
    # 脚本所在目录本身也可能是安装目录（把绿色版直接解压进安装目录的情况）
    $here = Split-Path -Parent $PSCommandPath
    if ((Test-Path (Join-Path $here $Script:StateFile)) -and -not $found.Contains($here)) {
        $found.Add($here)
    }
    return $found
}

# ------------------------------------------------------------------ 状态文件

function Write-State([string]$Dir, $Records) {
    $payload = [ordered]@{
        version = 1
        target  = $Dir
        files   = @($Records | ForEach-Object {
            [ordered]@{ name = $_.name; existed = [bool]$_.existed }
        })
    }
    $json = $payload | ConvertTo-Json -Depth 5
    $path = Join-Path $Dir $Script:StateFile
    [System.IO.File]::WriteAllText($path, $json, (New-Object System.Text.UTF8Encoding($false)))
}

function Read-State([string]$Dir) {
    $path = Join-Path $Dir $Script:StateFile
    if (-not (Test-Path $path)) { return $null }
    try {
        return (Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json)
    } catch {
        return $null
    }
}

# ------------------------------------------------------------------ 快捷方式

function New-DesktopShortcut([string]$Dir) {
    $desktop = [Environment]::GetFolderPath('DesktopDirectory')
    $link = Join-Path $desktop $Script:ShortcutName
    $exe = Join-Path $Dir 'RizomUVChineseLauncher.exe'

    $shell = New-Object -ComObject WScript.Shell
    $sc = $shell.CreateShortcut($link)
    $sc.TargetPath = $exe
    $sc.WorkingDirectory = $Dir
    $sc.IconLocation = (Join-Path $Dir $Script:HostExe) + ',0'
    $sc.Description = 'RizomUV（简体中文界面）'
    $sc.Save()
    return $link
}

# ------------------------------------------------------------------ 动作

function Invoke-Install {
    Write-Title 'RizomUV 简体中文补丁 —— 安装'

    $dir = Resolve-Target
    Write-Info "安装目录：$dir"

    $here = Split-Path -Parent $PSCommandPath
    $payloadDir = Join-Path $here 'payload'
    if (-not (Test-Path $payloadDir)) { $payloadDir = $here }

    foreach ($name in $Script:PayloadNames) {
        if (-not (Test-Path (Join-Path $payloadDir $name))) {
            throw "补丁文件不完整，缺少 $name。请重新解压绿色版压缩包。"
        }
    }

    # 运行中的程序会锁住 DLL，先提示退出
    $running = Get-Process -Name 'rizomuv' -ErrorAction SilentlyContinue
    if ($running) {
        Write-Warn 'RizomUV 正在运行，请先关闭程序。'
        if (-not $Silent) {
            Read-Host '  关闭后按回车继续' | Out-Null
        }
        $running = Get-Process -Name 'rizomuv' -ErrorAction SilentlyContinue
        if ($running) { throw 'RizomUV 仍在运行，已中止安装。' }
    }

    # 已有安装记录则先卸载，避免旧版本残留
    if (Test-Path (Join-Path $dir $Script:StateFile)) {
        Write-Info '检测到旧版本，先移除旧文件…'
        Invoke-Uninstall -Dir $dir -Quiet
    }

    $backup = Join-Path $dir $Script:BackupDir
    New-Item -ItemType Directory -Force -Path $backup | Out-Null

    $records = @()
    foreach ($name in $Script:PayloadNames) {
        $dest = Join-Path $dir $name
        $existed = Test-Path $dest
        if ($existed) {
            Copy-Item $dest (Join-Path $backup $name) -Force
        }
        Copy-Item (Join-Path $payloadDir $name) $dest -Force
        $records += [pscustomobject]@{ name = $name; existed = $existed }
        Write-Info "  写入 $name"
    }

    Write-State $dir $records

    try {
        $link = New-DesktopShortcut $dir
        Write-Info "  创建快捷方式：$link"
    } catch {
        Write-Warn "快捷方式创建失败（不影响使用）：$($_.Exception.Message)"
    }

    Write-Ok '安装完成。'
    Write-Host ''
    Write-Info '以后请用桌面上的「RizomUV 中文版」启动，'
    Write-Info '直接运行 rizomuv.exe 仍然是英文界面。'
    Pause-IfInteractive
}

function Invoke-Uninstall {
    param(
        [string]$Dir = '',
        [switch]$Quiet
    )

    if (-not $Quiet) { Write-Title 'RizomUV 简体中文补丁 —— 卸载' }

    if (-not $Dir) {
        $targets = @(Get-InstalledTargets)
        if ($targets.Count -eq 0) {
            if (-not $Quiet) {
                Write-Warn '没有找到已安装的汉化补丁。'
                Pause-IfInteractive
            }
            return
        }
        $Dir = $targets[0]
        if ($targets.Count -gt 1 -and -not $Silent) {
            Write-Info '找到多个安装位置：'
            for ($i = 0; $i -lt $targets.Count; $i++) {
                Write-Info ("    [{0}] {1}" -f ($i + 1), $targets[$i])
            }
            $pick = Read-Host "  请选择 [1-$($targets.Count)]，直接回车使用第 1 个"
            $n = 0
            if ([int]::TryParse($pick, [ref]$n) -and $n -ge 1 -and $n -le $targets.Count) {
                $Dir = $targets[$n - 1]
            }
        }
    }

    if (-not $Quiet) { Write-Info "安装目录：$Dir" }

    $state = Read-State $Dir
    $backup = Join-Path $Dir $Script:BackupDir

    if ($state -and $state.files) {
        foreach ($rec in $state.files) {
            $dest = Join-Path $Dir $rec.name
            $saved = Join-Path $backup $rec.name
            try {
                if ($rec.existed -and (Test-Path $saved)) {
                    Copy-Item $saved $dest -Force
                    if (-not $Quiet) { Write-Info "  还原 $($rec.name)" }
                } elseif (Test-Path $dest) {
                    Remove-Item $dest -Force
                    if (-not $Quiet) { Write-Info "  删除 $($rec.name)" }
                }
            } catch {
                Write-Warn "无法处理 $($rec.name)：$($_.Exception.Message)"
            }
        }
    } else {
        # 没有状态文件时按已知文件名清理，只删我们自己的文件
        foreach ($name in $Script:PayloadNames) {
            $dest = Join-Path $Dir $name
            if (Test-Path $dest) {
                try {
                    Remove-Item $dest -Force
                    if (-not $Quiet) { Write-Info "  删除 $name" }
                } catch {
                    Write-Warn "无法删除 $name：$($_.Exception.Message)"
                }
            }
        }
    }

    if (Test-Path $backup) {
        Remove-Item $backup -Recurse -Force -ErrorAction SilentlyContinue
    }
    Remove-Item (Join-Path $Dir $Script:StateFile) -Force -ErrorAction SilentlyContinue

    $link = Join-Path ([Environment]::GetFolderPath('DesktopDirectory')) $Script:ShortcutName
    Remove-Item $link -Force -ErrorAction SilentlyContinue

    if (-not $Quiet) {
        Write-Ok '卸载完成，界面已恢复英文。'
        Pause-IfInteractive
    }
}

function Invoke-Status {
    Write-Title 'RizomUV 简体中文补丁 —— 状态'

    # 显式指定目录时只看这一个，便于排查。
    if ($Target) {
        $targets = @($Target.Trim('"').TrimEnd('\', '/'))
    } else {
        $targets = @(Get-InstalledTargets)
    }
    if ($targets.Count -eq 0) {
        Write-Info '当前没有安装汉化补丁。'
        Write-Host ''
        $all = @(Get-CandidateDirs)
        if ($all.Count -gt 0) {
            Write-Info '检测到的 RizomUV 安装目录：'
            foreach ($d in $all) { Write-Info "    $d" }
        } else {
            Write-Info '也没有找到 RizomUV 安装目录。'
        }
        Pause-IfInteractive
        return
    }

    foreach ($dir in $targets) {
        Write-Info "安装目录：$dir"
        $state = Read-State $dir
        if ($state -and $state.files) {
            foreach ($rec in $state.files) {
                $dest = Join-Path $dir $rec.name
                $mark = if (Test-Path $dest) { '存在' } else { '缺失' }
                Write-Info ("    {0,-32} {1}" -f $rec.name, $mark)
            }
        }

        $dict = Join-Path $dir 'dictionary_zh.json'
        if (Test-Path $dict) {
            # 词典里存在仅大小写不同的键（运行时的匹配区分大小写，两者都要保留），
            # 而 PowerShell 的 ConvertFrom-Json 不区分大小写、会报重复键。
            # 这里只统计顶层条目数，不走 JSON 解析。
            $text = Get-Content $dict -Raw -Encoding UTF8
            $count = ([regex]::Matches($text, '^\s{2}"', 'Multiline')).Count
            if ($count -gt 0) {
                Write-Info "    词典词条：$count"
            } else {
                Write-Warn '    词典文件为空或格式异常。'
            }
        }

        $log = Join-Path $dir 'RizomUVChineseRuntime.log'
        if (Test-Path $log) {
            Write-Info "    运行日志：$log"
        }
    }

    Write-Host ''
    Write-Info '用桌面「RizomUV 中文版」启动即为中文；运行 rizomuv.exe 为英文。'
    Pause-IfInteractive
}

function Invoke-Shortcut {
    Write-Title '创建桌面快捷方式'

    $targets = @(Get-InstalledTargets)
    if ($targets.Count -eq 0) {
        Write-Warn '请先安装汉化补丁。'
        Pause-IfInteractive
        return
    }

    $link = New-DesktopShortcut $targets[0]
    Write-Ok "已创建：$link"
    Pause-IfInteractive
}

# ------------------------------------------------------------------ 入口

try {
    switch ($Action) {
        'install'   { Invoke-Install }
        # 显式指定 -Target 时优先用它，否则按状态文件自动查找。
        'uninstall' { Invoke-Uninstall -Dir $Target }
        'status'    { Invoke-Status }
        'shortcut'  { Invoke-Shortcut }
    }
} catch {
    Write-Host ''
    Write-Err $_.Exception.Message
    Pause-IfInteractive
    exit 1
}
