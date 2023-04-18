from rl import total_episodes
from rl import learn
import numpy as np

import matplotlib.pyplot as plt

N = 30
batch = 50
Qlearning = 1

def gen_data(learning_rate = 0.8, gamma = 0.95, method = Qlearning, param = "gamma"):

	#generate data for qlearning
	learn_data = np.zeros((N, total_episodes, 3))
	if method == Qlearning:
		met = "Qlearning"
	else:
		met = "Sarsa"
	for i in range(N):
		learn_data[i] = learn(learning_rate, gamma, method)
		if param == "gamma":
			np.savetxt("./data/%s/gamma/%d_%f.csv" % (met, i, gamma), learn_data[i], delimiter=",")
		else:
			np.savetxt("./data/%s/learning_rate/%d_%f.csv" %(met, i, learning_rate) , learn_data[i], delimiter=",")

def load_from_txt(learning_rate = 0.8, gamma = 0.95, method = Qlearning, param = "gamma"):

	#generate data for qlearning
	learn_data = np.zeros((N, total_episodes, 3))
	if method == Qlearning:
		met = "Qlearning"
	else:
		met = "Sarsa"
	for i in range(N):
		# learn_data[i] = learn(learning_rate, gamma, method)
		if param == "gamma":
			learn_data[i] = np.loadtxt("./data/%s/gamma/%d_%f.csv" % (met, i, gamma), delimiter=",")
		else:
			learn_data[i] = np.loadtxt("./data/%s/learning_rate/%d_%f.csv" %(met, i, learning_rate), delimiter=",")

	return learn_data

def ana_data(learn_data):
	
	succeed = np.zeros((int(total_episodes/batch), 3))

	for j in range(total_episodes):
		epoch = int(j/batch)

		for i in range(N):
			if learn_data[i, j, 1] == 1:
				succeed[epoch, 0] += learn_data[i, j, 0]
				succeed[epoch, 1] += 1
				if (j+1) % batch == 0: succeed[epoch, 2] += learn_data[i, j, 2]

		if (j+1) % batch == 0:
			succeed[epoch, 0] = succeed[epoch, 0] / succeed[epoch, 1]
			succeed[epoch, 2] = succeed[epoch, 2] / succeed[epoch, 1]
			succeed[epoch, 1] = succeed[epoch, 1] / (batch * N)
		# np.savetxt("succeed.csv", succeed, delimiter=",")
	return succeed

def plotData(data, label, color, info):
	(m,s,n) = data.shape
	plt.figure()
	for i in range(2):
		plt.subplot(2,1,i+1)
		plt.xlabel(info[i]['xlabel'])
		plt.ylabel(info[i]['ylabel'])
		plt.title(info[i]['title'])
		n = int(total_episodes / batch)
		for j in range(m):
			plt.scatter(np.arange(0,n,1), data[j, :, i], c=color[j], label=label[j])
		plt.legend()
	plt.show()

gammaList = [0.7, 0.8, 0.9, 0.95, 0.99]
lrList = [0.7, 0.75, 0.8, 0.85, 0.9]

for method in range(2):
	for gamma in gammaList:
		gen_data(gamma = gamma, method = method, param = "gamma")
	for lr in lrList:
		gen_data(learning_rate=lr, method=method, param = "lr")

data = np.zeros((5, 60, 3))
info = [{'xlabel': 'episode', 'ylabel':'avarage steps', 'title':"average steps to finish the game in every 100 episodes"},\
		{'xlabel': 'episode', 'ylabel':'success rate', 'title':"average successrate in every 100 episodes"}]

for method in range(2):
	label = []
	color = ['r', 'g', 'b', 'c', 'm']
	for i in range(5):
		learn_data = load_from_txt(gamma = gammaList[i], method = method, param = "gamma")
		data[i] = ana_data(learn_data)
		label.append( "gamma = %.2f" % gammaList[i])

	plotData(data, label, color, info)
	label = []
	for i in range(5):
		learn_data = load_from_txt(learning_rate=lrList[i], method=method, param = "lr")
		data[i] = ana_data(learn_data)
		label.append( "learning rate = %.2f" % lrList[i])
	# info = [{},{}]
	plotData(data, label, color, info)

data = np.zeros((2, 60, 3))
label = ["Sarsa", "Qlearning"]
color = ['r', 'g']
# info = [{'xlabel': 'episode', 'ylabel': 'avarage steps' }]
for lr in (0.7, 0.8, 0.9):
	#label = []
	for i in range(2):
		learn_data = load_from_txt(learning_rate=lr, method=i, param="lr")
		data[i] = ana_data(learn_data)
	info[0]['title'] = 'learning_rate=%.2f' % lr
	info[1]['title'] = ''
	plotData(data, label, color, info)