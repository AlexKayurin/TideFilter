import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FIELDFORMAT = ['Timestamp',
               'East',
               'North',
               ]


def ghfilter1d(track, dx, dt, g=0.1, h=0.5):
    x_est = track[0, 1]

    results = []
    for i, reading in enumerate(track[1:, :]):
        # prediction step
        x_pred = x_est + (dx*dt)
        dx = dx
        # update step
        residual = reading[1] - x_pred
        dx = dx + h * (residual) / dt
        x_est = x_pred + g * residual
        results.append(x_est)

    return np.array(results)

def plot(track_straight, track_filt_fwd, track_filt_bwd, track_filt_dwy):
    fig, ax = plt.subplots()
    ax.plot(track_straight[:, 1], track_straight[:, 2], markersize=2, linewidth=2, color='blue')
    # ax.plot(track_filt_fwd[:, 1], track_filt_fwd[:, 2], markersize=2, linewidth=1, color='green')
    # ax.plot(track_filt_bwd[:, 1], track_filt_bwd[:, 2], markersize=2, linewidth=1, color='red')
    ax.plot(track_filt_dwy[:, 1], track_filt_dwy[:, 2], markersize=2, linewidth=2, color='magenta')
    ax.set_aspect('equal')
    plt.grid()
    plt.show()



trackfilename: str = r'D:\AK\PyProj\UniFilter\TideFilter\project\A-B-Filter\Track_regular_backstep.csv'

track_straight = pd.read_csv(trackfilename, sep=r',|;|\s|\t|,',
                             skip_blank_lines=True, header=None, names=FIELDFORMAT,
                             dtype='object', engine='python').to_numpy(dtype=float)

track_flipped = np.flip(track_straight.copy(), axis=0)
track_flipped[:, 0] = track_straight[-1, 0] - np.flip(track_straight[:, 0], axis=0)


track_filt_fwd = np.zeros(track_straight.shape)
track_filt_fwd[0] = track_straight[0]
track_filt_fwd[1:, 0] = track_straight[1:, 0]
track_filt_fwd[1:, 1] = ghfilter1d(track_straight[:,[0, 1]], dx=0.001, dt=1)
track_filt_fwd[1:, 2] = ghfilter1d(track_straight[:,[0, 2]], dx=0.001, dt=1)

track_filt_bwd = np.zeros(track_flipped.shape)
track_filt_bwd[0] = track_flipped[0]
track_filt_bwd[1:, 0] = track_flipped[1:, 0]
track_filt_bwd[1:, 1] = ghfilter1d(track_flipped[:,[0, 1]], dx=-0.001, dt=1)
track_filt_bwd[1:, 2] = ghfilter1d(track_flipped[:,[0, 2]], dx=-0.001, dt=1)

track_filt_dwy = np.zeros(track_straight.shape)
track_filt_dwy[:, 0] = track_filt_fwd[:, 0]
track_filt_dwy[:, 1] = (track_filt_fwd[:, 1] + np.flip(track_filt_bwd[:, 1], axis=0)) / 2
track_filt_dwy[:, 2] = (track_filt_fwd[:, 2] + np.flip(track_filt_bwd[:, 2], axis=0)) / 2


plot(track_straight, track_filt_fwd, track_filt_bwd, track_filt_dwy)



