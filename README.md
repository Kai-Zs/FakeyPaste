<p align="center">
  <img src="app_icon.ico" width="80" alt="FakeyPaste">
</p>

<h1 align="center">🎯 FakeyPaste</h1>

<p align="center">
  <strong>轻量级模拟键盘输入工具 —— 解决网页 IDE、受限系统无法粘贴代码的难题</strong><br>
  <sup>逐字符模拟真实击键，智能缩进还原，玻璃拟态美学</sup>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/v2.0-ff5555?style=for-the-badge&logo=v&logoColor=white" alt="version">
  <img src="https://img.shields.io/badge/GPLv3-8be9fd?style=for-the-badge&logo=gnu&logoColor=white" alt="license">
  <img src="https://img.shields.io/badge/Python-3.10+-bd93f9?style=for-the-badge&logo=python&logoColor=white" alt="python">
  <img src="https://img.shields.io/badge/Windows-10|11-50fa7b?style=for-the-badge&logo=windows&logoColor=white" alt="windows">
</p>

<p align="center">
  <a href="https://www.kaizs.cn/fakeypastehelp/">📖 使用说明</a> ·
  <a href="https://www.kaizs.cn/fakeypastehelp/changelog.html">📋 更新历史</a> ·
  <a href="https://github.com/Kai-Zs/FakeyPaste/releases">⬇️ 下载</a> ·
  <a href="https://www.kaizs.cn">🌐 作者主页</a>
</p>

---

## 📥 下载

| 方式 | 地址 |
|---|---|
| **GitHub Releases** | [github.com/Kai-Zs/FakeyPaste/releases](https://github.com/Kai-Zs/FakeyPaste/releases) |
| **蓝奏云**（国内高速） | [yyskk.lanzoub.com/iW5je3o4wh2d](https://yyskk.lanzoub.com/iW5je3o4wh2d) 密码: `7os2` |
| **kaizs.cn 直链** | [kaizs.cn/download/FakeyPaste_v2.0.exe](https://www.kaizs.cn/download/FakeyPaste_v2.0.exe) |

---

## 📖 介绍

**FakeyPaste** 不是剪贴板管理器，而是一款智能的模拟键盘输入工具。它通过底层键盘接口将文本逐字符模拟为真实击键，完美绕过网页表单、受限系统等场景下的一切粘贴限制。

### ✨ v2.0 亮点

- ⚡ **简要/高级双模式** —— 标题栏分段开关一键切换，简要模式仅 3 个按钮
- 📌 **迷你置顶窗口** —— 一键缩为置顶小窗，简要迷你最小宽度仅 330px
- ⌨️ **全局快捷键** —— `Ctrl+Shift+P` 在简要模式下一键清空+粘贴+输入
- 🧠 **智能缩进还原** —— 保留代码原始缩进层级，Shift+Enter 换行跳过 IDE 自动缩进
- 🎨 **玻璃拟态 UI** —— Dracula 配色 + 毛玻璃卡片 + 自定义 Maple Mono 字体
- 📦 **单文件便携** —— 打包为独立 `exe`，无需安装 Python 环境

---

## 🚀 快速开始

### 运行打包版本（推荐）

直接下载 `FakeyPaste.exe`，双击运行。程序会自动注册内置字体。

### 从源码运行

```bash
pip install keyboard pyperclip customtkinter pillow
python fakeypaste.py
```

### 构建文档站点

```bash
cd docs
npm install
npm run build     # 输出到 docs/dist/
npm run preview   # 本地预览
```

---

## ⌨️ 快捷键

| 快捷键 | 简要模式 | 高级模式 |
|---|---|---|
| `Ctrl+Shift+P` | 清空+粘贴+开始输入 | 开始输入 / 恢复输入 |
| `Ctrl+Shift+L` | 暂停输入 | 暂停输入 |

> 输入过程中快捷键自动忽略，防止误操作。

---

## ⚙️ 配置选项

| 配置项 | 默认值 | 说明 |
|---|---|---|
| 字符间隔 | 50ms | 每个字符输入的间隔时间 |
| 开始延时 | 3s | 点击开始后延迟多少秒启动输入 |
| 智能缩进 | 开启 | 保留代码原始缩进层级 |
| 缩进宽度 | 4 空格 | 缩进单位宽度 |

---

## 📁 项目结构

```
FakeyPaste/
├── fakeypaste.py          # 主程序入口
├── typing_engine.py       # 模拟输入引擎
├── clipboard_manager.py   # 剪贴板管理
├── hotkey_handler.py      # 快捷键处理
├── font_manager.py        # 字体注册管理
├── constants.py           # 常量定义
├── fonts/                 # Maple Mono 字体
├── docs/                  # Vite+Vue3 使用说明网页
│   └── dist/              # 构建产物（可直接部署）
├── app_icon.ico           # 应用图标
└── LICENSE                # GPLv3
```

---

## 📄 许可证

[GNU General Public License v3.0](LICENSE)

FakeyPaste is free software: you can redistribute it and/or modify it under the terms of the GPLv3.

---

## 👤 作者

**凯Z闪 (KaiZs)** &nbsp;·&nbsp; [GitHub](https://github.com/Kai-Zs) &nbsp;·&nbsp; [主页](https://www.kaizs.cn)

---

<p align="center"><sup>Made with ❤️ by KaiZs for seamless text input</sup></p>
