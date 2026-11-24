#include "dictionary.h"

#include <string>
#include <unordered_map>
#include <vector>

#include "log.h"

namespace dict {
namespace {

struct Entry {
  std::wstring zh;
};

std::unordered_map<std::wstring, std::wstring> g_map;
bool g_loaded = false;
wchar_t g_status[512] = L"未加载";

// 长条目索引：宿主会把长段落按行拆开绘制，整串匹配必然失败。
// 这里单独保存长原文与译文，供 lookup_fragment 做区间映射。
struct LongEntry {
  std::wstring en;
  std::wstring zh;
};
std::vector<LongEntry> g_long;
constexpr size_t kLongThreshold = 60;

// ---------- UTF-8 -> UTF-16 ----------
void append_utf8_as_wstring(std::wstring& out, const std::string& s) {
  size_t i = 0;
  while (i < s.size()) {
    unsigned char c = (unsigned char)s[i];
    unsigned int cp = 0;
    int extra = 0;
    if (c < 0x80) { cp = c; extra = 0; }
    else if ((c & 0xE0) == 0xC0) { cp = c & 0x1F; extra = 1; }
    else if ((c & 0xF0) == 0xE0) { cp = c & 0x0F; extra = 2; }
    else if ((c & 0xF8) == 0xF0) { cp = c & 0x07; extra = 3; }
    else { i++; continue; }  // 非法字节，跳过

    if (i + extra >= s.size()) break;
    bool ok = true;
    for (int k = 1; k <= extra; k++) {
      unsigned char cc = (unsigned char)s[i + k];
      if ((cc & 0xC0) != 0x80) { ok = false; break; }
      cp = (cp << 6) | (cc & 0x3F);
    }
    i += extra + 1;
    if (!ok) continue;

    if (cp <= 0xFFFF) {
      out.push_back((wchar_t)cp);
    } else {
      cp -= 0x10000;
      out.push_back((wchar_t)(0xD800 + (cp >> 10)));
      out.push_back((wchar_t)(0xDC00 + (cp & 0x3FF)));
    }
  }
}

// ---------- 极简 JSON 解析 ----------
// 只支持对象 / 字符串 / 数字 / 布尔 / null，足够读取词典。
struct Json {
  const std::string& s;
  size_t i = 0;
  explicit Json(const std::string& text) : s(text) {}

  void ws() {
    while (i < s.size()) {
      char c = s[i];
      if (c == ' ' || c == '\t' || c == '\n' || c == '\r') i++;
      else break;
    }
  }

  bool eat(char c) {
    ws();
    if (i < s.size() && s[i] == c) { i++; return true; }
    return false;
  }

  bool parse_string(std::string& out) {
    ws();
    if (i >= s.size() || s[i] != '"') return false;
    i++;
    out.clear();
    while (i < s.size()) {
      char c = s[i++];
      if (c == '"') return true;
      if (c != '\\') { out.push_back(c); continue; }
      if (i >= s.size()) return false;
      char e = s[i++];
      switch (e) {
        case '"': out.push_back('"'); break;
        case '\\': out.push_back('\\'); break;
        case '/': out.push_back('/'); break;
        case 'b': out.push_back('\b'); break;
        case 'f': out.push_back('\f'); break;
        case 'n': out.push_back('\n'); break;
        case 'r': out.push_back('\r'); break;
        case 't': out.push_back('\t'); break;
        case 'u': {
          if (i + 4 > s.size()) return false;
          unsigned int cp = 0;
          for (int k = 0; k < 4; k++) {
            char h = s[i++];
            cp <<= 4;
            if (h >= '0' && h <= '9') cp |= (unsigned)(h - '0');
            else if (h >= 'a' && h <= 'f') cp |= (unsigned)(h - 'a' + 10);
            else if (h >= 'A' && h <= 'F') cp |= (unsigned)(h - 'A' + 10);
            else return false;
          }
          // 代理对
          if (cp >= 0xD800 && cp <= 0xDBFF && i + 6 <= s.size() &&
              s[i] == '\\' && s[i + 1] == 'u') {
            size_t save = i;
            i += 2;
            unsigned int lo = 0;
            bool ok = true;
            for (int k = 0; k < 4; k++) {
              char h = s[i++];
              lo <<= 4;
              if (h >= '0' && h <= '9') lo |= (unsigned)(h - '0');
              else if (h >= 'a' && h <= 'f') lo |= (unsigned)(h - 'a' + 10);
              else if (h >= 'A' && h <= 'F') lo |= (unsigned)(h - 'A' + 10);
              else { ok = false; break; }
            }
            if (ok && lo >= 0xDC00 && lo <= 0xDFFF) {
              unsigned int full = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00);
              out.push_back((char)(unsigned char)(0xF0 | (full >> 18)));
              out.push_back((char)(unsigned char)(0x80 | ((full >> 12) & 0x3F)));
              out.push_back((char)(unsigned char)(0x80 | ((full >> 6) & 0x3F)));
              out.push_back((char)(unsigned char)(0x80 | (full & 0x3F)));
            } else {
              i = save;
              // 孤立高代理，按替换字符处理
              out += "\xEF\xBF\xBD";
            }
          } else if (cp >= 0xDC00 && cp <= 0xDFFF) {
            out += "\xEF\xBF\xBD";
          } else if (cp < 0x80) {
            out.push_back((char)(unsigned char)cp);
          } else if (cp < 0x800) {
            out.push_back((char)(unsigned char)(0xC0 | (cp >> 6)));
            out.push_back((char)(unsigned char)(0x80 | (cp & 0x3F)));
          } else {
            out.push_back((char)(unsigned char)(0xE0 | (cp >> 12)));
            out.push_back((char)(unsigned char)(0x80 | ((cp >> 6) & 0x3F)));
            out.push_back((char)(unsigned char)(0x80 | (cp & 0x3F)));
          }
          break;
        }
        default: return false;
      }
    }
    return false;
  }

  bool skip_value(int depth = 0) {
    if (depth > 32) return false;
    ws();
    if (i >= s.size()) return false;
    char c = s[i];
    if (c == '"') { std::string tmp; return parse_string(tmp); }
    if (c == '{') {
      i++;
      if (eat('}')) return true;
      while (true) {
        std::string k;
        if (!parse_string(k)) return false;
        if (!eat(':')) return false;
        if (!skip_value(depth + 1)) return false;
        if (eat(',')) continue;
        return eat('}');
      }
    }
    if (c == '[') {
      i++;
      if (eat(']')) return true;
      while (true) {
        if (!skip_value(depth + 1)) return false;
        if (eat(',')) continue;
        return eat(']');
      }
    }
    // 数字 / 布尔 / null
    while (i < s.size()) {
      char d = s[i];
      if (d == ',' || d == '}' || d == ']' || d == ' ' || d == '\n' || d == '\r' || d == '\t') break;
      i++;
    }
    return true;
  }
};

bool read_file(const wchar_t* path, std::string& out) {
  HANDLE h = CreateFileW(path, GENERIC_READ, FILE_SHARE_READ, nullptr,
                         OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
  if (h == INVALID_HANDLE_VALUE) return false;
  LARGE_INTEGER size = {0};
  if (!GetFileSizeEx(h, &size) || size.QuadPart <= 0 || size.QuadPart > (64 << 20)) {
    CloseHandle(h);
    return false;
  }
  out.resize((size_t)size.QuadPart);
  DWORD read = 0;
  BOOL ok = ReadFile(h, &out[0], (DWORD)out.size(), &read, nullptr);
  CloseHandle(h);
  if (!ok) return false;
  out.resize(read);
  return true;
}

}  // namespace

bool load(const wchar_t* dir) {
  unload();

  wchar_t path[MAX_PATH];
  _snwprintf_s(path, MAX_PATH, _TRUNCATE, L"%s\\dictionary_zh.json", dir);

  std::string raw;
  if (!read_file(path, raw)) {
    wcscpy_s(g_status, L"找不到 dictionary_zh.json，保持英文");
    rzlog::write("[词典] 未找到 dictionary_zh.json，界面保持英文");
    return false;
  }

  // 去掉 UTF-8 BOM
  if (raw.size() >= 3 && (unsigned char)raw[0] == 0xEF &&
      (unsigned char)raw[1] == 0xBB && (unsigned char)raw[2] == 0xBF) {
    raw.erase(0, 3);
  }

  Json j(raw);
  if (!j.eat('{')) {
    wcscpy_s(g_status, L"词典格式错误：根节点不是对象");
    rzlog::write("[词典] 解析失败：根节点不是对象");
    return false;
  }

  int count = 0;
  bool saw_translations = false;

  if (!j.eat('}')) {
    while (true) {
      std::string key;
      if (!j.parse_string(key)) {
        wcscpy_s(g_status, L"词典格式错误：键不是字符串");
        rzlog::write("[词典] 解析失败：键不是字符串");
        return false;
      }
      if (!j.eat(':')) {
        wcscpy_s(g_status, L"词典格式错误：缺少冒号");
        rzlog::write("[词典] 解析失败：缺少冒号");
        return false;
      }

      if (key == "translations") {
        saw_translations = true;
        if (!j.eat('{')) {
          wcscpy_s(g_status, L"translations 不是对象");
          rzlog::write("[词典] 解析失败：translations 不是对象");
          return false;
        }
        if (!j.eat('}')) {
          while (true) {
            std::string ek, ev;
            if (!j.parse_string(ek) || !j.eat(':') || !j.parse_string(ev)) {
              wcscpy_s(g_status, L"词典格式错误：translations 条目无效");
              rzlog::write("[词典] 解析失败：translations 条目无效");
              g_map.clear();
              return false;
            }
            std::wstring wk, wv;
            append_utf8_as_wstring(wk, ek);
            append_utf8_as_wstring(wv, ev);
            if (!wk.empty() && !wv.empty()) {
              if (wk.size() >= kLongThreshold) g_long.push_back({wk, wv});
              g_map[wk] = wv;
              count++;
            }
            if (j.eat(',')) continue;
            if (!j.eat('}')) {
              wcscpy_s(g_status, L"词典格式错误：translations 未闭合");
              rzlog::write("[词典] 解析失败：translations 未闭合");
              g_map.clear();
              return false;
            }
            break;
          }
        }
      } else {
        if (!j.skip_value()) {
          wcscpy_s(g_status, L"词典格式错误：无法跳过的字段");
          rzlog::write("[词典] 解析失败：无法跳过的字段");
          g_map.clear();
          return false;
        }
      }

      if (j.eat(',')) continue;
      if (!j.eat('}')) {
        wcscpy_s(g_status, L"词典格式错误：根对象未闭合");
        rzlog::write("[词典] 解析失败：根对象未闭合");
        g_map.clear();
        return false;
      }
      break;
    }
  }

  if (!saw_translations) {
    wcscpy_s(g_status, L"词典缺少 translations 字段");
    rzlog::write("[词典] 解析失败：缺少 translations 字段");
    g_map.clear();
    return false;
  }

  g_loaded = true;
  _snwprintf_s(g_status, 512, _TRUNCATE, L"已加载 %d 条词条", count);
  rzlog::printf("[词典] 已加载 %d 条词条", count);
  return true;
}

void unload() {
  g_map.clear();
  g_long.clear();
  g_loaded = false;
}

const wchar_t* lookup(const wchar_t* s, int n) {
  if (!g_loaded || !s || n <= 0) return nullptr;
  // 常见情况是短标签，避免构造临时 wstring 的开销
  static thread_local std::wstring key;
  key.assign(s, (size_t)n);
  auto it = g_map.find(key);
  if (it == g_map.end()) return nullptr;
  return it->second.c_str();
}

// 长文本片段查表。见头文件里的说明。
const wchar_t* lookup_fragment(const wchar_t* s, int n) {
  if (!g_loaded || !s || n < 12) return nullptr;

  static thread_local std::wstring frag;
  frag.assign(s, (size_t)n);

  // 去掉首尾空白后再匹配，宿主折行时常在行尾留一个空格
  size_t b = 0, e = frag.size();
  while (b < e && (frag[b] == L' ' || frag[b] == L'\t')) b++;
  while (e > b && (frag[e - 1] == L' ' || frag[e - 1] == L'\t')) e--;
  if (e <= b) return nullptr;

  static thread_local std::wstring needle;
  needle.assign(frag, b, e - b);

  // 记住上一次命中的长条目：折行绘制是连续的，同一段文本的相邻行
  // 几乎总是落在同一条目里，先查它可省掉大部分线性扫描。
  static thread_local const LongEntry* last = nullptr;

  auto slice = [&](const LongEntry* ent) -> const wchar_t* {
    size_t pos = ent->en.find(needle);
    if (pos == std::wstring::npos) return nullptr;

    // 按字符比例把原文区间映射到译文区间
    double k = (double)ent->zh.size() / (double)ent->en.size();
    size_t zs = (size_t)(pos * k);
    size_t ze = (size_t)((pos + needle.size()) * k);
    if (ze <= zs) ze = zs + 1;
    if (zs >= ent->zh.size()) zs = ent->zh.size() - 1;
    if (ze > ent->zh.size()) ze = ent->zh.size();

    static thread_local std::wstring out;
    out.assign(ent->zh, zs, ze - zs);
    return out.c_str();
  };

  if (last) {
    const wchar_t* r = slice(last);
    if (r) return r;
    last = nullptr;
  }

  for (auto& ent : g_long) {
    const wchar_t* r = slice(&ent);
    if (r) {
      last = &ent;
      return r;
    }
  }
  return nullptr;
}

int size() { return (int)g_map.size(); }

const wchar_t* status() { return g_status; }

}  // namespace dict
