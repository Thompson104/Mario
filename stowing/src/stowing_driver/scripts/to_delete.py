from apc_global_params import *
from ur5_lib import MarioFullSystem
from math import pi
import IPython

# kin  			= MarioFullSystem(True)
# cartesian 		= [0,0,0] + base_displacement_to_bot_left_bin['ready_bin_A']
# cartesian[3] 	= cartesian[3] - 0.345
# sol 			= kin.cartesian_to_ik(cartesian)[0]
# IPython.embed()
# sol[0:5] 		*= -1
# sol[5] 			= -pi/2
# kin.action_server_move_arm(sol,1)

kin  			= MarioFullSystem(True)
kin.action_server_move_arm(global_params['starting_position'],1)
