import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class add_two_ints_server(Node):
    def __init__(self):
        super().__init__("add_two_ints_server")
        self.server = self.create_service(AddTwoInts, "add_two_ints", self.callback_add_two_ints)
        
    def callback_add_two_ints(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(str(response.sum))
        return response
        
def main(args=None):
    rclpy.init(args=args)
    node = add_two_ints_server()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()