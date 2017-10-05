import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

def add_positional_error(df):
    df['X'] = df['vRadius'] * np.cos(df['vTheta']/180*np.pi)
    df['Y'] = df['vRadius'] * np.sin(df['vTheta']/180*np.pi)
    df['pX'] = df['pRadius'] * np.cos(df['pTheta']/180*np.pi)
    df['pY'] = df['pRadius'] * np.sin(df['pTheta']/180*np.pi)
    df['dX'] = df['pX'] - df['X']
    df['dY'] = df['pY'] - df['Y']
    df['Error'] = np.hypot(df['dX'], df['dY'])
    return df


def add_quiver_plot(ax, df, num_points):
    X = df['X']
    Y = df['Y']
    U = df['dX']
    V = df['dY']
    E = df['Error']

    ax.set_title('Location of\nPositional Error', fontsize=38)
    ax.set_xlabel('X-Position (Inches)', fontsize=24)
    ax.set_ylabel('Y-Position (Inches)', fontsize=24)
    ax.tick_params(labelsize=20)
    ax.set_xticks(range(-35, 45, 10))
    ax.set_xlim([-37, 37])
    ax.set_yticks(range(-35, 45, 10))
    ax.set_ylim([-37, 37])

    # Add the axis
    ax.axhline(linewidth=1, color='black', alpha=0.25, xmin=0.025, xmax=0.975)
    ax.axvline(linewidth=1, color='black', alpha=0.25, ymin=0.025, ymax=0.975)

    ax.text(35, 2, '0 or 360', fontsize=18, horizontalalignment='right',color='#EA7D00')
    ax.text(2, 33, '90', fontsize=18, horizontalalignment='left',color='#EA7D00')
    ax.text(-35, -6, '180', fontsize=18, horizontalalignment='left',color='#EA7D00')
    ax.text(-2, -34, '270', fontsize=18, horizontalalignment='right',color='#EA7D00')

    Q = ax.quiver(X[:num_points], Y[:num_points], U[:num_points],
                    V[:num_points], E[:num_points], units='width')


def add_histogram(ax, df):
    ax.set_title('Frequency of\nPositional Error', fontsize=38)
    ax.set_xlabel('Error (Inches)', fontsize=24)
    ax.set_ylabel("Frequencey", fontsize=24)
    ax.tick_params(labelsize=20)
    # ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: ('%.1d')%(y*1e-3)))

    ax.text(5.7, 0.5, 'Mean = {:2.1f}'.format(df['Error'].mean()),
            fontsize=24, horizontalalignment='right')
    ax.text(5.7, 0.45, 'Std. Dev. = {:2.1f}'.format(df['Error'].std()),
            fontsize=24, horizontalalignment='right')

    bins = np.arange(0, 6, 0.25) - 0.125
    ax.hist(df['Error'].abs(), bins, color='#EA7D00', edgecolor='black', normed=True)
    ax.set_xticks(range(0,6))
    ax.set_xlim([-0.125, 6])


def add_double_histogram(ax, index_df, pred_df):
    # Filter the prediction data to remove the predictions around the edges.
    theta_range = (45, 325)
    radius_range = (18, 28)
    mask = np.array((index_df.Theta >= theta_range[0]) & (index_df.Theta <= theta_range[1]) & \
                (index_df.Radius >= radius_range[0]) & (index_df.Radius <=radius_range[1]), dtype=bool)
    trimmed_df = pred_df[mask]

    ax.set_title('Frequency of\nPositional Error', fontsize=38)
    ax.set_xlabel('Error (Inches)', fontsize=24)
    ax.set_ylabel("Frequencey", fontsize=24)
    ax.tick_params(labelsize=20)
    # ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: ('%.1d')%(y*1e-3)))

    ax.text(5.7, 0.5, 'Mean = {:2.1f}'.format(trimmed_df['Error'].mean()),
            fontsize=24, horizontalalignment='right')
    ax.text(5.7, 0.45, 'Std. Dev. = {:2.1f}'.format(trimmed_df['Error'].std()),
            fontsize=24, horizontalalignment='right')

    bins = np.arange(0, 6, 0.25) - 0.125
    ax.hist(trimmed_df['Error'].abs(), bins, color='#EA7D00', edgecolor='black', normed=True)
    ax.set_xticks(range(0,6))
    ax.set_xlim([-0.125, 6])


def main():
    # pred_filename = '/Users/nathanatkins/mono-prod-64x64-data/results/1507063195_predictions.csv'
    pred_filename = '/Users/nathanatkins/mono-prod-64x64-data/results/1507125152_predictions.csv'
    index_filename = '/Users/nathanatkins/mono-prod-64x64-data/model/64x64/label_val.npy'

    show = True

    pred_df = pd.read_csv(pred_filename)
    pred_df = add_positional_error(pred_df)

    index_df = pd.DataFrame(np.load(index_filename), columns=['Theta', 'Radius', 'Alpha', 'X', 'Y'])

    fig1, ax1 = plt.subplots(1, figsize=(7,6))
    add_histogram(ax1, pred_df)
    plt.tight_layout()

    if show:
        plt.show()
    else:
        plt.savefig('Histogram-Error.png', transparent=True)


    fig2, ax2 = plt.subplots(1, figsize=(7,6))
    add_double_histogram(ax2, index_df, pred_df)
    plt.tight_layout()

    if show:
        plt.show()
    else:
        plt.savefig('Histogram-Error.png', transparent=True)


    fig3, ax3 = plt.subplots(1, figsize=(7,6))
    add_quiver_plot(ax3, pred_df, 750)
    plt.tight_layout()

    if show:
        plt.show()
    else:
        plt.savefig('Quiver-Error.png', transparent=True)


if __name__ == '__main__':
    main()
