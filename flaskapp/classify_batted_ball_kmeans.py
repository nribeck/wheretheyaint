	
import numpy as np

def bin_lookup_flat(v_query, a_query, v_range, a_range, num_edges):
    v_min, v_max = v_range
    v_binsize = (v_max - v_min)/(num_edges - 1.)
    
    a_min, a_max = a_range
    a_binsize = (a_max - a_min)/(num_edges - 1.)
    
    v_bin = int(np.floor((v_query - v_min)/v_binsize))
    a_bin = int(np.floor((a_query - a_min)/a_binsize))
    
    return v_bin * (num_edges - 1) + a_bin

def classify_batted_ball(hit_speed, hit_angle, v_range, a_range, num_edges):
	bin_flat = bin_lookup_flat(hit_speed, hit_angle, v_range, a_range, num_edges)

	kmeans_labels = np.load("kmeans_labels.npy")
	labels_indexes = np.load("labels_indexes.npy")
	ball_type = kmeans_labels[np.where(labels_indexes == bin_flat)][0]
	#will have to add a fix for new data, if balls don't fall in am already defined bin, then where(labels_indexes == bin_flat) will be empty

	return ball_type