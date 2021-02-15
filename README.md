# Example Braid Triggering

This is a ROS package. Put it in your catkin workspace and install.

You will need the ROS flydra message to run the emulator. Make sure you have this installed too: https://github.com/strawlab/ros_flydra

You will also need pynumdiff for the emulator to generate trajectories. `pip install pynumdiff`. 

# Running it

1. Emulating braid. To test things out, you can use the emulator. By default the emulator will randomly generate some trajectories that are born and die and move with some sinusoidal behavior. `rosrun braid_trigger braid_emulator.py`. You can customize your trajectories if you like, look at braid_emulator.py's main script for some hints.

2. Visualizing the trajectories. Braid publishes data in a not so ROS friendly package format. You can get some more ROS friendly topics by running `rosrun braid_trigger braid_ros_decoder.py` to republish a subset of objects to stable ROS topics, like /braid_ros_objs_0. Then run this to get a real time visualization of the x,y,z position: `rqt_plot /braid_ros_objs_0/point/x:y:z`. With a little more  work and editing to braid_ros_decoder.py it should be possible to use rviz to see a 3D rendering...  There may also be a more elegant solution in https://github.com/strawlab/ros_flydra, but I didn't get it working quickly.

2. Runing the trigger. An example volumetric trigger is given in braid_trigger_in_volume.py. It requires a configuation file, and example is given in configurations/. To run the trigger, run `rosrun braid_trigger braid_trigger_in_volume.py --config=PATH_TO_CONFIGURATION`. 
