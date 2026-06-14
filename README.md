# 🎮 zomsniper — 游戏自动化辅助工具

基于图像识别与状态机的游戏自动化辅助工具，支持自动战斗、技能选择和奖励领取，专为 macOS 设计。

## ✨ 特性

- 🤖 **状态机驱动** — 自动识别游戏界面状态（主界面 / 战斗中），动态切换检测策略
- 🎯 **图像识别** — 基于 OpenCV 模板匹配，精准定位游戏按钮和界面元素
- ⚔️ **智能技能选择** — 优先级机制（子弹 > 温压弹 > 其他技能），自动完成战斗
- 🎁 **奖励自动领取** — 检测并领取等级提升、见面礼、任务礼等奖励
- 🔄 **容错机制** — 连续未匹配时触发全量检测，确保不遗漏任何操作
- 🖱️ **模拟人类操作** — 随机偏移、随机延迟、双击，降低被检测风险
- 🍎 **macOS 原生支持** — PyAutoGUI + PyObjC，完美适配 macOS 及模拟器
- 🚗 **快速巡逻** — 自动巡逻车 + 广告滚动，支持循环巡逻

## 🚀 快速开始

### 环境要求

- Python 3.14+
- macOS 系统
- [uv](https://docs.astral.sh/uv/) 包管理器

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/moyanach/zomsniper.git
cd zomsniper

# 2. 安装依赖
uv sync

# 3. 运行
uv run python main.py
```

### 首次配置

1. **打开游戏窗口**（模拟器或原生窗口），并置于前台
2. **授予辅助功能权限**：
   ```
   系统设置 → 隐私与安全性 → 辅助功能 → 添加终端 / iTerm / VS Code
   ```
3. **启动脚本**：
   ```bash
   uv run python main.py
   ```

## 📖 工作流程

```
┌──────────────────────────────────────────┐
│                 主循环启动                 │
└──────────────────┬───────────────────────┘
                   │
                   ▼
     ┌─────────────────────────┐
     │    主界面状态 (IDLE)      │
     │  · 前往下一关             │
     │  · 开始战斗               │
     │  · 等级提升 / 见面礼 / 任务礼 │
     └────────────┬────────────┘
                  │
         检测到开始/前往？
                  │
         ┌───────┴───────┐
         │ 是             │ 否
         ▼                ▼
  ┌──────────────┐  ┌──────────────┐
  │ 进入战斗模式  │  │ 继续主界面检测 │
  │ (BATTLE)     │  └──────────────┘
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │   战斗状态     │
  │  · 选择技能    │
  │  · 检测返回    │
  └──────┬───────┘
         │
  检测到返回按钮？
         │
    ┌────┴────┐
    │ 是       │ 否
    ▼          ▼
┌──────┐  ┌──────────┐
│返回主界面│  │ 继续战斗  │
└───┬──┘  └──────────┘
    │
    └── 循环...
```

### 容错机制

| 场景 | 阈值 | 行为 |
|------|------|------|
| 主界面连续未匹配 | 3 轮 | 触发全量检测 |
| 战斗界面连续未匹配 | 3 轮 | 触发全量检测 |
| 全量检测 | — | 依次扫描所有主界面和战斗按钮 |

### 日志示例

```
🚀 辅助工具已启动，请将游戏窗口置于前台...
✅ [主界面] 检测到开始按钮，点击进入关卡
✅ [战斗中] 已选择技能
🎉 [战斗结束] 检测到返回按钮，准备下一局
⚠️ [主界面] 未检测到任何按钮 (连续 2/3 轮)
🔄 [全量检测] 连续 3 轮未识别到按钮，开始全量检测所有按钮...
```

## 🏗️ 项目结构

```
zomsniper/
├── main.py                        # 主入口，状态机循环
├── common/
│   ├── base_autogui.py            # 底层自动化（模板匹配、点击、滚动）
│   └── base_skill.py              # 技能/按钮基类（图片加载与匹配）
├── buttons/
│   ├── click_button.py            # 按钮调度（统一入口，按名称分发）
│   ├── start_game.py              # 开始战斗按钮
│   ├── next_map.py                # 前往下一关按钮
│   ├── back_index.py              # 返回主界面按钮
│   └── stay_index.py              # 主界面按钮（等级提升/见面礼/任务礼）
├── skills/
│   ├── choose_skill.py            # 技能选择调度（优先级逻辑）
│   ├── choose_zidan.py            # 基础子弹
│   ├── choose_wenydadan.py        # 温压弹
│   ├── choose_shandian.py         # 闪电技能
│   ├── choose_shexian.py          # 射线技能
│   └── choose_random.py           # 随机技能
├── quick_patroal/
│   └── quick_patroal.py           # 快速巡逻（巡逻车 + 广告滚动）
├── assets/                        # 游戏截图模板（70 个 PNG）
│   ├── btns/                      # 按钮模板
│   │   ├── back/                  # 返回按钮
│   │   ├── index/                 # 主界面按钮
│   │   ├── nextmap/               # 下一关按钮
│   │   └── startgame/             # 开始游戏按钮
│   ├── skills/                    # 技能模板
│   │   ├── a_zi_dan/              # 基础子弹
│   │   ├── b_wen_ya_dan/          # 温压弹
│   │   ├── c_shan_dian/           # 闪电
│   │   ├── e_shexian/             # 射线
│   │   ├── f_dianzi/              # 电子
│   │   ├── f_ganbingdan/          # 干冰弹
│   │   ├── g_wurenji/             # 无人机
│   │   ├── h_zhuang_jia_che/      # 装甲车
│   │   ├── z_bingbao/             # 冰雹
│   │   ├── z_binglong/            # 冰龙
│   │   └── z_randoms/             # 随机技能集
│   └── quick_xunluo/              # 巡逻相关模板
├── pyproject.toml                 # 项目配置与依赖
└── README.md
```

## ⚙️ 配置说明

### 调整置信度

编辑 `common/base_autogui.py`，修改 `match_image` 方法的 `confidence` 参数（默认 `0.85`）：

```python
def match_image(self, template_path, confidence=0.85):
```

### 调整检测间隔

编辑 `main.py`：

```python
# 主界面休眠
time.sleep(1)       # _idle_mode 末尾

# 战斗界面休眠
time.sleep(1)       # _battle_mode 末尾

# 全量检测阈值
max_no_match = 3    # 第 27 行
```

### 添加新按钮

1. 截图保存至 `assets/` 对应子目录
2. 在 `buttons/` 下创建按钮类（继承 `BaeSkill`）
3. 在 `buttons/click_button.py` 中注册到 `btn_maps`
4. 在 `main.py` 的 `_idle_mode` / `_battle_mode` / `_full_scan_mode` 中添加调用

### 添加新技能

1. 截图保存至 `assets/skills/<技能名>/`
2. 在 `skills/` 下创建技能类（继承 `BaeSkill`）
3. 在 `skills/choose_skill.py` 中注册并配置优先级

## 📦 依赖

| 包 | 用途 |
|----|------|
| [pyautogui](https://pyautogui.readthedocs.io/) | 鼠标键盘自动化 |
| [opencv-python](https://opencv.org/) | 图像模板匹配 |
| [numpy](https://numpy.org/) | 数值计算 |
| [pillow](https://pillow.readthedocs.io/) | 图像处理 |
| [pyobjc](https://pyobjc.readthedocs.io/) | macOS 原生 API |
| [mss](https://python-mss.readthedocs.io/) | 高性能屏幕截图 |
| [pynput](https://pynput.readthedocs.io/) | 键盘监听 |
| [pygetwindow](https://github.com/asweigart/PyGetWindow) | 窗口管理 |

## 🔧 故障排除

| 问题 | 解决方案 |
|------|----------|
| 点击没有反应 | 检查 macOS 辅助功能权限是否已授予终端 / iTerm / IDE |
| 图片识别失败 | 确保游戏窗口位置、大小、缩放比例与截图时一致；可降低 `confidence` 阈值 |
| 坐标超出屏幕 | 模拟器环境下检查 `base_autogui.py` 中的坐标缩放系数 |
| 技能选择失败 | 确认 `assets/skills/` 下存在对应技能截图 |

### 调试日志

```bash
uv run python main.py 2>&1 | tee debug.log
```

## 🛡️ 免责声明

本项目仅供学习和技术研究使用。使用本工具进行游戏自动化可能违反游戏服务条款，请自行承担风险。作者不对任何损失负责。

## 📄 许可证

仅供个人学习使用，请勿用于商业用途。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系

- GitHub: [moyanach](https://github.com/moyanach)

---

<div align="center">
  <sub>Built with ❤️ by moyanach</sub>
</div>
