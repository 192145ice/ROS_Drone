#!/usr/bin/env python3

import rospy
import sys
import tty
import termios
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates

class KeyboardControl:
    def __init__(self):
        self.rate = rospy.Rate(10)
        self.takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=10)
        self.land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=10)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.current_z = 0.0
        self.drone_name = "ardrone_gazebo"  # 替換成你機器人的名字
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.z_callback)
        rospy.sleep(2)

        self.takeoff_msg = Empty()
        self.land_msg = Empty()
        self.cmd_msg = Twist()

    def z_callback(self, data):
        if self.drone_name in data.name:
            index = data.name.index(self.drone_name)
            self.current_z = data.pose[index].position.z

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def smooth_land(self):
        rospy.loginfo("降落程序...")
        twist = Twist()

        while not rospy.is_shutdown():
            z = self.current_z

            if z > 2.0:
                twist.linear.z = -1.0  # 快速下降
            elif z > 0.2:
                twist.linear.z = -0.3  # 緩慢下降
            else:
                twist.linear.z = 0.0
                self.cmd_vel_pub.publish(twist)
                rospy.sleep(1)
                self.land_pub.publish(self.land_msg)
                break

            self.cmd_vel_pub.publish(twist)
            self.rate.sleep()

    def run(self):
        rospy.loginfo("Keyboard control started. Use WASD to move, QE to turn, RF for up/down, T to takeoff, L to land, Ctrl-C to exit.")
        while not rospy.is_shutdown():
            key = self.get_key()
            twist = Twist()

            if key == 'w':
                twist.linear.x = 1.0
            elif key == 's':
                twist.linear.x = -1.0
            elif key == 'a':
                twist.linear.y = 1.0
            elif key == 'd':
                twist.linear.y = -1.0
            elif key == 'q':
                twist.angular.z = 1.0
            elif key == 'e':
                twist.angular.z = -1.0
            elif key == 'r':
                twist.linear.z = 1.0
            elif key == 'f':
                twist.linear.z = -1.0
            elif key == 't':
                rospy.loginfo("Takeoff!")
                self.takeoff_pub.publish(self.takeoff_msg)
                continue
            elif key == 'l':
                if self.current_z > 2.0:
                    self.smooth_land()
                else:
                    rospy.loginfo("高度已低，直接降落")
                    self.land_pub.publish(self.land_msg)
                continue
            elif key == '\x03':  # Ctrl-C
                break
            else:
                twist.linear.x = 0.0
                twist.linear.y = 0.0
                twist.linear.z = 0.0
                twist.angular.x = 0.0
                twist.angular.y = 0.0
                twist.angular.z = 0.0

            self.cmd_vel_pub.publish(twist)
            self.rate.sleep()

if __name__ == "__main__":
    rospy.init_node('keyboard_control', anonymous=True)
    keyboard_control = KeyboardControl()
    try:
        keyboard_control.run()
    except rospy.ROSInterruptException:
        pass


