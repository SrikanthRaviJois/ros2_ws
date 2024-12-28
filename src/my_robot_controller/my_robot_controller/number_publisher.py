import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class number_publisher(Node):
    def __init__(self):
        super().__init__("number_publisher")
        self.declare_parameter("test")
        self.publisher = self.create_publisher(Int64, 'number', 10)
        self.timer = self.create_timer(1.0, self.publisher_callback)
        self.get_logger().info("Hello from ROS2")
        
    def publisher_callback(self):
        msg = Int64()
        msg.data = 5
        self.publisher.publish(msg)
        
        
def main(args=None):
    rclpy.init(args=args)
    node = number_publisher()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()