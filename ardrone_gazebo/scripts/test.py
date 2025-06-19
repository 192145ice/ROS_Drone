from ultralytics import YOLO

model = YOLO("yolov8m.pt")
results = model(r"/home/haveice/catkin_ws/src/ardrone_gazebo/scripts/image.png")

# 取出第一張圖的結果並顯示
results[0].show()
