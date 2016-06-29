	
import numpy as np

def is_hardhit(hit_speed, hit_angle, best_v, best_a):
	min_speed_hardhit = 100.
	min_angle_hardhit = 15.
	speed_distance = (hit_speed - best_v) / (best_v - min_speed_hardhit)
	if speed_distance > 0:
		speed_distance = 0
	angle_distance = (hit_angle - best_a) / (best_a - min_angle_hardhit)
	pythag_distance = np.sqrt(angle_distance**2 + speed_distance**2)
	return pythag_distance <= 1.

def is_medhit(hit_speed, hit_angle, best_v, best_a):
#to be applied only after is_hardhit
	min_speed_medhit = 90.
	min_angle_medhit = 5.
	speed_distance = (hit_speed - best_v) / (best_v - min_speed_medhit)
	if speed_distance > 0:
		speed_distance = 0
	angle_distance = (hit_angle - best_a) / (best_a - min_angle_medhit)
	pythag_distance = np.sqrt(angle_distance**2 + speed_distance**2)
	return pythag_distance <= 1.

def is_blooper(hit_speed, hit_angle):
	#to be applied only after is_medhit
	min_angle_bloop = 0.
	max_angle_bloop = 50.
	min_speed_bloop = 55.
	return hit_angle >= min_angle_bloop and hit_angle <= max_angle_bloop and hit_speed >= min_speed_bloop

def is_dribbler(hit_speed, hit_angle):
	#to be applied only after is_blooper
	max_angle_dribbler = 0.
	max_speed_dribbler = 85.
	return  hit_angle <= max_angle_dribbler and hit_speed <= max_speed_dribbler

def classify_batted_ball(hit_speed, hit_angle, v_range, a_range, num_edges):
	slugging = np.load("slg_lookup_table.npy")
	totalbip = np.load("totalbip_lookup_table.npy")
	#find most common no-doubter bin
	best_bins = np.transpose(np.where(slugging == np.nanmax(slugging)))
	bip_in_best_bins = [totalbip[best_bins[i,0], best_bins[i,1]] for i in xrange(len(best_bins))]
	best_bin = best_bins[np.argmax(bip_in_best_bins)]

	#find center of most common no-doubter bin
	best_v = best_bin[0] * (v_range[1] - v_range[0])/(num_edges - 1.5) + v_range[0]
	best_a = best_bin[1] * (a_range[1] - a_range[0])/(num_edges - 1.5) + a_range[0]

	if is_hardhit(hit_speed, hit_angle, best_v, best_a):
		ball_type = 0
	elif is_medhit(hit_speed, hit_angle, best_v, best_a):
		ball_type = 1
	elif is_blooper(hit_speed, hit_angle):
		ball_type = 2
	elif is_dribbler(hit_speed, hit_angle):
		ball_type = 3
	else:
		ball_type = 4

	return ball_type