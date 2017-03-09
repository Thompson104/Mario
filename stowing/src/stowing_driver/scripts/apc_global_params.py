from math import pi

base_displacement_to_bot_left_bin 	= {
	"ready_bin_A" 		: [0.920, 0.640, 0.215],
	"ready_bin_B"		: [0.920, 0.260, 0.215],
	"ready_bin_C"		: [0.920, -0.125, 0.215],
	"ready_bin_D"		: [0.920, 0.640, -0.215],
	"ready_bin_E"		: [0.920, 0.260, -0.215],
	"ready_bin_F"		: [0.920, -0.125, -0.215],
	"ready_bin_G"		: [0.920, 0.640, -0.610],
	"ready_bin_H"		: [0.920, 0.260, -0.610],
	"ready_bin_I"		: [0.920, -0.125, -0.610],
}

global_params 				= {
	"starting_position"	: [0.020888630543844044, 0.7978475729571741, -2.387481927871704, 4.654271070157186, pi/2, -pi/2],
	"ready_bin_A" 		: [-0.500,  1.16817439, -1.56612827, 3.586388, 2.00005043, -pi/2],
	"ready_bin_B"		: [6.51163147e-05, 8.00717891e-02, 1.57081565e+00, 1.49114679e+00, 1.57082155e+00, -pi/2],
	"ready_bin_C"		: [-3.0,3.5, -1.86349296569824, 1.571, -pi/2, -pi/2],
	"ready_bin_D"		: [-0.76830311, -0.97443018, 1.99574396, 2.19125088, 2.2563175, -pi/2],
	"ready_bin_E"		: [0.0687414328204554, -1.1837163130389612, 2.313135242462158, 1.942, pi/2, -pi/2],
	"ready_bin_F"		: [-2.69997912, 2.42858568, 2.00564294, -1.41869187, -1.89998613, -pi/2],
	"ready_bin_G"		: [],
	"ready_bin_H"		: [-0.00, -pi/2, pi/2, -0.00, -pi/2, pi/2],
	"ready_bin_I"		: [],
	"main_tote" 		: [0,0,0, 0, 0, 0],
	"amnesty_tote" 		: [0,0,0, 0, 0, 0],
}

camera_positions 			= {
	"ready_bin_A" 		: [-0.57299638390541077, 1.5469663778888147, -1.7536349296569824, 0.21938344637026006, -1.9383693933486938, pi/2],
	"ready_bin_B"		: [0.31387550035585576, 1.6476472059832972, -1.788032054901123, 0.18084508577455694, -1.260462999343872, pi/2],
	"ready_bin_C"		: [1.0160048643695276, 1.2169478575335901, -1.3308324813842773, 0.2612422148333948, -0.617775559425354, pi/2],
	"ready_bin_D"		: [-0.5330857038497925, 0.9731491247760218, -1.8527922630310059, 0.9038141409503382, -2.0302555561065674, pi/2],
	"ready_bin_E"		: [0.2687414328204554, 0.9837163130389612, -2.213135242462158, 1.3010690847979944, -1.2809619903564453, pi/2],
	"ready_bin_F"		: [],
	"ready_bin_G"		: [],
	"ready_bin_H"		: [0.32377750078310186, -0.055146217346191406, -1.664074420928955, 1.7988851706134241, -1.1632136106491089, pi/2],
	"ready_bin_I"		: [],
	"main_tote"			: [],
	"amnesty_tote" 		: [],
}

# Delete this field. Not supposed to be used
# In roll / pitch / yaw / x / z / y
hard_coded_items 			= {
	"ready_bin_A" 		: {"coords" : [0, 0, 0, 0.20, 0.01, 0.05], "id" : 1}, 
	"ready_bin_B" 		: {"coords" : [0, 0, 0, 0.18, 0.1, 0.08], "id" : 1}, 
	"ready_bin_C" 		: {"coords" : [0, 0, 0, 0.20, 0.01, 0.05], "id" : 3}, 
	"ready_bin_D" 		: {"coords" : [0, 0, 0, 0.20, 0.01, 0.05], "id" : 4}, 
	"ready_bin_E" 		: {"coords" : [0, 0, 0, 0.18, 0.10, 0.08], "id" : 1}, 
	"ready_bin_F" 		: {"coords" : [0, 0, 0, 0.20, 0.01, 0.05], "id" : 6}, 
	"ready_bin_G" 		: {"coords" : [0, 0, 0, 0.20, 0.01, 0.05], "id" : 7}, 
	"ready_bin_H" 		: {"coords" : [0, 0, 0, 0.20, 0.01, 0.05], "id" : 8}, 
	"ready_bin_I" 		: {"coords" : [0, 0, 0, 0.20, 0.01, 0.05], "id" : 9}, 
}