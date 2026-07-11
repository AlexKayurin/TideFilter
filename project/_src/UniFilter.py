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
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import Qt
import pyqtgraph as pg
import _UI_Control


OPTIONS = QFileDialog.Options()


class MainWindow(QtWidgets.QMainWindow, _UI_Control.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dataplot.setMenuEnabled(False)
        self.setAcceptDrops(True)
        self.vb_dataplot = self.dataplot.plotItem.vb  # for correct mouse tracking

        # set form
        self.le_filt_val.setValidator(QIntValidator())
        self.le_spike.setValidator(QDoubleValidator())
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
        self.le_spike.setText(str(SPIKE))
        if SHOWDESPIKELIM:
            self.ch_showspike.setChecked(True)
        else:
            self.ch_showspike.setChecked(False)


        # set signals
        self.dataplot.scene().sigMouseMoved.connect(self.mouse_moved)
        self.ch_showraw.stateChanged.connect(self.plotraw)
        self.le_tshift.textChanged.connect(self.shiftdata)
        self.le_zshift.textChanged.connect(self.shiftdata)
        self.b_reject.clicked.connect(self.reject_pressed)
        self.b_run.clicked.connect(self.runfilters)
        self.b_despike.clicked.connect(self.despike)
        self.b_export.clicked.connect(self.export)
        self.b_Yup.clicked.connect(self.y_change)
        self.b_Ydown.clicked.connect(self.y_change)
        self.b_Yall.clicked.connect(self.y_change)
        self.sp_subsample.valueChanged.connect(self.downsample)
        self.actionLoad.triggered.connect(self.selectfile)
        self.actionExport.triggered.connect(self.export)
        self.actionLoad_config.triggered.connect(self.selectfile)
        self.actionShow_config.triggered.connect(self.showconfig)
        for rb in [self.rb_Gauss, self.rb_FIR, self.rb_Median, self.rb_Mean, ]:
            rb.toggled.connect(self.setfilter)

        # set graph axis
        self.h_axis = pg.DateAxisItem(orientation='bottom')
        self.dataplot.setAxisItems({'bottom': self.h_axis})
        self.dataplot.showGrid(x=True, y=True)

        # variables
        self.rejectflag = False                         # reject mode on/off
        self.zoom = 1                                   # reject rectangle zoom multiplier


    def loadconfig(self, fName):
        global LASTFOLDER
        global LINESTOSKIP
        global FIELDFORMAT
        global EXPORTFORMAT
        global DATETIMEFORMAT
        global SHOWFIELD
        global SUBSAMPLE
        global SIGMA
        global SPIKE
        global SHOWDESPIKELIM
        global SHOWMAXIMIZED

        try:
            with open(fName) as cfgfile:
                cfg = json.load(cfgfile)
            LASTFOLDER = cfg['LASTFOLDER']
            LINESTOSKIP = cfg['LINESTOSKIP']
            FIELDFORMAT = cfg['FIELDFORMAT']
            EXPORTFORMAT = cfg['EXPORTFORMAT']
            DATETIMEFORMAT = cfg['DATETIMEFORMAT']
            SHOWFIELD = cfg['SHOWFIELD']
            SUBSAMPLE  = cfg['SUBSAMPLE']
            SIGMA = cfg['SIGMA']
            SPIKE = cfg['SPIKE']
            SHOWDESPIKELIM = cfg['SHOWDESPIKELIM']
            SHOWMAXIMIZED = cfg['SHOWMAXIMIZED']

            self.sp_linestoskip.setValue(LINESTOSKIP)
            self.sp_subsample.setValue(SUBSAMPLE)
            self.le_filt_val.setText(str(SIGMA))
            self.le_spike.setText(str(SPIKE))

            # save cfg file in ..\_internal\cfg.json
            SHOWDESPIKELIM = 1 if self.ch_showspike.isChecked() else 0
            CFG = {
                '#0:': r"Filed names in 'FIELDFORMAT' list MUST BE UNIQUE. Use alternative names (indexes, suffixes, prefixes) if some of them are originally duplicated.",
                '#1:': r"'Date' and 'Time' fields must be specified in 'FIELDFORMAT' list exactly as it is written (i.e. 'Date' 'Time').",
                '#2:': r"Date format examples: 30012026 - %d%m%Y; 30/01/2026 - %d/%m/%Y; 30-01-2026 - %d-%m-%Y",
                '#3:': r"Time format examples: 235959 - %H%M%S; 23:59:59 - %H:%M:%S; 23:59:59.000 - %H:%M:%S.%f",
                '#4:': r"App adds fields:   'Timestamp_shifted' - shifted DATA timestamp;",
                '#5:': r"                   'DateTime_Shifted' - shifted DATA Date/Time;",
                '#6:': r"                   'VALUE_Shift_DeSpike' - shifted and despiked DATA;",
                '#7:': r"                   'VALUE_Filtered' - shifted, despiked and smoothed DATA;",
                '#8:': r"                   'VALUE_Delta' - auxiliary field.",
                '#9:': r"----------------------------------------------------------------------------------------------------------------------------------------------------",
                'LASTFOLDER' : LASTFOLDER,
                'LINESTOSKIP' : self.sp_linestoskip.value(),
                'FIELDFORMAT' : FIELDFORMAT,
                'EXPORTFORMAT' : EXPORTFORMAT,
                'DATETIMEFORMAT' : DATETIMEFORMAT,
                'SHOWFIELD' : SHOWFIELD,
                'SUBSAMPLE' : self.sp_subsample.value(),
                'SIGMA' : int(self.le_filt_val.text()),
                'SPIKE' : float(self.le_spike.text()),
                'SHOWDESPIKELIM' : SHOWDESPIKELIM,
                'SHOWMAXIMIZED' : SHOWMAXIMIZED,
            }
            json_str = json.dumps(CFG, indent=0)
            with open(configfile, 'w') as outfile:
                outfile.write(json_str)
        except:
            logging.exception('Config file was not loaded and saved:')
            messagepop('Config file was not loaded and saved!')


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
            self.dataplot.setXRange(self.datasub['Timestamp_shifted'].min(), self.datasub['Timestamp_shifted'].max())
            self.dataplot.setYRange(self.datasub['VALUE_Shift_DeSpike'].min(),
                                    self.datasub['VALUE_Shift_DeSpike'].max())
            self.dataplot.setAspectLocked(False)


    def closeEvent(self, e):
        try:
            # save cfg file in ..\_internal\cfg.json
            SHOWDESPIKELIM = 1 if self.ch_showspike.isChecked() else 0
            CFG = {
                '#0:': r"Filed names in 'FIELDFORMAT' list MUST BE UNIQUE. Use alternative names (indexes, suffixes, prefixes) if some of them are originally duplicated.",
                '#1:': r"'Date' and 'Time' fields must be specified in 'FIELDFORMAT' list exactly as it is written (i.e. 'Date' 'Time').",
                '#2:': r"Date format examples: 30012026 - %d%m%Y; 30/01/2026 - %d/%m/%Y; 30-01-2026 - %d-%m-%Y",
                '#3:': r"Time format examples: 235959 - %H%M%S; 23:59:59 - %H:%M:%S; 23:59:59.000 - %H:%M:%S.%f",
                '#4:': r"App adds fields:   'Timestamp_shifted' - shifted DATA timestamp;",
                '#5:': r"                   'DateTime_Shifted' - shifted DATA Date/Time;",
                '#6:': r"                   'VALUE_Shift_DeSpike' - shifted and despiked DATA;",
                '#7:': r"                   'VALUE_Filtered' - shifted, despiked and smoothed DATA;",
                '#8:': r"                   'VALUE_Delta' - auxiliary field.",
                '#9:': r"----------------------------------------------------------------------------------------------------------------------------------------------------",
                'LASTFOLDER' : LASTFOLDER,
                'LINESTOSKIP' : self.sp_linestoskip.value(),
                'FIELDFORMAT' : FIELDFORMAT,
                'EXPORTFORMAT' : EXPORTFORMAT,
                'DATETIMEFORMAT' : DATETIMEFORMAT,
                'SHOWFIELD' : SHOWFIELD,
                'SUBSAMPLE' : self.sp_subsample.value(),
                'SIGMA' : int(self.le_filt_val.text()),
                'SPIKE' : float(self.le_spike.text()),
                'SHOWDESPIKELIM' : SHOWDESPIKELIM,
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


    def mouseReleaseEvent(self, e):
        self.release_pos = e.position()

        # REJECT
        if e.button() == Qt.LeftButton and self.press_pos == self.release_pos:
            # interpolate/delete from DF where:
            # left ROI limit < 'Timestamp_shifted' < right ROI limit &
            # low ROI limit < 'VALUE_Shift_DeSpike' < high ROI limit
            condition = ((self.datasub['Timestamp_shifted'] > (self.cursor.x() - self.h_span)) &
                         (self.datasub['Timestamp_shifted'] < (self.cursor.x() + self.h_span)) &
                         (self.datasub['VALUE_Shift_DeSpike'] > (self.cursor.y() - self.v_span)) &
                         (self.datasub['VALUE_Shift_DeSpike'] < (self.cursor.y() + self.v_span))
                         )

            if self.rb_interpolate.isChecked():
                self.datasub.loc[condition, 'VALUE_Shift_DeSpike'] = np.nan
                x = self.datasub['VALUE_Shift_DeSpike'].interpolate()
                self.datasub.loc[:, 'VALUE_Shift_DeSpike'] = x
                self.datasub.loc[:, 'VALUE_Filtered'] = x

            if self.rb_remove.isChecked():
                self.datasub = self.datasub[~condition]

            self.plotraw()

        # REACCEPT
        if e.button() == Qt.RightButton and self.press_pos == self.release_pos:
            # left ROI limit < 'Timestamp_shifted' < right ROI limit &
            # low ROI limit < 'VALUE_Shift_DeSpike' < high ROI limit
            condition = ((self.datasub['Timestamp_shifted'] > (self.cursor.x() - self.h_span)) &
                         (self.datasub['Timestamp_shifted'] < (self.cursor.x() + self.h_span)) &
                         (self.datasub[SHOWFIELD] > (self.cursor.y() - self.v_span)) &
                         (self.datasub[SHOWFIELD] < (self.cursor.y() + self.v_span))
                         )

            # if self.rb_interpolate.isChecked():
            self.datasub.loc[condition, 'VALUE_Shift_DeSpike'] = self.datasub.loc[condition, SHOWFIELD]
            self.datasub.loc[:, 'VALUE_Filtered'] = self.datasub.loc[:, 'VALUE_Shift_DeSpike']

            self.plotraw()


    def keyPressEvent(self, e):
        if self.rejectflag:
            if e.key() == 45:           # Minus
                self.zoom *=1.1
            if e.key() == 43:           # Plus
                self.zoom *=0.9


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        fNames = e.mimeData().text().strip().replace('file:///', '')
        self.loaddata(fNames.split('\n'))


    def reject_pressed(self):
        self.rejectflag = True if not self.rejectflag else False

        if self.rejectflag:
            self.b_reject.setChecked(True)
            self.b_reject.setStyleSheet("background-color: cyan")
            self.l_text.setText('L Mouse Button to reject\nR Mouse Button to re-accept\n+ to increase eraser\n- to decrease eraser')
        else:
            self.b_reject.setChecked(False)
            self.b_reject.setStyleSheet("background-color: none")
            self.l_text.setText('')
            try:
                self.dataplot.removeItem(self.reject_rect)
            except:
                pass


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
            fNames, _ = QFileDialog.getOpenFileNames(self, 'Load data file', f'{LASTFOLDER}',
                                                   'ASCII data files (*.*)', options=OPTIONS)
            if fNames:
                self.loaddata(fNames)

        if sender == 'actionLoad_config':
            fName, _ = QFileDialog.getOpenFileName(self, 'Load configuration file', f'{configfold}',
                                                   'json file (*.json);;All Files (*.*)', options=OPTIONS)
            if fName:
                self.loadconfig(fName)


    def loaddata(self, fNames):
        global LASTFOLDER

        if fNames:
            LASTFOLDER = os.path.dirname(fNames[0])

            try:
                datalist = []
                for fName in fNames:
                    singledata = pd.read_csv(fName, sep=r',|;|\s|\t|,',
                                             skiprows=[x for x in range(int(self.sp_linestoskip.value()))],
                                             skip_blank_lines=True, header=None, names=FIELDFORMAT,
                                             dtype='object', engine='python')

                    # #  add concatenated 'DateTime' col
                    # singledata['DateTime'] = singledata['Date'] + ' ' + singledata['Time']
                    # convert date column to datetime.date & time column to datetime.time
                    datadate = pd.to_datetime(singledata['Date'],
                                              format=DATETIMEFORMAT[0], errors='coerce').dt.date
                    datatime = pd.to_datetime(singledata['Time'],
                                              format=DATETIMEFORMAT[1], errors='coerce').dt.time
                    # create and add timestamps (and shifted timestamps) col
                    singledata['Timestamp'] = pd.Series([pd.Timestamp.combine(d, t) for d, t in
                                                        zip(datadate, datatime)]).astype('int') / 1000000
                    singledata['Timestamp_shifted'] = singledata['Timestamp']

                    #  convert 'Data' str to float and interpolate missing data (and add shifted field)
                    singledata[SHOWFIELD] = singledata[SHOWFIELD].astype(float).interpolate(method='linear',
                                                                                      limit_area='inside')
                    singledata['VALUE_Shift_DeSpike'] = singledata[SHOWFIELD]

                    # add filtered field
                    singledata['VALUE_Filtered'] = singledata['VALUE_Shift_DeSpike']

                    datalist.append(singledata)

                #  concat and sort concatenated data
                self.data = pd.concat(datalist)
                self.data.sort_values(by=['Timestamp'], inplace=True)

                self.plotlegend = self.dataplot.addLegend()

                self.downsample()

            except:
                logging.exception(f'Could not load data file(s): {fNames}')
                messagepop('Check data file (header, format, etc.) and cfg file')


    def downsample(self):
        self.downrate = self.sp_subsample.value()

        # subsample ORIGINAL df
        self.datasub = self.data.iloc[::self.downrate].copy()
        self.datasub.reset_index(drop=True, inplace=True)
        self.datasub[SHOWFIELD] = self.datasub['VALUE_Shift_DeSpike']
        self.dataplot.setXRange(self.datasub['Timestamp_shifted'].min(), self.datasub['Timestamp_shifted'].max())
        self.dataplot.setYRange(self.datasub['VALUE_Shift_DeSpike'].min(), self.datasub['VALUE_Shift_DeSpike'].max())
        self.dataplot.setAspectLocked(False)
        self.plotraw()


    def shiftdata(self):
        self.data['VALUE_Shift_DeSpike'] = self.data[SHOWFIELD] + float(self.le_zshift.text())
        self.data['Timestamp_shifted'] = self.data['Timestamp'] + int(self.le_tshift.text())

        self.downsample()


    def plotraw(self):
        try:
            self.plotlegend.removeItem(self.datacurve)
            self.plotlegend.removeItem(self.datacurvesub)
            self.plotlegend.removeItem(self.flt)
        except:
            pass

        self.dataplot.clear()

        parent_box = pg.PlotDataItem()

        if self.ch_showraw.isChecked():
            self.datacurve = pg.PlotDataItem(x=self.data['Timestamp_shifted'], y=self.data['VALUE_Shift_DeSpike'],
                                             pen=pg.mkPen((51, 153, 255, 255), width=0.5))
            self.datacurve.setParentItem(parent_box)
            self.plotlegend.addItem(self.datacurve, 'Raw')

        self.datacurvesub = pg.PlotDataItem(x=self.datasub['Timestamp_shifted'], y=self.datasub['VALUE_Shift_DeSpike'],
                                            pen=pg.mkPen((205, 205, 0, 255), width=1))
        self.datacurvesub.setParentItem(parent_box)
        self.dataplot.addItem(parent_box)
        self.plotlegend.addItem(self.datacurvesub, 'Raw Downsampled')

        # time span in status string
        tssh_ix = self.datasub.columns.get_indexer(['Timestamp_shifted'])[0]
        start = datetime.fromtimestamp(self.datasub.iloc[0, tssh_ix])
        end = datetime.fromtimestamp(self.datasub.iloc[-1, tssh_ix])
        self.l_filename.setText(f'{start} - {end}')


    def runfilters(self):
        self.plotraw()

        try:
            if self.rb_Gauss.isChecked():
                # Gaussian 1D filter
                gauss_sigma = int(self.le_filt_val.text())
                self.filtered = gaussian_filter1d(self.datasub['VALUE_Shift_DeSpike'], gauss_sigma)
                self.datasub['VALUE_Filtered'] = self.filtered

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
                self.filtered = lfilter(taps, 1.0, self.datasub['VALUE_Shift_DeSpike'])

                # fill 'VALUE_Filtered' field
                self.datasub.loc[self.datasub.index[0:-delay], 'VALUE_Filtered'] = self.filtered[delay:]
                self.datasub.loc[self.datasub.index[0:delay], 'VALUE_Filtered'] = self.filtered[2 * delay]
                self.datasub.loc[self.datasub.index[-delay:], 'VALUE_Filtered'] = self.filtered[-1]

            elif self.rb_Median.isChecked():
                # Median filter / make kernel odd
                kernel = int(self.le_filt_val.text()) + 1 if int(self.le_filt_val.text()) % 2 == 0\
                    else int(self.le_filt_val.text())

                self.filtered = medfilt(self.datasub['VALUE_Shift_DeSpike'], kernel)
                self.datasub['VALUE_Filtered'] = self.filtered

            elif self.rb_Mean.isChecked():
                # Mean filter
                kernel = int(self.le_filt_val.text())
                self.filtered = np.convolve(self.datasub['VALUE_Shift_DeSpike'], np.ones(kernel), 'same') / kernel
                self.datasub['VALUE_Filtered'] = self.filtered


            #  plot
            self.rejectflag = True
            self.reject_pressed()
            self.plotraw()

            spikevalue = float(self.le_spike.text())
            parent_box = pg.PlotDataItem()
            self.flt = pg.PlotDataItem(x=self.datasub['Timestamp_shifted'], y=self.datasub['VALUE_Filtered'],
                                             pen=pg.mkPen((255, 0, 255, 255), width=4))
            self.flt.setParentItem(parent_box)

            if self.ch_showspike.isChecked():
                self.spike_up = pg.PlotDataItem(x=self.datasub['Timestamp_shifted'], y=self.datasub['VALUE_Filtered'] + spikevalue,
                                                pen=pg.mkPen((255, 0, 255, 255), width=0.5))
                self.spike_dn = pg.PlotDataItem(x=self.datasub['Timestamp_shifted'], y=self.datasub['VALUE_Filtered'] - spikevalue,
                                                pen=pg.mkPen((255, 0, 255, 255), width=0.5))
                self.spike_up.setParentItem(parent_box)
                self.spike_dn.setParentItem(parent_box)

            self.dataplot.addItem(parent_box)

            # legend
            self.plotlegend.addItem(self.flt, 'Filtered')

        except:
            logging.exception('Somthing went wrong, check log file')
            messagepop('Somthing went wrong, check log file')


    def despike(self):
        spikevalue = float(self.le_spike.text())

        self.datasub['VALUE_Delta'] = (self.datasub['VALUE_Filtered'] - self.datasub['VALUE_Shift_DeSpike']).abs()
        if self.rb_interpolate.isChecked():
            self.datasub.loc[(self.datasub['VALUE_Delta'] > spikevalue), 'VALUE_Shift_DeSpike'] = np.nan
            x = self.datasub['VALUE_Shift_DeSpike'].interpolate()
            self.datasub.loc[:, 'VALUE_Shift_DeSpike'] = x
            self.datasub.loc[:, 'VALUE_Filtered'] = x

        if self.rb_remove.isChecked():
            self.datasub.drop(self.datasub[self.datasub['VALUE_Delta'] > spikevalue].index, inplace=True)
            self.datasub.reset_index(inplace=True)

        self.plotraw()


    def export(self):
        fName, _ = QFileDialog.getSaveFileName(self, 'Export data', f'{LASTFOLDER}',
                                               'csv file (*.csv);;All Files (*.*)', options=OPTIONS)
        if fName:
            # Shifted DateTime from timestamp
            self.datasub['DateTime_Shifted'] =\
                [datetime.fromtimestamp(x).strftime(f'{DATETIMEFORMAT[0]} {DATETIMEFORMAT[1]}') for x in self.datasub['Timestamp_shifted']]
            # # round 'VALUE_Shift_DeSpike' & 'VALUE_Filtered' 3 decimals
            # self.datasub['VALUE_Shift_DeSpike'] = self.datasub['VALUE_Shift_DeSpike'].apply(lambda x: round(x, 3))
            # self.datasub['VALUE_Filtered'] = self.datasub['VALUE_Filtered'].apply(lambda x: round(x, 3))

            self.datasub.to_csv(fName, columns=EXPORTFORMAT, index=False, header=True)

            # self.datasub.to_csv(fName, index=False)

            messagepop('File exported')


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
    global icon
    global iconhere
    global configfold
    global configfile
    global iconfile
    global LASTFOLDER
    global LINESTOSKIP
    global FIELDFORMAT
    global EXPORTFORMAT
    global DATETIMEFORMAT
    global SHOWFIELD
    global SUBSAMPLE
    global SIGMA
    global SPIKE
    global SHOWDESPIKELIM
    global SHOWMAXIMIZED


    # executable parent folder and path to config.bin
    iconhere = False
    parentfold = os.path.dirname(sys.argv[0])
    configfold = os.path.join(parentfold, '_internal')
    configfile = os.path.join(configfold, 'cfg.json')
    logfile = os.path.join(configfold, 'error.log')
    iconfile = os.path.join(configfold, 'icon_tide.ico')

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
        SHOWFIELD = cfg['SHOWFIELD']
        SUBSAMPLE  = cfg['SUBSAMPLE']
        SIGMA = cfg['SIGMA']
        SPIKE = cfg['SPIKE']
        SHOWDESPIKELIM = cfg['SHOWDESPIKELIM']
        SHOWMAXIMIZED = cfg['SHOWMAXIMIZED']

    except:
        LASTFOLDER = parentfold
        LINESTOSKIP = 0
        FIELDFORMAT = ['Date', 'Time', 'Tide']
        EXPORTFORMAT = ['DateTime_Shifted', 'Tide', 'VALUE_Shift_DeSpike', 'VALUE_Filtered']
        DATETIMEFORMAT = ['%d/%m/%Y', '%H:%M:%S']
        SHOWFIELD = 'Tide'
        SUBSAMPLE  = 10
        SIGMA = 25
        SPIKE = 0.2
        SHOWDESPIKELIM = 0
        SHOWMAXIMIZED = 0


    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')

    mc = MainWindow()

    # icon
    if os.path.isfile(iconfile):
        iconhere = True
        icon = QtGui.QIcon(iconfile)
        mc.setWindowIcon(icon)

    mc.setWindowTitle(f'UniFilter v.2 - akayurin@gmail.com \u00A9 2026')
    if SHOWMAXIMIZED:
        mc.showMaximized()

    mc.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()