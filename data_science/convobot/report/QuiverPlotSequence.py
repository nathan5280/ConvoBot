import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import os
import subprocess

'''
Generate a series of plots for the error based on predictions of the
validation data with models throughout the training stage.   This module
is dependent on the TrackingTrainer running the validation predictions
periodically and saving the information in a csv.

The graphs generated are a histogram of the error distribution and
a quiver plot of the error location.
'''

# TODO: Switch the radian / degree  conversions to the math package methods.
# TODO: Consider switching the RMSE error method in the optimizer to the
#           Euclidean error.

def add_positional_error(df):
    '''
    Calculate the euclidean distance error between the labeled location and
    the predicted location.

    Args:
      df: DataFrame of the predicted results.

    Returns: DataFrame with dX, dy and Error columns added.

    '''
    df['X'] = df['vRadius'] * np.cos(df['vTheta'] / 180 * np.pi)
    df['Y'] = df['vRadius'] * np.sin(df['vTheta'] / 180 * np.pi)
    df['pX'] = df['pRadius'] * np.cos(df['pTheta'] / 180 * np.pi)
    df['pY'] = df['pRadius'] * np.sin(df['pTheta'] / 180 * np.pi)
    df['dX'] = df['pX'] - df['X']
    df['dY'] = df['pY'] - df['Y']
    df['Error'] = np.hypot(df['dX'], df['dY'])
    return df


def add_quiver_plot(ax, df, num_points):
    '''
    Generate the quiver plot for the error and add it to the axis.

    Args:
      ax: The target axis for the quiver plot.
      df: The data to plot.
      num_points: The number of points to plot on the quiver plot.

    Returns:  None
    '''

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

    # Add the axis lines
    ax.axhline(linewidth=1, color='black', alpha=0.25, xmin=0.025, xmax=0.975)
    ax.axvline(linewidth=1, color='black', alpha=0.25, ymin=0.025, ymax=0.975)

    # Label the axis
    ax.text(35, 2, '0 or 360', fontsize=18,
            horizontalalignment='right', color='#EA7D00')
    ax.text(2, 33, '90', fontsize=18,
            horizontalalignment='left', color='#EA7D00')
    ax.text(-35, -6, '180', fontsize=18,
            horizontalalignment='left', color='#EA7D00')
    ax.text(-2, -34, '270', fontsize=18,
            horizontalalignment='right', color='#EA7D00')

    Q = ax.quiver(X[:num_points], Y[:num_points], U[:num_points],
                  V[:num_points], E[:num_points], units='width')


def add_histogram(ax, df, check_point):
    '''
    Generate the histogram plot for the error and add it to the axis.

    Args:
      ax: The target axis for the quiver plot.
      df: The data to plot.
      check_point: The index of the check point used to annotate the the plot.

    Returns: None

    '''
    ax.set_title('Frequency of\nPositional Error', fontsize=38)
    ax.set_xlabel('Error (Inches)', fontsize=24)
    ax.set_ylabel("Frequencey", fontsize=24)
    ax.tick_params(labelsize=20)
    # ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: ('%.1d')%(y*1e-3)))

    ax.text(5.7, 0.59, 'Check Point:  {}'.format(check_point),
            fontsize=24, horizontalalignment='right')
    ax.text(5.7, 0.52, 'Mean = {:2.1f}'.format(df['Error'].mean()),
            fontsize=24, horizontalalignment='right')
    ax.text(5.7, 0.45, 'Std. Dev. = {:2.1f}'.format(df['Error'].std()),
            fontsize=24, horizontalalignment='right')

    bins = np.arange(0, 6, 0.25) - 0.125
    ax.hist(
        df['Error'].abs(),
        bins,
        color='#EA7D00',
        edgecolor='black',
        normed=True)

    # Fudge the x axis tick marks to get the tick marks and the bins lined up.
    ax.set_xticks(range(0, 6))
    ax.set_xlim([-0.125, 6])
    ax.set_ylim([0, 0.8])


def main():
    '''
    Loop through all the images in order and generate a png file for each
    pair (histogram and quiver plot) that we have predictions for.

    Use ffmpeg to build the individual plots into a gif movie.
    '''
    root_dir_path = '/Users/nathanatkins/convobot-prod2'
    # TODO: Get the count of images by doing a listdir instead of having
    # the count hardcoded.
    pred_file_path_list = [
        os.path.join(
            root_dir_path,
            'prediction',
            '{0:04d}'.format(i) +
            '.csv') for i in range(50)]

    show = False    # Toggle between displaying the images or generating files.
    for counter, pred_file_path in enumerate(pred_file_path_list):

        pred_df = pd.read_csv(pred_file_path)
        pred_df = add_positional_error(pred_df)

        fig, ax = plt.subplots(1, 2, figsize=(14, 6))
        plt.tight_layout()
        add_histogram(ax[0], pred_df, '{0:02d}'.format(counter))
        add_quiver_plot(ax[1], pred_df, 1000)

        if show:
            plt.show()
        else:
            # Filename format 0000_error_plot.png
            output_filepath = os.path.join(
                root_dir_path, 'tmp', '{0:04d}_error_plot.png'.format(counter))
            print(output_filepath)
            plt.savefig(output_filepath, dpi=600)

        plt.close()

    if not show:
        # TODO: Figure out how to use color palettes or filters to clean up
        # yellow aliasing that is in the current gif.
        src_file_pattern = os.path.join(
            root_dir_path, 'tmp', '%04d_error_plot.png')
        dst_file_path = os.path.join(root_dir_path, 'movies', 'error.gif')

        # Run ffmpeg to convert the still png files to a movie.
        cmd_arr = ['ffmpeg', '-r', '1', '-i', src_file_pattern, dst_file_path]
        subprocess.run(cmd_arr)


if __name__ == '__main__':
    main()
