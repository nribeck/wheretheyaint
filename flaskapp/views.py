from flask import render_template
from flaskapp import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import numpy as np
import psycopg2
from itertools import izip
from flask import request
from regression_algorithm import regression_algorithm

user = 'ribeck'
host = 'localhost'
dbname = 'statcast'
pswd = 'pass'
#db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
#con = psycopg2.connect(database = dbname, user = user)
con = psycopg2.connect(database = dbname, user = user, host = host, password = pswd)

def get_player_list():
	player_list_query = "SELECT player_name FROM statcast_data_table WHERE hit_speed != 0 GROUP BY player_name HAVING count(*)>100 ORDER BY player_name"
	player_list_df = pd.read_sql_query(player_list_query, con)
	player_list = player_list_df['player_name'].values
	last_names = [str.rsplit(None, 3)[-1] for str in player_list]
	last_names_lower = [i.lower() for i in last_names]
	for i in xrange(len(last_names)):
		if last_names[i] == 'Jr.' or last_names[i] =='III':
			last_names[i] = player_list[i].rsplit(None, 3)[-2]
			last_names_lower[i] = last_names[i].lower()

	player_list_sorted = [y for (x,y) in sorted(izip(last_names_lower, player_list))]
	last_names_sorted = [y for (x,y) in sorted(izip(last_names_lower, last_names))]
	first_names_sorted = [x.replace(' '+y, '') for (x,y) in izip(player_list_sorted, last_names_sorted)]
	formatted_name = [x + ', ' + y for (x,y) in izip(last_names_sorted, first_names_sorted)]
	name_info = []
	for i in xrange(len(player_list)):
		name_info.append(dict(full_name = player_list_sorted[i], formatted_name = formatted_name[i]))

	return name_info


@app.route('/index')
@app.route('/')
def statcast_input():
	
	name_info = get_player_list()

	return render_template("index.html", name_info = name_info)

@app.route('/output')
def statcast_output():

	name_info = get_player_list()

	selection = request.args.get('player_dropdown')
	if selection == 'none':
		player = request.args.get('player_name')
	else:
		player = selection
	if player == '':
		return render_template('error.html')


	#previous_days = request.args.get('previous_days')

	all_check = request.args.get('whole')
	if all_check == '1':
		previous_days = 1000
	else:
		previous_days = request.args.get('previous_days')
	if previous_days == '':
		return render_template('error.html')

	#will have to alter any other algorithm to take dates
	balls, date_list, slg, exp_slg, total_bip = regression_algorithm(player, previous_days)

	hit_chart_data1 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==0]
	hit_chart_data2 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==1]
	hit_chart_data3 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==2]
	hit_chart_data4 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==3]
	hit_chart_data5 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==4]
	hit_chart_data6 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==5]
	hit_chart_data7 = [[balls[i]['hit_speed'], balls[i]['hit_angle']] for i in xrange(len(balls)) if balls[i]['hit_type']==6]
	
	exp_bases = np.cumsum([balls[i]['exp_bases'] for i in xrange(len(balls))])
	actual_bases = np.cumsum([balls[i]['bases_acquired'] for i in xrange(len(balls))])
	luck_bases = actual_bases - exp_bases

	#something like this (?) for later when I can pass dates through to the luck-chart
	#exp_bases_data = [[date_list[i], exp_bases[i]] for i in xrange(len(balls))]
	#actual_bases_data = [[date_list[i], actual_bases[i]] for i in xrange(len(balls))]
	#luck_bases_data = [[date_list[i], luck_bases[i]] for i in xrange(len(balls))]

	sigma_luck = 0.056057531110422901

	luck = slg - exp_slg
	if luck > 0:
		if luck < sigma_luck*0.75:
			luck_desc = 'about as expected'
		elif luck < sigma_luck*1.75:
			luck_desc = 'lucky'
		else:
			luck_desc = 'very lucky'
	else:
		if luck > -sigma_luck*0.75:
			luck_desc = 'about as expected'
		elif luck > -sigma_luck*1.75:
			luck_desc = 'unlucky'
		else :
			luck_desc = 'very unlucky'	

	return render_template("output.html", date = date_list, exp_bases = exp_bases.tolist(), actual_bases = actual_bases.tolist(), luck_bases = luck_bases.tolist(), player = player, slg = slg, exp_slg = exp_slg, luck = luck, luck_desc = luck_desc, name_info = name_info, balls = balls, hit_chart_data1 = hit_chart_data1, hit_chart_data2 = hit_chart_data2, hit_chart_data3 = hit_chart_data3, hit_chart_data4 = hit_chart_data4, hit_chart_data5 = hit_chart_data5, hit_chart_data6 = hit_chart_data6, hit_chart_data7 = hit_chart_data7)


@app.route('/slides')
def slides():
	return render_template("slides.html")

@app.route('/contact')
def contact():
		return render_template("contact.html")

@app.errorhandler(400)
def page_not_found(e):
    return render_template('error.html'), 400

@app.errorhandler(403)
def page_not_found(e):
    return render_template('error.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html'), 500



