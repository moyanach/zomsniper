# 🎮 zomsniper - 游戏自动化辅助工具

> 基于图像识别和状态机自动化的游戏辅助工具，支持自动战斗、技能选择和奖励领取。

## ✨ 特性

- 🤖 **智能状态机**：自动识别游戏界面状态（主界面/战斗中），切换检测策略
- 🎯 **图像识别**：基于 OpenCV 模板匹配，精准识别游戏按钮和界面元素
- 🛡️ **自动战斗**：智能选择技能，自动完成战斗流程
- 🎁 **奖励领取**：自动检测并领取等级提升、见面礼、任务礼等奖励
- 🔄 **容错机制**：连续未匹配时自动触发全量检测，确保稳定性
- 🖱️ **模拟人类操作**：随机偏移、延迟等，降低被检测风险
- 🍎 **macOS 原生支持**：基于 PyAutoGUI + PyObjC，完美支持 macOS 系统

## 📸 截图

![游戏截图](assets/start_game.png)

## 🚀 快速开始

### 环境要求

- Python 3.14+
- macOS 系统（支持模拟器）
- uv 包管理器

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

### 首次运行

1. **配置游戏窗口**
   - 打开游戏（模拟器或原生窗口）
   - 将游戏窗口置于前台

2. **配置 macOS 辅助功能权限**
   ```
   系统设置 → 隐私与安全性 → 辅助功能
   → 添加终端/iTerm/VS Code
   ```

3. **启动脚本**
   ```bash
   uv run python main.py
   ```

## 📖 使用说明

### 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                     主循环启动                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
        ┌──────────────────────┐
        │   主界面状态 (IDLE)   │
        │  - 开始战斗           │
        │  - 前往下一关         │
        │  - 等级提升           │
        │  - 见面礼             │
        │  - 任务礼             │
        └──────────┬───────────┘
                   │
          检测到开始战斗？
                   │
          ┌────────┴────────┐
          │ 是               │ 否
          ▼                 ▼
   ┌──────────────┐   ┌──────────────┐
   │ 进入战斗模式  │   │ 继续检测...  │
   │ (BATTLE)     │   └──────────────┘
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  战斗状态     │
   │  - 选择技能   │
   │  - 返回       │
   └──────┬───────┘
          │
   检测到返回按钮？
          │
   ┌──────┴──────┐
   │ 是           │ 否
   ▼             ▼
┌────────┐  ┌──────────┐
│返回主界面│  │ 继续战斗  │
└───┬────┘  └──────────┘
    │
    └─── 循环...
```

### 容错机制

- **主界面**：连续 3 轮未匹配到按钮 → 触发全量检测
- **战斗界面**：连续 5 轮未匹配到技能 → 触发全量检测
- **全量检测**：扫描所有可能的按钮，确保不会漏掉任何操作

### 日志说明

```
🚀 辅助工具已启动，请将游戏窗口置于前台...
✅ [主界面] 检测到开始按钮，点击进入关卡
✅ [战斗中] 已选择技能
🎉 [战斗结束] 检测到返回按钮，准备下一局
⚠️ [主界面] 未检测到任何按钮 (连续 2/3 轮)
🔄 [全量检测] 连续 3 轮未识别到按钮，开始全量检测...
```

## 🏗️ 项目结构

```
zomsniper/
├── main.py                    # 主入口，状态机循环
├── common/
│   ├── base_autogui.py        # 基础自动化操作（匹配、点击、滚动）
│   └── find_image.py          # 图像识别工具
├── skills/
│   ├── base_skill.py          # 技能基类
│   ├── choose_skill.py        # 技能选择逻辑
│   ├── choose_zidan.py        # 子弹技能
│   ├── choose_wenydadan.py    # 烟雾弹技能
│   ├── choose_shandian.py     # 闪电技能
│   ├── choose_zhuangjiache.py # 载具技能
│   └── choose_random.py       # 随机技能
├── quick_patroal/
│   └── quick_patroal.py       # 快速巡逻功能
├── assets/                    # 游戏截图模板
│   ├── start_game.png         # 开始战斗按钮
│   ├── next_map.png           # 前往下一关按钮
│   ├── back.png               # 返回按钮
│   ├── level_up.png           # 等级提升按钮
│   ├── face_gift.png          # 见面礼按钮
│   ├── task_gift.png          # 任务礼按钮
│   └── ...
├── pyproject.toml             # 项目配置和依赖
└── README.md                  # 项目说明
```

## ⚙️ 配置说明

### 调整置信度

编辑 `common/base_autogui.py`：

```python
def match_image(self, template_path, confidence=0.85):  # 修改 confidence 值
```

### 调整休眠时间

编辑 `main.py`：

```python
# 主界面休眠时间
time.sleep(1)  # 第 108 行

# 战斗界面休眠时间
time.sleep(0.5)  # 第 161 行

# 触发全量检测的阈值
max_no_match = 3  # 第 27 行（主界面）
max_no_match = 5  # 战斗界面（第 119 行附近）
```

### 添加新的按钮检测

1. 截图保存按钮图片到 `assets/` 目录
2. 在 `_idle_mode()` 或 `_battle_mode()` 中添加检测逻辑
3. 在 `_full_scan_mode()` 的全量检测列表中添加

## 🔧 故障排除

### 常见问题

**Q: 点击没有反应**

A: 检查 macOS 辅助功能权限是否已授予终端/iTerm/VS Code。

**Q: 图片识别失败**

A: 确保游戏窗口位置、大小、缩放比例与截图时一致。可以尝试调整置信度阈值。

**Q: 坐标超出屏幕范围**

A: 如果游戏运行在模拟器中，需要设置模拟器窗口偏移量。

**Q: 技能选择失败**

A: 检查 `assets/` 目录下是否有对应的技能图标截图。

### 日志调试

运行脚本时观察日志输出，根据错误信息定位问题：

```bash
uv run python main.py 2>&1 | tee debug.log
```

## 📦 依赖

- [pyautogui](https://pyautogui.readthedocs.io/) - 鼠标键盘自动化
- [opencv-python](https://opencv.org/) - 图像识别
- [numpy](https://numpy.org/) - 数值计算
- [pillow](https://pillow.readthedocs.io/) - 图像处理
- [pyobjc](https://pyobjc.readthedocs.io/) - macOS 原生支持

## 🛡️ 免责声明

本项目仅供学习和技术研究使用。使用本工具进行游戏自动化可能违反游戏服务条款，请自行承担风险。作者不对任何损失负责。

## 📄 许可证

本项目仅供个人学习使用，请勿用于商业用途。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系

- GitHub: [moyanach](https://github.com/moyanach)

---

<div align="center">
  <sub>Built with ❤️ by moyanach</sub>
</div>
