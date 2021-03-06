#! /usr/bin/env python
import rospy

from sensor_msgs.msg import *
from math import *
from std_msgs.msg import *
from visualization_msgs.msg import *

from numpy.ma.core import abs


class HumanDetection:
    markerPublisher = visualization_msgs.msg.MarkerArray()
    HumanDetected = 0
    leg_mid_point_inclass = 0
    torso_mid_point_inclass = 0
    leg_mid_range_inclass = 0
    torso_mid_range_inclass = 0
    laserResoloution = 0.5  # TODO :: make it dynamic
    pi = 3.14159
    count = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    t1 = True
    t2 = True
    t3 = True
    t4 = True
                           
    def __init__(self):                
        self.leg_mid_point_inclass = 0
        self.torso_mid_point_inclass = 0
        self.leg_mid_range_inclass = 0
        self.torso_mid_range_inclass = 0

        if self.t1:
            rospy.Subscriber("/LegDetectionRange", Float32, self.call_back1range, None, 10)
            self.t1 = False

        rospy.Subscriber("/HumanStart", std_msgs.msg.Bool, self.call_back, None, 10)
        self.rate = rospy.Rate(10)  # 10hz
        
        self.humanPublish = rospy.Publisher("/HumanDetection", std_msgs.msg.Bool, queue_size=10)
        self.markerPublisher = rospy.Publisher(
            "/HumanMarker", visualization_msgs.msg.MarkerArray, queue_size=10
        )
        self.StartPublisher = rospy.Publisher("/HumanStart", std_msgs.msg.Bool, queue_size=1)
        self.humanInFront = rospy.Publisher("/HumanInFront", std_msgs.msg.Bool, queue_size=1)
        
    def visualize(self, data):
        arr = MarkerArray()
        arr2 = MarkerArray()
        i = 0
        for points in data:    
            m1 = self.genMarker(points[0], points[1], True, i)
            m3 = self.genMarker_head(points[0], points[1], True, i)
            m1.lifetime = rospy.Duration(1, 1)
            m3.lifetime = rospy.Duration(1, 1)
            arr.markers.append(m1)
            arr.markers.append(m3)
            i += 1  # qablan i + 2 bud!
        self.markerPublisher.publish(arr)        
        self.markerPublisher.publish(arr2) 
        
    def genMarker(self, x, y, is_start, id):
        m = visualization_msgs.msg.Marker()
        m.header.frame_id = '/velodyne'
        m.header.stamp = rospy.Time.now()        
        m.ns = 'human_points'
        m.action = visualization_msgs.msg.Marker.ADD
        m.pose.orientation.w = 1.0
        m.id=id
        m.type = visualization_msgs.msg.Marker.CYLINDER                     
        
        if is_start:
            m.color.r = 2
            m.color.b = 1
        else:
            m.color.g = 2
        
        m.color.a = 1.0
        
        m.pose.position.x = x
        m.pose.position.y = y
        m.pose.position.z = -0.4
        
        m.pose.orientation.x = 0
        m.pose.orientation.y = 0
        m.pose.orientation.z = 0
        m.pose.orientation.w = 1
        
        m.scale.x = 0.01
        m.scale.y = 0.3
        m.scale.z = 0.8
        
        return m
    
    def genMarker_head(self, x, y, is_start, id):
        m2 = visualization_msgs.msg.Marker()         
        m2.header.frame_id = '/velodyne'
        m2.header.stamp = rospy.Time.now()        
        m2.ns = 'human_head_points'
        m2.action = visualization_msgs.msg.Marker.ADD
        m2.pose.orientation.w = 1.0
        m2.id=id
        m2.type = visualization_msgs.msg.Marker.SPHERE                    
        
        if is_start:
            m2.color.r = 2
            m2.color.b = 1
        else:
            m2.color.g = 2
        
        m2.color.a = 1.0
        
        m2.pose.position.x = x
        m2.pose.position.y = y
        m2.pose.position.z = 0.5
        
        m2.pose.orientation.x = 0
        m2.pose.orientation.y = 0
        m2.pose.orientation.z = 0
        m2.pose.orientation.w = 1
        
        m2.scale.x = 0.2
        m2.scale.y = 0.2
        m2.scale.z = 0.23
        
        return m2
    
    def call_back1range(self, leg_mid_range):
        if self.t2:
            self.leg_mid_range_inclass = leg_mid_range.data
            self.t2 = False
            rospy.Subscriber("/LegDetectionPoint", Float32, self.call_back1point, None, 2)
        
    def call_back1point(self, leg_mid_point):
        if self.t3:
            self.leg_mid_point_inclass = leg_mid_point.data
            self.t3 = False
            rospy.Subscriber("/TorsoDetectionRange", Float32, self.call_back2range, None, 2)

    def call_back2range(self, torso_mid_range):
        if self.t4:
            self.torso_mid_range_inclass = torso_mid_range.data
            self.t4 = False
            rospy.Subscriber("/TorsoDetectionPoint", Float32, self.call_back2point, None, 2)

    def call_back2point(self, torso_mid_point):
        self.torso_mid_point_inclass = torso_mid_point.data                
        self.StartPublisher.publish(True)
        
    def call_back(self, flag):
        veto = True
        if (flag and self.humanPublish.get_num_connections() > 0) or \
                (flag and self.humanInFront.get_num_connections() > 0) or veto:
            res = self.laserResoloution                                            
            ii1 = self.leg_mid_point_inclass
            ii9 = self.torso_mid_point_inclass
            range1 = self.leg_mid_range_inclass
            range9 = self.torso_mid_range_inclass

            rad4 = ((ii1 * res * pi) / 180) - pi  # "-pi" is a TF
            rad5 = ((ii9 * res * pi) / 180) - pi  # "-pi" is a TF
                                           
            xleg = range1 * cos(rad4) 
            yleg = range1 * sin(rad4)               
                              
            xtor = range9 * cos(rad5) 
            ytor = range9 * sin(rad5)
            
            if ii1 != 0 and ii9 != 0 and range1 != 0 and range9 != 0:
                # print "x,y leg", xleg, yleg, "x,y torso", xtor, ytor
                
                if (abs(xleg - xtor) < 0.4) and (abs(yleg - ytor) < 0.4):
                    self.count = self.count + 1
                    print (self.count, "Human Detected")
                    self.humanPublish.publish(True)  # for scenario
                    if yleg < 1.5 and xleg < 1:
                        print "there is human in front robina"
                        self.humanInFront.publish(True)                             
            
                    i = 0        
                    positions = []
                    while i < 1:  # :D
                        positions.append([])
                        positions[0].append(xtor)
                        positions[0].append(ytor)

                        i = i + 1
                         
                    self.visualize(positions) 
                                                  
        self.t1 = True
        self.t2 = True
        self.t3 = True
        self.t4 = True


if __name__ == '__main__':
    rospy.init_node('agn_human_detection', anonymous=True)
    HumanDetection = HumanDetection()
    rospy.spin() 
