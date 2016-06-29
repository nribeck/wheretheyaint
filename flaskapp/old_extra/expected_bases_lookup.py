import numpy as np

def expected_bases_lookup(v_query, a_query, v_range, a_range, num_edges):
    v_min, v_max = v_range
    v_binsize = (v_max - v_min)/(num_edges - 1.)
    
    a_min, a_max = a_range
    a_binsize = (a_max - a_min)/(num_edges - 1.)
    
    v_bin = int(np.floor((v_query - v_min)/v_binsize))
    a_bin = int(np.floor((a_query - a_min)/a_binsize))
    
    return v_bin, a_bin  