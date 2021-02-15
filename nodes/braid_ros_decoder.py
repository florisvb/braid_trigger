#!/usr/bin/env python

# Command line arguments
from optparse import OptionParser

# ROS imports
import roslib, rospy

# numpy imports - basic math and matrix manipulation
import numpy as np
import time

import yaml

from geometry_msgs.msg import PointStamped

# flydra message
from ros_flydra.msg import *

################################################################################

################################################################################

class BraidDecoder:
    def __init__(self, 
                 num_objects=3,
                 braid_topic="/flydra_mainbrain/super_packets"):
        '''
        Choose the three "oldest" objects and republish those to standard ROS messages for viewing on rtk_plot, etc.
        '''

        self.num_objects = num_objects

        # Subscriber
        self.braid_sub = rospy.Subscriber(braid_topic, flydra_mainbrain_super_packet, self.trigger_callback)

        # Publishers
        self.braid_ros_obj = [rospy.Publisher('braid_ros_objs_'+str(i), PointStamped) for i in range(num_objects)]
        
        # keep track of how old objects are, and when last trigger was
        self.obj_birth_times = {}
        self.braid_to_ros_obj_mapping = {}

    def run(self):
        # ROS
        rospy.init_node('braid_decoder', anonymous=True)
        rospy.spin()

    def trigger_callback(self, super_packet):
        tcall = time.time()
        obj_ids = []
        for packet in super_packet.packets:
            for obj in packet.objects:
                obj_ids.append(obj.obj_id)

                # if it is a new object, save birth time
                if obj.obj_id not in self.obj_birth_times.keys():
                    self.obj_birth_times[obj.obj_id] = tcall
                    continue
                # if it is an old object, check to make sure the trajectory is long enough
                elif (tcall - self.obj_birth_times[obj.obj_id]) < 0.2:
                    continue

                # If trajectory is long enough and there is an open slot, map it to the open slot
                if obj.obj_id not in self.braid_to_ros_obj_mapping.keys():
                    if len(self.braid_to_ros_obj_mapping) < self.num_objects:
                        n = 0
                        while n in self.braid_to_ros_obj_mapping.values():
                            n += 1

                        self.braid_to_ros_obj_mapping[obj.obj_id] = n

                # if this is an object that is being mapped, then publish the point
                if obj.obj_id in self.braid_to_ros_obj_mapping.keys():
                    msg = PointStamped()
                    msg.point.x = obj.position.x
                    msg.point.y = obj.position.y
                    msg.point.z = obj.position.z 
                    msg.header.stamp = rospy.Time.now()
                    msg.header.frame_id = 'origin'

                    n = self.braid_to_ros_obj_mapping[obj.obj_id]
                    self.braid_ros_obj[n].publish(msg)

        
        # kill off old objects
        for obj_id in self.obj_birth_times.keys():
            if obj_id not in obj_ids:
                self.obj_birth_times.pop(obj_id, None)
                self.braid_to_ros_obj_mapping.pop(obj_id, None)
################################################################################

if __name__ == '__main__':    
    parser = OptionParser()
    parser.add_option("--num_objects", type="int", dest="num_objects", default=5,
                        help="Max number of objects to keep track of?")
    (options, args) = parser.parse_args()

    braid_decoder = BraidDecoder(num_objects=options.num_objects)
    braid_decoder.run()




    
