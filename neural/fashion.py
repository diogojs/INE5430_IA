import timeit
import itertools
import enum

import numpy as np
import pandas as pd
import csv
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class FashionType(enum.Enum):
    TshirtTop = 0
    Trouser = 1
    Pullover = 2
    Dress = 3
    Coat = 4
    Sandal = 5
    Shirt = 6
    Sneaker = 7
    Bag = 8
    AnkleBoot = 9


data_path = 'data/'
print('Reading train file...')
train_df = pd.read_csv(data_path + 'fashion-mnist_train.csv',
            header=0)
train_data = train_df.values

print('Splitting train and test data...')
X_train, X_test, y_train, y_test = train_test_split(
    train_data[0::,1::],
    train_data[0::,0],
    test_size=0.2,
    random_state=0)
print(f'Training size: {len(X_train)}')
print(f'Test size: {len(X_test)}')

methods = ['adam', 'lbfgs', 'sgd']
activations = ['logistic', 'tanh', 'relu']
sizes = [(10,), (50,), (100,), (10, 10)]

for met, act, s in itertools.product(methods, activations, sizes):
    print(f'Solver: {met}')
    print(f'Function: {act}')
    print(f'Hidden Layers: {s}')

    nn = MLPClassifier(
            activation=act,
            solver=met,
            hidden_layer_sizes=s,
            max_iter=100,
            epsilon=1e-6)
    start_time = timeit.default_timer()
    print('Training Neural Network...')
    nn.fit(X_train, y_train)
    tscore = nn.score(X_train, y_train)
    print("Training set score: %f" % tscore)
    end_time = timeit.default_timer() - start_time
    print(f'Time: {end_time}')

    layers = str(s).replace(',', '').replace('(', '').replace(')', '').replace(' ', '')
    filename = 'coefs_' + met + act + layers + '.csv'
    with open(filename, 'w') as coeffile:
        for item in nn.coefs_:
            if type(item) == float:
                coeffile.write(str(item))
            else:
                for bitem in item:
                    coeffile.write(str(bitem))

    print('Testing Neural Network...')
    predict_output = nn.predict(X_test)
    tscore2 = nn.score(X_test, y_test)
    print("Test set score: %f" % tscore2)

    filename = 'output_' + met + act + layers + '.csv'
    pf = open(filename, 'w')
    csvobj = csv.writer(pf)
    ids = list(range(len(predict_output)))
    
    translated_labels = [FashionType(x).name for x in predict_output]
    csvobj.writerow([f'Solver: {met}'])
    csvobj.writerow([f'Function: {act}'])
    csvobj.writerow([f'Hidden Layers: {s}'])
    csvobj.writerow([f'Time: {end_time}'])
    csvobj.writerow([f'Train Score: {tscore}'])
    csvobj.writerow([f'Test Score: {tscore2}'])
    csvobj.writerow(['ImageId', 'Label', 'RealLabel'])
    csvobj.writerows(zip(ids, predict_output, translated_labels))
    pf.close()

print('Finished')
