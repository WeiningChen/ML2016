import numpy as np
import pandas as pd
import math as math
import sys
import os


def process_data(filename, skiprow=0):
  '''
  Load and process data omtp a list of pandas DataFrame
  each element in the list = one id
  '''
  df = pd.read_csv(filename, header=None, skiprows=skiprow)
  # drop id
  df.drop(0,axis=1,inplace=True)

  return df

def generate_dataset(data):
  '''
  Store training data as numpy matrix
  '''
  data_X = np.zeros(data.shape)
  data_X[:,:-1] = np.array(data.ix[:,0:data.shape[1]-1], dtype=float)
  data_X[:,-1] = np.zeros(data_X.shape[0])+1
  data_y = np.array(data.ix[:,data.shape[1]], dtype=float)
  return [data_X, data_y]

def sigmoid(z):
  '''
  truncated sigmoid to avoid overflows
  '''
  if z >= 100:
    return 1
  if z <= -100:
    return 0  
  return 1/(1+np.exp(-z))

def grad_cross_entropy(dataset, w):
  '''
  gradient function of cross entropy
  '''
  [data_X, data_y] = dataset
  g = 0
  for idx in range(len(data_y)):
    x = data_X[idx]
    y = data_y[idx]
    g += (sigmoid(w.T.dot(x))-y)*x
    #print "w*x"
    #print -y*w.T.dot(x)
    #print "sigmoid(w*x)"
    #print sigmoid(-y * w.T.dot(x)) 
  return g / len(data_y)

def cross_entropy(dataset,w):
  ce = 0
  e = 1e-100
  [data_X, data_y] = dataset
  for x,y in zip(data_X, data_y):
    ce += y*np.log(sigmoid(np.dot(x,w))+e)+(1-y)*np.log(1-sigmoid(np.dot(x,w))+e)
  return -1*ce/len(dataset)
  

def ERM_solver(dataset, loss, grad_loss, model_init = 0,  eta = 0.1, it = 60000): 
  [data_X, data_y]=dataset
  if(str(model_init) == '0') :
    w = np.zeros(len(data_X[0]))
    gd_sum = 1e-10
    print "Initial Models"
  else :
    w = model_init[0]
    gd_sum = model_init[1]
    print "Using Existing Models"
  for i in range(it):
    gd = grad_loss(dataset, w)
    gd_sum = gd_sum+np.dot(gd,gd)
    w = w - eta/np.sqrt(gd_sum)*gd 
    if i%200==0:
      print "Effective eta :"
      print eta/np.sqrt(gd_sum)
      print "current risk: "
      print loss(dataset, w)
      print 'current gradient norm: '
      print np.dot(gd,gd)
      print "# "+str(i)+" iterations"
      print "-----------------------"
  return np.array([w, gd_sum])

def predict(data, models):
  if sigmoid(np.dot(data, models)) > 0.5:
    return 1
  return 0 
  

if __name__ == '__main__':
  # Training data processing
  data = process_data('data/spam_train.csv')
  [train_X, train_y] = generate_dataset(data)
  print train_X[0:10,0:10]
  print train_y[0:10]
 
  # Train the model
  if os.path.isfile('models.npy'):
    models_init = np.load('models.npy')
  else :
    models_init = 0
  eta = 0.1
  it = 10000
  models = ERM_solver([train_X[0:3500], train_y[0:3500]], cross_entropy, grad_cross_entropy, models_init, eta, it)
  print models[0]  
  print np.dot(models[0],train_X[0])
  
  
  labels = []
  results = []
  cnt = 0

  # Validation Section
  for i in range(3600,3700):
    results.append(sigmoid(np.dot(models[0],train_X[i])))
    labels.append(predict(train_X[i],models[0]))
    if int(predict(train_X[i], models[0])) == int(train_y[i]):
      cnt += 1
  
  print "Sigmoid output: " + str(results)
  print "Accuracy: " + str(cnt) + "%"
  
  # Save the potential models
  if cnt >= 85:
    np.save('models_eta'+str(eta)+'_it'+str(it), models)
    print 'Models with good potential, save it !!'
  
  else:
    print 'Terrible result !!'
  

