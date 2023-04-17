import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.linear_model import LinearRegression

def get_train_data(data_size=100, differ=0):
  data_label = np.zeros((2 * data_size, 1))
  # class 1 
  var = [0.6, 0.8] if differ == 1 else [0.3, 0.5]
  x1 = np.reshape(np.random.normal(1, var[0], data_size), (data_size, 1))
  y1 = np.reshape(np.random.normal(1, var[1], data_size), (data_size, 1))
  data_train = np.concatenate((x1,y1), axis=1)
  data_label[0:data_size, : ] = -1
  # class 2
  x2 = np.reshape(np.random.normal(-1, 0.3, data_size), (data_size, 1))
  y2 = np.reshape(np.random.normal(-1, 0.5, data_size), (data_size, 1))
  data_train = np.concatenate((data_train, np.concatenate((x2, y2), axis=1)), axis=0)
  data_label[data_size: 2 * data_size, :] = 1
  return data_train, data_label

def get_test_data(data_size=10, differ=0):
  testdata_label = np.zeros((2 * data_size, 1))
  # class 1
  var = [0.6, 0.8] if differ == 1 else [0.3, 0.5]
  x1 = np.reshape(np.random.normal(1, var[0], data_size), (data_size, 1))
  y1 = np.reshape(np.random.normal(1, var[1], data_size), (data_size, 1))
  data_test = np.concatenate((x1, y1), axis=1)
  testdata_label[0:data_size, :] = -1
  #class 2
  x2 = np.reshape(np.random.normal(-1, 0.3, data_size), (data_size, 1))
  y2 = np.reshape(np.random.normal(-1, 0.5, data_size), (data_size, 1))
  data_test = np.concatenate((data_test, np.concatenate((x2, y2), axis=1)), axis=0)
  testdata_label[data_size: 2 * data_size, :] = 1
  return data_test, testdata_label

# function for LinerRegression
# parameter: training data
# returns: Regression coefficient
def LR(data_train, data_label):
  model = LinearRegression()
  model.fit(data_train, data_label)
  b  = model.intercept_#截距
  w = model.coef_#回归系数
  return w, b

# function for LDA
# parameter: X1, X2, datasets of two different class
# returns: Coefficient of linear discriminant
def LDA(X1, X2):
  mju1 = np.mean(X1, axis=0)#求中心点
  mju2 = np.mean(X2, axis=0)
  cov1 = np.dot((X1 - mju1).T, (X1 - mju1))
  cov2 = np.dot((X2 - mju2).T, (X2 - mju2))
  Sw = cov1 + cov2
  w = np.dot(np.mat(Sw).I, (mju1 - mju2).reshape((len(mju1), 1)))  # 计算w
  return w

for differ in [1,0] :
  data_train, data_label = get_train_data(100, differ)
  data_test, testdata_label = get_test_data(10, differ)

  # plt.figure(figsize=(4.5,5.5), dpi=100)
  plt.scatter(data_train[0:100,0], data_train[0:100,1], c='green', s=20, label='class 1')
  plt.scatter(data_train[100:200,0], data_train[100:200,1], c='blue', s=20, label='class 2')
  plt.scatter(data_test[:,0], data_test[:,1], c='red', s=30, label='test data')

  # LinerRegresion
  w, b = LR(data_train, data_label)
  plt.axline((0,  - b[0] / w[0][1]), (- b[0] / w[0][0], 0), color="r",ls="-",lw=2.5, label='Linear Regression')

  # LDA
  X1 = data_train[0:100,:]
  X2 = data_train[100:200,:]
  w = LDA(X1, X2)
  plt.axline((0, 0), (- w[1, 0], w[0, 0]), color="g",ls="-",lw=2.5, label='LDA')

  plt.legend(loc='best')
  plt.show()

  # LDA prediction 
  color = ['r' for i in range(20)]
  for i in range(20):
    y = np.dot(w.T, data_test[i])
    color[i] = 'g' if y[0][0] > 0 else 'b'
  plt.scatter(data_test[:,0], data_test[:,1], c=color, s=30, label='')
  plt.legend(loc='best', title='LDA prediction, blue for class 1, green for class 2')
  plt.show()