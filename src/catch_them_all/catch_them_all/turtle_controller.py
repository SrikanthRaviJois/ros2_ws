#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import Kill
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.msg import Turtle
from turtlesim.msg import Pose
import math

class turtle_controller(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.pose_sub = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.subscriber = self.create_subscription(TurtleArray, "/alive_turtles", self.subscriber_callback, 10)
        self.publisher =self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.error_theta = 0.0
        self.distance = 0.0
        self.location_x = 0.0
        self.location_y = 0.0
        self.theta = 0.0
        self.alive_turtles_array = []
        self.counter = 0
        
    def kill_turtle(self):
            client = self.create_client(Kill, "/kill")
            while not client.wait_for_service(1.0):
                self.get_logger().warn("Waiting for server...")
            request = Kill.Request()
            request.name = str(self.alive_turtles_array[self.counter].name)
            
            future = client.call_async(request)
            future.add_done_callback(self.remove_turtle) 
        
    def pose_callback(self, temp: Pose):
        if len(self.alive_turtles_array) != 0:
            self.get_logger().info(str(temp.x) + str(temp.y))
            self.location_x = temp.x
            self.location_y = temp.y
            self.theta = temp.theta
            error_x = (self.alive_turtles_array[self.counter].x_coord - self.location_x)
            error_y = (self.alive_turtles_array[self.counter].y_coord - self.location_y)
            self.distance = (error_x**2 + error_y**2)**0.5
            desired_theta = math.atan2(error_y, error_x)
            self.error_theta =  (desired_theta - self.theta)
            Kp_dist = 0.7
            Kp_theta = 2
            while self.error_theta > math.pi:
                self.error_theta -= 2.0 * math.pi
            while self.error_theta < -math.pi:
                self.error_theta += 2.0 * math.pi

            l_v = Kp_dist * abs(self.distance)
            a_v = Kp_theta * self.error_theta  
            cmd_vel = Twist()
            cmd_vel.linear.x = l_v
            cmd_vel.angular.z = a_v
            self.publisher.publish(cmd_vel)
            if self.distance <= 0.2:
                self.kill_turtle()

    def remove_turtle(self, future):
        try:
            result =future.result()
            if self.counter < len(self.alive_turtles_array)-1:
                self.counter += 1
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))
        
        
    def subscriber_callback(self, msg: TurtleArray):
        self.alive_turtles_array = msg.turtles
        
        
        
def main(args=None):
    rclpy.init(args=args)
    node = turtle_controller()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()