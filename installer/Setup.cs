// RizomUV 简体中文补丁 —— 安装器
//
// 设计原则：
//   * 只往安装目录写入三个文件（启动器、运行时 DLL、词典），
//     不改动 rizomuv.exe，不写注册表，不接管文件关联；
//   * 安装前把即将写入的文件登记到 backup 清单，卸载时按清单删除，
//     目录里本来就有同名文件时先备份再覆盖，卸载时还原；
//   * 检测不到安装目录时让用户手动选择，而不是猜。
//
// 编译：
//   csc /target:winexe /out:Setup.exe Setup.cs /win32manifest:app.manifest
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Text;
using System.Windows.Forms;
using Microsoft.Win32;

namespace RizomUVChinese
{
    internal static class Program
    {
        internal const string ProductName = "RizomUV 简体中文补丁";
        internal const string HostExe = "rizomuv.exe";
        internal const string LauncherExe = "RizomUVChineseLauncher.exe";
        internal const string RuntimeDll = "RizomUVChineseRuntime.dll";
        internal const string DictionaryFile = "dictionary_zh.json";
        internal const string StateFile = "chinese_patch.json";
        internal const string BackupDir = "chinese_patch_backup";

        [STAThread]
        private static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            bool silent = HasFlag(args, "/S") || HasFlag(args, "-silent");
            bool uninstall = HasFlag(args, "/uninstall") || HasFlag(args, "-uninstall");

            try
            {
                if (uninstall)
                {
                    RunUninstall(silent, args);
                    return;
                }

                string target = FindTarget(args);
                if (target == null)
                {
                    if (!silent)
                    {
                        MessageBox.Show(
                            "没有找到 RizomUV 安装目录。\n\n" +
                            "请把安装包放到 RizomUV 安装目录中运行，或使用 /dir=\"路径\" 参数指定。",
                            ProductName, MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    }
                    Environment.ExitCode = 2;
                    return;
                }

                RunInstall(target, silent);
            }
            catch (Exception ex)
            {
                if (!silent)
                {
                    MessageBox.Show(ex.Message, ProductName + " —— 出错了",
                        MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                Environment.ExitCode = 1;
            }
        }

        private static bool HasFlag(string[] args, string flag)
        {
            foreach (string a in args)
            {
                if (string.Equals(a, flag, StringComparison.OrdinalIgnoreCase)) return true;
            }
            return false;
        }

        // ---------------------------------------------------------------- 安装

        private static void RunInstall(string target, bool silent)
        {
            if (silent)
            {
                // 静默安装也创建快捷方式：它是中文界面的主要入口，
                // 少了它用户很可能直接运行 rizomuv.exe 而看不到汉化。
                Install(target, true);
                return;
            }

            using (var form = new InstallForm(target))
            {
                if (form.ShowDialog() != DialogResult.OK) return;
                Install(form.TargetDir, form.CreateShortcut);
            }

            MessageBox.Show(
                "汉化安装完成。\n\n" +
                "以后请用桌面上的「RizomUV 中文版」快捷方式启动，\n" +
                "直接运行 rizomuv.exe 仍然是英文界面。",
                ProductName, MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        internal static void Install(string target, bool createShortcut)
        {
            if (!File.Exists(Path.Combine(target, HostExe)))
                throw new InvalidOperationException(
                    "所选目录里没有 " + HostExe + "，请选择 RizomUV 的安装目录。");

            string source = ExtractPayload();
            var payload = new[] { LauncherExe, RuntimeDll, DictionaryFile };
            foreach (string name in payload)
            {
                if (!File.Exists(Path.Combine(source, name)))
                    throw new InvalidOperationException(
                        "安装包不完整，缺少 " + name + "。请重新下载。");
            }

            // 已安装过就先卸掉，避免残留旧版本
            if (File.Exists(Path.Combine(target, StateFile))) Uninstall(target);

            string backup = Path.Combine(target, BackupDir);
            Directory.CreateDirectory(backup);

            var state = new State { target = target, files = new List<FileRecord>() };

            foreach (string name in payload)
            {
                string dest = Path.Combine(target, name);
                var rec = new FileRecord { name = name, existed = false };

                if (File.Exists(dest))
                {
                    // 目标已存在同名文件：备份后覆盖，卸载时还原
                    rec.existed = true;
                    File.Copy(dest, Path.Combine(backup, name), true);
                }

                File.Copy(Path.Combine(source, name), dest, true);
                state.files.Add(rec);
            }

            SaveState(target, state);

            if (createShortcut) CreateShortcut(target);
        }

        // ---------------------------------------------------------------- 载荷解包

        // 安装包把三个文件作为嵌入资源带在自身里，运行时解到临时目录。
        // 如果找不到嵌入资源（开发期直接编译运行），退回读取程序所在目录，
        // 这样调试时不必每次都重新嵌入。
        private static string ExtractPayload()
        {
            Assembly asm = Assembly.GetExecutingAssembly();
            var names = new[] { LauncherExe, RuntimeDll, DictionaryFile };

            bool embedded = true;
            foreach (string n in names)
            {
                if (asm.GetManifestResourceInfo(n) == null) { embedded = false; break; }
            }

            if (!embedded)
                return Path.GetDirectoryName(asm.Location);

            string dir = Path.Combine(Path.GetTempPath(),
                "RizomUVChineseSetup_" + Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(dir);

            foreach (string n in names)
            {
                using (Stream s = asm.GetManifestResourceStream(n))
                {
                    if (s == null)
                        throw new InvalidOperationException("安装包缺少资源：" + n);
                    using (FileStream f = File.Create(Path.Combine(dir, n)))
                    {
                        s.CopyTo(f);
                    }
                }
            }

            AppDomain.CurrentDomain.ProcessExit += delegate { TryDeleteDirectory(dir); };
            return dir;
        }

        private static void CreateShortcut(string target)
        {
            try
            {
                string link = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory),
                    "RizomUV 中文版.lnk");
                string exe = Path.Combine(target, LauncherExe);

                // 用 WScript.Shell 建快捷方式，避免依赖 COM 互操作程序集
                Type shellType = Type.GetTypeFromProgID("WScript.Shell");
                if (shellType == null) return;
                object shell = Activator.CreateInstance(shellType);
                object shortcut = shellType.InvokeMember("CreateShortcut",
                    BindingFlags.InvokeMethod, null, shell, new object[] { link });

                Type sc = shortcut.GetType();
                sc.InvokeMember("TargetPath", BindingFlags.SetProperty, null, shortcut, new object[] { exe });
                sc.InvokeMember("WorkingDirectory", BindingFlags.SetProperty, null, shortcut,
                    new object[] { target });
                sc.InvokeMember("IconLocation", BindingFlags.SetProperty, null, shortcut,
                    new object[] { Path.Combine(target, HostExe) + ",0" });
                sc.InvokeMember("Description", BindingFlags.SetProperty, null, shortcut,
                    new object[] { "RizomUV（简体中文界面）" });
                sc.InvokeMember("Save", BindingFlags.InvokeMethod, null, shortcut, null);
            }
            catch
            {
                // 快捷方式只是便利功能，失败不影响安装
            }
        }

        // ---------------------------------------------------------------- 卸载

        private static void RunUninstall(bool silent, string[] args)
        {
            string target = FindTarget(args) ?? FindInstalledTarget();
            if (target == null)
            {
                if (!silent)
                {
                    MessageBox.Show("没有找到已安装的汉化补丁。", ProductName,
                        MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                Environment.ExitCode = 2;
                return;
            }
            if (!silent)
            {
                DialogResult r = MessageBox.Show(
                    "将移除 RizomUV 中文补丁并还原英文界面。\n\n目录：" + target + "\n\n继续吗？",
                    ProductName + " —— 卸载", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                if (r != DialogResult.Yes) return;
            }

            Uninstall(target);

            if (!silent)
            {
                MessageBox.Show("已卸载，界面恢复英文。", ProductName,
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        internal static void Uninstall(string target)
        {
            State state = LoadState(target);
            if (state != null)
            {
                foreach (FileRecord rec in state.files)
                {
                    string dest = Path.Combine(target, rec.name);
                    string saved = Path.Combine(target, BackupDir, rec.name);

                    try
                    {
                        if (rec.existed && File.Exists(saved))
                        {
                            File.Copy(saved, dest, true);
                        }
                        else if (File.Exists(dest))
                        {
                            File.Delete(dest);
                        }
                    }
                    catch
                    {
                        // 文件被占用时保留，交给用户手动处理
                    }
                }
            }

            TryDeleteDirectory(Path.Combine(target, BackupDir));
            TryDelete(Path.Combine(target, StateFile));

            string link = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory),
                "RizomUV 中文版.lnk");
            TryDelete(link);
        }

        private static void TryDelete(string path)
        {
            try { if (File.Exists(path)) File.Delete(path); }
            catch { }
        }

        private static void TryDeleteDirectory(string path)
        {
            try { if (Directory.Exists(path)) Directory.Delete(path, true); }
            catch { }
        }

        // ---------------------------------------------------------------- 目录定位

        private static string FindTarget(string[] args)
        {
            string explicitDir = GetDirArg(args);
            if (explicitDir != null && File.Exists(Path.Combine(explicitDir, HostExe)))
                return explicitDir;

            string self = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            if (File.Exists(Path.Combine(self, HostExe))) return self;

            foreach (string candidate in KnownLocations())
            {
                if (File.Exists(Path.Combine(candidate, HostExe))) return candidate;
            }

            return null;
        }

        private static string GetDirArg(string[] args)
        {
            foreach (string a in args)
            {
                const string prefix = "/dir=";
                if (a.StartsWith(prefix, StringComparison.OrdinalIgnoreCase))
                {
                    string p = a.Substring(prefix.Length).Trim('"');
                    if (p.Length > 0) return p;
                }
            }
            return null;
        }

        private static IEnumerable<string> KnownLocations()
        {
            // 1. 卸载信息里记录的安装位置（最可靠）
            string[] roots =
            {
                @"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                @"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            };
            foreach (string root in roots)
            {
                foreach (RegistryKey hive in new[] { Registry.LocalMachine, Registry.CurrentUser })
                {
                    using (RegistryKey key = hive.OpenSubKey(root))
                    {
                        if (key == null) continue;
                        foreach (string sub in key.GetSubKeyNames())
                        {
                            using (RegistryKey item = key.OpenSubKey(sub))
                            {
                                if (item == null) continue;
                                string name = item.GetValue("DisplayName") as string;
                                if (name == null || name.IndexOf("RizomUV", StringComparison.OrdinalIgnoreCase) < 0)
                                    continue;

                                string loc = item.GetValue("InstallLocation") as string;
                                if (!string.IsNullOrEmpty(loc)) yield return loc.Trim('"');

                                string icon = item.GetValue("DisplayIcon") as string;
                                if (!string.IsNullOrEmpty(icon))
                                {
                                    icon = icon.Trim('"');
                                    int comma = icon.LastIndexOf(',');
                                    if (comma > 0) icon = icon.Substring(0, comma);
                                    string dir = Path.GetDirectoryName(icon);
                                    if (!string.IsNullOrEmpty(dir)) yield return dir;
                                }
                            }
                        }
                    }
                }
            }

            // 2. Program Files 下的常见布局
            foreach (string baseDir in new[]
            {
                Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles),
                Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86),
            })
            {
                if (string.IsNullOrEmpty(baseDir)) continue;
                foreach (string vendor in new[] { "Rizom Lab", "Rizom-Lab", "RizomUV" })
                {
                    string root = Path.Combine(baseDir, vendor);
                    if (!Directory.Exists(root)) continue;
                    yield return root;

                    string[] dirs;
                    try { dirs = Directory.GetDirectories(root); }
                    catch { continue; }
                    foreach (string d in dirs) yield return d;
                }
            }
        }

        private static string FindInstalledTarget()
        {
            string self = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            if (File.Exists(Path.Combine(self, StateFile))) return self;

            foreach (string candidate in KnownLocations())
            {
                if (File.Exists(Path.Combine(candidate, StateFile))) return candidate;
            }
            return null;
        }

        // ---------------------------------------------------------------- 状态文件

        [Serializable]
        internal class FileRecord
        {
            public string name;
            public bool existed;
        }

        [Serializable]
        internal class State
        {
            public int version = 1;
            public string target;
            public List<FileRecord> files = new List<FileRecord>();
        }

        private static void SaveState(string target, State state)
        {
            var sb = new StringBuilder();
            sb.Append("{\n  \"version\": 1,\n  \"target\": \"").Append(Escape(target)).Append("\",\n");
            sb.Append("  \"files\": [\n");
            for (int i = 0; i < state.files.Count; i++)
            {
                FileRecord r = state.files[i];
                sb.Append("    {\"name\": \"").Append(Escape(r.name))
                  .Append("\", \"existed\": ").Append(r.existed ? "true" : "false").Append("}");
                if (i + 1 < state.files.Count) sb.Append(',');
                sb.Append('\n');
            }
            sb.Append("  ]\n}\n");
            File.WriteAllText(Path.Combine(target, StateFile), sb.ToString(), new UTF8Encoding(false));
        }

        private static State LoadState(string target)
        {
            string path = Path.Combine(target, StateFile);
            if (!File.Exists(path)) return null;

            string text = File.ReadAllText(path, Encoding.UTF8);
            var state = new State { target = target, files = new List<FileRecord>() };

            // 状态文件格式固定，用极简解析避免引入 JSON 依赖
            foreach (string line in text.Split('\n'))
            {
                string t = line.Trim();
                if (!t.StartsWith("{\"name\"")) continue;
                var rec = new FileRecord();
                rec.name = ReadJsonString(t, "\"name\": \"");
                rec.existed = t.Contains("\"existed\": true");
                if (!string.IsNullOrEmpty(rec.name)) state.files.Add(rec);
            }
            return state;
        }

        private static string ReadJsonString(string line, string marker)
        {
            int i = line.IndexOf(marker, StringComparison.Ordinal);
            if (i < 0) return null;
            i += marker.Length;
            var sb = new StringBuilder();
            while (i < line.Length && line[i] != '"')
            {
                if (line[i] == '\\' && i + 1 < line.Length)
                {
                    i++;
                    switch (line[i])
                    {
                        case 'n': sb.Append('\n'); break;
                        case 't': sb.Append('\t'); break;
                        case 'r': sb.Append('\r'); break;
                        default: sb.Append(line[i]); break;
                    }
                }
                else
                {
                    sb.Append(line[i]);
                }
                i++;
            }
            return sb.ToString();
        }

        private static string Escape(string s)
        {
            var sb = new StringBuilder();
            foreach (char c in s)
            {
                switch (c)
                {
                    case '\\': sb.Append("\\\\"); break;
                    case '"': sb.Append("\\\""); break;
                    case '\n': sb.Append("\\n"); break;
                    case '\r': sb.Append("\\r"); break;
                    case '\t': sb.Append("\\t"); break;
                    default: sb.Append(c); break;
                }
            }
            return sb.ToString();
        }
    }

    // -------------------------------------------------------------------- 界面

    internal sealed class InstallForm : Form
    {
        private readonly TextBox _path;
        private readonly CheckBox _shortcut;

        public string TargetDir { get { return _path.Text.Trim(); } }
        public bool CreateShortcut { get { return _shortcut.Checked; } }

        public InstallForm(string target)
        {
            Text = Program.ProductName;
            FormBorderStyle = FormBorderStyle.FixedDialog;
            StartPosition = FormStartPosition.CenterScreen;
            MaximizeBox = false;
            MinimizeBox = false;
            ClientSize = new Size(520, 190);
            Font = new Font("Microsoft YaHei UI", 9f);

            var title = new Label
            {
                Text = "安装简体中文界面",
                Font = new Font("Microsoft YaHei UI", 12f, FontStyle.Bold),
                Location = new Point(18, 16),
                AutoSize = true,
            };

            var hint = new Label
            {
                Text = "补丁只新增文件，不修改 rizomuv.exe，卸载后可完整还原英文。",
                Location = new Point(20, 48),
                Size = new Size(480, 20),
                ForeColor = Color.FromArgb(90, 90, 90),
            };

            var label = new Label
            {
                Text = "RizomUV 安装目录：",
                Location = new Point(20, 78),
                AutoSize = true,
            };

            _path = new TextBox
            {
                Text = target,
                Location = new Point(20, 100),
                Size = new Size(400, 24),
            };

            var browse = new Button
            {
                Text = "浏览...",
                Location = new Point(428, 99),
                Size = new Size(74, 26),
            };
            browse.Click += (s, e) =>
            {
                using (var dlg = new FolderBrowserDialog())
                {
                    dlg.Description = "选择 RizomUV 安装目录（包含 rizomuv.exe）";
                    dlg.SelectedPath = _path.Text;
                    if (dlg.ShowDialog(this) == DialogResult.OK) _path.Text = dlg.SelectedPath;
                }
            };

            _shortcut = new CheckBox
            {
                Text = "在桌面创建「RizomUV 中文版」快捷方式",
                Location = new Point(20, 132),
                Size = new Size(400, 22),
                Checked = true,
            };

            var ok = new Button
            {
                Text = "安装",
                Location = new Point(340, 158),
                Size = new Size(78, 26),
                DialogResult = DialogResult.OK,
            };
            var cancel = new Button
            {
                Text = "取消",
                Location = new Point(424, 158),
                Size = new Size(78, 26),
                DialogResult = DialogResult.Cancel,
            };

            ok.Click += (s, e) =>
            {
                if (!File.Exists(Path.Combine(_path.Text.Trim(), Program.HostExe)))
                {
                    MessageBox.Show(this, "该目录里没有 " + Program.HostExe + "，请重新选择。",
                        Program.ProductName, MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    DialogResult = DialogResult.None;
                }
            };

            Controls.AddRange(new Control[]
            {
                title, hint, label, _path, browse, _shortcut, ok, cancel,
            });

            AcceptButton = ok;
            CancelButton = cancel;
        }
    }
}
