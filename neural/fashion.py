from sys import argv
import timeit
import itertools
import enum
import csv
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib


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


DEBUG = True


def log(txt):
    if DEBUG:
        print(txt)


def usage(err=0):
    print('Usage:')
    print(f'{argv[0]} <command> [--help]')
    print('Commands:')
    print('train <training_file> <output_file> <epochs> <layer-sizes>')
    print('test <network_file> <test_file>')
    exit(err)


def read_csv(filepath: str):
    with open(filepath) as fp:
        reader = csv.reader(fp)
        next(reader)  # ignore header

        # normalize
        for label, *pxs in reader:
            pxs = np.array(pxs).astype(np.float) / 255

            yield label, pxs


def train(train_filepath: str, output_filepath: str, epochs: int, layer_sizes: tuple):
    log('Reading train file...')
    Y_data, X_data = zip(*read_csv(train_filepath))

    log('Splitting training and validation data...')
    X_train, X_validation, y_train, y_validation = train_test_split(
        X_data,
        Y_data,
        test_size=0.2,
        random_state=0)
    log(f'Training size: {len(X_train)}')
    log(f'Test size: {len(X_validation)}')

    methods = ['adam']  # , 'lbfgs', 'sgd']
    activations = ['logistic']  # , 'tanh', 'relu']
    for met, act in itertools.product(methods, activations):
        log(f'Solver: {met}')
        log(f'Function: {act}')
        log(f'Hidden Layers: {layer_sizes}')

        nn = MLPClassifier(
            activation=act,
            solver=met,
            hidden_layer_sizes=layer_sizes,
            max_iter=epochs,
            epsilon=1e-6)
        start_time = timeit.default_timer()
        log('Training Neural Network...')
        nn.fit(X_train, y_train)
        tscore = nn.score(X_train, y_train)
        log("Training set score: %f" % tscore)
        end_time = timeit.default_timer() - start_time
        log(f'Time: {end_time}')

        log('Saving trained neural network...')
        layers = str(layer_sizes).replace(',', '').replace(
            '(', '').replace(')', '').replace(' ', '')
        out_filename = output_filepath + met + act + layers
        joblib.dump(nn, out_filename)

        log('Validating Neural Network...')
        nn.predict(X_validation)
        tscore2 = nn.score(X_validation, y_validation)
        log("Validation set score: %f" % tscore2)

        filename = 'output_' + met + act + layers + '.csv'
        with open(filename, 'w') as fp:
            fp.write(f'Solver: {met}\n')
            fp.write(f'Function: {act}\n')
            fp.write(f'Hidden Layers: {layer_sizes}\n')
            fp.write(f'Time: {end_time}\n')
            fp.write(f'Train Score: {tscore}\n')
            fp.write(f'Validation Score: {tscore2}\n')

        log('Finish training\n\n')


def test(network_file: str, test_file: str):
    log('Loading saved network...')
    nn = joblib.load(network_file)

    log('Reading dataset file...')
    # test_df = pd.read_csv(test_file, header=0)
    # test_data = [[x/255 for x in a[1:]] for a in test_df.values]
    # test_y = [a[0] for a in test_df.values]

    Y_data, X_data = zip(*read_csv(test_file))

    log('Testing dataset...')
    output = nn.predict(X_data)
    final_score = accuracy_score(Y_data, output)
    log("Testing set score: %f" % final_score)
    conf_matrix = confusion_matrix(Y_data, output)
    print(conf_matrix)


if __name__ == '__main__':
    try:
        command = argv[1]
    except IndexError:
        usage(1)

    if '--help' in argv:
        usage()

    if command == 'train':
        try:
            _, _, train_filepath, output_filepath, epochs, *ls = argv
            layer_sizes = tuple([int(l) for l in ls])
        except (ValueError, TypeError):
            usage(1)
        else:
            train(train_filepath, output_filepath, int(epochs), layer_sizes)
    elif command == 'test':
        try:
            _, _, network_file, test_file = argv
        except (ValueError, TypeError):
            usage(1)
        else:
            test(network_file, test_file)

    log('Finished')
