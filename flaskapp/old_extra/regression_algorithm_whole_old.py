import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sklearn.linear_model import LinearRegression
from expected_bases_lookup import expected_bases_lookup
from classify_batted_ball import classify_batted_ball

def query_for_player_events(name, con):
	fixed_name = name.replace("'", "''")
	sql_query = "SELECT player_name, hit_speed, hit_angle, (CASE WHEN events='Single' THEN 1 WHEN events='Double' THEN 2 WHEN events='Triple' THEN 3 WHEN events='Home Run' THEN 4 ELSE 0 END) AS bases_acquired FROM statcast_data_table WHERE hit_speed != 0 AND player_name='%s';" % fixed_name
	player_events_df = pd.read_sql_query(sql_query, con)
	return player_events_df

def create_player_events_subset(df_in, subset):
	if subset == 'all':
		df_out = df_in
	elif subset == 'odd':
		df_out = df_in.iloc[1::2]
	elif subset == 'even':
		df_out = df_in.iloc[::2]
	return df_out

def player_actual_hit_values(player_events_df, subset):
	total_bases = 0.
	df_subset = create_player_events_subset(player_events_df, subset)
	total_bip = len(df_subset)
	for i in xrange(total_bip): 
		bases_acquired = df_subset.iloc[i]['bases_acquired']
		total_bases += bases_acquired
	return total_bases, total_bip

def player_hit_type_counts(player_events_df, subset, v_range, a_range, num_edges):
	hit_type_counts = [0., 0., 0., 0., 0.]
	df_subset = create_player_events_subset(player_events_df, subset)
	for i in xrange(len(df_subset)):    
		hit_speed = df_subset.iloc[i]['hit_speed']
		hit_angle = df_subset.iloc[i]['hit_angle']
		ball_type = classify_batted_ball(hit_speed, hit_angle, v_range, a_range, num_edges)
		hit_type_counts[ball_type] += 1.
	return hit_type_counts

def regression_algorithm():

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
	
	#gets total balls in play for each player with >= min_bip BIP
	min_bip = 100

	#gets total balls in play for each player with >= min_bip BIP
	#sql_query = "SELECT player_name, COUNT(*) AS total_bip FROM statcast_data_table WHERE hit_speed != 0 GROUP BY player_name HAVING COUNT(*) > %d ORDER BY total_bip desc;" % num_bip
	#qualifying_players = pd.read_sql_query(sql_query, con)

	#join fangraphs tables and qualifying-players-query on player names
	#gets total balls in play and speed rating for each player with >= min_bip BIP
	sql_query = "SELECT s.player_name, s.total_bip, f.spd, fb.pull FROM (SELECT player_name, COUNT(*) as total_bip FROM statcast_data_table WHERE hit_speed != 0 GROUP BY player_name HAVING COUNT(*) > %d) AS s JOIN fangraphs_data_table AS f ON s.player_name=f.name JOIN fangraphs_bb_data_table AS fb ON s.player_name=fb.name GROUP BY s.player_name, s.total_bip, f.spd, fb.pull ORDER BY s.total_bip DESC;" % min_bip
	qualifying_players = pd.read_sql_query(sql_query, con)

	subset1= 'all'
	subset2= 'all'

	hardhit_rates = []
	medhit_rates = []
	blooper_rates = []
	dribbler_rates = []
	other_rates = []

	slg = []

	for i in xrange(len(qualifying_players)):
		name = qualifying_players.iloc[i]['player_name']
		player_events_df = query_for_player_events(name, con)

		#calculate hit type rates for subset1
		hit_type_counts = player_hit_type_counts(player_events_df, subset1, v_range, a_range, num_edges)
		total_bip1 = np.sum(hit_type_counts)

		hardhit_rates.append(hit_type_counts[0]/total_bip1)
		medhit_rates.append(hit_type_counts[1]/total_bip1)
		blooper_rates.append(hit_type_counts[2]/total_bip1)
		dribbler_rates.append(hit_type_counts[3]/total_bip1)
		other_rates.append(hit_type_counts[4]/total_bip1)
		
		#add up actual production in subset2
		total_bases, total_bip2 = player_actual_hit_values(player_events_df, subset2)
		slg.append(total_bases/total_bip2)

	qualifying_players['hardhit'] = hardhit_rates
	qualifying_players['medhit'] = medhit_rates
	qualifying_players['blooper'] = blooper_rates
	qualifying_players['dribbler'] = dribbler_rates
	qualifying_players['other'] = other_rates
	qualifying_players['slg'] = slg

	X = qualifying_players[['hardhit', 'medhit', 'blooper','dribbler', 'other','spd','pull']]
	y = qualifying_players['slg']
	weights = qualifying_players['total_bip']

	linreg = LinearRegression()
	linreg.fit(X, y, sample_weight = weights)
	y_int = linreg.intercept_
	coeffs = linreg.coef_
	
	return y_int, coeffs