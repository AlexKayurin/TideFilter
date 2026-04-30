import os
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
        self.tideplot.setMenuEnabled(False)
        self.setAcceptDrops(True)
        self.vb_tideplot = self.tideplot.plotItem.vb  # for correct mouse tracking

        # set form
        self.le_filt_val.setValidator(QIntValidator())
        self.le_zshift.setValidator(QDoubleValidator())
        self.le_tshift.setValidator(QIntValidator())
        self.l_text.setText('')
        self.l_filename.setText('')

        # set values
        self.sp_linestoskip.setValue(int(LINESTOSKIP))
        self.sp_subsample.setValue(int(SUBSAMPLE))
        self.le_filt_val.setText(str(SIGMA))

        # set signals
        self.tideplot.scene().sigMouseMoved.connect(self.mouse_moved)
        self.ch_showraw.stateChanged.connect(self.plotraw)
        self.b_reject.clicked.connect(self.reject)
        self.b_run.clicked.connect(self.runfilters)
        self.b_export.clicked.connect(self.export)
        self.sp_subsample.valueChanged.connect(self.downsample)
        self.actionLoad.triggered.connect(self.selectfile)
        self.actionExport.triggered.connect(self.export)
        for rb in [self.rb_Gauss, self.rb_FIR, self.rb_Median, self.rb_Mean, ]:
            rb.toggled.connect(self.setfilter)
        # set graph axis
        self.h_axis = pg.DateAxisItem(orientation='bottom')
        self.tideplot.setAxisItems({'bottom': self.h_axis})
        self.tideplot.showGrid(x=True, y=True)

        # variables
        self.rejectflag = False


    def closeEvent(self, e):
        try:
            # save cfg file in ..\_internal\cfg.json
            CFG = {
                'LASTFOLDER' : LASTFOLDER,
                'LINESTOSKIP' : self.sp_linestoskip.value(),
                'FIELDFORMAT' : FIELDFORMAT,
                'DATETIMEFORMAT' : DATETIMEFORMAT,
                'SUBSAMPLE' : self.sp_subsample.value(),
                'SIGMA' : int(self.le_filt_val.text()),
                '#Date format examples:' : '30012026 - %d%m%Y; '
                                           '30/01/2026 - %d/%m/%Y; '
                                           '30-01-2026 - %d-%m-%Y',
                '#Time format examples: ' : '235959 - %H%M%S; '
                                            '23:59:59 - %H:%M:%S; '
                                            '23:59:59.000 - %H:%M:%S.%f'
            }
            json_str = json.dumps(CFG, indent=0)
            with open(configfile, 'w') as outfile:
                outfile.write(json_str)
        except:
            logging.exception('Config file was not saved:')
            messagepop('Config file was not saved!')


    def mouse_moved(self, e):
        self.cursor = self.vb_tideplot.mapSceneToView(e)
        self.ltime.setText(f'{datetime.fromtimestamp(int(self.cursor.x()))}')
        self.ltide.setText(f'{round(self.cursor.y(), 2)}')


    def keyPressEvent(self, e):
        if self.rejectflag:
            if e.key() == Qt.Key_Delete:
                # delete from DF where:
                if self.rb_RejectPoint.isChecked():
                    # left ROI limit < 'Timestamp_sh' < right ROI limit &
                    # low ROI limit < 'Tide_sh' < high ROI limit
                    condition = ((self.tide['Timestamp_sh'] > self.roi.pos()[0]) &
                                 (self.tide['Timestamp_sh'] < (self.roi.pos()[0] + self.roi.size()[0])) &
                                 (self.tide['Tide_sh'] > self.roi.pos()[1]) &
                                 (self.tide['Tide_sh'] < (self.roi.pos()[1] + self.roi.size()[1]))
                                 )
                if self.rb_RejectTime.isChecked():
                    # left ROI limit < 'Timestamp_sh' < right ROI limit &
                    condition = ((self.tide['Timestamp_sh'] > self.roi.pos()[0]) &
                                 (self.tide['Timestamp_sh'] < (self.roi.pos()[0] + self.roi.size()[0]))
                                 )

                self.tide = self.tide[~condition]

                self.downsample()


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
                    singletide['Timestamp_sh'] = singletide['Timestamp']

                    #  convert 'Tide' str to float and interpolate missing tide (and add shifted Tide)
                    singletide['Tide'] = singletide['Tide'].astype(float).interpolate(method='linear',
                                                                                      limit_area='inside')
                    singletide['Tide_sh'] = singletide['Tide']

                    # add filtered field
                    singletide['Filtered'] = singletide['Tide_sh']

                    tides.append(singletide)

                #  concat and sort concatenated tide
                self.tide = pd.concat(tides)
                self.tide.sort_values(by=['Timestamp'], inplace=True)

                self.plotlegend = self.tideplot.addLegend()

                self.downsample()
                # print(self.tide.columns)

            except:
                logging.exception(f'Could not load tide file(s): {fNames}')
                messagepop('Check file (header, format, etc.)')


    def downsample(self):
        self.downrate = self.sp_subsample.value()

        # subsample Tide df and add 'Filtered' col
        self.tidesub = self.tide.iloc[::self.downrate]
        self.tidesub.reset_index(drop=True, inplace=True)
        self.plotraw()


    def plotraw(self):
        try:
            self.plotlegend.removeItem(self.tidecurve)
            self.plotlegend.removeItem(self.tidecurvesub)
            self.plotlegend.removeItem(self.flt)
        except:
            pass

        self.tideplot.clear()

        parent_box = pg.PlotDataItem()

        if self.ch_showraw.isChecked():
            self.tidecurve = pg.PlotDataItem(x=self.tide['Timestamp_sh'], y=self.tide['Tide_sh'],
                                             pen=pg.mkPen((51, 153, 255, 255), width=2))
            self.tidecurve.setParentItem(parent_box)
            self.plotlegend.addItem(self.tidecurve, 'Raw')

        self.tidecurvesub = pg.PlotDataItem(x=self.tidesub['Timestamp_sh'], y=self.tidesub['Tide_sh'],
                                            pen=pg.mkPen((205, 205, 0, 255), width=0.5))
        self.tidecurvesub.setParentItem(parent_box)
        self.tideplot.addItem(parent_box)
        self.plotlegend.addItem(self.tidecurvesub, 'Raw Subsampled')

        self.tideplot.setXRange(self.tidesub['Timestamp_sh'].min(), self.tidesub['Timestamp_sh'].max())
        self.tideplot.setYRange(self.tidesub['Tide_sh'].min(), self.tidesub['Tide_sh'].max())

        # time span in status string
        start = datetime.fromtimestamp(self.tidesub.iloc[0, 4])
        end = datetime.fromtimestamp(self.tidesub.iloc[-1, 4])
        self.l_filename.setText(f'{start} - {end}')

        self.plotroi()


    def reject(self):
        self.rejectflag = True if not self.rejectflag else False

        if self.rejectflag:
            self.b_reject.setChecked(True)
            self.b_reject.setStyleSheet("background-color: cyan")
            self.l_text.setText('Press DEL to reject')
            self.groupBox_2.setEnabled(True)
            self.plotroi()
        else:
            self.b_reject.setChecked(False)
            self.b_reject.setStyleSheet("background-color: none")
            self.l_text.setText('')
            self.groupBox_2.setEnabled(False)
            try:
                self.tideplot.removeItem(self.roi)
            except:
                pass


    def plotroi(self):
        if self.rejectflag:
            aspect = self.vb_tideplot.getAspectRatio()
            v_span = (np.max(self.tideplot.viewRange()[1]) - np.min(self.tideplot.viewRange()[1])) / 10
            self.roi = pg.RectROI([mean(self.tideplot.viewRange()[0]), self.tide.loc[:, 'Tide'].mean()],
                                  [v_span / aspect, v_span], pen='r')
            self.tideplot.addItem(self.roi)


    def runfilters(self):
        self.tide['Tide_sh'] = self.tide['Tide'] + float(self.le_zshift.text())
        self.tide['Timestamp_sh'] = self.tide['Timestamp'] + int(self.le_tshift.text())
        self.downsample()

        try:
            if self.rb_Gauss.isChecked():
                # Gaussian 1D filter
                gauss_sigma = int(self.le_filt_val.text())
                self.filtered = gaussian_filter1d(self.tidesub['Tide_sh'], gauss_sigma)
                self.tidesub['Filtered'] = self.filtered

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
                self.filtered = lfilter(taps, 1.0, self.tidesub['Tide_sh'])

                # fill 'Filtered' field
                self.tidesub.iloc[0:-delay, 6] = self.filtered[delay:]
                self.tidesub.iloc[0:delay, 6] = self.filtered[2 * delay]
                self.tidesub.iloc[-delay:, 6] = self.filtered[-1]

            elif self.rb_Median.isChecked():
                # Median filter / make kernel odd
                kernel = int(self.le_filt_val.text()) + 1 if int(self.le_filt_val.text()) % 2 == 0\
                    else int(self.le_filt_val.text())

                self.filtered = medfilt(self.tidesub['Tide_sh'], kernel)
                self.tidesub['Filtered'] = self.filtered

            elif self.rb_Mean.isChecked():
                # Mean filter
                kernel = int(self.le_filt_val.text())
                self.filtered = np.convolve(self.tidesub['Tide_sh'], np.ones(kernel), 'same') / kernel
                self.tidesub['Filtered'] = self.filtered


            #  plot
            self.rejectflag = True
            self.reject()
            self.plotraw()

            parent_box = pg.PlotDataItem()
            self.flt = pg.PlotDataItem(x=self.tidesub['Timestamp_sh'], y=self.tidesub['Filtered'],
                                             pen=pg.mkPen((255, 0, 255, 255), width=4))
            self.flt.setParentItem(parent_box)
            self.tideplot.addItem(parent_box)

            # legend
            self.plotlegend.addItem(self.flt, 'Filtered')

        except:
            logging.exception('Somthing went wrong, check log file')
            messagepop('Somthing went wrong, check log file')


    def export(self):
        fName, _ = QFileDialog.getSaveFileName(self, 'Export filtered tide', f'{LASTFOLDER}',
                                               'csv file (*.csv);;All Files (*.*)', options=OPTIONS)
        if fName:
            # Shifted DateTime from timestamp
            self.tidesub['DateTime'] = [datetime.fromtimestamp(x) for x in self.tidesub['Timestamp_sh']]
            # round 'Filtered' 3 decimals
            self.tidesub['Filtered'] = self.tidesub['Filtered'].apply(lambda x: round(x, 3))

            self.tidesub.to_csv(fName, columns=['DateTime','Filtered'], index=False, header=False)

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
    global DATETIMEFORMAT
    global SUBSAMPLE
    global SIGMA


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
        DATETIMEFORMAT = cfg['DATETIMEFORMAT']
        SUBSAMPLE  = cfg['SUBSAMPLE']
        SIGMA  = cfg['SIGMA']

    except:
        LASTFOLDER = parentfold
        LINESTOSKIP = 0
        FIELDFORMAT = ['Date', 'Time', 'Tide']
        DATETIMEFORMAT = ['%d/%m/%Y', '%H:%M:%S']
        SUBSAMPLE  = 10
        SIGMA  = 25


    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')

    mc = MainWindow()

    # icon
    if os.path.isfile(iconfile):
        iconhere = True
        icon = QtGui.QIcon(iconfile)
        mc.setWindowIcon(icon)

    mc.setWindowTitle(f'Simple Tide Filter - akayurin@gmail com \u00A9 2026')

    mc.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()