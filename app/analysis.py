import pandas as pd  
import matplotlib.pyplot as plt, numpy
import statistics

def summaryize(dataset):
 return dataset.describe()

def correlation(filePath,course1,course2):
  dataset=pd.read_csv(filePath)
  x=pd.Series(dataset[course1])
  y=pd.Series(dataset[course2])
  return x.corr(y)

def histogram(filePath):
  dataset=pd.read_csv(filePath)
  degree_counts = dataset.columns.value_counts()
  dictionary={}
  for i, key in enumerate(degree_counts):  
     dictionary[degree_counts.keys()[i]]=statistics.mean(dataset[degree_counts.keys()[i]])
  print(dictionary)
  for i, key in enumerate(dictionary):  
    plt.bar(i, dictionary[key])
    plt.xticks(numpy.arange(len(dictionary)),  dictionary.keys())
  return plt


