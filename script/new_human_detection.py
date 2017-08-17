#! /usr/bin/env python
import rospy
import numpy
import sensor_msgs
from sensor_msgs.msg import *
from math import *
from Crypto.Util.number import size
from std_msgs.msg import *
from wx.lib.pubsub import pub
from visualization_msgs.msg import *

from docutils.parsers.rst.directives import flag
from gtk import FALSE
from numpy.ma.core import abs
from _dbus_bindings import Array


class HumanDetection:
    #initializing 
    markerPublisher = visualization_msgs.msg.MarkerArray()
    HumanDetected = 0
    leg_mid_point_inclass = 0
    torso_mid_point_inclass = 0
    leg_mid_range_inclass = 0
    torso_mid_range_inclass = 0
    laserResoloution = 0.25
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
        
        ###Clear Data###
        self.leg_mid_point_inclass = 0
        self.torso_mid_point_inclass = 0
        self.leg_mid_range_inclass = 0
        self.torso_mid_range_inclass = 0
        ###End of Clear###  
        if self.t1 :
            rospy.Subscriber("/LegDetectionRange", Float32, self.call_back1range, None, 10 )    
            self.t1 = False    
#         LegFlag = rospy.wait_for_message("/LegDetectionRange", Float32,timeout=None)
#         if (LegFlag):
#             self.leg_mid_range_inclass = leg_mid_range.data
#             rospy.Subscriber("/LegDetectionPoint", Float32, self.call_back1point, None, 2 )
        
        #rospy.Subscriber("/TorsoDetection", Float32, self.call_back2, None, 2 )
        rospy.Subscriber("/HumanStart", std_msgs.msg.Bool, self.call_back, None, 10 )
        self.rate = rospy.Rate(10) # 10hz      
        
        self.humanPublish = rospy.Publisher("/HumanDetection", std_msgs.msg.Bool, queue_size = 10)
        self.markerPublisher = rospy.Publisher("/HumanMarker", visualization_msgs.msg.MarkerArray, queue_size = 10)
        self.StartPublisher = rospy.Publisher("/HumanStart", std_msgs.msg.Bool , queue_size = 1) 
        self.humanInFront = rospy.Publisher("/HumanInFront", std_msgs.msg.Bool, queue_size = 1)      
        
    def visualize(self,data):   
        arr= MarkerArray()
        arr2= MarkerArray()
        i=0
        for points in data:    
            m1=self.genMarker(points[0],points[1],True,i)  #be jaye 0 chy mi2nam bzaram?
            m3=self.genMarker_head(points[0],points[1],True,i)  #be jaye 0 chy mi2nam bzaram?
            m1.lifetime=rospy.Duration(1,1)
            m3.lifetime=rospy.Duration(1,1)
            ##m2=self.genMarker(points[2],points[3],False,i+1)
            ##m2.lifetime=rospy.Duration(1,1)                    
            arr.markers.append(m1)
            arr.markers.append(m3)
            ##arr.markers.append(m2)            
            i=i+1 #qablan i + 2 bud!
        self.markerPublisher.publish(arr)        
        self.markerPublisher.publish(arr2) 
        
    def genMarker(self,x,y,is_start,id):   
        #print "hello" #this is ok
        m = visualization_msgs.msg.Marker()         
        m.header.frame_id = '/laser'
        m.header.stamp = rospy.Time.now()        
        m.ns = 'human_points'
        m.action = visualization_msgs.msg.Marker.ADD
        m.pose.orientation.w = 1.0
        m.id=id
        m.type = visualization_msgs.msg.Marker.CYLINDER                     
        
        if(is_start==True):             
            m.color.r = 2
            m.color.b = 1
        else: m.color.g=2
        
        m.color.a = 1.0;
        
        m.pose.position.x=x
        m.pose.position.y=y
        m.pose.position.z=0.6
        
        m.pose.orientation.x=0
        m.pose.orientation.y=0
        m.pose.orientation.z=0
        m.pose.orientation.w=1
        
        m.scale.x=0.01
        m.scale.y=0.3
        m.scale.z=0.8
        
        return m
    
    def genMarker_head(self,x,y,is_start,id):   
        m2 = visualization_msgs.msg.Marker()         
        m2.header.frame_id = '/laser'    #chra bayad /laser bashe /ubg_laser chra nmishe??
        m2.header.stamp = rospy.Time.now()        
        m2.ns = 'human_head_points'
        m2.action = visualization_msgs.msg.Marker.ADD
        m2.pose.orientation.w = 1.0
        m2.id=id
        m2.type = visualization_msgs.msg.Marker.SPHERE                    
        
        if(is_start==True): 
            m2.color.r = 2
            m2.color.b = 1
        else: m2.color.g=2
        
        m2.color.a = 1.0;
        
        m2.pose.position.x=x
        m2.pose.position.y=y
        m2.pose.position.z=1.5
        
        m2.pose.orientation.x=0
        m2.pose.orientation.y=0
        m2.pose.orientation.z=0
        m2.pose.orientation.w=1
        
        m2.scale.x=0.2
        m2.scale.y=0.2
        m2.scale.z=0.23
        
        return m2
    
    def call_back1range(self,leg_mid_range):
        if self.t2:
            #print "Legs Detected"
            #self.count1 = 1 + self.count1
            #print (self.count1, "  1")         
            self.leg_mid_range_inclass = leg_mid_range.data
            #self.rate.sleep()
            self.t2 = False
            rospy.Subscriber("/LegDetectionPoint", Float32, self.call_back1point, None, 2 )
        
    def call_back1point(self,leg_mid_point):
        if self.t3 :
            #print "Legs Detected2"
            #self.count2 = 1 + self.count2
            #print (self.count2, "  2")             
            self.leg_mid_point_inclass = leg_mid_point.data
            #self.rate.sleep()
            self.t3 = False
            rospy.Subscriber("/TorsoDetectionRange", Float32, self.call_back2range, None, 2 )    

    def call_back2range(self, torso_mid_range):
        if self.t4 :
            #print "And Torso Detected"      
            #self.count3 = 1 + self.count3
            #print (self.count3, "  3")                  
            self.torso_mid_range_inclass = torso_mid_range.data
            #self.rate.sleep()                        
            self.t4 = False
            rospy.Subscriber("/TorsoDetectionPoint", Float32, self.call_back2point, None, 2 )

    def call_back2point(self, torso_mid_point):
        #print "And Torso Detected2"  
        #self.count4 = 1 + self.count4
        #print (self.count4, "  4")                        
        self.torso_mid_point_inclass = torso_mid_point.data                
        self.StartPublisher.publish(True)
        #self.rate.sleep()
         
                
        
    def call_back(self, flag):        
        #print("Starttttttttttttttttttttt")                            
        #print self.leg_mid_point_inclass
        #print self.torso_mid_point_inclass        
        if ((flag) and self.humanPublish.get_num_connections() > 0) or ((flag) and self.humanInFront.get_num_connections() > 0) : #for scenario
            res = self.laserResoloution                                            
            ii1 = self.leg_mid_point_inclass
            ii9 = self.torso_mid_point_inclass
            range1 = self.leg_mid_range_inclass
            range9 = self.torso_mid_range_inclass
            #print ii1,range1 #this is ok
            #print ii9,range9 #this is ok
            ##print "hello"         
            
            rad4 = ((ii1 * res * pi) / 180) - (pi / 2)  #"pi/2" baraye taqir noqte 0 e mokhtasat mibashad
            rad5 = ((ii9 * res * pi) / 180) - (pi / 2)
                                           
            xleg = range1 * cos(rad4) 
            yleg = range1 * sin(rad4)               
                              
            xtor = range9 * cos(rad5) 
            ytor = (range9 * sin(rad5)) #+ 0.16 #faseleye laser paEn ba bala  
            
            if ii1 != 0 and ii9 != 0 and range1 != 0 and range9 != 0 :                                                                                    
                print "qable if"
                print "x,y leg", xleg, yleg, "x,y torso", xtor, ytor
                
                if (abs(xleg - xtor) < 0.4) and (abs(yleg - (ytor - 0.16)) < 0.4) :
                    self.count = self.count + 1
                    print (self.count, "Human Detected")
                    self.humanPublish.publish(True) #for scenario      
                    if yleg < 1.5 and xleg < 1 :
                        print "there is human in front robina"
                        self.humanInFront.publish(True)                             
            
                    i = 0        
                    positions = []
                    x1 = []
                    y1 = []
                    x2 = []
                    y2 = []                                
                    ###if len(goodIndexes) > 0:    #modified  #create marker        
                    while i < 1:   #:D
                         positions.append([])
                         #positions.append([]) 
                         ##lif = Legs_Indexes[i][0] # LIF means, is, Legs Indexes First 
                         ##lie = Legs_Indexes[i][1] # chon har shakhs 2pa darad pas 1 yany paye 2vvome fard            
                         ##end = len(clustersPoints[lie]) - 1
                         ##t0 =  theta0
                         ##res = self.laserResoloution
                         #i1 =  clustersPoints[i][0]
                         #i9 =  clustersPoints[i][end]
                         ##ii1 = clustersPoints[lif][0]                        
                         ##ii9 = clustersPoints[lie][end]
                         ##rad4 = ((ii1 * res * pi) / 180) - (pi / 2)  #"pi/2" baraye taqir noqte 0 e mokhtasat mibashad
                         ##rad5 = ((ii9 * res * pi) / 180) - (pi / 2)
                                                    
                         ##x1.append(laser.ranges[ii1] * cos(rad4)) # qermez
                         ##y1.append(laser.ranges[ii1] * sin(rad4)) #+ (laser.ranges[ii1] / 2)              
                                       
                         ##x2.append(laser.ranges[ii9] * cos(rad5)) # sabz
                         ##y2.append(laser.ranges[ii9] * sin(rad5)) #+ (laser.ranges[ii9] / 4)                          
                          
                         positions[0].append(xtor)
                         positions[0].append(ytor)
                         #positions[1].append(x2[i])
                         #positions[3].append(y2[i])
                         #self.visualize(positions) # for test is here
                                       
                         i = i + 1
                         
                    self.visualize(positions) 
                                                  
        self.t1 = True
        self.t2 = True
        self.t3 = True
        self.t4 = True
                    
if __name__ == '__main__':
    
    rospy.init_node('new_human_detection', anonymous=True)
    HumanDetection = HumanDetection()
    rospy.spin() 
