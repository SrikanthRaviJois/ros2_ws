import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class subscriber_node(Node):
    def __init__(self):
        super().__init__("subscriber_node")
        self.subscriber = self.create_subscription(String, "/robot_news", self.subscriber_callback, 10 )
        
    def subscriber_callback(self, msg:String):
        self.get_logger().info(msg.data)
        
        
def main(args = None):
    rclpy.init(args = args)
    node = subscriber_node()
    rclpy.spin(node)
    rclpy.shutdown()