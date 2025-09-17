#!/usr/bin/env python

# This code is in part inspired by the following
# code found at this url:
# http://cs460.coins-lab.org/index.php?title=Lab_05._Bug_Algorithms
# In particular, we modify the wander, 
# odomCallback, and scanCallback functions in
# the code. 

import rospy
from geometry_msgs.msg import Twist, Pose
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

# Declare some constants that will probably change during testing 
error = 0.05
vel = 0.5
goal = 7
lastmpoint = [0, 0]

# variable for laser scanning ranges
ranges = [None] * 30
x_pos = 0
y_pos = 0
z_orient = 0
pos = [x_pos, y_pos]

def Scan(data):
    '''
    Reads the laser scan input and info.
    The list is stored as a global
    variable.
    '''
    global ranges
    ranges = data.ranges

def Odom(data):
    '''
    Reads the odometry data and stores
    the x- and y-positions and the z-
    orientation as global variables.
    Uses pos as the global list for the
    Cartesian value point of the robot 
    ''' 
    global z_orient, x_pos, y_pos, pos
    x_pos = data.pose.pose.position.x
    y_pos = data.pose.pose.position.y
    pos = [x_pos, y_pos]
    z_orient = data.pose.pose.orientation.z

def nearMline():
    ''' 
    Calculates to see if the list of size two
    (which is a point) is near the M-line.
    '''
    global pos, lastmpoint
    return (abs(pos[1]) < error)

def nearEndpoint():
    '''
    Calculates to see if the list of size two
    (which is a point) is near the goal.
    '''
    global pos
    return (((pos[1])**2 + (pos[0] - goal)**2)**0.5 < error)

def returnToOrientation():
    '''
    Moves the robot until it reaches the
    original orientation it started from
    '''
    global z_orient
    move_cmd = Twist()
    r = rospy.Rate(10)
    print 'reorienting'      
    while not rospy.is_shutdown():
        move_cmd.angular.z = vel
        move_cmd.linear.x = 0.0
        if (abs(z_orient) < error):
            move_cmd.angular.z = 0
            break
        cmd_vel.publish(move_cmd)
        r.sleep()
    cmd_vel.publish(move_cmd)
    r.sleep()                        

def obstacleFollow():
    '''
    Obstacle following code for the robot
    based off of the wander() function
    from the code found online. See above
    for more notes. Also stores information
    in the global variable 'solveable' to 
    determine if the maze is solveable.
    Function takes the current point, which
    is 'published' by the odometry callback
    '''
    global solveable, ranges, pos
    move_cmd = Twist()
    r = rospy.Rate(30)
    while not rospy.is_shutdown():
        global pos, lastmpoint
        if (ranges[15] < 0.8):
            # Checks to see what the robot 'sees' in front
            move_cmd.angular.z = 5.0
            move_cmd.linear.x = 0.0
        elif (ranges[15] < 1.0):
            move_cmd.angular.z = 3.0
            move_cmd.linear.x = 0.3
        elif (ranges[15] > 2.0):
            move_cmd.angular.z = -3.0
            move_cmd.linear.x = 0.3
        elif (ranges[28] < 0.8 or ranges[2] < 0.8):
            move_cmd.angular.z = 0.0
            move_cmd.linear.x = 0.2
        else:
            move_cmd.angular.z = 0.0
            move_cmd.linear.x = 0.3
        if nearMline() and (pos[0] > lastmpoint[0]):
            # Different point near the M-line
            if pos != lastmpoint:
                lastmpoint = pos
                solveable = True
                break
            pass
        if nearMline() and abs(pos[0] - lastmpoint[0]) < 0:
            # Same point on the M-line
            solveable = False
            break
        cmd_vel.publish(move_cmd)
        r.sleep()
    move_cmd.angular.z = 0.0
    move_cmd.linear.x = 0.0
    cmd_vel.publish(move_cmd)
    r.sleep()

def bug():
    '''
    Implementation of the bug 2
    algorithm. 
    '''
    global ranges, x_pos, y_pos
    move_cmd = Twist()
    r = rospy.Rate(30)
    obstacleNumber = 0
    while not rospy.is_shutdown():
        global ranges
        if (ranges[15] < 5.0 or ranges[15] == None):
            #print 'going to goal'
            move_cmd.angular.z = 0.0
            move_cmd.linear.x = 0.25
        if (ranges[15] < 0.8 and ranges[15] != None):
            obstacleNumber += 1
            print('Encountered Obstacle ', obstacleNumber)
            lastmpoint = [x_pos, y_pos]
            print lastmpoint
            #print ranges[15]
            obstacleFollow()
            print('Done following obstacle!')
            returnToOrientation()
            if solveable == False:
                print('Failed to reach goal.  :(')
                break
        if nearEndpoint():
            print('Success! Goal reached! ', pos)
            break
        cmd_vel.publish(move_cmd)
    move_cmd.angular.z = 0.0
    move_cmd.linear.x = 0.0
    cmd_vel.publish(move_cmd)
    r.sleep()


if __name__ == '__main__':
#    try:
    rospy.init_node('ME133_Final_Project', anonymous=True)
    cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)
    move_cmd = Twist()
    odomSubscriber = rospy.Subscriber("odom", Odometry, Odom)
    laserSubscriber = rospy.Subscriber("scan", LaserScan, Scan)
    bug()

#    except:
#        rospy.loginfo("Robot node terminated.")




