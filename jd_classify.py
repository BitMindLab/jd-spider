#!coding:utf-8
'''
Created on Dec 9, 2014

@author: xx
'''

import os
import numpy as np
import scipy.sparse as sparse
from sklearn import linear_model
from sklearn import svm
import sklearn.cross_validation as cross_validation
from sklearn.metrics import accuracy_score

import jd_config


def load(fname, fileFormat='libSVM'):
    print 'loading data in ' + fname
    f_BOW = open(fname)
    lines = f_BOW.readlines()
    
    # load matrix
    y=[]
    row = []
    col = []
    data = []
    for i in range(len(lines)):
        line = lines[i].split(' ')
        y.append(float(line[0]))
        row.extend([i for Str in line[1:]])
        col.extend([int(Str.split(':')[0]) for Str in line[1:]])
        data.extend([float(Str.split(':')[1]) for Str in line[1:]])
    
    # sparse matrix to dense matrix
    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    X = np.array(sparse.coo_matrix((data,(row,col)), shape=(max(row)+1,max(col)+1)).todense())
    y = np.array(y)
    return X, y



fname = os.path.join(jd_config.dataPath, 'product.BOW')    
X,y = load(fname)

# 逻辑斯帝回归
    
X_train, X_test, y_train, y_test = cross_validation.train_test_split(
            X, y, test_size=0.2, random_state=0)
logreg = linear_model.LogisticRegression(C=1e5)
logreg.fit(X_train, y_train)

# test and evaluation
y_pred = logreg.predict(X_test)
print 'logistic regression for classification:' 
print 'accuracy:' + str(accuracy_score(y_test, y_pred))    

# SVM
clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
print 'SVM for classification:' 
print 'accuracy:' + str(accuracy_score(y_test, y_pred))    

    
    



