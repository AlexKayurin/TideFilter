import os
import sys
import json
from datetime import datetime
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd
from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QFileDialog, QMessageBox
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
        self.le_sg_win.setValidator(QIntValidator())
        self.le_sg_ord.setValidator(QIntValidator())
        self.le_ma_win.setValidator(QIntValidator())
        # set signals
        self.tideplot.scene().sigMouseMoved.connect(self.mouse_moved)
        self.b_run.clicked.connect(self.runfilters)
        self.b_export.clicked.connect(self.export)
        self.sp_subsample.valueChanged.connect(self.downsample)
        self.actionLoad.triggered.connect(self.selectfile)
        self.actionExport.triggered.connect(self.export)
        # set graph axis
        self.h_axis = pg.DateAxisItem(orientation='bottom')
        self.tideplot.setAxisItems({'bottom': self.h_axis})


    def closeEvent(self, e):
        try:
            # save cfg file in ..\_internal\cfg.json
            CFG = {
                'LASTFOLDER' : LASTFOLDER,
                'LINESTOSKIP' : LINESTOSKIP,
                'FIELDFORMAT' : FIELDFORMAT,
                'DATETIMEFORMAT' : DATETIMEFORMAT,
            }
            json_str = json.dumps(CFG, indent=0)
            with open(configfile, 'w') as outfile:
                outfile.write(json_str)
        except:
            messagepop('Config file was not saved!')


    def mouse_moved(self, e):
        cursor = self.vb_tideplot.mapSceneToView(e)
        cursor = self.vb_tideplot.mapSceneToView(e)
        self.ltime.setText(f'{datetime.fromtimestamp(int(cursor.x()))}')
        self.ltide.setText(f'{round(cursor.y(), 2)}')


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

            try:
                self.tide = pd.read_csv(fName, sep=r';|\s|\t|,', skiprows=[x for x in range(int(LINESTOSKIP))],
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
                messagepop('Check file (header, format, etc.)')


    def downsample(self):
        self.downrate = self.sp_subsample.value()

        # subsample Tide df
        self.tidesub = self.tide.iloc[::self.downrate]
        self.plotraw()


    def plotraw(self):
        try:
            self.plotlegend.removeItem(self.tidecurve)
            self.plotlegend.removeItem(self.tidecurvesub)
            self.plotlegend.removeItem(self.sgf)
            self.plotlegend.removeItem(self.sga)
        except:
            pass

        self.tideplot.clear()

        parent_box = pg.PlotDataItem()
        self.tidecurve = pg.PlotDataItem(x=self.tide['Timestamp'], y=self.tide['Tide'],
                                         pen=pg.mkPen((204, 0, 204, 255), width=0.5))
        self.tidecurvesub = pg.PlotDataItem(x=self.tidesub['Timestamp'], y=self.tidesub['Tide'],
                                            pen=pg.mkPen((255, 128, 0, 255), width=0.5))

        self.tidecurve.setParentItem(parent_box)
        self.tidecurvesub.setParentItem(parent_box)
        self.tideplot.addItem(parent_box)

        self.tideplot.setXRange(self.tide['Timestamp'].min(), self.tide['Timestamp'].max())
        self.tideplot.setYRange(self.tide['Tide'].min(), self.tide['Tide'].max())

        self.plotlegend.addItem(self.tidecurve, 'Raw')
        self.plotlegend.addItem(self.tidecurvesub, 'Raw Subsampled')


    def runfilters(self):
        self.plotraw()

        mawin = int(self.le_ma_win.text())

        # sav_gol filter & moving average convolution------------------------------------------------------------------
        self.sgfiltered = savgol_filter(self.tidesub['Tide'], int(self.le_sg_win.text()),
                                        int(self.le_sg_ord.text()), mode='nearest')
        self.sgaveraged = np.convolve(self.sgfiltered, np.ones(mawin),
                                      'same') / mawin
        self.sgaveraged[:mawin] = self.sgfiltered[:mawin]
        self.sgaveraged[-mawin:] = self.sgfiltered[-mawin:]

        self.tidesub['Filtered'] = self.sgaveraged

        parent_box = pg.PlotDataItem()
        self.sgf = pg.PlotDataItem(x=self.tidesub['Timestamp'], y=self.sgfiltered,
                                         pen=pg.mkPen((0, 204, 204, 255), width=1))
        self.sga = pg.PlotDataItem(x=self.tidesub['Timestamp'], y=self.sgaveraged,
                                         pen=pg.mkPen((255, 204, 204, 255), width=4))
        # sav_gol filter & moving average convolution------------------------------------------------------------------

        self.sgf.setParentItem(parent_box)
        self.sga.setParentItem(parent_box)

        self.tideplot.addItem(parent_box)

        self.plotlegend.addItem(self.sgf, 'SG Filtered')
        self.plotlegend.addItem(self.sga, 'SG Averaged')


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


    # executable parent folder and path to config.bin
    iconhere = False
    parentfold = os.path.dirname(sys.argv[0])
    configfold = os.path.join(parentfold, '_internal')
    configfile = os.path.join(configfold, 'cfg.json')
    iconfile = os.path.join(configfold, 'blob.ico')

    try:
        with open(configfile) as cfgfile:
            cfg = json.load(cfgfile)
        LASTFOLDER = cfg['LASTFOLDER']
        LINESTOSKIP = cfg['LINESTOSKIP']
        FIELDFORMAT = cfg['FIELDFORMAT']
        DATETIMEFORMAT = cfg['DATETIMEFORMAT']

    except:
        LASTFOLDER = parentfold
        LINESTOSKIP = 0
        FIELDFORMAT = ['Date', 'Time', 'Tide']
        DATETIMEFORMAT = ['%d/%m/%Y', '%H:%M:%S']


    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')

    mc = MainWindow()

    # icon
    if os.path.isfile(iconfile):
        iconhere = True
        icon = QtGui.QIcon(iconfile)
        mc.setWindowIcon(icon)

    mc.setWindowTitle(f'Tide Filter - akayurin@gmail com \u00A9 2026')

    mc.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()