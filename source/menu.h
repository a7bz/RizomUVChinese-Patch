// 原生菜单汉化。
//
// RizomUV 的菜单栏是真正的 Win32 HMENU（不是自绘），因此可以用
// SetMenuItemInfoW 直接替换文字，并保留 ID、快捷键、图标与子菜单。
//
// 时机很关键：宿主会反复重建菜单（切换编辑模式、更新勾选状态等）。
// 所以这里在启动阶段反复扫描一段时间，发现未翻译的菜单项就替换。
#pragma once

namespace menubar {

// 开始监视并汉化主窗口菜单。必须在 UI 线程之外调用（内部自建线程）。
void start();

// 停止监视。
void stop();

// 已翻译的菜单项数量。
int translated();

}  // namespace menubar
