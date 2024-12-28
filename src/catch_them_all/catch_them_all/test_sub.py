#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray


class test_sub(Node):
    def __init__(self):
        super().__init__("test_sub")
        self.subscriber = self.create_subscription(TurtleArray, '/alive_turtles', )
        
        
def main(args=None):
    rclpy.init(args=args)
    node = test_sub()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()