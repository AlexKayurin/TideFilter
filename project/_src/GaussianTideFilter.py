import os
import sys
import json
from datetime import datetime
import logging
from statistics import mean
from scipy.ndimage import gaussian_filter1d
import numpy as np
import pandas as pd
from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import Qt
import pyqtgraph as pg
import _UI_Control_GAUSS


OPTIONS = QFileDialog.Options()


class MainWindow(QtWidgets.QMainWindow, _UI_Control_GAUSS.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tideplot.setMenuEnabled(False)
        self.setAcceptDrops(True)
        self.vb_tideplot = self.tideplot.plotItem.vb  # for correct mouse tracking

        # set form
        self.le_gauss_sigma.setValidator(QIntValidator())
        self.l_text.setText('')
        self.l_filename.setText('')

        # set values
        self.sp_linestoskip.setValue(int(LINESTOSKIP))
        self.sp_subsample.setValue(int(SUBSAMPLE))
        self.le_gauss_sigma.setText(str(SIGMA))

        # set signals
        self.tideplot.scene().sigMouseMoved.connect(self.mouse_moved)
        self.b_reject.clicked.connect(self.reject)
        self.b_run.clicked.connect(self.runfilters)
        self.b_export.clicked.connect(self.export)
        self.sp_linestoskip.valueChanged.connect(self.setlinestoskip)
        self.sp_subsample.valueChanged.connect(self.downsample)
        self.actionLoad.triggered.connect(self.selectfile)
        self.actionExport.triggered.connect(self.export)
        # set graph axis
        self.h_axis = pg.DateAxisItem(orientation='bottom')
        self.tideplot.setAxisItems({'bottom': self.h_axis})

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
                'SIGMA' : int(self.le_gauss_sigma.text()),
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
                # delete from DF where: left ROI limit < 'Timestamp' < right ROI limit
                condition = ((self.tide['Timestamp'] > self.roi.pos()[0]) &
                             (self.tide['Timestamp'] < (self.roi.pos()[0] + self.roi.size()[0])))
                self.tide = self.tide[~condition]

                self.downsample()


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        fName = e.mimeData().text().strip().replace('file:///', '')
        self.loadtide(fName)


    def selectfile(self):
        fName, _ = QFileDialog.getOpenFileName(self, 'Load tide file', f'{LASTFOLDER}',
                                               'ASCII tide files (*.*)', options=OPTIONS)
        if fName:
            self.loadtide(fName)


    def loadtide(self, fName):
        global LASTFOLDER

        if fName:
            LASTFOLDER = os.path.dirname(fName)

            self.l_filename.setText(os.path.basename(fName))
            try:
                self.tide = pd.read_csv(fName, sep=r',|;|\s|\t|,', skiprows=[x for x in range(int(LINESTOSKIP))],
                                        skip_blank_lines=True, header=None, names=FIELDFORMAT,
                                        dtype='object', engine='python')

                #  add concatenated 'DateTime' col
                self.tide['DateTime'] = self.tide['Date'] + ' ' + self.tide['Time']
                # convert date column to datetime.date & time column to datetime.time
                self.tidedate = pd.to_datetime(self.tide['Date'],
                                                   format=DATETIMEFORMAT[0], errors='coerce').dt.date
                self.tidetime = pd.to_datetime(self.tide['Time'],
                                                   format=DATETIMEFORMAT[1], errors='coerce').dt.time
                # create and add timestamps col
                self.tide['Timestamp'] = pd.Series([pd.Timestamp.combine(d, t) for d, t in
                                                    zip(self.tidedate, self.tidetime)]).astype('int') / 1000000

                #  convert 'Tide' str to float and interpolate missing tide
                self.tide['Tide'] = self.tide['Tide'].astype(float).interpolate(method='linear', limit_area='inside')

                self.plotlegend = self.tideplot.addLegend()
                self.downsample()

            except:
                logging.exception('Could not load tide file')
                messagepop('Check file (header, format, etc.)')


    def setlinestoskip(self):
        global LINESTOSKIP
        LINESTOSKIP = self.sp_linestoskip.value()


    def downsample(self):
        self.downrate = self.sp_subsample.value()

        # subsample Tide df
        self.tidesub = self.tide.iloc[::self.downrate]
        self.plotraw()


    def plotraw(self):
        try:
            self.plotlegend.removeItem(self.tidecurve)
            self.plotlegend.removeItem(self.tidecurvesub)
            self.plotlegend.removeItem(self.g1d)
        except:
            pass

        self.tideplot.clear()

        parent_box = pg.PlotDataItem()
        self.tidecurve = pg.PlotDataItem(x=self.tide['Timestamp'], y=self.tide['Tide'],
                                         pen=pg.mkPen((255, 128, 0, 255), width=1))
        self.tidecurvesub = pg.PlotDataItem(x=self.tidesub['Timestamp'], y=self.tidesub['Tide'],
                                            pen=pg.mkPen((204, 0, 204, 255), width=0.5))

        self.tidecurve.setParentItem(parent_box)
        self.tidecurvesub.setParentItem(parent_box)
        self.tideplot.addItem(parent_box)

        self.tideplot.setXRange(self.tide['Timestamp'].min(), self.tide['Timestamp'].max())
        self.tideplot.setYRange(self.tide['Tide'].min(), self.tide['Tide'].max())

        self.plotlegend.addItem(self.tidecurve, 'Raw')
        self.plotlegend.addItem(self.tidecurvesub, 'Raw Subsampled')

        self.plotroi()


    def reject(self):
        self.rejectflag = True if not self.rejectflag else False

        if self.rejectflag:
            self.b_reject.setChecked(True)
            self.b_reject.setStyleSheet("background-color: cyan")
            self.l_text.setText('Press DEL to reject')
            self.plotroi()
        else:
            self.b_reject.setChecked(False)
            self.b_reject.setStyleSheet("background-color: none")
            self.l_text.setText('')
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
        try:
            # Gaussian 1D filter-------------------------------------------------------------------------------------------
            gauss_sigma = int(self.le_gauss_sigma.text())
            self.gaussfiltered = gaussian_filter1d(self.tidesub['Tide'], gauss_sigma)
            # Gaussian 1D filter-------------------------------------------------------------------------------------------

            self.tidesub['Filtered'] = self.gaussfiltered

            #  plot
            self.rejectflag = True
            self.reject()
            self.plotraw()
            parent_box = pg.PlotDataItem()

            self.g1d = pg.PlotDataItem(x=self.tidesub['Timestamp'], y=self.gaussfiltered,
                                             pen=pg.mkPen((0, 255, 0, 255), width=4))

            self.g1d.setParentItem(parent_box)
            self.tideplot.addItem(parent_box)

            # legend
            self.plotlegend.addItem(self.g1d, 'Gauss Filtered')

        except:
            logging.exception('Somthing went wrong, check log file')
            messagepop('Somthing went wrong, check log file')


    def export(self):
        fName, _ = QFileDialog.getSaveFileName(self, 'Export filtered tide', f'{LASTFOLDER}',
                                               'csv file (*.csv);;All Files (*.*)', options=OPTIONS)
        if fName:
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
    iconfile = os.path.join(configfold, 'blob.ico')

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

    mc.setWindowTitle(f'Gaussian Tide Filter - akayurin@gmail com \u00A9 2026')

    mc.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()