# 🛸 Ardrone YOLOv8 ROS Integration

本專案整合 YOLOv8 與 ROS Gazebo 模擬器，實現無人機在模擬環境中即時物件辨識功能。

## 📦 安裝需求

### 系統環境
- Ubuntu 20.04 / 22.04
- ROS Noetic
- Gazebo 11+
- Python 3.8+

### Python 套件安裝

使用 pip 安裝：

```bash
pip install ultralytics opencv-python cv_bridge numpy
```
## 🚀 使用方式

### 1️⃣ 將檔案放入工作區裡
```bash
cd ~/catkin_ws
git clone https://github.com/192145ice/ROS_Drone.git
```
將ROS_Drone資料夾改名為src

### 2️⃣ 編譯工作區和檔案權限
```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash

cd ~/catkin_ws/src/ardrone_gazebo/scripts
chmod +x yolo_detector.py
chmod +x ardrone_teleop.py
```
### 3️⃣ 啟動模擬器與無人機模型
```bash
roslaunch ardrone_gazebo single_ardrone.launch
```

### 4️⃣ 啟動 YOLOv8 ROS 節點 + 控制移動
開新2個新bash分別跑
```bash
rosrun ardrone_gazebo ardrone_teleop.py
rosrun ardrone_gazebo yolo_detector.py 
```
畫面會顯示即時影像與物件偵測框與標籤

## 📁 專案架構說明

```bash
ardrone_gazebo/
├── launch/                  # ROS 啟動檔 (.launch)
├── models/                  # Gazebo 模型資料夾
├── plugins/                 # 自訂 Gazebo 外掛 .so 檔案
├── scripts/                 # Python 節點程式（含 YOLO 推論程式）
├── src/                     # C++ 外掛原始碼
├── urdf/                    # 無人機的 URDF 模型描述
├── world/                   # Gazebo 模擬世界檔案
├── CMakeLists.txt
└── package.xml
```

