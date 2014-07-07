import os
import numpy as np
import pandas as pd
import datetime as dt




def initiate() :

	ssm = {}
	theta = {}
	prior = []


def write_data(dates, cases) :
	"""
	Takes in a list or array of datetime objects
	and a list or array of ints or floats,
	and generates a data object for json dumping.
	"""

	# Check formats
	if type(dates) != list and type(dates) != np.ndarray :
		print "List or array expected for dates."
		return

	if type(dates[0]) != dt.datetime and type(dates[0]) != float :
		print "Elements of dates need to be floats or Python datetime objects."
		return

	if type(cases) != list and type(dates) != np.ndarray :
		print "List or array expected for cases."
		return


	# Convert float dates into pandas datetime objects
	if type(dates[0]) == float :
		years = np.floor(dates).astype(int)
		days = (dates - years) * 365
		D = [(dt.date(y, 1, 1) + dt.timedelta(days = d)).isoformat() for y, d in zip(years, days)]


	if not os.path.exists("data") :
		os.mkdir("data")

	pd.DataFrame({"dates" : dates, "cases" : cases}).to_csv("data/data.csv", index=False)

	print "Wrote data.csv."







def write_prior(name, distribution, params) :
	# name is the parameter's name
	# params is a list of parameters for that distribution

	pd.DataFrame({"name" : distribution, "params" : params}).to_json("data/%s.json" % name)






def wizard() :

	print "We need a list or array of dates at which we have observed something."
	print ""