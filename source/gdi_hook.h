// GDI 文字钩子：在 IAT 层接管宿主进程的文字绘制/测量入口。
//
// 为什么用 IAT 而不是内联补丁：
//   * 不修改宿主的任何指令字节，宿主完整性校验照常通过；
//   * 卸载只需把槽位写回原地址，进程退出前可完全还原；
//   * 宿主没有启用 Control Flow Guard 的间接调用不受影响。
//
// 覆盖的入口：
//   ExtTextOutW / TextOutW / DrawTextW          —— 绘制
//   GetTextExtentPoint32W / GetTextExtentExPointW —— 测量（决定控件宽度）
//   DrawStateW                                   —— 按钮/图标+文字
//
// 关键点：**绘制与测量必须用同一份译文**，否则控件会按英文宽度排版却画中文，
// 造成文字溢出或截断。
#pragma once

namespace gdihook {

// 安装钩子。返回被改写的 IAT 槽位数量。
int install();

// 卸载钩子，恢复原函数地址。
void uninstall();

// 已安装的槽位数量。
int installed();

// 各入口的命中计数（诊断用）。
struct Stats {
  unsigned long long draw;      // ExtTextOutW + TextOutW + DrawTextW + DrawStateW
  unsigned long long measure;   // GetTextExtent*
  unsigned long long hits;      // 实际命中词典
  unsigned long long missed;    // 未命中词典
  unsigned long long glyph;     // 以字形索引方式绘制（无法按字符串替换）
};
Stats stats();

// 把未命中的界面字符串写到文件（UTF-16LE），便于补词条。
// 仅在 debug_enabled() 为真时有意义。返回写入条数。
int dump_misses(const wchar_t* path);

// 是否启用未命中诊断（环境变量 RIZOMUV_ZH_DEBUG=1）。
bool debug_enabled();
void set_debug(bool on);

}  // namespace gdihook
