#!/usr/bin/env python3
import rospy
import math
import time
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty

global turtle_pose
turtle_pose = Pose()


def poseCallback(pose_message):
    global turtle_pose
    turtle_pose.x = pose_message.x
    turtle_pose.y = pose_message.y
    turtle_pose.theta = pose_message.theta

def degree2radian(angle):
    return angle * math.pi / 180.0

def getDistance(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))

def move(speed, distance, isForward):
    vel_msg = Twist()

    if(isForward):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)

    vel_msg.linear.y = 0
    vel_msg.linear.z = 0

    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    # current time
    t0 = time.time()
    current_distance = 0.0

    loop_rate = rospy.Rate(10)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    while current_distance < distance:
        rospy.loginfo('Moving Forward')
        velocity_publisher.publish(vel_msg)

        t1 = time.time()
        current_distance = speed * (t1 - t0)
        loop_rate.sleep()

    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)    

def rotate(speed, angle, clockwise):
    vel_msg = Twist()

    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # clockwise -> negative
    if(clockwise):
        vel_msg.angular.z = -abs(speed)
    else:
        vel_msg.angular.z = abs(speed)

    current_angle = 0.0
    t0 = time.time()
    loop_rate = rospy.Rate(10)

    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    while True:
        rospy.loginfo("Rotating Rover")
        velocity_publisher.publish(vel_msg)

        t1 = time.time()
        current_angle = speed * (t1 - t0)
        loop_rate.sleep()

        if current_angle > angle:
            rospy.loginfo("Rotating Complete")
            break

    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)


def gridClean():
    loop_rate = rospy.Rate(1)
    loop_rate.sleep()
    
    rospy.loginfo("1st Point")
    move(0.2, 2.0, True)
    rospy.loginfo("1st rotate")
    rotate(0.2, degree2radian(90), False)
    loop_rate.sleep()

    rospy.loginfo("2nd Point")
    move(0.2, 2.0, True)
    rospy.loginfo("2nd rotate")
    rotate(0.2, degree2radian(90), False)
    
    rospy.loginfo("3rd Point")
    move(0.2, 2.0, True)
    rospy.loginfo("3rd rotate")
    rotate(0.2, degree2radian(90), False)
    loop_rate.sleep()

    rospy.loginfo("4th Point")
    move(0.2, 2.0, True)
    rospy.loginfo("4th rotate")
    rotate(0.2, degree2radian(90), False)
    loop_rate.sleep()
    


if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_motion', anonymous=True)

        publisher_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(publisher_topic, Twist, queue_size = 10)

        pose_topic = '/turtle1/pose'
        pose_subscriber = rospy.Subscriber(pose_topic, Pose, poseCallback)

        '''
        goal_pose = Pose()
        goal_pose.x = 1
        goal_pose.y = 1
        goal_pose.theta = 0
        moveGoal(goal_pose, 0.01)
        '''

        gridClean()
      

        time.sleep(2)

    except rospy.ROSInterruptException:
        rospy.loginfo('Node terminated')