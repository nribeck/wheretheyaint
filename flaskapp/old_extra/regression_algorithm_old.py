import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from classify_batted_ball import classify_batted_ball
import datetime

def regression_algorithm(player, previous_days):

	user = 'ribeck'
	host = 'localhost'
	dbname = 'statcast'
	db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
	con = None
	con = psycopg2.connect(database = dbname, user = user)

	v_range = [10., 130.]
	a_range = [-100., 100.]
	num_edges = 50

	y_int = 1.0203793921274737
	coeffs = np.array([2.10518416, 0.01759147, -0.74004531, -0.7881145, -0.59461581, 0.01258065, 0.12374782])

	
	#the actual today, for when autoloading of db works
	#today = datetime.date.today()
	
	today = datetime.datetime.strptime('2016-06-01', '%Y-%m-%d')
	query_start_day = today - datetime.timedelta(days = int(previous_days))
	query_start_day_string = query_start_day.strftime('%Y-%m-%d')

	statcast_query = "SELECT player_name, hit_speed, hit_angle, events, game_date, (CASE WHEN events='Single' THEN 1 WHEN events='Double' THEN 2 WHEN events='Triple' THEN 3 WHEN events='Home Run' THEN 4 ELSE 0 END) AS bases_acquired FROM statcast_data_table WHERE hit_speed != 0 AND game_date >= '%s' AND player_name = '%s';" % (query_start_day_string, player)
	statcast_results = pd.read_sql_query(statcast_query, con)
		
	fangraphs_query = "SELECT name, spd FROM fangraphs_data_table WHERE name = '%s';" % player
	fangraphs_results = pd.read_sql_query(fangraphs_query, con)
	spd = fangraphs_results.iloc[0]['spd']

	fangraphs_bb_query = "SELECT name, pull FROM fangraphs_bb_data_table WHERE name = '%s';" % player
	fangraphs_bb_results = pd.read_sql_query(fangraphs_bb_query, con)
	pull = fangraphs_bb_results.iloc[0]['pull']

	total_bip = statcast_results.shape[0]
	total_bases = statcast_results['bases_acquired'].sum()
	
	date_df = statcast_results['game_date']
	date_list = [datetime.datetime.strptime(date_df.iloc[i], '%Y-%m-%d') for i in xrange(total_bip)]
	
	balls = []
	hit_type_counts = [0., 0., 0., 0., 0.]
	for i in xrange(total_bip):
		hit_speed = statcast_results.iloc[i]['hit_speed']
		hit_angle = statcast_results.iloc[i]['hit_angle']
		bases_acquired = statcast_results.iloc[i]['bases_acquired']
		ball_type = classify_batted_ball(hit_speed, hit_angle, v_range, a_range, num_edges)
		exp_bases = y_int + coeffs[ball_type] + coeffs[5] * spd + coeffs[6] * pull
		hit_type_counts[ball_type] += 1
		balls.append(dict(player_name = statcast_results.iloc[i]['player_name'], hit_speed = hit_speed, hit_angle = hit_angle, bases_acquired = bases_acquired, hit_type = ball_type, exp_bases = exp_bases))

	slg = float(total_bases)/float(total_bip)
	exp_slg = y_int + np.sum((coeffs[0:5] * hit_type_counts) / float(total_bip)) + coeffs[5] * spd + coeffs[6] * pull

	return balls, date_list, slg, exp_slg, total_bip