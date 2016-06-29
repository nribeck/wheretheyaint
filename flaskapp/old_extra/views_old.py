from flask import render_template
from flaskapp import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import numpy as np
import psycopg2
import pandas_highcharts.core
from flask import request
from regression_algorithm import regression_algorithm
from calibration_algorithm import calibration_algorithm

user = 'ribeck'
host = 'localhost'
dbname = 'statcast'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)

@app.route('/input')
def statcast_input():
	return render_template("input.html")

@app.route('/test')
def test():
	return render_template("test.html")

@app.route('/output')
def statcast_output():
	#pull 'player_name' from input field and store it
	player = request.args.get('player_name')
	previous_days = request.args.get('previous_days')

	#statcast_query = "SELECT player_name, hit_speed, hit_angle, events, (CASE WHEN events='Single' THEN 1 WHEN events='Double' THEN 2 WHEN events='Triple' THEN 3 WHEN events='Home Run' THEN 4 ELSE 0 END) AS bases_acquired FROM statcast_data_table WHERE hit_speed != 0 AND player_name = '%s' ORDER BY hit_speed DESC;" % player
	#statcast_query = "SELECT hit_speed, hit_angle, events, game_date FROM statcast_data_table WHERE hit_speed != 0 AND player_name = '%s';" % player
	#statcast_results = pd.read_sql_query(statcast_query, con)

	#hit_speeds = statcast_results['hit_speed'].values.tolist()
	#hit_angles = statcast_results['hit_angle'].values.tolist()

	#hit_chart_data = np.transpose(np.array([hit_speeds, hit_angles])).tolist()


	#will have to alter any other algorithm to take dates
	balls, date_list, slg, exp_slg, total_bip = regression_algorithm(player, previous_days)

	hit_chart_data0 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==0]
	hit_chart_data1 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==1]
	hit_chart_data2 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==2]
	hit_chart_data3 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==3]
	hit_chart_data4 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==4]
	
	exp_bases = np.cumsum([balls[i]['exp_bases'] for i in xrange(len(balls))])
	actual_bases = np.cumsum([balls[i]['bases_acquired'] for i in xrange(len(balls))])
	luck_bases = actual_bases - exp_bases


	#exp_bases_data = [[date_list[i], exp_bases[i]] for i in xrange(len(balls))]
	#actual_bases_data = [[date_list[i], actual_bases[i]] for i in xrange(len(balls))]
	#luck_bases_data = [[date_list[i], luck_bases[i]] for i in xrange(len(balls))]



	sigma_luck = 0.051311643184888726


	luck = slg - exp_slg
	if luck > 0:
		if luck < sigma_luck*0.5:
			luck_desc = 'about as expected'
		elif luck < sigma_luck*1.25:
			luck_desc = 'lucky'
		else:
			luck_desc = 'very lucky'
	else:
		if luck > -sigma_luck*0.5:
			luck_desc = 'about as expected'
		elif luck > -sigma_luck*1.25:
			luck_desc = 'unlucky'
		else :
			luck_desc = 'very unlucky'	

	return render_template("output.html", date = date_list, exp_bases = exp_bases.tolist(), actual_bases = actual_bases.tolist(), luck_bases = luck_bases.tolist(), player = player, slg = slg, exp_slg = exp_slg, luck = luck, luck_desc = luck_desc, balls = balls, hit_chart_data0 = hit_chart_data0, hit_chart_data1 = hit_chart_data1, hit_chart_data2 = hit_chart_data2, hit_chart_data3 = hit_chart_data3, hit_chart_data4 = hit_chart_data4)




