from scipy.ndimage import gaussian_filter1d
from scipy.signal import kaiserord, lfilter, firwin, medfilt
import numpy as np
import pandas as pd


class Model:
    def __init__(self):
        pass


    def stz_tide(self, tide, downrate, zshift, tshift):
        # z/t shift and downsample Tide df
        tide['Tide_shifted'] = tide['Tide'] + zshift
        tide['Timestamp_shifted'] = tide['Timestamp'] + tshift

        tidesub = tide.iloc[::downrate]
        tidesub.reset_index(drop=True, inplace=True)
        tidesub['Tide'] = tidesub['Tide_shifted']

        return tide, tidesub


    def runfilter(self, tidesub, filtertype, sigma):
        if filtertype == 'Gauss':
            # Gaussian 1D filter
            gauss_sigma = sigma
            filtered = gaussian_filter1d(tidesub['Tide_shifted'], gauss_sigma)
            tidesub['Tide_filtered'] = filtered

        elif filtertype == 'FIR':
            # FIR filter
            sample_rate = sigma
            nyq_rate = sample_rate / 2
            width = 5 / nyq_rate
            ripple_db = 60
            cutoff_hz = 1

            N, beta = kaiserord(ripple_db, width)
            taps = firwin(N, cutoff_hz / nyq_rate, window=('kaiser', beta))

            # The phase delay of the filtered signal.
            delay = int(0.5 * (N - 1))

            # Use lfilter to filter x with the FIR filter.
            filtered = lfilter(taps, 1.0, tidesub['Tide_shifted'])

            # fill 'Tide_filtered' field
            tidesub.iloc[0:-delay, 6] = filtered[delay:]
            tidesub.iloc[0:delay, 6] = filtered[2 * delay]
            tidesub.iloc[-delay:, 6] = filtered[-1]

        elif filtertype == 'Median':
            # Median filter / make kernel odd
            kernel = sigma + 1 if sigma % 2 == 0 else sigma

            filtered = medfilt(tidesub['Tide_shifted'], kernel)
            tidesub['Tide_filtered'] = filtered

        elif filtertype == 'Mean':
            # Mean filter
            kernel = sigma
            filtered = np.convolve(tidesub['Tide_shifted'], np.ones(kernel), 'same') / kernel
            tidesub['Tide_filtered'] = filtered

        return tidesub


    def augment(self, tide):
        # timestamp median update rate
        diff = tide['Timestamp'].diff()
        upd_rate = diff.median()

        # identify gaps (timestamp diff > update rate)
        gaps = tide[diff > upd_rate]
        ixs_gap_start = gaps.index - 1
        ixs_gap_end = gaps.index

        # create empty dfs for gaps and interpolate start<->end values
        for i in range(len(ixs_gap_start)):
            timediff = diff[diff > upd_rate].iloc[i]
            rows_to_add = int(timediff / upd_rate) - 1

            nan_rows = pd.DataFrame([tide.loc[ixs_gap_start[i]]] * rows_to_add).copy()
            nan_rows.iloc[:] = np.nan

            augmented = pd.concat((pd.DataFrame([tide.loc[ixs_gap_start[i]]]),
                                   nan_rows,
                                   pd.DataFrame([tide.loc[ixs_gap_end[i]]]))).reset_index(drop=True)

            for col in ['Tide', 'Tide_shifted', 'Tide_filtered',
                        'Timestamp', 'Timestamp_shifted',
                        ]:
                xx = augmented[col].interpolate(method='index')
                augmented[col] = xx

            tide = (pd.concat([tide, augmented], ignore_index=True))
            tide.reset_index(drop=True, inplace=True)

        # sort and reset ix on tide df
        tide.sort_values(by=['Timestamp'], inplace=True)
        tide.reset_index(drop=True, inplace=True)

        return tide


    def align(self, gap_start, gap_end, tidesub):
        # find nearest data point (timestamp) to gap start/end
        gap_timestamp = []
        for point in [gap_start, gap_end]:
            diff = np.abs(tidesub['Timestamp_shifted'] - point[0])
            near_ix = diff.idxmin()
            gap_timestamp.append(tidesub.loc[near_ix, 'Timestamp_shifted'])
            tidesub.loc[near_ix, 'Tide_shifted'] = point[1]

        condition = ((tidesub['Timestamp_shifted'] > gap_timestamp[0]) &
                     (tidesub['Timestamp_shifted'] < gap_timestamp[1]))

        # interpolate tide between gap start/end
        tidesub.loc[condition, 'Tide_shifted'] = np.nan
        xx = tidesub['Tide_shifted'].interpolate()
        tidesub.loc[:, 'Tide_shifted'] = xx

        return tidesub


    def reject_accept(self, mode, tidesub, x, y, h_span, v_span):

        # REJECT
        if mode == 'R':
            # interpolateDF where:
            # left ROI limit < 'Timestamp_shifted' < right ROI limit &
            # low ROI limit < 'Tide_shifted' < high ROI limit
            condition = ((tidesub['Timestamp_shifted'] > (x - h_span)) &
                         (tidesub['Timestamp_shifted'] < (x + h_span)) &
                         (tidesub['Tide_shifted'] > (y - v_span)) &
                         (tidesub['Tide_shifted'] < (y + v_span))
                         )
            tidesub.loc[condition, 'Tide_shifted'] = np.nan
            x = tidesub['Tide_shifted'].interpolate()
            tidesub.loc[:, 'Tide_shifted'] = x

        # REACCEPT
        if mode == 'A':
            # restore 'Tide_shifted' form 'Tide'
            # left ROI limit < 'Timestamp_shifted' < right ROI limit &
            # low ROI limit < 'Tide_shifted' < high ROI limit
            condition = ((tidesub['Timestamp_shifted'] > (x - h_span)) &
                         (tidesub['Timestamp_shifted'] < (x + h_span)) &
                         (tidesub['Tide'] > (y - v_span)) &
                         (tidesub['Tide'] < (y + v_span))
                         )
            tidesub.loc[condition, 'Tide_shifted'] = tidesub.loc[condition, 'Tide']

        return tidesub