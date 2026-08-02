# 02/08/2026 16:26 UTC

import os
import platform
import subprocess
import sys
import json
from datetime import datetime
import logging
from statistics import mean

from scipy.ndimage import gaussian_filter1d
from scipy.signal import kaiserord, lfilter, firwin, medfilt
import numpy as np
import pandas as pd
from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QIntValidator, QDoubleValidator, QMouseEvent
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QCoreApplication, Qt, QEvent
import pyqtgraph as pg
import _UI_Control
import _UI_Config


OPTIONS = QFileDialog.Options()


class ConfigWindow(QtWidgets.QMainWindow, _UI_Config.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.b_ok.clicked.connect(self.ok)
        self.b_cancel.clicked.connect(self.cancel)

    def ok(self):
        global FIELDFORMAT
        global DATETIMEFORMAT

        FIELDFORMAT = self.le_file_format.text().split(',')
        DATETIMEFORMAT[0] = self.le_date_format.text()
        DATETIMEFORMAT[1] = self.le_time_format.text()

        try:
            # save cfg file in ..\_internal\cfg.json
            CFG = {
                '#0:': r"Filed names in 'FIELDFORMAT' list MUST BE UNIQUE. Use alternative names (indexes, suffixes, prefixes) if some of them are originally duplicated.",
                '#1:': r"'Date' and 'Time' fields must be specified in 'FIELDFORMAT' list exactly as it is written (i.e. 'Date' 'Time').",
                '#2:': r"Date format examples: 30012026 - %d%m%Y; 30/01/2026 - %d/%m/%Y; 30-01-2026 - %d-%m-%Y",
                '#3:': r"Time format examples: 235959 - %H%M%S; 23:59:59 - %H:%M:%S; 23:59:59.000 - %H:%M:%S.%f",
                '#4:': r"App adds fields:   'Timestamp_shifted' - shifted DATA timestamp;",
                '#5:': r"                   'DateTime_shifted' - shifted DATA Date/Time;",
                '#6:': r"                   'Tide_shifted' - shifted DATA;",
                '#7:': r"                   'Tide_filtered' - shifted and smoothed DATA;",
                '#8:': r"----------------------------------------------------------------------------------------------------------------------------------------------------",
                'LASTFOLDER' : LASTFOLDER,
                'LINESTOSKIP' : mc.sp_linestoskip.value(),
                'FIELDFORMAT' : FIELDFORMAT,
                'EXPORTFORMAT' : EXPORTFORMAT,
                'DATETIMEFORMAT' : DATETIMEFORMAT,
                'SUBSAMPLE' : mc.sp_subsample.value(),
                'SIGMA' : int(mc.le_filt_val.text()),
                'SHOWMAXIMIZED' : SHOWMAXIMIZED,
            }
            json_str = json.dumps(CFG, indent=0)
            with open(configfile, 'w') as outfile:
                outfile.write(json_str)
        except:
            logging.exception('Config file was not saved:')
            messagepop('Config file was not saved!')

        self.close()


    def cancel(self):
        self.close()


class MainWindow(QtWidgets.QMainWindow, _UI_Control.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dataplot.setMenuEnabled(False)
        self.setAcceptDrops(True)
        self.vb_dataplot = self.dataplot.plotItem.vb  # for correct mouse tracking

        # set form
        self.le_filt_val.setValidator(QIntValidator())
        self.le_zshift.setValidator(QDoubleValidator())
        self.le_tshift.setValidator(QIntValidator())
        self.l_text.setText('')
        self.l_filename.setText('')
        self.b_Yup.setText('\u23F6')
        self.b_Ydown.setText('\u23F7')
        self.reject_pen = pg.mkPen(color='r', width=2)

        # set values
        self.sp_linestoskip.setValue(int(LINESTOSKIP))
        self.sp_subsample.setValue(int(SUBSAMPLE))
        self.le_filt_val.setText(str(SIGMA))

        # set signals
        self.dataplot.scene().sigMouseMoved.connect(self.mouse_moved)
        self.ch_showraw.stateChanged.connect(self.plotdata)
        self.le_tshift.textChanged.connect(self.shiftdata)
        self.le_zshift.textChanged.connect(self.shiftdata)
        self.b_augment.clicked.connect(self.augment)
        self.b_align.clicked.connect(self.align_btn_pressed)
        self.b_reject.clicked.connect(self.reject_btn_pressed)
        self.b_run.clicked.connect(self.runfilters)
        self.b_export.clicked.connect(self.export)
        self.b_Yup.clicked.connect(self.y_change)
        self.b_Ydown.clicked.connect(self.y_change)
        self.b_Yall.clicked.connect(self.y_change)
        self.sp_subsample.valueChanged.connect(self.downsample)
        self.actionLoad.triggered.connect(self.selectfile)
        self.actionExport.triggered.connect(self.export)
        self.actionEdit_config.triggered.connect(self.editconfig)
        self.actionShow_config.triggered.connect(self.showconfig)
        self.actionManual.triggered.connect(self.showdoc)
        self.actionLicense.triggered.connect(self.showdoc)
        for rb in [self.rb_Gauss, self.rb_FIR, self.rb_Median, self.rb_Mean, ]:
            rb.toggled.connect(self.setfilter)

        # set graph axis
        self.h_axis = pg.DateAxisItem(orientation='bottom')
        self.dataplot.setAxisItems({'bottom': self.h_axis})
        self.dataplot.showGrid(x=True, y=True)

        # variables
        self.augmented = False
        self.alignflag = False
        self.alignpoint = 0
        self.rejectflag = False
        self.zoom = 1                                   # reject rectangle zoom multiplier


    def showdoc(self):
        # open application manual/license
        sender = self.sender().objectName()

        to_open = manualfile if sender == 'actionManual' else licensefile
        platf = platform.system()
        if platf == 'Linux':
            subprocess.call(['xdg-open', to_open])  # , check=True)
        if platf == 'Windows':
            os.startfile(to_open)


    def editconfig(self):
        global LASTFOLDER
        global LINESTOSKIP
        global FIELDFORMAT
        global EXPORTFORMAT
        global DATETIMEFORMAT
        global SUBSAMPLE
        global SIGMA
        global SHOWMAXIMIZED

        cw.show()
        cw.le_file_format.setText(','.join(FIELDFORMAT))
        cw.le_date_format.setText(DATETIMEFORMAT[0])
        cw.le_time_format.setText(DATETIMEFORMAT[1])


    def showconfig(self):
        # show configuration
        platf = platform.system()
        if platf == 'Linux':
            subprocess.call(['xdg-open', configfile])  # , check=True)
        if platf == 'Windows':
            os.startfile(configfile)


    def y_change(self):
        aspect = self.dataplot.getViewBox().getAspectRatio()

        sender = self.sender().objectName()

        if sender == 'b_Yup':
            aspect *= 0.8
            self.dataplot.setAspectLocked(True, ratio=aspect)

        if sender == 'b_Ydown':
            aspect *= 1.2
            self.dataplot.setAspectLocked(True, ratio=aspect)

        if sender == 'b_Yall':
            self.dataplot.setAspectLocked(False)
            self.dataplot.setXRange(self.tidesub['Timestamp_shifted'].min(), self.tidesub['Timestamp_shifted'].max())
            self.dataplot.setYRange(self.tidesub['Tide_shifted'].min(),
                                    self.tidesub['Tide_shifted'].max())


    def closeEvent(self, e):
        try:
            # save cfg file in ..\_internal\cfg.json
            CFG = {
                '#0:': r"Filed names in 'FIELDFORMAT' list MUST BE UNIQUE. Use alternative names (indexes, suffixes, prefixes) if some of them are originally duplicated.",
                '#1:': r"'Date' and 'Time' fields must be specified in 'FIELDFORMAT' list exactly as it is written (i.e. 'Date' 'Time').",
                '#2:': r"Date format examples: 30012026 - %d%m%Y; 30/01/2026 - %d/%m/%Y; 30-01-2026 - %d-%m-%Y",
                '#3:': r"Time format examples: 235959 - %H%M%S; 23:59:59 - %H:%M:%S; 23:59:59.000 - %H:%M:%S.%f",
                '#4:': r"App adds fields:   'Timestamp_shifted' - shifted DATA timestamp;",
                '#5:': r"                   'DateTime_shifted' - shifted DATA Date/Time;",
                '#6:': r"                   'Tide_shifted' - shifted DATA;",
                '#7:': r"                   'Tide_filtered' - shifted and smoothed DATA;",
                '#8:': r"----------------------------------------------------------------------------------------------------------------------------------------------------",
                'LASTFOLDER' : LASTFOLDER,
                'LINESTOSKIP' : self.sp_linestoskip.value(),
                'FIELDFORMAT' : FIELDFORMAT,
                'EXPORTFORMAT' : EXPORTFORMAT,
                'DATETIMEFORMAT' : DATETIMEFORMAT,
                'SUBSAMPLE' : self.sp_subsample.value(),
                'SIGMA' : int(self.le_filt_val.text()),
                'SHOWMAXIMIZED' : SHOWMAXIMIZED,
            }
            json_str = json.dumps(CFG, indent=0)
            with open(configfile, 'w') as outfile:
                outfile.write(json_str)
        except:
            logging.exception('Config file was not saved:')
            messagepop('Config file was not saved!')


    def mouse_moved(self, e):
        self.cursor = self.vb_dataplot.mapSceneToView(e)

        # cursor coordinates
        self.ltime.setText(f'{datetime.fromtimestamp(int(self.cursor.x()))}')
        self.ldata.setText(f'{round(self.cursor.y(), 2)}')

        self.plot_reject_rect()


    def plot_reject_rect(self):
        # reject rectangle
        if self.rejectflag:
            try:
                self.dataplot.removeItem(self.reject_rect)
            except:
                pass

            #  calc reject rectangle
            aspect = self.vb_dataplot.getAspectRatio()
            self.v_span = (np.max(self.dataplot.viewRange()[1]) - np.min(self.dataplot.viewRange()[1])) / (20 * self.zoom)
            self.h_span = self.v_span / aspect

            self.reject_rect = pg.PlotCurveItem([-self.h_span, -self.h_span, self.h_span, self.h_span, -self.h_span],
                                                [-self.v_span, self.v_span, self.v_span, -self.v_span, -self.v_span])
            self.reject_rect.setPos(self.cursor.x(), self.cursor.y())
            self.reject_rect.setPen(self.reject_pen)
            self.dataplot.addItem(self.reject_rect)


    def mousePressEvent(self, e):
        # track mousePressEvent position to compare with mouseReleaseEvent position to reject spike
        self.press_pos = e.position()

        # cursor positions for gaps start/end
        x, y = self.cursor.x(), self.cursor.y()

        if self.alignflag and self.alignpoint % 2 == 0:
            self.gap_start = [x, y]

        if self.alignflag and self.alignpoint % 2 == 1:
            self.gap_end = [x, y]

            # alignment
            # find nearest data point (timestamp) to gap start/end
            if self.gap_start[0] > self.gap_end[0]:
                self.gap_start, self.gap_end = self.gap_end, self.gap_start

            gap_timestamp = []
            for point in [self.gap_start, self.gap_end]:
                diff = np.abs(self.tidesub['Timestamp_shifted'] - point[0])
                near_ix = diff.idxmin()
                gap_timestamp.append(self.tidesub.loc[near_ix, 'Timestamp_shifted'])
                self.tidesub.loc[near_ix, 'Tide_shifted'] = point[1]

            condition = ((self.tidesub['Timestamp_shifted'] > gap_timestamp[0]) &
                         (self.tidesub['Timestamp_shifted'] < gap_timestamp[1]))

            # interpolate tide between gap start/end
            self.tidesub.loc[condition, 'Tide_shifted'] = np.nan
            xx = self.tidesub['Tide_shifted'].interpolate()
            self.tidesub.loc[:, 'Tide_shifted'] = xx
            # self.tidesub.loc[:, 'Tide_filtered'] = xx

        self.alignpoint += 1
        self.plotdata()


    def mouseReleaseEvent(self, e):
        self.release_pos = e.position()

        if self.rejectflag:
            # REJECT
            if e.button() == Qt.LeftButton and self.press_pos == self.release_pos:
                # interpolate/delete from DF where:
                # left ROI limit < 'Timestamp_shifted' < right ROI limit &
                # low ROI limit < 'Tide_shifted' < high ROI limit
                condition = ((self.tidesub['Timestamp_shifted'] > (self.cursor.x() - self.h_span)) &
                             (self.tidesub['Timestamp_shifted'] < (self.cursor.x() + self.h_span)) &
                             (self.tidesub['Tide_shifted'] > (self.cursor.y() - self.v_span)) &
                             (self.tidesub['Tide_shifted'] < (self.cursor.y() + self.v_span))
                             )

                self.tidesub.loc[condition, 'Tide_shifted'] = np.nan
                x = self.tidesub['Tide_shifted'].interpolate()
                self.tidesub.loc[:, 'Tide_shifted'] = x
                # self.tidesub.loc[:, 'Tide_filtered'] = x

            # REACCEPT
            if e.button() == Qt.RightButton and self.press_pos == self.release_pos:
                # left ROI limit < 'Timestamp_shifted' < right ROI limit &
                # low ROI limit < 'Tide_shifted' < high ROI limit
                condition = ((self.tidesub['Timestamp_shifted'] > (self.cursor.x() - self.h_span)) &
                             (self.tidesub['Timestamp_shifted'] < (self.cursor.x() + self.h_span)) &
                             (self.tidesub['Tide'] > (self.cursor.y() - self.v_span)) &
                             (self.tidesub['Tide'] < (self.cursor.y() + self.v_span))
                             )

                self.tidesub.loc[condition, 'Tide_shifted'] = self.tidesub.loc[condition, 'Tide']
                # self.tidesub.loc[:, 'Tide_filtered'] = self.tidesub.loc[:, 'Tide_shifted']

            self.plotdata()


    def keyPressEvent(self, e):
        if self.rejectflag:

            if e.key() == 49:           # Minus
                self.zoom *=1.1
            if e.key() == 50:           # Plus
                self.zoom *=0.9

            self.plot_reject_rect()


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        fNames = e.mimeData().text().strip().replace('file:///', '')
        self.loadtide(fNames.split('\n'))


    def setfilter(self):
        if self.rb_Gauss.isChecked():
            self.l_filt_parameter.setText('Sigma')
        elif self.rb_FIR.isChecked():
            self.l_filt_parameter.setText('Samples')
        elif self.rb_Median.isChecked():
            self.l_filt_parameter.setText('Kernel')
        elif self.rb_Mean.isChecked():
            self.l_filt_parameter.setText('Window')


    def selectfile(self):
        sender = self.sender().objectName()

        if sender == 'actionLoad':
            fNames, _ = QFileDialog.getOpenFileNames(self, 'Load tide file', f'{LASTFOLDER}',
                                                   'ASCII tide files (*.*)', options=OPTIONS)
            if fNames:
                self.loadtide(fNames)


    def loadtide(self, fNames):
        global LASTFOLDER

        if fNames:
            LASTFOLDER = os.path.dirname(fNames[0])

            try:
                tides = []
                for fName in fNames:
                    singletide = pd.read_csv(fName, sep=r',|;|\s|\t|,',
                                             skiprows=[x for x in range(int(self.sp_linestoskip.value()))],
                                             skip_blank_lines=True, header=None, names=FIELDFORMAT,
                                             dtype='object', engine='python')

                    # #  add concatenated 'DateTime' col
                    # singletide['DateTime'] = singletide['Date'] + ' ' + singletide['Time']
                    # convert date column to datetime.date & time column to datetime.time
                    tidedate = pd.to_datetime(singletide['Date'],
                                              format=DATETIMEFORMAT[0], errors='coerce').dt.date
                    tidetime = pd.to_datetime(singletide['Time'],
                                              format=DATETIMEFORMAT[1], errors='coerce').dt.time
                    # create and add timestamps (and shifted timestamps) col
                    singletide['Timestamp'] = pd.Series([pd.Timestamp.combine(d, t) for d, t in
                                                        zip(tidedate, tidetime)]).astype('int') / 1000000
                    singletide['Timestamp_shifted'] = singletide['Timestamp']

                    #  convert 'Tide' str to float and interpolate missing tide (and add shifted Tide)
                    singletide['Tide'] = singletide['Tide'].astype(float).interpolate(method='linear',
                                                                                      limit_area='inside')
                    singletide['Tide_shifted'] = singletide['Tide']

                    # add filtered field
                    singletide['Tide_filtered'] = singletide['Tide_shifted']

                    tides.append(singletide)

                #  concat and sort concatenated tide
                self.tide = pd.concat(tides)
                self.tide.sort_values(by=['Timestamp'], inplace=True)
                self.tide.reset_index(drop=True, inplace=True)

                self.plotlegend = self.dataplot.addLegend()

                self.augmented = False
                self.b_augment.setText('Augment')
                self.b_augment.setStyleSheet("background-color: none")
                self.b_augment.setEnabled(True)
                self.b_align.setEnabled(False)

                self.downsample()

            except:
                logging.exception(f'Could not load tide file(s): {fNames}')
                messagepop('Check file (header, format, etc.)')


    def augment(self):
        # augment gaps with interpolated values based on median data update rate
        # timestamp median update rate
        diff = self.tide['Timestamp'].diff()
        upd_rate = diff.median()
        # identify gaps (timestamp diff > update rate)
        gaps = self.tide[diff > upd_rate]
        ixs_gap_start = gaps.index - 1
        ixs_gap_end = gaps.index

        # create empty dfs for gaps and interpolate start<->end values
        for i in range(len(ixs_gap_start)):
            timediff = diff[diff > upd_rate].iloc[i]
            rows_to_add = int(timediff / upd_rate) - 1

            nan_rows = pd.DataFrame([self.tide.loc[ixs_gap_start[i]]] * rows_to_add).copy()
            nan_rows.iloc[:] = np.nan

            augmented = pd.concat((pd.DataFrame([self.tide.loc[ixs_gap_start[i]]]),
                                   nan_rows,
                                   pd.DataFrame([self.tide.loc[ixs_gap_end[i]]]))).reset_index(drop=True)

            for col in ['Tide', 'Tide_shifted', 'Tide_filtered',
                        'Timestamp', 'Timestamp_shifted',
                        ]:
                xx = augmented[col].interpolate(method='index')
                augmented[col] = xx

            self.tide = (pd.concat([self.tide, augmented], ignore_index=True))
            self.tide.reset_index(drop=True, inplace=True)

        # sort and reset ix on tide df
        self.tide.sort_values(by=['Timestamp'], inplace=True)
        self.tide.reset_index(drop=True, inplace=True)

        self.augmented = True
        self.b_augment.setText('Augmented')
        self.b_augment.setStyleSheet("background-color: green")
        self.b_augment.setEnabled(False)

        self.b_align.setEnabled(True)

        self.downsample()


    def downsample(self):
        self.downrate = self.sp_subsample.value()

        # subsample Tide df and add 'Tide_filtered' col
        self.tidesub = self.tide.iloc[::self.downrate]
        self.tidesub.reset_index(drop=True, inplace=True)
        self.tidesub['Tide'] = self.tidesub['Tide_shifted']
        self.dataplot.setXRange(self.tidesub['Timestamp_shifted'].min(), self.tidesub['Timestamp_shifted'].max())
        self.dataplot.setYRange(self.tidesub['Tide_shifted'].min(), self.tidesub['Tide_shifted'].max())
        self.dataplot.setAspectLocked(False)
        self.plotdata()


    def shiftdata(self):
        self.tide['Tide_shifted'] = self.tide['Tide'] + float(self.le_zshift.text())
        self.tide['Timestamp_shifted'] = self.tide['Timestamp'] + int(self.le_tshift.text())

        self.downsample()


    def reject_btn_pressed(self):
        self.rejectflag = True if not self.rejectflag else False

        if self.rejectflag:
            self.b_augment.setEnabled(False)
            self.b_align.setEnabled(False)
            self.b_run.setEnabled(False)
            self.b_export.setEnabled(False)
            self.b_reject.setStyleSheet("background-color: cyan")
            self.l_text.setText('L Mouse Button to reject\nR Mouse Button to re-accept\n1 to decrease eraser\n2 to increase eraser')
        else:
            if not self.augmented:
                self.b_augment.setEnabled(True)
            self.b_align.setEnabled(True)
            self.b_run.setEnabled(True)
            self.b_export.setEnabled(True)
            self.b_reject.setStyleSheet("background-color: none")
            self.l_text.setText('')
            try:
                self.dataplot.removeItem(self.reject_rect)
            except:
                pass


    def align_btn_pressed(self):
        self.alignflag = True if not self.alignflag else False
        self.alignpoint = 0

        if self.alignflag:
            self.b_reject.setEnabled(False)
            self.b_run.setEnabled(False)
            self.b_export.setEnabled(False)
            self.b_align.setStyleSheet("background-color: cyan")
            self.l_text.setText('Click on start/end \nof the area to align')
        else:
            self.b_reject.setEnabled(True)
            self.b_run.setEnabled(True)
            self.b_export.setEnabled(True)
            self.b_align.setStyleSheet("background-color: none")
            self.l_text.setText('')


    def runfilters(self):
        try:
            if self.rb_Gauss.isChecked():
                # Gaussian 1D filter
                gauss_sigma = int(self.le_filt_val.text())
                self.filtered = gaussian_filter1d(self.tidesub['Tide_shifted'], gauss_sigma)
                self.tidesub['Tide_filtered'] = self.filtered

            elif self.rb_FIR.isChecked():
                # FIR filter
                sample_rate = int(self.le_filt_val.text())
                nyq_rate = sample_rate / 2
                width = 5 / nyq_rate
                ripple_db = 60
                cutoff_hz = 1

                N, beta = kaiserord(ripple_db, width)
                taps = firwin(N, cutoff_hz / nyq_rate, window=('kaiser', beta))

                # The phase delay of the filtered signal.
                delay = int(0.5 * (N - 1))

                # Use lfilter to filter x with the FIR filter.
                self.filtered = lfilter(taps, 1.0, self.tidesub['Tide_shifted'])

                # fill 'Tide_filtered' field
                self.tidesub.iloc[0:-delay, 6] = self.filtered[delay:]
                self.tidesub.iloc[0:delay, 6] = self.filtered[2 * delay]
                self.tidesub.iloc[-delay:, 6] = self.filtered[-1]

            elif self.rb_Median.isChecked():
                # Median filter / make kernel odd
                kernel = int(self.le_filt_val.text()) + 1 if int(self.le_filt_val.text()) % 2 == 0\
                    else int(self.le_filt_val.text())

                self.filtered = medfilt(self.tidesub['Tide_shifted'], kernel)
                self.tidesub['Tide_filtered'] = self.filtered

            elif self.rb_Mean.isChecked():
                # Mean filter
                kernel = int(self.le_filt_val.text())
                self.filtered = np.convolve(self.tidesub['Tide_shifted'], np.ones(kernel), 'same') / kernel
                self.tidesub['Tide_filtered'] = self.filtered

            #  plot
            self.plotdata()


        except:
            logging.exception('Somthing went wrong, check log file')
            messagepop('Somthing went wrong, check log file')


    def export(self):
        fName, _ = QFileDialog.getSaveFileName(self, 'Export filtered tide', f'{LASTFOLDER}',
                                               'csv file (*.csv);;All Files (*.*)', options=OPTIONS)
        if fName:
            # Shifted DateTime from timestamp
            self.tidesub['DateTime_Shifted'] =\
                [datetime.fromtimestamp(x).strftime(f'{DATETIMEFORMAT[0]} {DATETIMEFORMAT[1]}') for x in self.tidesub['Timestamp_shifted']]
            # round 'Tide_filtered' 3 decimals
            self.tidesub['Tide_filtered'] = self.tidesub['Tide_filtered'].apply(lambda x: round(x, 3))

            self.tidesub.to_csv(fName, columns=['DateTime_Shifted','Tide_filtered'], index=False, header=False)

            messagepop('File exported')


    def plotdata(self):
        try:
            self.plotlegend.removeItem(self.tidecurve)
            self.plotlegend.removeItem(self.tidecurvesub)
            self.plotlegend.removeItem(self.flt)
        except:
            pass

        self.dataplot.clear()

        parent_box = pg.PlotDataItem()

        if self.ch_showraw.isChecked():
            self.tidecurve = pg.PlotDataItem(x=self.tide['Timestamp_shifted'], y=self.tide['Tide_shifted'],
                                             pen=pg.mkPen((51, 153, 255, 255), width=0.5))
            self.tidecurve.setParentItem(parent_box)
            self.plotlegend.addItem(self.tidecurve, 'Raw')

        self.tidecurvesub = pg.PlotDataItem(x=self.tidesub['Timestamp_shifted'], y=self.tidesub['Tide_shifted'],
                                            pen=pg.mkPen((205, 205, 0, 255), width=1))
        self.tidecurvesub.setParentItem(parent_box)
        self.plotlegend.addItem(self.tidecurvesub, 'Raw Downsampled')

        self.flt = pg.PlotDataItem(x=self.tidesub['Timestamp_shifted'], y=self.tidesub['Tide_filtered'],
                                   pen=pg.mkPen((255, 0, 255, 255), width=4))
        self.flt.setParentItem(parent_box)
        self.plotlegend.addItem(self.flt, 'Filtered')

        self.dataplot.addItem(parent_box)

        # time span in status string
        start = datetime.fromtimestamp(self.tidesub.iloc[0, 4])
        end = datetime.fromtimestamp(self.tidesub.iloc[-1, 4])
        self.l_filename.setText(f'{start} - {end}')


def messagepop(message):
    msg = QMessageBox()
    msg.setWindowTitle('Warning')
    msg.setText(message)
    if iconhere:
        msg.setWindowIcon(icon)
    msg.show()
    msg.exec()


def main():
    global mc
    global cw
    global icon
    global iconhere
    global configfold
    global configfile
    global iconfile
    global manualfile
    global licensefile
    global LASTFOLDER
    global LINESTOSKIP
    global FIELDFORMAT
    global EXPORTFORMAT
    global DATETIMEFORMAT
    global SUBSAMPLE
    global SIGMA
    global SHOWMAXIMIZED


    # executable parent folder and path to config.bin
    iconhere = False
    parentfold = os.path.dirname(sys.argv[0])
    configfold = os.path.join(parentfold, '_internal')
    configfile = os.path.join(configfold, 'cfg.json')
    logfile = os.path.join(configfold, 'error.log')
    iconfile = os.path.join(configfold, 'icon_tide.ico')
    manualfile = os.path.join(configfold, 'manual.pdf')
    licensefile = os.path.join(configfold, 'license.pdf')

    # Remove old log file
    if os.path.isfile(logfile):
        os.remove(logfile)

    # Set up the basic configuration for logging
    logging.basicConfig(filename=logfile, level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.debug('App started')

    try:
        with open(configfile) as cfgfile:
            cfg = json.load(cfgfile)
        LASTFOLDER = cfg['LASTFOLDER']
        LINESTOSKIP = cfg['LINESTOSKIP']
        FIELDFORMAT = cfg['FIELDFORMAT']
        EXPORTFORMAT = cfg['EXPORTFORMAT']
        DATETIMEFORMAT = cfg['DATETIMEFORMAT']
        SUBSAMPLE  = cfg['SUBSAMPLE']
        SIGMA  = cfg['SIGMA']
        SHOWMAXIMIZED = cfg['SHOWMAXIMIZED']

    except:
        LASTFOLDER = parentfold
        LINESTOSKIP = 0
        FIELDFORMAT = ['Date', 'Time', 'Tide']
        EXPORTFORMAT = ['DateTime_shifted', 'Tide_filtered']
        DATETIMEFORMAT = ['%d/%m/%Y', '%H:%M:%S']
        SUBSAMPLE  = 10
        SIGMA  = 25
        SHOWMAXIMIZED = 0


    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')

    mc = MainWindow()
    cw = ConfigWindow()

    # icon
    if os.path.isfile(iconfile):
        iconhere = True
        icon = QtGui.QIcon(iconfile)
        mc.setWindowIcon(icon)
        cw.setWindowIcon(icon)

    mc.setWindowTitle(f'SimpleTideFilter v.2 - akayurin@gmail.com \u00A9 2026')
    cw.setWindowTitle(f'SimpleTideFilter v.2 - akayurin@gmail.com \u00A9 2026')

    if SHOWMAXIMIZED:
        mc.showMaximized()

    mc.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()