"""
Author: Johan Kok Zhi Kang 

Description:
This module serves as the motion planner for the UR5 robot. The environment models the actual
competition from APC 2016. 

The file UR5.dae contains the UR5 robot collada model. The manipulator present is called "arm".
Details can be found on OpenRave main site, universalrobots-ur6-85-5-a Robot. 

Sequence of use:
a) Initialize OP_motion_planning object
b) Call init_planning_setup to initialize robot configuration and collision checking
c) Call optimize to obtain trajectories 
d) Call simulate to display motion

Dependencies:
1) Openrave 0.9
2) TrajOpt
3) or_ompl python bindings
4) ur5_lib.py		- Custom library with UR5 kinematics
5) UR5.dae
6) apc_env.xml
"""


import openravepy as op
import trajoptpy
import json
import time
import IPython
import numpy as np
import rospy
from ur5_lib import Ur5_motion_planner
from trajoptpy.check_traj import traj_is_safe


class OR_motion_planning:
	def __init__(self, env_file):
		"""
		Constructor to initialize the environment and the UR5 robot in APC 2016 settings
		params: 
			env_file <string>	: 	The environment file you want to load
		"""
		self.env 			= op.Environment()
		self.load_environment_context(env_file)

		self.robot 			= self.env.GetRobots()[0]
		self.mario_arm 		= self.robot.GetManipulator('arm')

		self.ur_kin 		= Ur5_motion_planner()

	def load_environment_context(self, env_file):
		try:
			self.env.StopSimulation()
			self.env.SetViewer('qtcoin')
			self.env.Load(env_file)
		except Exception as e:
			print("Failed to load environment")
		return

	def init_planning_setup(self, init_joint_val, collision_struct):
		# Before planning, initilize robot's current configuration and collision checking options
		try:
			self.__init_arm_joint(init_joint_val)
			self.__init_collision_checker(collision_struct)
		except Exception as e:
			print("Failed to initialize planning setup")
			print(e)

	def __init_arm_joint(self, init_joint_val):
		with self.env:
			arm_indx 				= self.mario_arm.GetArmIndices()
			self.get_robot().SetActiveDOFs(arm_indx)	
			self.get_robot().SetActiveManipulator(self.mario_arm)	
			self.get_robot().SetActiveDOFValues(init_joint_val)

	def __init_collision_checker(self, collision_struct):
		"""
		params: 
			collision_struct <dict> with <key> : <param> values:
				checker <string> : The name of the Checker used for collision detection. Eg. 'pqp' collision checker
				collision_options <list><op::CollisionOptions> : Various collision options available expressed as a list
		"""
		checker 					= collision_struct['checker']
		collision_options 			= collision_struct['collision_options']
		collisionChecker 			= op.RaveCreateCollisionChecker(self.env, checker)

		j = 0
		for i in collision_options:
			j = j|i

		collisionChecker.SetCollisionOptions(j)
		self.env.SetCollisionChecker(collisionChecker)

	def optimize_ompl_trajopt(self, joint_target, algorithm):
		"""
		Optimization of the robot via initialization of motion through different way points
		We start by perform intermediate way point calculations using the OMPL planner with given algorithm
		Optimization of the trajectory is done through a call to TrajOpt
		Params:
			joint_target <list><list><float>	: A series of joint goals combined to form a list
			algorithm <string>					: OMPL_*** algorithm. If 'RRTConnect', then we are using the 'OML_RRTConnect' algorithm
		"""
		# self.__update_DOF()		# Call to refresh DOF of the robot
		trajectory 					= self.__init_traj(joint_target=joint_target, algorithm=algorithm) # Performs initial OMPL_*** planning
		self.traj 					= []
		trajectory_interp 			= self.__interpolate(trajectory=trajectory, n=10)	# Interpolation between waypoints generated by OMPL for finer resolution

		self.__set_request(joint_goal=trajectory[-1], n_steps=len(trajectory_interp))
		self.request.update({"init_info" : {"type" : "given_traj", "data" : trajectory_interp}})				# Way point initialization after path planning			

		jd 							= json.dumps(self.request) 					
		prob 						= trajoptpy.ConstructProblem(jd, self.env) 	
		result 						= trajoptpy.OptimizeProblem(prob) 			

		# if self.__check_safe(result.GetTraj()):
		# 	pass
		# else:
		# 	raise Exception('No path is safe')
	 	#final_trajectory 	=	planner.optimize_ompl_trajopt(joint_target=joint_target, algorithm="RRTstar")
		return result.GetTraj().tolist()

	def __init_traj(self, joint_target, algorithm):
		"""
		Creates an initial trajectory plan between start and end goal poses
		"""
		# Issue with the init and goal configuratons -> Planner thinks that the arms are in collision

		algo 					= "OMPL_" + algorithm
		planner 				= op.RaveCreatePlanner(self.env, algo)		# Initializes a planner with algorithm
		simplifier 				= op.RaveCreatePlanner(self.env, 'OMPL_Simplifier')

		params 		 			= planner.PlannerParameters()				# Creates an empty param to be filled 
		params.SetRobotActiveJoints(self.robot)
		params.SetGoalConfig(joint_target)

		extraParams 			= ('<_nmaxiterations>{:d}</_nmaxiterations>'.format(10000))

		params.SetExtraParameters(extraParams)

		with self.env:
			with self.get_robot():
				print "Starting intial plan using {:s} algorithm".format(algorithm)
				traj 		= op.RaveCreateTrajectory(self.env, '')
				planner.InitPlan(self.get_robot(), params)
				result 		= planner.PlanPath(traj)
				IPython.embed()
				assert result == op.PlannerStatus.HasSolution

				# print 'Calling the OMPL_Simplifier for shortcutting.'
				# simplifier.InitPlan(self.get_robot(), op.Planner.PlannerParameters())
				# result 		= simplifier.PlanPath(traj)
				# assert result == op.PlannerStatus.HasSolution

				trajectory 	= [traj.GetWaypoint(i).tolist() for i in range(traj.GetNumWaypoints())]
				return trajectory

	def __interpolate(self,trajectory, n=10):
		"""
		Takes in a trajectory in joint space and interpolates between successive trajectories
		This is done to provide TrajOpt with more points to perform its optimization
		"""
		interpolated_traj 				= []

		for itr in range(len(trajectory) -1):
			current_arm_pose			= trajectory[itr]
			next_arm_pose				= trajectory[itr +1]

			start 						= np.array(current_arm_pose)
			end 						= np.array(next_arm_pose)
			interpolated_traj 			+= [list(start + ii*(end - start)/(n)) for ii in range(n +1)]

		# TODO: Figure out how to change a 3D X / Y / Z orientation into joint space. Read up about TrajOpt to understand how it works
		return interpolated_traj

	def __set_request(self, joint_goal, n_steps):
		"""
		Initializes a request dictionary that allows for TrajOpt motion planning
		You can change the collision cost penalties as well as the distance to enforce those penalties
		You can add now constraints and penalties if you want
		Params:
			manip <string>			 : "left_arm" or "right_arm"
			joint_goal <list><float> : The goal (in DOF space) to be reached by the planning arm (manip)
			n_steps <int>			 : Number of planning points for TrajOpt. Must correspond to the number of points generated by OMPL
		"""
		self.plan_arm 	= self.mario_arm 	# Sets the planning arm for visual purpose
		self.goal 		= joint_goal

		self.request = {
		  "basic_info" : {
			"n_steps" : n_steps,
			"manip" : "arm",
			"start_fixed" : True 			# i.e., DOF values at first timestep are fixed based on current robot state
		  },

		  "costs" : [
		  {
			"type" : "joint_vel", 			# joint-space velocity cost
			"params": {"coeffs" : [100]} 	# list of length 1 is will be expanded to all DOF 
		  },
		  {
		  	# Self collision checker
			"type" : "collision",
			"params" : {
			  "coeffs" : [10000], 
			  "dist_pen" : [0.05], 			# robot-obstacle distance that penalty kicks in. expands to length n_timesteps
			  "continuous" : True
			}
		  },

		  {
			"type" : "collision",
			"params" : {
			  "coeffs" : [10000], # penalty coefficients. list of length one is automatically expanded to a list of length n_timesteps
			  "dist_pen" : [0.05], # robot-obstacle distance that penalty kicks in. expands to length n_timesteps
			  "continuous" : False
			}
		  }    
		  ],

		  "constraints" : [
		  {
			"type" : "joint", # joint-space target
			"params" : {"vals" : joint_goal} # length of vals = # dofs of manip
			},	
		  ]
		}
		return

	def __get_n_val(self, starting_cartesian, target_cartesian, steps_per_meter):
		start 					= np.array(starting_cartesian)
		end 					= np.array(target_cartesian)
		dist 					= np.linalg.norm(end -start)
		n_steps 				= np.ceil(dist *steps_per_meter)

		return int(n_steps)

	def __get_n_steps_from_dist(self, starting_DOF, joint_target):
		starting_cartesian 		= self.ur_kin.cartesian_from_joint(starting_DOF)[3:]
		target_cartesian 		= self.ur_kin.cartesian_from_joint(joint_target)[3:]
		steps_per_meter			= 350 		# 100 steps per meter

		return self.__get_n_val(starting_cartesian, target_cartesian, steps_per_meter)

	def optimize_trajopt(self, joint_target):

		def __construct_problem(request):
			jd 				= json.dumps(request) # convert dictionary into json-formatted string
			prob 			= trajoptpy.ConstructProblem(jd, self.env) # create object that stores optimization problem
			return trajoptpy.OptimizeProblem(prob) # do optimization

		starting_DOF 		= self.get_manip_DOF()

		n_steps = self.__get_n_steps_from_dist(starting_DOF, joint_target)

		request = {
		  "basic_info" : {
		    "n_steps" : n_steps,
		    "manip" : "arm", # see below for valid values
		    "start_fixed" : True # i.e., DOF values at first timestep are fixed based on current robot state
		  },
		  "costs" : [
		  {
			"type" : "joint_vel", 			# joint-space velocity cost
			"params": {"coeffs" : [1]} 	# list of length 1 is will be expanded to all DOF 
		  },
		  {
		  	# Self collision checker
			"type" : "collision",
			"params" : {
			  "coeffs" : [100], 
			  "dist_pen" : [0.01], 			# robot-obstacle distance that penalty kicks in. expands to length n_timesteps
			  "continuous" : True
			}
		  },

		  {
			"type" : "collision",
			"params" : {
			  "coeffs" : [100], # penalty coefficients. list of length one is automatically expanded to a list of length n_timesteps
			  "dist_pen" : [0.01], # robot-obstacle distance that penalty kicks in. expands to length n_timesteps
			  "continuous" : False
			}
		  }    
		  ],
		  "constraints" : [
	  		{
		    "type" : "joint", # joint-space target
		    "params" : {"vals" : joint_target } # length of vals = # dofs of manip
		  },
			{	
		    "type" : "cart_vel",
		    "name" : "cart_vel",
		    "params" : {
		        "max_displacement" : 0.1,
		        "first_step" : 0,
		        "last_step" : n_steps-1, #inclusive
		        "link" : "link6"
		    },
		  }
		  ],
		  "init_info" : {
		      "type" : "straight_line", # straight line in joint space.
		      "endpoint" : joint_target
		      # "type" : "stationary",
		  }
		}

		result 							= __construct_problem(request)

		try:
			assert traj_is_safe(result.GetTraj(), self.robot) 
		except AssertionError:
			print("Straight line planning failed. Reverting to stationary planning")
			self.get_robot().SetActiveDOFValues(starting_DOF)		# Reset arm positioning

			request["init_info"]		= {"type" : "stationary"}
			result 						= __construct_problem(request)

		rospy.loginfo("No of points -> {0}".format(n_steps))
		return result.GetTraj()

	def simulate(self, trajectory):
		"""
		Call to simulate the movement of the desired manip to joint goal
		"""
		for each_traj in trajectory:
			self.robot.SetDOFValues(each_traj, self.get_manip().GetArmIndices())
			time.sleep(0.05)

	def __check_safe(self, trajectory):
		"""
		Asserts a safe path by calling the collision checker through every iteration of the resultant trajectory
		Return:
			bool : If the path is safe then return True, else False
		"""
		self.env.GetCollisionChecker().SetCollisionOptions(op.CollisionOptions.Contacts)

		for each_traj in trajectory:
			self.robot.SetDOFValues(each_traj, self.get_manip().GetArmIndices())
			flag = self.env.CheckCollision(kin.GetLinks()[3], kin.GetLinks()[6])		

			if flag == True:
				return False		# That means that collision happened
			time.sleep(0.05)
		return True

	def get_robot(self):	
		return self.robot

	def get_manip(self):
		return self.mario_arm

	def get_manip_DOF(self):
		return self.get_manip().GetArmDOFValues()

	def set_manip_DOF(self, DOF):
		"""
		Sets the DOF for a given manipulator. Thereafter, a call to update the global DOF status of the robot will be done
		""" 
		arm_indices				= self.get_manip().GetArmIndices()
		self.get_robot().SetDOFValues(DOF, arm_indices)


if __name__ == "__main__":	
	joint_start 		= [-0.97,0.2,-1.4,2.75,1.5,0]
	bin1 				= [-0.3,0,1,2.2,1.8,0]
	bin2 				= [0.1,-0.1,1.2,1.9,1.8,0]
	bin3 				= [0.5,-0.2,1.5,1.9,0.9,0]
	bin4 				= [-0.37,-0.5,1.25,2.4,1.5,0]
	bin5 				= [0.07,-0.5,1.25,2.4,1.5,0]
	bin6 				= [0.47,-0.4,0.95,2.3,1.1,0]
	bin7 				= [-0.25,-0.8,1.25,2.4,1.5,0]
	bin8 				= [0.15,-0.8,1.10,2.9,1.3,1.2]
	bin9 				= [0.85,-0.8,1.10,2.9,1.3,1.2]
	bin10 				= [-0.25,-1.0,1.60,3.1,2.0,1.2]
	bin11 				= [0.25,-1.3,1.60,2.9,1.3,1.2]
	bin12 				= [0.75,-1.3,1.60,2.9,1.3,1.2]

	robot_path 			= [joint_start] + [bin1] + [bin2] + [bin3] + [bin4] + [bin5] + [bin6] + [bin7] + [bin8] + [bin9] + [bin10] + [bin11] + [bin12]  

	planner 			= OR_motion_planning('apc_env.xml')

	collision_struct 	= {"checker":'pqp', 
							"collision_options":[op.CollisionOptions.Contacts]}

	IPython.embed()
	driver 		= Ur5_motion_planner()
	driver.move_arm(joint_start)
 	raw_input("Press enter to continue: ")

	for itr in range(12):
		#  Move from bin to tote
	 	planner.init_planning_setup(robot_path[0], collision_struct)
	 	final_trajectory 	=	planner.optimize_trajopt(joint_target=robot_path[itr +1])
	 	planner.simulate(trajectory=final_trajectory)
		driver.move_arm(joint_space=final_trajectory, v_profile="ramp")

	 	raw_input("Press enter to continue: ")

	 	# Move from tote to bin
	 	planner.init_planning_setup(robot_path[itr +1], collision_struct)
	 	final_trajectory 	=	planner.optimize_trajopt(joint_target=robot_path[0])
	 	planner.simulate(trajectory=final_trajectory)
	 	driver.move_arm(joint_space=final_trajectory, v_profile="ramp")

	 	raw_input("Press enter to continue: ")

	# import random
	# prev_itr 				= 0
	# itr 					= prev_itr

	# while(raw_input("Press enter to continue or q to quit: ") != 'q'):
	# 	while(prev_itr == itr):
	# 		itr 				= random.randint(0, len(robot_path) -1)

	# 	planner.init_planning_setup(robot_path[0], collision_struct)

	# 	final_trajectory 	=	planner.optimize_trajopt(joint_target=robot_path[itr])
	# 	planner.simulate(trajectory=final_trajectory)
		
	# 	prev_itr 			= itr
