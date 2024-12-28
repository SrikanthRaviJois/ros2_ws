import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class number_counter(Node):
    def __init__(self):
        super().__init__("number_counter")
        self.counter = 0
        self.subscriber = self.create_subscription(Int64, "/number", self.subscriber_callback, 10)
        self.publisher = self.create_publisher(Int64, "number_count", 10)
        self.server = self.create_service(SetBool, "reset_counter", self.server_callback)
        
    def server_callback(self, request, response):
        if request.data == True:
            self.counter = 0
        response.success = True
        response.message = "Success"
        return response
        
    def subscriber_callback(self, msg:Int64):
        self.counter += msg.data
        self.get_logger().info(str(self.counter))
        
    def publisher_callback(self):
        self.publisher.publish(self.counter)
        
def main(args=None):
    rclpy.init(args=args)
    node = number_counter()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()