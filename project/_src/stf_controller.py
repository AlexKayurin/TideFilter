import os
import json
import logging
from datetime import datetime
import platform
import subprocess
import numpy as np
import pandas as pd
from PySide6 import QtGui
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt

class Controller:
    def __init__(self, config, view, model, parentfold):
        self._config = config
        self._view = view
        self._model = model

        # subscribe views to controller
        self._view.subscribe_controller(self)
        self._config.subscribe_controller(self)

        # init configuration
        self._parentfold = parentfold
        self._configfold = os.path.join(self._parentfold, '_internal')
        self._configfile = os.path.join(self._configfold, 'cfg.json')
        self._logfile = os.path.join(self._configfold, 'error.log')
        self._icon = QtGui.QIcon(os.path.join(self._configfold, 'icon_tide.ico'))
        self._manualfile = os.path.join(self._configfold, 'manual.pdf')
        self._licensefile = os.path.join(self._configfold, 'license.pdf')

        # read configuration from ./_internal/cfg.json and set up variables
        try:
            with open(self._configfile) as _cfgfile:
                cfg = json.load(_cfgfile)
            self._LASTFOLDER = cfg['LASTFOLDER']
            self._LINESTOSKIP = cfg['LINESTOSKIP']
            self._FIELDFORMAT = cfg['FIELDFORMAT']
            self._EXPORTFORMAT = cfg['EXPORTFORMAT']
            self._DATETIMEFORMAT = cfg['DATETIMEFORMAT']
            self._SUBSAMPLE  = cfg['SUBSAMPLE']
            self._SIGMA  = cfg['SIGMA']
            self._SHOWMAXIMIZED = cfg['SHOWMAXIMIZED']
        except:
            self._LASTFOLDER = self._parentfold
            self._LINESTOSKIP = 0
            self._FIELDFORMAT = ['Date', 'Time', 'Tide']
            self._EXPORTFORMAT = ['DateTime_shifted', 'Tide_filtered']
            self._DATETIMEFORMAT = ['%d/%m/%Y', '%H:%M:%S']
            self._SUBSAMPLE  = 10
            self._SIGMA  = 25
            self._SHOWMAXIMIZED = 0

        self._ZSHIFT = 0
        self._TSHIFT = 0
        self._augmented = False
        self._alignflag = False
        self._alignpoint = 0
        self._rejectflag = False
        self._zoom = 1


        # Set up the basic configuration for logging
        if os.path.isfile(self._logfile):
            os.remove(self._logfile)
        logging.basicConfig(filename=self._logfile, level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.debug('App started')

        # set up view UI
        self._view.setWindowIcon(self._icon)
        self._view.setWindowTitle(f'SimpleTideFilter v.2 - akayurin@gmail.com \u00A9 2026')
        self._config.setWindowIcon(self._icon)
        self._config.setWindowTitle(f'SimpleTideFilter v.2 - akayurin@gmail.com \u00A9 2026')
        self._view.l_text.setText('')
        self._view.l_filename.setText('')
        self._view.b_Yup.setText('\u23F6')
        self._view.b_Ydown.setText('\u23F7')
        self._view.sp_linestoskip.setValue(int(self._LINESTOSKIP))
        self._view.sp_subsample.setValue(int(self._SUBSAMPLE))
        self._view.le_filt_val.setText(str(self._SIGMA))
        if self._SHOWMAXIMIZED:
            self._view.showMaximized()


    def handle_mouse_moved(self, e):
        self.cursor = self._view.vb_dataplot.mapSceneToView(e)

        # cursor coordinates
        self._view.ltime.setText(f'{datetime.fromtimestamp(int(self.cursor.x()))}')
        self._view.ldata.setText(f'{round(self.cursor.y(), 2)}')

        if self._alignflag and self._alignpoint % 2 == 1:
            self._view.align_line.setData(x=[self.gap_start[0], self.cursor.x()],
                                          y=[self.gap_start[1], self.cursor.y()])

        if self._rejectflag:
            self.plot_reject_rect()


    def handle_mouse_pressed(self, e):
        # track mousePressEvent position to compare with mouseReleaseEvent position to reject spike
        self._press_pos = e.position()

        x, y = self.cursor.x(), self.cursor.y()

        if self._alignflag and self._alignpoint % 2 == 0:
            self.gap_start = [x, y]
            self._view.align_start.setData([x], [y])

        if self._alignflag and self._alignpoint % 2 == 1:
            self.gap_end = [x, y]

            # flip start/end if start < end
            if self.gap_start[0] > self.gap_end[0]:
                self.gap_start, self.gap_end = self.gap_end, self.gap_start

            # alignment
            self.tidesub = self._model.align(self.gap_start, self.gap_end, self.tidesub)

            self.plot_tide_data(resetview=0)

        self._alignpoint += 1


    def handle_mouse_released(self, e):
        self._release_pos = e.position()

        if e.button() == Qt.MouseButton.LeftButton:
            mode = 'R'
        elif e.button() == Qt.MouseButton.RightButton:
            mode = 'A'

        if self._rejectflag and self._press_pos == self._release_pos:
            self.tidesub = self._model.reject_accept(mode, self.tidesub,
                                                     self.cursor.x(), self.cursor.y(),
                                                     self.h_span, self.v_span)

            self.plot_tide_data(resetview=0)


    def handle_key_pressed(self, e):
        if self._rejectflag:

            if e.key() == 49:           # Minus
                self._zoom *=1.1
            if e.key() == 50:           # Plus
                self._zoom *=0.9

            self.plot_reject_rect()


    def handle_loadtide(self, fNames):
        self._LASTFOLDER = os.path.dirname(fNames[0])

        try:
            tides = []
            for fName in fNames:
                singletide = pd.read_csv(fName, sep=r',|;|\s|\t|,',
                                         skiprows=[x for x in range(int(self._view.sp_linestoskip.value()))],
                                         skip_blank_lines=True, header=None, names=self._FIELDFORMAT,
                                         dtype='object', engine='python')

                # #  add concatenated 'DateTime' col
                # singletide['DateTime'] = singletide['Date'] + ' ' + singletide['Time']
                # convert date column to datetime.date & time column to datetime.time
                tidedate = pd.to_datetime(singletide['Date'],
                                          format=self._DATETIMEFORMAT[0], errors='coerce').dt.date
                tidetime = pd.to_datetime(singletide['Time'],
                                          format=self._DATETIMEFORMAT[1], errors='coerce').dt.time
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

            # concat and sort concatenated tide
            self.tide = pd.concat(tides)
            self.tide.sort_values(by=['Timestamp'], inplace=True)
            self.tide.reset_index(drop=True, inplace=True)

            # reset augmentation settings
            self.augmented = False
            self._view.b_augment.setText('Augment')
            self._view.b_augment.setStyleSheet("background-color: none")
            self._view.b_augment.setEnabled(True)
            self._view.b_align.setEnabled(False)

            self.stz_tide(self._SUBSAMPLE,
                          float(self._view.le_zshift.text()),
                          int(self._view.le_tshift.text()))
            self.plot_tide_data(resetview=1)


        except:
            logging.exception(f'Could not load tide file(s): {fNames}')
            self.messagepop('Check file (header, format, etc.)', self._icon)


    def handle_savetide(self, fName):
        # Shifted DateTime from timestamp
        self.tidesub['DateTime_Shifted'] = \
            [datetime.fromtimestamp(x).strftime(f'{self._DATETIMEFORMAT[0]} {self._DATETIMEFORMAT[1]}') for x in
             self.tidesub['Timestamp_shifted']]
        # round 'Tide_filtered' 3 decimals
        self.tidesub['Tide_filtered'] = self.tidesub['Tide_filtered'].apply(lambda x: round(x, 3))

        self.tidesub.to_csv(fName, columns=['DateTime_Shifted', 'Tide_filtered'], index=False, header=False)

        self.messagepop('File exported', self._icon)


    def stz_tide(self, downrate, zshift, tshift):
        # downsample & plot
        try:
            self._SUBSAMPLE = downrate
            self._ZSHIFT = zshift
            self._TSHIFT = tshift
            self.tide, self.tidesub = self._model.stz_tide(self.tide, self._SUBSAMPLE, self._ZSHIFT, self._TSHIFT)
            self.plot_tide_data(resetview=1)
        except:
            pass


    def handle_augment(self):
        # augment gaps with interpolated values based on median data update rate
        # !!! NOTE THAT AUGMENTED DATA RECORDS ARE ADDED TI LOADED TIDE DF
        # THEREFORE IT CANNOT BE RESET BY SHFT OR DOWNSAMPLE

        self.tide = self._model.augment(self.tide)

        self._augmented = True
        self._view.b_augment.setText('Augmented')
        self._view.b_augment.setStyleSheet("background-color: green")
        self._view.b_augment.setEnabled(False)

        self._view.b_align.setEnabled(True)

        self.stz_tide(self._SUBSAMPLE,
                      float(self._view.le_zshift.text()),
                      int(self._view.le_tshift.text()))
        self.plot_tide_data(resetview=0)


    def handle_align(self):
        self._alignflag = True if not self._alignflag else False
        self._alignpoint = 0

        if self._alignflag:
            self._view.b_reject.setEnabled(False)
            self._view.b_run.setEnabled(False)
            self._view.b_export.setEnabled(False)
            self._view.align_start.setVisible(True)
            self._view.align_line.setVisible(True)
            self._view.b_align.setStyleSheet("background-color: cyan")
            self._view.l_text.setText('Click on start/end \nof the area to align')
        else:
            self._view.b_reject.setEnabled(True)
            self._view.b_run.setEnabled(True)
            self._view.b_export.setEnabled(True)
            self._view.align_start.setVisible(False)
            self._view.align_start.setData([], [])
            self._view.align_line.setVisible(False)
            self._view.align_line.setData([], [])
            self._view.b_align.setStyleSheet("background-color: none")
            self._view.l_text.setText('')


    def handle_runfilter(self):
        try:
            if self._view.rb_Gauss.isChecked():
                filtertype = 'Gauss'
            elif self._view.rb_FIR.isChecked():
                filtertype = 'FIR'
            elif self._view.rb_Median.isChecked():
                filtertype = 'Median'
            elif self._view.rb_Mean.isChecked():
                filtertype = 'Mean'

            self._SIGMA = int(self._view.le_filt_val.text())

            self.tidesub = self._model.runfilter(self.tidesub, filtertype, self._SIGMA)
            self.plot_tide_data(resetview=0)

        except:
            logging.exception('Somthing went wrong, check log file')
            self.messagepop('Somthing went wrong, check log file', self._icon)


    def handle_scaleview(self, aspect, sender):
        if sender == 'b_Yup':
            aspect *= 0.8
            self._view.dataplot.setAspectLocked(True, ratio=aspect)

        if sender == 'b_Ydown':
            aspect *= 1.2
            self._view.dataplot.setAspectLocked(True, ratio=aspect)

        if sender == 'b_Yall':
            self._view.dataplot.setAspectLocked(False)
            self._view.dataplot.setXRange(self.tidesub['Timestamp_shifted'].min(),
                                          self.tidesub['Timestamp_shifted'].max())
            self._view.dataplot.setYRange(self.tidesub['Tide_shifted'].min(),
                                          self.tidesub['Tide_shifted'].max())


    def handle_reject(self):
        self._rejectflag = True if not self._rejectflag else False

        if self._rejectflag:
            self._view.b_augment.setEnabled(False)
            self._view.b_align.setEnabled(False)
            self._view.b_run.setEnabled(False)
            self._view.b_export.setEnabled(False)
            self._view.reject_rect.setVisible(True)
            self._view.b_reject.setStyleSheet("background-color: cyan")
            self._view.l_text.setText('L Mouse Button to reject\nR Mouse Button to re-accept\n1 to decrease eraser\n2 to increase eraser')
        else:
            if not self._augmented:
                self._view.b_augment.setEnabled(True)
            self._view.b_align.setEnabled(True)
            self._view.b_run.setEnabled(True)
            self._view.b_export.setEnabled(True)
            self._view.reject_rect.setVisible(False)
            self._view.b_reject.setStyleSheet("background-color: none")
            self._view.l_text.setText('')
            try:
                self._view.dataplot.removeItem(self._view.reject_rect)
            except:
                pass


    def handle_showdoc(self, sender):
        # open application manual/license
        match sender:
            case 'actionManual':
                to_open = self._manualfile
            case 'actionLicense':
                to_open = self._licensefile
            case 'actionShow_config':
                to_open = self._configfile

        platf = platform.system()
        if platf == 'Linux':
            subprocess.call(['xdg-open', to_open])  # , check=True)
        if platf == 'Windows':
            os.startfile(to_open)


    def handle_close_ui(self):
        self.saveconfig()


    def handle_editconfig(self):
        self._config.le_file_format.setText(','.join(self._FIELDFORMAT))
        self._config.le_date_format.setText(self._DATETIMEFORMAT[0])
        self._config.le_time_format.setText(self._DATETIMEFORMAT[1])
        self._config.show()


    def handle_saveconfig(self):
        self._FIELDFORMAT = self._config.le_file_format.text().split(',')
        self._DATETIMEFORMAT[0] = self._config.le_date_format.text()
        self._DATETIMEFORMAT[1] = self._config.le_time_format.text()

        self.saveconfig()
        self._config.close()


    def saveconfig(self) -> None:
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
                'LASTFOLDER' : self._LASTFOLDER,
                'LINESTOSKIP' : self._view.sp_linestoskip.value(),
                'FIELDFORMAT' : self._FIELDFORMAT,
                'EXPORTFORMAT' : self._EXPORTFORMAT,
                'DATETIMEFORMAT' : self._DATETIMEFORMAT,
                'SUBSAMPLE' : self._view.sp_subsample.value(),
                'SIGMA' : int(self._view.le_filt_val.text()),
                'SHOWMAXIMIZED' : self._SHOWMAXIMIZED,
            }
            json_str = json.dumps(CFG, indent=0)
            with open(self._configfile, 'w') as outfile:
                outfile.write(json_str)
        except:
            logging.exception('Config file was not saved:')
            self.messagepop('Config file was not saved!', self._icon)


    def plot_reject_rect(self) -> None:
        #  calc reject rectangle
        aspect = self._view.vb_dataplot.getAspectRatio()
        self.v_span = (np.max(self._view.dataplot.viewRange()[1]) -
                       np.min(self._view.dataplot.viewRange()[1])) / (20 * self._zoom)
        self.h_span = self.v_span / aspect

        self._view.reject_rect.setData(x=[-self.h_span, -self.h_span, self.h_span, self.h_span, -self.h_span],
                                 y=[-self.v_span, self.v_span, self.v_span, -self.v_span, -self.v_span])

        self._view.reject_rect.setPos(self.cursor.x(), self.cursor.y())


    def plot_tide_data(self, resetview) -> None:
        if resetview:
            # plot range and aspect
            self._view.dataplot.setXRange(self.tidesub['Timestamp_shifted'].min(), self.tidesub['Timestamp_shifted'].max())
            self._view.dataplot.setYRange(self.tidesub['Tide_shifted'].min(), self.tidesub['Tide_shifted'].max())
            self._view.dataplot.setAspectLocked(False)

        # time span in status string
        start = datetime.fromtimestamp(self.tidesub.iloc[0, 4])
        end = datetime.fromtimestamp(self.tidesub.iloc[-1, 4])
        self._view.l_filename.setText(f'{start} - {end}')

        self._view.tidecurve.setData(x=self.tide['Timestamp_shifted'], y=self.tide['Tide_shifted'])
        self._view.tidecurvesub.setData(x=self.tidesub['Timestamp_shifted'], y=self.tidesub['Tide_shifted'])
        self._view.flt.setData(x=self.tidesub['Timestamp_shifted'], y=self.tidesub['Tide_filtered'])


    def messagepop(self, message, icon):
        _msg = QMessageBox()
        _msg.setWindowTitle('Warning')
        _msg.setText(message)
        _msg.setWindowIcon(icon)
        _msg.show()
        _msg.exec()