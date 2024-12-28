import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class Publisher(Node):
    def __init__(self):
        super().__init__("publisher_node")
        self.publisher = self.create_publisher(String, "robot_news", 10)
        self.timer = self.create_timer(0.5, self.publish_news)
        self.get_logger().info("hello from ROS2")
    
    def publish_news(self):
        msg = String()
        msg.data = "Hello"
        self.publisher.publish(msg)
        
def main(args = None):
    rclpy.init(args = args)
    node = Publisher()
    rclpy.spin(node)
    rclpy.shutdown()