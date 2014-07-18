import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import os
import json

colours = seaborn.color_palette("deep", 8)
flags = ""


def loud() :
	flags += " -v -n"



def multicore(cores = 8) :
	flags += " -N %d" % cores



# Compile
def compile() :
	os.system("ssm")



# Simulate from current state
def sim(jsonfile = "mle", out = 0) :
	os.chdir("bin")

	if os.path.isfile("../%s.json" % jsonfile) :
		print "Simulating from %s.json." % jsonfile
		os.system("cat ../%s.json | ./simul -N 8 -P .. --traj -I %d%s > /dev/null" % (jsonfile, out, flags))
	else :
		print "%s.json does not exist, simulating using theta.json."
		os.system("cat ../theta.json | ./simul -N 8 -P .. --traj%d%s > /dev/null" % (out, flags))

	os.chdir("..")



# Simplex
def simplex(runs = 10000) :
	os.chdir("bin")
	os.system("cat ../theta.json | ./simplex -M %d %s > mle.json" % (runs, flags))
	os.rename("mle.json", "../mle.json")
	os.chdir("..")



# Plot original data
def plotdata(show = True) :
	data = pd.read_csv("data/data.csv", parse_dates = True, index_col = "date")
	data.plot(legend = False)
	plt.xlabel("Time")
	plt.ylabel("Observed Cases")
	plt.title("Observed Data")
	if show :
		plt.show()



# Plot data and simulated trace
def plotsim(jsonfile = "theta") :
	sim(jsonfile)
	trace = pd.read_csv("X_0.csv", parse_dates = True, index_col = "date")
	plotdata(False)
	trace.plot(y="I", c = colours[2])
	plt.legend(["Observed data", "Simulated trace"])
	plt.show()



# Parameter evolutions
def plottrace() :
	"blah"



# Summarise parameters and model fits
def summary(jsonfile = "mle") :

	if os.path.isfile("%s.json" % jsonfile) :
		s = json.load(open("%s.json" % jsonfile))
	else :
		print "%s.json does not exist; summarising theta.json.\n" % jsonfile
		s = json.load(open("theta.json"))

	for key, value in s["resources"][0]["data"].items() :
		print("%s" % key + "\t" + "%s" % value).expandtabs(20)



# Particle MCMC
def pmcmc(steps = 100000, burn = 10000) :
	"blah"
