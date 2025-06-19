#!/usr/bin/env python3
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from ultralytics import YOLO

class YoloRosNode:
    def __init__(self):
        rospy.init_node('yolov8_ros_node', anonymous=True)
        self.model = YOLO("yolov8n.pt")  # 輕量版
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/ardrone/front_camera/image_raw", Image, self.image_callback)
        self.frame_count = 0
        rospy.loginfo("✅ YOLOv8 ROS 節點啟動完成，等待影像...")

    def image_callback(self, msg):
        self.frame_count += 1
        if self.frame_count % 5 != 0:   
            return  # 跳過部分幀，降低負載

        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            # 調整置信度與IoU閾值參數
            results = self.model(frame, conf=0.35, iou=0.45)  # conf和iou都可調

            result = results[0]
            boxes = result.boxes

            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = f"{self.model.names[cls_id]} {conf:.2f}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)

            cv2.imshow("YOLOv8 Detection", frame)
            cv2.waitKey(5)
        except Exception as e:
            rospy.logerr(f"❌ 影像處理錯誤: {e}")


    def run(self):
        rospy.spin()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        node = YoloRosNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
