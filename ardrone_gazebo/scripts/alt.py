#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import ModelStates

class AltitudeMonitor:
    def __init__(self):
        rospy.init_node('altitude_monitor')
        self.drone_name = "ardrone_gazebo"  # ← 替換成你在 /gazebo/model_states 中看到的無人機名稱
        self.z = 0.0
        self.sub = rospy.Subscriber("/gazebo/model_states", ModelStates, self.callback)
        rospy.Timer(rospy.Duration(1.0), self.print_altitude)  # 每 1 秒印一次高度

    def callback(self, data):
        if self.drone_name in data.name:
            index = data.name.index(self.drone_name)
            self.z = data.pose[index].position.z
        else:
            rospy.logwarn(f"找不到模型名稱 '{self.drone_name}'")

    def print_altitude(self, event):
        rospy.loginfo(f"目前高度 Z = {self.z:.2f} 公尺")

if __name__ == '__main__':
    try:
        AltitudeMonitor()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
