from numpy import *
import numpy as np

# convert class string to 0 1 2 for function np.loadtxt
def conv(kind):
  if kind == b"Iris-setosa": return 0
  if kind == b"Iris-versicolor": return 1
  if kind == b"Iris-virginica": return 2
def sigmoid(X):
	return 1 / (1 + e**X)

def dsigmoid(X):
	return multiply(sigmoid(X), 1 - sigmoid(X))

#extract data. X as the input matrix, y_matrix as the target matrix
data = np.loadtxt("Iris.data", delimiter = ",", converters={4:conv})
X = mat(data[:,0:4])
y = data[:,4].astype(int)
e3 = eye(3)
y_matrix = e3[y]

ni = 4 # input layer size
nh = 15 # hidden layer size
no = 3 # output layer size

# init weight matrix wi and wo
epsilon_init = 0.01# sqrt(6/(ni+nh))
wi = (1 - np.random.rand(nh, ni + 1) * 2) * epsilon_init
#print(wi)
epsilon_init = 0.01# sqrt(6/(nh+no))
wo = (1 - np.random.rand(no, nh + 1) * 2) * epsilon_init

m = X.shape[0]
n = X.shape[1]
# feature normalization
for i in range(0, n):
	X[:,i] = (X[:,i] - np.mean(X[:,i])) / np.std(X[:,i])
X = np.c_[np.ones(m), X]

iter_nums = 10000
correct_rate = np.zeros(iter_nums)
lr = 0.01
for i in range(0,iter_nums):
	# Forward Algorithm
	# compute hidden layer
	z2 = X*mat(wi).T
	g2 = sigmoid(array(z2))
	g2 = np.c_[ones(m), g2] # add bias term

	# compute output layer
	z3 = mat(g2)*mat(wo).T
	g3 = sigmoid(array(z3))
	# compute cost function
	do = - g3 + y_matrix # delta of output layer
	cost_matrix = multiply(do, do)
	cost = np.sum(cost_matrix)
	
	# Back Propogation Algorithm
	weight_propogate = array(mat(do)*mat(wo[:,1:]))
	dh = multiply(weight_propogate, dsigmoid(array(z2))) # delta of hidden layer
	
	Delta2 = mat(do).T * mat(g2) / m
	Delta1 = mat(dh).T * X / m
	
	# update gradient
	wi = wi - lr * array(Delta1)
	wo = wo - lr * array(Delta2)
	# compute training set accuracy
	correct_rate[i] = sum(np.argmax(g3, axis=1) == y)/150
	# print(correct_rate[i])

	# change learning rate so the gradient would not be too 
	# large to cause correct rate up and down
	if correct_rate[i] > 0.6: lr = 0.001
	if correct_rate[i] > 0.7: lr = 0.0005
	if correct_rate[i] > 0.8: lr = 0.0002

# print(np.argmax(g3, axis=1) == y)
# print(sum(np.argmax(g3, axis=1) == y)/150)
# print max training set accuracy
print(max(correct_rate))
