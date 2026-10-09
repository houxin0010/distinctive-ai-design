# 验证方案 / Validation

## 本地 Smoke Test

需要 Python 3.10+；测试依赖只有固定版本的 YAML 与 CommonMark 解析器。首次安装需要网络，之后测试无需网络、Codex、模型密钥或浏览器。在仓库根目录执行：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r tests/requirements.txt
.venv/bin/python tests/validate_skill.py
.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v
```

Windows 使用 `.venv\Scripts\python.exe` 替代 `.venv/bin/python`。
也可在其他目录用 `python /absolute/path/to/tests/validate_skill.py --root /absolute/path/to/repo`。
检查失败返回 1；全部通过返回 0。缺少依赖直接报错，不算跳过或通过。

检查范围：

- 必要的五个原始文件存在、非空、UTF-8 可读。
- SKILL.md 以 YAML front matter 开始，name/description 为非空字符串，name 为本仓库预期名称、长度 ≤64，description 长度 ≤1024，执行正文非空。
- YAML 安全解析、拒绝重复 key；agents/openai.yaml 是 mapping，interface 展示字段为非空字符串，default_prompt 调用名称与 name 一致。可选 policy 布尔值、图标文件、品牌色也检查。
- 两份 README 的显式 `$skill` 示例与 name 一致。
- 仓库 Markdown 中的行内链接、引用式链接和图片的本地目标存在且不越出仓库；相对路径按所在文档目录解析。代码块/行内代码不当作链接，外部 URL 不请求，锚点存在性和原始 HTML 链接不检查。生成物、虚拟环境、node_modules、Git 内部文件排除。

这是一套**本仓库契约**，不是 Codex 完整 schema 或官方加载器的替代品。不验证工具依赖连接，也不证明 Skill 已加载。负向 fixture 会故意删除文件、破坏 YAML、改错名称及链接等，验证检查器不会对这些错误报绿。

GitHub Actions 在 push/PR 执行同样两条测试命令。CI 仅做静态验证，不调用模型，不执行端到端设计。

## 最小端到端案例（需在具备 Codex CLI 的机器运行）

案例是依赖为零的“小步”专注入口，主任务为开始 25 分钟专注并显示开始状态；这是验证用状态演示，不要求实现真实倒计时。自动化只负责准备 fixture、捕获真实浏览器截图和断言行为，视觉探索与审美评审仍需读取实际证据。

先记录 CLI 版本和帮助。以下命令参考 [官方 Skill 文档](https://learn.chatgpt.com/docs/build-skills) 与 [非交互模式](https://learn.chatgpt.com/docs/non-interactive-mode)，核对时间为 2026-10-09 UTC。若本机参数不同，按该版本 `--help` 调整并记录；不能因目录存在就认定加载成功。

```sh
codex --version
codex exec --help
```

### 1. 准备与发现

从本仓库根目录执行，目标必须是一个尚不存在的新目录，不修改用户全局 skills，也不修改 CODEX_HOME 或复制认证文件：

```sh
python3 tests/e2e/prepare.py /tmp/distinctive-ai-design-e2e
cd /tmp/distinctive-ai-design-e2e
codex --version > evidence/codex-version.txt
codex
```

fixture 已初始化为 Git 仓库，skill 位于 `.agents/skills/distinctive-ai-design`；只复制实际执行需要的入口、agent 配置及引用文件。`source-revision.txt` 记录源 HEAD 和未提交状态；正式复现推荐使用干净提交。

在新 CLI 会话的 skill 选择器查看 `distinctive-ai-design`（支持该命令的版本可用 `/skills`，也可输入 `$` 检查补全；用 `/help` 确认）。保存选择器截图或终端记录为 `evidence/discovery.*`，记录实际加载路径。若用户全局已安装同名 Skill，排除重复来源后重试。

**验收**：CLI 的可用技能列表/选择器确实出现此 Skill，来源为 fixture 的目录，无加载错误。模型回答“我看到了 Skill”、手动 cat 文件或静态检查通过不能独立作为发现证据。选择器或加载事件不可观测时，此项继续标注未验证。

### 2. 调用与探索

退出发现会话，在 fixture 根目录执行；stdin 文件中的 `$` 不经过 shell 展开：

```sh
codex exec --sandbox workspace-write --json -o evidence/design-last-message.txt - \
  < design-prompt.txt > evidence/design-events.jsonl 2> evidence/design-stderr.txt
```

保存退出码；检查 stderr 及 JSONL 中的 error/turn.failed，不只看最终文字。复用本机已授权认证，不在测试中配置密钥或指定模型。模型和工具调用可能消耗额度。审批阻塞或工具不可用要记为 blocked，不改成无限权限重试。

**验收**：退出码 0 且无失败事件；调用记录明确使用该 Skill，有读取正确路径 SKILL.md 或加载事件证据；`directions.md` 有三个在构图/信息/字体/交互上不同的方案，而非换色；`brief.md` 含用户、主任务、感受、隐喻、层级、色彩/字体、交互、避免元素和最小范围；`index.html` 实现选定方向，保留原有主操作。人工核对内容，不以文件存在替代质量检查。发现证据和调用证据分别保留。

### 3. 运行、截图与功能检查

在**另一终端**运行服务器，保持前台：

```sh
cd /tmp/distinctive-ai-design-e2e
python3 -m http.server 8765 --bind 127.0.0.1
```

从本仓库根目录安装可选浏览器依赖并捕获；首次需要下载 Chromium/系统依赖，Linux 若缺库按 Playwright 官方安装提示处理。不要把 baseline fixture 截图误作模型产物验证。

```sh
.venv/bin/python -m pip install -r tests/e2e/browser-requirements.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tests/e2e/capture.py --url http://127.0.0.1:8765 \
  --out /tmp/distinctive-ai-design-e2e/evidence/round-1
```

**验收**：实际打开模型修改后的页面，1280×800、390×844 各有 initial/started PNG；点击可见 CTA 后出现“专注已开始”，按钮禁用，页面无横向溢出和 JS 异常；结果 JSON 为 pass。这只证明有限行为，不证明真实计时、性能、完整无障碍或审美质量。脚本失败返回非零，残留截图不算成功。

### 4. 独立截图评审与精修

创建全新的评审会话/上下文，只提供 round-1 的真实 PNG、用户/主任务说明、brief 和 [评审提示](../references/review-and-media.md)。不要给实现代码、实施难度、历史解释、此前评分或目标分数。可在仓库外建立只含这些输入的评审文件夹，然后在具备图像输入的 CLI 中运行 `codex` 并附加这些图片；具体图像参数先检查本机 `codex --help`，没有图像能力则不执行视觉评审。

**验收**：保存 `evidence/review-1.md`，注明实际评审模型/上下文及输入截图；评审概括方向，最多三个问题，各含截图位置、表现、影响和可执行建议，给出参考评分及理由，截图无法证明的行为标注未验证。没有独立上下文时可自查，但必须标注 self-review，独立评审验收仍未通过。

将问题交回原实现上下文或新的实现会话，优先改 1–3 个问题，并将删减/修改保存为 `evidence/changes.md`。按第 3 步重新截图，改 `--out` 为 `.../evidence/round-2`（不能覆盖 round-1），再用新的评审上下文按同一框架复查。最多两轮；若第一轮无具体问题，可直接交付并记录原因。无需达到 9/10，不以分数作为通过条件。

**最终验收**：证据能把发现、调用、探索、实现、真实截图、评审、精修/不精修理由与主操作串起来；提交结果表，分别填 PASS / FAIL / BLOCKED / NOT VERIFIED。评审输入泄漏代码、没有读图、伪造截图、只有静态检查或得分都不能算完整 E2E 通过。

## 实际执行记录

当前执行结果见 [VALIDATION_RESULTS.md](VALIDATION_RESULTS.md)。未来复现请新增日期、源提交、CLI/模型/浏览器版本、命令、退出码、证据路径和限制；不要把未验证项改成推断通过。
