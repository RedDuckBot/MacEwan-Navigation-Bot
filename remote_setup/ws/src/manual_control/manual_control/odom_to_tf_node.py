#!/usr/bin/env python3
import rclpy  
from rclpy.node import Node 
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry

class odom_to_tf_node(Node):

    def __init__(self):
        super().__init__("odom_to_tf")

        self.tf_pub = self.create_publisher(TFMessage, "/tf", 10)
        self.odom_sub = self.create_subscription(Odometry, "/odom", self.send_tf, 10)


    def send_tf(self, odom):
        tf = TransformStamped()

        tf.header = odom.header
        tf.child_frame_id = odom.child_frame_id

        tf.transform.translation.x = odom.pose.pose.position.x
        tf.transform.translation.y = odom.pose.pose.position.y
        tf.transform.translation.z = odom.pose.pose.position.z
        tf.transform.rotation = odom.pose.pose.orientation

        msg = TFMessage()

        msg.transforms = [tf]

        self.tf_pub.publish(msg)
        


def main(args=None):
    rclpy.init(args=args)
    node = odom_to_tf_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()