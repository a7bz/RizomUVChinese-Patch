// 运行日志：写入 DLL 同目录，失败时回退到 %LOCALAPPDATA%。
#pragma once

namespace rzlog {

// 打开日志。path 为 DLL 所在目录。
void open(const wchar_t* dir);

// 关闭日志。
void close();

// 写入一行（UTF-8 转换由调用方完成，这里接收已编码的 UTF-8）。
void write(const char* line);

// 格式化写入 ASCII 诊断信息。
void printf(const char* fmt, ...);

// 日志文件完整路径（未打开时为空）。
const wchar_t* path();

}  // namespace rzlog
