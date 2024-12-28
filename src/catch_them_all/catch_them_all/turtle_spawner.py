#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
import random

class TurtleSpawner(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        self.timer = self.create_timer(7.0, self.spawn_turtle)
        self.publisher1 = self.create_publisher(TurtleArray, "/alive_turtles", 10)
        self.alive_turtles = []
        self.count = 2
        self.x = 0.0
        self.y = 0.0
    
    def publisher_callback(self):
        msg = Turtle()
        msg.name = "turtle" + str(self.count)
        msg.x_coord = self.x
        msg.y_coord = self.y
        self.count += 1        
        self.alive_turtles.append(msg)
        msg2 = TurtleArray()
        msg2.turtles = self.alive_turtles
        self.publisher1.publish(msg2)
    
    def spawn_turtle(self):
        client = self.create_client(Spawn, "/spawn")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for server...")
        request = Spawn.Request()
        request.x = random.uniform(0.0, 11.0)
        self.x = request.x
        request.y = random.uniform(0.0, 11.0)
        self.y = request.y
        request.theta = 0.0       
        
        future = client.call_async(request)
        future.add_done_callback(self.callback_spawn_turtle) 
        
        
    def callback_spawn_turtle(self, future):
        try:
            response = future.result()
            self.publisher_callback()
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))
        
def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawner()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()