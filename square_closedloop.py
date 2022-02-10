#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

    def update_pose(self, data):

        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidean_distance(self, goal_pose):

        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=0.7): 

        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):

        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=10.5): 

        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        node = 5
        while node != 0:
            goal_pose = Pose()

            #Corners/Nodes of the desired square
            node1, node2 = (5,5)
            node3, node4 = (8,5)
            node5, node6 = (8,8)
            node7, node8 = (5,8)
            node9, node10 = (5,5)

            #Initializing the first node
            goal_pose.x = node1
            goal_pose.y = node2
            distance_tolerance = 0.01

            vel_msg = Twist()

            while self.euclidean_distance(goal_pose) > distance_tolerance:

                # Linear velocity in the x-axis.
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

                # Angular velocity in the z-axis.
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)

                # Publishing our vel_msg
                self.velocity_publisher.publish(vel_msg)

                # Publish at the desired rate.
                self.rate.sleep()
                node = node - 1 

            goal_pose = Pose()
            goal_pose.x = node3
            goal_pose.y = node4

            while self.euclidean_distance(goal_pose) > distance_tolerance:

                # Linear velocity in the x-axis.
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

                # Angular velocity in the z-axis.
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)

                # Publishing our vel_msg
                self.velocity_publisher.publish(vel_msg)

                # Publish at the desired rate.
                self.rate.sleep()
                node = node - 1 

            goal_pose = Pose()
            goal_pose.x = node5
            goal_pose.y = node6

            while self.euclidean_distance(goal_pose) > distance_tolerance:

                # Linear velocity in the x-axis.
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

                # Angular velocity in the z-axis.
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)
                
                # Publishing vel_msg
                self.velocity_publisher.publish(vel_msg)

                # Publish at the desired rate.
                self.rate.sleep()
                node = node - 1 

            goal_pose = Pose()
            goal_pose.x = node7
            goal_pose.y = node8

            while self.euclidean_distance(goal_pose) > distance_tolerance:

                # Linear velocity in the x-axis.
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

                # Angular velocity in the z-axis.
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)

                # Publishing vel_msg
                self.velocity_publisher.publish(vel_msg)

                # Publish at the desired rate.
                self.rate.sleep()
                node = node - 1 

            goal_pose = Pose()
            goal_pose.x = node9
            goal_pose.y = node10

            while self.euclidean_distance(goal_pose) > distance_tolerance:

                # Linear velocity in the x-axis.
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

                # Angular velocity in the z-axis.
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)

                # Publishing vel_msg
                self.velocity_publisher.publish(vel_msg)

                # Publish at the desired rate.
                self.rate.sleep()
                node = node - 1 

        # Stopping the robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass