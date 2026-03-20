#!usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math 


class WaypointNavigator(Node):
    def __init__(self):
        super().__init__('waypoint_navigator')
        self.publisher_ = self.create_publisher(Twist , "/turtle1/cmd_vel", 10)
        self.subscription_ = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.get_logger().info("Waypoint Navigator Node has been started.")

        self.waypoints = [
            (5.5, 9.0),
            (2.3, 3.5),   
            (8.7, 7.2),   
            (2.3, 7.2),   
            (8.7, 3.5),   
            (5.5, 9.0),
    ]  
        self.current_waypoint_index = 0
        self.goal_tolerance = 0.1
        self.linear_gain = 1.5
        self.angular_gain = 6.0


    def pose_callback(self, msg: Pose):
        
        if self.current_waypoint_index >= len(self.waypoints):
            self.get_logger().info("All waypoints reached.")
            self.publisher_.publish(Twist())
            return
        
        tx, ty = self.waypoints[self.current_waypoint_index]

        dx = tx - msg.x
        dy = ty - msg.y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance < self.goal_tolerance:
            self.get_logger().info(f"Waypoint {self.current_waypoint_index}: ({tx}, {ty}) reached.")

            self.current_waypoint_index += 1
            return
        

        angle_to_goal = math.atan2(dy, dx)
        heading_error = angle_to_goal - msg.theta
        heading_error = math.atan2(math.sin(heading_error), math.cos(heading_error))

        cmd = Twist()
        cmd.linear.x = min(self.linear_gain * distance, 2.0)
        cmd.angular.z = self.angular_gain * heading_error
        self.publisher_.publish(cmd)



def main(args=None):
    rclpy.init(args=args)
    waypoint_navigator = WaypointNavigator()
    rclpy.spin(waypoint_navigator)
    rclpy.shutdown()


if __name__ == '__main__':
    main()