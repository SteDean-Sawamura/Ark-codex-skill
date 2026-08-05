# Ark Codex Skill

用AI辅助制作的一个用于制作《明日方舟》透明桌面宠物（Codex 桌宠）的 Codex skill。给它一个干员名（可选皮肤名），它会自动从 PRTS Wiki 导出该干员的基建 WebM 动画，转换成带透明通道的 PNG 帧，生成桌宠并加入桌宠库。

> 仓库：[AstrariaX/Ark-codex-skill](https://github.com/AstrariaX/Ark-codex-skill)

## 功能特性

- 自动检索 PRTS 干员页面并加载“干员模型”查看器
- 默认使用原皮（默认时装），也可指定任意时装组
- 模型组固定使用“基建”，导出 `Default / Interact / Move / Relax / Sit / Sleep` 六段动画
- 自动跳过 PRTS 导出的坏文件（`Default` 经常是 110 字节空文件）
- 将 WebM 抽帧为 1000×1000、20fps 的透明 PNG，自动计算包围盒并生成 `manifest.json`
- 支持桌宠库：可以存放多个干员，右键“桌宠库”随时切换
- 生成的项目自带完整桌宠程序：状态字幕、拖动、锁定、迷你模式、全屏自动隐藏、按角色记忆位置/大小/倍速、随 ChatGPT/Codex 启动

## 目录结构

```text
ark-codex-skill/
├── README.md
├── .gitignore
└── skill/
    ├── SKILL.md                 # Codex skill 主说明
    ├── agents/
    │   └── openai.yaml          # Codex UI 元数据
    ├── scripts/
    │   ├── scaffold_deskpet.py  # 生成桌宠项目
    │   ├── setup_env.py         # 创建 .venv 并安装依赖
    │   ├── prts_export.py       # 从 PRTS 导出 WebM
    │   └── process_webm.py      # WebM 转透明 PNG 帧
    ├── references/
    │   └── prts-ui.md           # PRTS 查看器 DOM 参考
    └── assets/
        └── deskpet-app/         # 桌宠应用模板
```

## 环境要求

- Windows 10/11（桌宠程序目前仅适配 Windows）
- Python 3.10 或更高版本
- 可访问 `https://prts.wiki`
- 有网络权限安装依赖（PySide6、Playwright）

所有依赖都安装到项目自己的 `.venv`，不会影响全局 Python 环境。

## 使用指南

### 第一步：部署这个 skill

直接对 Codex 说：

```text
安装 GitHub 仓库 AstrariaX/Ark-codex-skill 里的 ark-codex-skill skill
```

也可以手动安装：把仓库里的 `skill/` 目录复制到 `~/.codex/skills/ark-codex-skill/`。

### 第二步：调用

默认原皮：

```text
用 ark-codex-skill 制作干员 浊心斯卡蒂 的桌宠
```

指定皮肤：

```text
用 ark-codex-skill 制作干员 浊心斯卡蒂 的桌宠，皮肤用 升华
```

不写皮肤就是默认原皮。制作完成后右键小人 -> 桌宠库，可以随时切换已入库的角色。

## 桌宠功能

- 单击播放互动动画
- 双击切换迷你模式（隐藏/显示字幕条）
- 拖动播放走路动画，松手恢复之前状态
- 右键菜单：坐下 / 放松 / 睡觉 / 桌宠库 / 锁定 / 设置 / 放大 / 缩小 / 退出
- 头顶字幕：Codex 运行状态、最近任务、模型、运行时长、Token 用量、最近完成时间
- 每个角色独立记住位置、大小、动作倍速
- 迷你模式、全屏应用自动隐藏
- 可设置随 ChatGPT / Codex 启动和关闭
- 监听 `~/.codex/sessions/`，只读不修改 Codex 数据

## 常见问题

### PRTS 导出失败或按钮找不到

PRTS 页面改版会影响脚本。先看 `skill/references/prts-ui.md` 里的 DOM 说明，再同步更新 `skill/scripts/prts_export.py` 的选择器。

### 打开后没有看到小人

运行 `my-deskpet/调试运行.bat`，把控制台报错或 `pet_error.log` 内容发出来。

### 需要手动从网站下载素材

可以直接在 PRTS 干员页的“干员模型”里手动操作：

1. 点击“点此载入模型”
2. 时装组选默认（或指定皮肤）
3. 模型组选“基建”
4. 动画依次选 `Default / Interact / Move / Relax / Sit / Sleep`
5. 点击下载图标按钮导出 WebM，把文件放进 `my-deskpet/work/webm/`
6. 把文件放进 `my-deskpet/work/webm/`，再让 Codex 用 skill 继续抽帧入库

## 注意事项

- 《明日方舟》素材版权归 Hypergryph 所有，PRTS 资料遵循其站内许可。本项目仅用于个人学习与自用，请勿用于商业发布。
- 桌宠程序目前仅支持 Windows；macOS/Linux 可以运行素材处理脚本，但桌宠程序需要额外适配。

## 贡献

欢迎提交 PR 修复 PRTS 页面变动、增加新动画映射、优化抽帧速度或补充平台适配。
