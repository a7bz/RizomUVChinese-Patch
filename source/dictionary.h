// 词典：加载 UTF-8 JSON，提供只读的 UTF-16 查表。
//
// 词典格式：
//   {
//     "version": 1,
//     "translations": {
//       "Files": "文件",
//       "Unwrap": "展开"
//     }
//   }
//
// 匹配规则是**整串精确匹配**（区分大小写、保留空格与标点）。
// 不做子串替换，避免把 "Enable" 误伤到 "Enable Grid Snap" 之类的长句里。
#pragma once

#include <windows.h>

namespace dict {

// 从目录加载 dictionary_zh.json。成功返回 true。
bool load(const wchar_t* dir);

// 卸载并释放全部内存。
void unload();

// 查表。命中返回 UTF-16 译文指针（生命周期到 unload），未命中返回 nullptr。
// n 是英文的字符数（不含结尾 NUL）。
const wchar_t* lookup(const wchar_t* s, int n);

// 长文本片段查表。
//
// 宿主绘制帮助说明这类长段落时，会先按窗口宽度折行，再把每一行单独交给
// GDI 测量与绘制，所以词典里保存的整段原文永远匹配不上单行。
//
// 这里在长条目（原文 ≥ 60 字符）里找包含该行的那一条，然后按该行在原文中
// 的字符区间，等比例映射到译文里切出对应的中文片段。中文不需要词间空格，
// 逐行切出来的片段拼回去就是通顺的整段。
//
// 命中返回 UTF-16 指针（内部缓冲，调用方不要长期持有），未命中返回 nullptr。
const wchar_t* lookup_fragment(const wchar_t* s, int n);

// 已加载词条数。
int size();

// 加载状态描述（用于日志）。
const wchar_t* status();

}  // namespace dict
