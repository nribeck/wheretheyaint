#!/Users/ribeck/miniconda2/envs/insight_project/bin/python
from flaskapp import app

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug = True)