#!/bin/bash
# ┌─────────────────────────────────────────────────────────────┐
# │ 脚本模版：一键弹终端，启动项目节点，方便看各节点 log          │
# │                                                             │
# │ 以后给新项目写启动脚本，复制改：                               │
# │ ① --title="窗口标题"                                         │
# │ ② ros2 run 包名 节点名 ...（要几个节点写几行）                 │
# │                                                             │
# │ 节点启动规则：                                                │
# │ - 最后一行不加 &  → 前台跑，Ctrl+C 停这个节点也停全部          │
# │ - 前面加 &         → 后台跑                                    │
# │ - trap 'kill 0'    → Ctrl+C 时杀掉本终端所有子进程              │
# └─────────────────────────────────────────────────────────────┘
#
# 用法：
#   ./start.sh                          # 弹终端，启动 launch 文件
#
# 和 launch 文件的区别：
#   - launch 文件：一体管理，Ctrl+C 全部停，生命周期统一
#   - start.sh：独立终端，关了不影响其他节点，适合调试看 log

# ── 配置 ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"  # scripts/ 目录
WS_DIR="$(dirname "${SCRIPT_DIR}")"          # ros2_ws/ 目录

# ── 弹新终端，在里面启动所有节点 ──
gnome-terminal --title="话题通信" -- bash -c "
  # ① 必须先 source ROS2 环境
  source ${WS_DIR}/install/setup.bash

  # ② 运行 launch 文件
  # 格式：ros2 launch 包名 launch文件名
  ros2 launch learning_topic topic_demo_launch.py
" &
