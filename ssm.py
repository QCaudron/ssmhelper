import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import os
import json
from sklearn.neighbors import NearestNeighbors

colours = seaborn.color_palette("deep", 8)
flags = ""




# TODO : Use varargout to control whether anything is returned




# Compile the model
def compile() :
	os.system("ssm")
	# TODO : add error checks; check through JSON files for syntax errors if compile fails
	# If none found, suggest the user cry a little







# Simulate from current state
def sim(jsonfile = "mle", out = 0) :

	os.chdir("bin")

	if os.path.isfile("../%s.json" % jsonfile) :
		print "Simulating from %s.json." % jsonfile
		os.system("cat ../%s.json | ./simul -N 8 -P .. --traj -I %d > /dev/null" % (jsonfile, out))
	else :
		print "%s.json does not exist, simulating using theta.json."
		os.system("cat ../theta.json | ./simul -N 8 -P .. --traj -I %d > /dev/null" % (out))

	os.chdir("..")
	
	# TODO : look into stochastic simulations ( -J particles )
	# Create flags for turning off demographic stochasticity, white noises and diffusions









# Simplex
def simplex(steps = 10000, jsonfile = "mle") :
	os.chdir("bin")

	if os.path.isfile("../%s.json" % jsonfile) :
		print "Simplex on %s.json, %d iterations." % (jsonfile, steps)
		os.system("cat ../%s.json | ./simplex -M %d > ../out.json" % (jsonfile, steps))

	else :
		print "%s.json does not exist; running Simplex on theta.json, %d iterations.\n" % (jsonfile, steps)
		os.system("cat ../theta.json | ./simplex -M %d > ../out.json" % (steps))
	
	os.rename("../out.json", "../mle.json")
	os.chdir("..")

	# TODO : Create flags for turning off demographic stochasticity, white noises and diffusions











# Plot original data
def plotdata(show = True) :
	data = pd.read_csv("data/data.csv", parse_dates = True, index_col = "date")
	data.plot(legend = False)
	plt.xlabel("Time")
	plt.ylabel("Observed Cases")
	plt.title("Observed Data")
	if show :
		plt.show()
	# TODO : return original data as a dataframe








# Plot data and simulated trace
def plotsim(jsonfile = "mle", trajfile = "X_0") :
	sim(jsonfile)
	traj = pd.read_csv("%s.csv" % trajfile, parse_dates = True, index_col = "date")
	plotdata(False)
	traj.plot(y = "I", c = colours[2])
	plt.legend(["Observed data", "Simulated trace"])
	plt.xlabel("Time")
	plt.show()
	# TODO : think about defaulting to jsonfile = pmcmc, or drop pmcmc.json altogether







# Plot parameter evolutions
def plottrace(tracefile = "trace_0") :
	t = trace(tracefile)
	
	if t is not None :
		t.plot(subplots = True)
		plt.show()
		





# Return parameter evolutions as dataframe
def trace(tracefile = "trace_0") :
	if not os.path.isfile("%s.csv" % tracefile) :
		print "%s.csv not found, please specify another trace file." % tracefile
	else :
		t = pd.read_csv("%s.csv" % tracefile, index_col = "index")
		return t









# Summarise parameters and model fits
def summary(jsonfile = "mle") :

	if os.path.isfile("%s.json" % jsonfile) :
		print "Summary of %s.json :\n" % jsonfile
		s = json.load(open("%s.json" % jsonfile))
	else :
		print "%s.json does not exist; summarising theta.json.\n" % jsonfile
		s = json.load(open("theta.json"))

	for key, value in s["resources"][0]["data"].items() :
		print("%s" % key + "\t" + "%s" % value).expandtabs(20)

	if len(s["resources"]) > 2 :
		print("\nLog likelihood" + "\t" + "%s" % s["resources"][2]["data"]["log_likelihood"]).expandtabs(20)
		print("DIC" + "\t" + "%s" % s["resources"][2]["data"]["DIC"]).expandtabs(20)
		print("AIC" + "\t" + "%s" % s["resources"][2]["data"]["AIC"]).expandtabs(20)







# Particle MCMC
def pmcmc(steps = 100000, burn = 10000, particles = 1000, jsonfile = "mle", out = 0) :
	os.chdir("bin")

	if os.path.isfile("../%s.json" % jsonfile) :
		print "Particle MCMC from %s.json, %d particles, %d iterations ( %d single-particle burn-in )." % (jsonfile, particles, steps, burn)
		os.system("cat ../%s.json | ./pmcmc -N 8 -M %d | ./pmcmc -J %d -M %d --trace -N 8 -P .. -I %d > ../out.json" % (jsonfile, burn, particles, steps, out))
	else :
		print "%s.json does not exist, performing Particle MCMC using theta.json, %d particles, %d iterations ( %d single-particle burn-in )." % (jsonfile, particles, steps, burn)
		os.system("cat ../theta.json | ./pmcmc -J %d -N 8 -M %d | ./pmcmc -J %d -M %d --trace -N 8 -P .. -I %d > ../out.json" % (burn, particles, steps, out))

	os.rename("../out.json", "../pmcmc.json")
	os.chdir("..")
	# TODO : Create flags for turning off demographic stochasticity, white noises and diffusions








# Kalman Simplex
def ksimplex(steps = 10000, out = 0, jsonfile = "mle") :
	os.chdir("bin")

	if os.path.isfile("../%s.json" % jsonfile) :
		print "Kalman Simplex from %s.json." % jsonfile
		os.system("cat ../%s.json | ./ksimplex -M %d -P .. -I %d > ../out.json" % (jsonfile, steps, out))
	else :
		print "%s.json does not exist, simulating using theta.json." % jsonfile
		os.system("cat ../theta.json | ./ksimplex -M %d -P .. -I %d > ../out.json" % (steps, out))

	os.rename("../out.json", "../mle.json")
	os.chdir("..")
	# TODO : Create flags for turning off demographic stochasticity, white noises and diffusions







# Kalman MCMC
def kmcmc(steps = 100000, jsonfile = "mle", out = 0, burn = 10000) :
	os.chdir("bin")

	if os.path.isfile("../%s.json" % jsonfile) :
		print "Kalman MCMC from %s.json, %d iterations ( %d burn-in )." % (jsonfile, steps, burn)
		os.system("cat ../%s.json | ./kmcmc -M %d | ./kmcmc -M %d -P .. --trace -I %d%s > ../out.json" % (jsonfile, burn, steps, out, flags))
	else :
		print "%s.json does not exist, performing Kalman MCMC using theta.json, %d iterations ( %d burn-in )." % (jsonfile, steps, burn)
		os.system("cat ../theta.json | ./kmcmc -M %d | ./kmcmc -M %d -P .. --trace -I %d%s > ../out.json" % (jsonfile, burn, steps, out, flags))

	os.rename("../out.json",  "../mle.json")
	os.chdir("..")
	# TODO : Create flags for turning off demographic stochasticity, white noises and diffusions







# Shortcut : black box generic inference. Expensive.
def blackbox(short = False) :
	if not short :
		compile()
		simplex(jsonfile = "theta")
		ksimplex()
		kmcmc()
		pmcmc(steps = 500000)
		plotsim("pmcmc")

	else :
		compile()
		simplex(jsonfile = "theta", steps = 100)
		ksimplex(steps = 50)
		kmcmc(steps = 100, burn = 10)
		pmcmc(steps = 100, burn = 10, particles = 2)
		plotsim("pmcmc")









# Generate a set of uncorrelated, space-filling initial conditions 
# using Mitchell's Best Candidate algorithm to approximate a Poisson disc sampling
def icsetup(IC = 5000, candidates = 500) :

	# Evaluate the number of dimensions
	dimensions = len(pd.read_json("theta.json").resources[0]["data"])

	print "Creating %d initial parameter value sets over %d parameters, using %d candidates per point." % (IC, dimensions, candidates)

	# Seed the parameter space with a single uniform sample
	initialconditions = np.random.rand(1, dimensions)

	# We get each accepted LH point by :
	for i in range(1, IC) :
		
		# Generating some candidate points
		c = np.random.rand(candidates, dimensions)

		# Selecting the candidate with the greatest distance to its nearest neighbour
		idx = np.argmax(NearestNeighbors(n_neighbors = 1).fit(initialconditions).kneighbors(c)[0])

		# And keeping that one
		initialconditions = np.append(initialconditions, np.reshape(c[idx, :], (1, dimensions)), axis = 0)

	
	# Next, 




	# TODO : Create IC initial conditions, sampled from parameter space
	# Make a backup of the user's IC files
	# For each IC, write a new file, run a simplex, ...
	# HERE : determine if we stop at simplex or follow with a ksimplex
	# Decide if we reject some before ksimplex
	# What do we do with the top solutions ?
	# How are they determined ?



