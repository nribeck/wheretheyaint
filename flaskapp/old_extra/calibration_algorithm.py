import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from expected_bases_lookup import expected_bases_lookup

def calibration_algorithm(player):

	user = 'ribeck'
	host = 'localhost'
	dbname = 'statcast'
	db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
	con = None
	con = psycopg2.connect(database = dbname, user = user)

	#slugging lookup table and characteristics
	slugging_table = np.load("slg_lookup_table.npy")
	v_range = [10., 130.]
	a_range = [-100., 100.]
	num_edges = 50
	
	#just select the player from the statcast database that the user inputs
	query = "SELECT player_name, hit_speed, hit_angle, events FROM statcast_data_table WHERE hit_speed != 0 AND player_name = '%s' ORDER BY hit_speed DESC" % player
	print query
	query_results = pd.read_sql_query(query, con)
	print query_results
	
	actual_total_bases = 0
	expected_total_bases = 0
	total_bip = query_results.shape[0]
	balls = []
	for i in xrange(0, total_bip):
		lookup_indexes = expected_bases_lookup(v_query = query_results.iloc[i]['hit_speed'], a_query = query_results.iloc[i]['hit_angle'], v_range = v_range, a_range = a_range, num_edges = num_edges)
		expected_bases = slugging_table[lookup_indexes]
		expected_total_bases += expected_bases
		event = query_results.iloc[i]['events']
		
		if event == 'Single':
			actual_bases = 1
		elif event == 'Double':
			actual_bases = 2
		elif event == 'Triple':
			actual_bases = 3
		elif event == 'Home Run':
			actual_bases = 4
		else:
			actual_bases = 0
		actual_total_bases += actual_bases

		balls.append(dict(player_name = query_results.iloc[i]['player_name'], hit_speed = format(query_results.iloc[i]['hit_speed'], '.2f'), events = query_results.iloc[i]['events'], expected_bases = str(format(expected_bases, '.2f'))))
	
	slg = float(actual_total_bases)/float(total_bip)
	exp_slg = float(expected_total_bases)/float(total_bip)

	return balls, slg, exp_slg, total_bip