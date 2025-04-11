#!/usr/bin/env bash
# 退出前报告错误
set -e

# 升级 pip 和安装工具
pip install --upgrade pip setuptools wheel

# 设置环境变量，强制使用纯 Python 实现
export PYAML_FORCE_PYTHON=1

# 安装依赖项（使用源代码安装）
pip install -r requirements.txt --no-binary :all:

# 这里可以添加您的其他构建命令