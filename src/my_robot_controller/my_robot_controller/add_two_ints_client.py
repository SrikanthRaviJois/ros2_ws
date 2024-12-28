#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial

class add_two_ints_client(Node):
    def __init__(self):
        super().__init__("add_two_ints_client")
        input_a = int(input("Enter value of a"))
        input_b = int(input("Enter value of b"))
        self.client = self.create_client(AddTwoInts, "add_two_ints")
        while not self.client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for server...")
        request = AddTwoInts.Request()
        request.a = input_a
        request.b = input_b
        
        future = self.client.call_async(request)
        future.add_done_callback(partial(self.callback_add_two_ints, a = input_a, b = input_b))
        
    def callback_add_two_ints(self, future, a, b):
        try:
            response = future.result()
            self.get_logger().info(str(a) + '+' + str(b) + '=' + str(response.sum))
        except Exception as e:
            self.get_logger().error("Error!")
        
        
def main(args=None):
    rclpy.init(args=args)
    node = add_two_ints_client()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()