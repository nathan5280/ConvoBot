import matplotlib.pyplot as plt
import numpy as np
from numpy import ma
import pandas as pd

def add_quiver_plot(ax, df):
    df['X'] = df['vRadius'] * np.cos(df['vTheta']/180*np.pi)
    df['Y'] = df['vRadius'] * np.sin(df['vTheta']/180*np.pi)
    df['pX'] = df['pRadius'] * np.cos(df['pTheta']/180*np.pi)
    df['pY'] = df['pRadius'] * np.sin(df['pTheta']/180*np.pi)
    df['dX'] = df['pX'] - df['X']
    df['dY'] = df['pY'] - df['Y']
    df['C'] = np.hypot(df['dX'], df['dY'])

    X = df['X']
    Y = df['Y']
    U = df['dX']
    V = df['dY']
    C = df['C']

    v = df.values
    print(df.columns)
    print(v[0])

    num_sites = 2500

    # plt.figure()
    plt.title('testing')
    # Q = plt.quiver(X, Y, U, V, C, units='width')
    Q = ax.quiver(X[:num_sites], Y[:num_sites], U[:num_sites], V[:num_sites], C[:num_sites], units='width')
    qk = ax.quiverkey(Q, 0.9, 0.9, 2, 'Radial and Theta Errors', labelpos='E', coordinates='figure')

    # qk = plt.quiverkey(Q, 0.9, 0.9, 2, r'$2 \frac{m}{s}$', labelpos='E',
    #                    coordinates='figure')


def main():
    # fig, ax = plt.subplots(1,2)
    fig, ax = plt.subplots(1,1)
    filename = '/Users/nathanatkins/mono-test-data/results/1507049446_predictions.csv'
    # filename = '/Users/nathanatkins/mono-prod-64x64-data/results/mono-predictions-64x64.csv'
    df = pd.read_csv(filename)
    print(df.columns)
    # add_quiver_plot(ax[0], df)
    add_quiver_plot(ax, df)

    # filename = '/Users/nathanatkins/stereo-prod-64x64-data/results/stereo-predictions-64x64.csv'
    # df = pd.read_csv(filename)
    # add_quiver_plot(ax[1], df)

    print('Plotting')
    plt.show()
    # plt.savefig('RT-Error.png')


if __name__ == '__main__':
    main()
