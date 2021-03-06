import sys
import pandas as pd
import numpy as np
import pickle
import logistic_regression


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
  data_X = np.zeros((data.shape[0], data.shape[1]+1))
  data_X[:,:-1] = np.array(data.ix[:,0:data.shape[1]], dtype=float)
  data_X[:,-1] = np.zeros(data_X.shape[0])+1
  return data_X


if __name__ == '__main__':
  testData = process_data(file(sys.argv[2]))
  test_X = generate_dataset(testData)
  
  model = pickle.load(open(sys.argv[1], 'rb'))

  labels = model.predict(test_X)
  ids = [i+1  for i in range(len(labels))]

  output = pd.DataFrame({'id': ids, 'label': labels})
  output.to_csv(sys.argv[3], index = False)
  
