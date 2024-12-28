#!/usr/bin/env python3
import rclpy
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int32MultiArray
from cv_bridge import CvBridge
import cv2

class OpenCVNode(Node):
    def __init__(self):
        super().__init__("opencv_node")
        self.camera_sub = self.create_subscription(Image, "/camera_sensor/image_raw", self.subscriber_callback, 10)
        self.bridge = CvBridge()
        self.centre_pub = self.create_publisher(Int32MultiArray, 'centre_topic', 10)
        
    def subscriber_callback(self, msg:Image):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        #cv2.imshow('cv_image', cv_image)
        hsv= cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        light_grey= np.array([0, 100, 70])
        dark_grey= np.array([180, 255, 255])
        mask =cv2.inRange(hsv, light_grey, dark_grey)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            center2 = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]
            msg = Int32MultiArray()
            msg.data = center2
            if radius > 10:
                cv2.circle(cv_image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(cv_image, center, 5, (0, 0, 255), -1)
                self.centre_pub.publish(msg)

        cv2.imshow("cv_image", cv_image)
        cv2.waitKey(1)
        

def main(args=None):
    rclpy.init(args=args)
    node = OpenCVNode()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()