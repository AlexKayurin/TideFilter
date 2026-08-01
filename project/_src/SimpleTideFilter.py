import os
import platform
import subprocess
import sys
import json
import logging
from datetime import datetime
import numpy as np
import pandas as pd
from dearpygui.dearpygui import mvPlotScale_Time
from scipy.ndimage import gaussian_filter1d
from scipy.signal import kaiserord, lfilter, firwin, medfilt
import dearpygui.dearpygui as dpg
import DearPyGui_DragAndDrop as dpg_dnd


# pd. set_option('display.max_columns', None)


class SimpleTideWindow():
    def __init__(self,
                 configfold, configfile, logfile, iconfile, manual, license,
                 LASTFOLDER, LINESTOSKIP, FIELDFORMAT, EXPORTFORMAT,
                 DATETIMEFORMAT, SUBSAMPLE, SIGMA,):
        self.configfold = configfold
        self.configfile = configfile
        self.logfile = logfile
        self.iconfile = iconfile
        self.manual = manual
        self.license = license
        self.LASTFOLDER = LASTFOLDER
        self.LINESTOSKIP = LINESTOSKIP
        self.FIELDFORMAT = FIELDFORMAT
        self.EXPORTFORMAT = EXPORTFORMAT
        self.DATETIMEFORMAT = DATETIMEFORMAT
        self.SUBSAMPLE = SUBSAMPLE
        self.SIGMA = SIGMA

        self.message = ''


    def create_window(self):
        dpg.create_context()
        dpg_dnd.initialize()

        # add a font registry, font and bind default font
        with dpg.font_registry():
            default_font  = dpg.add_font(os.path.join(self.configfold, 'arial.ttf'), 14)
        dpg.bind_font(default_font)


        def close_message():
            # handles messagebox closing
            dpg.configure_item('Warning', show=False)


        def on_exit_callback():
            # handles exit event - save cfg file
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
                    'LASTFOLDER': self.LASTFOLDER,
                    'LINESTOSKIP': dpg.get_value('linestoskip_tag'),
                    'FIELDFORMAT': self.FIELDFORMAT,
                    'EXPORTFORMAT': self.EXPORTFORMAT,
                    'DATETIMEFORMAT': self.DATETIMEFORMAT,
                    'SUBSAMPLE': dpg.get_value('downrate_tag'),
                    'SIGMA': dpg.get_value('filter_value_tag'),
                }
                json_str = json.dumps(CFG, indent=0)
                with open(self.configfile, 'w') as outfile:
                    outfile.write(json_str)
            except:
                self.message = 'Configuration was not saved'
                dpg.set_value('messaget_text_tag', self.message)
                dpg.configure_item('Warning', show=True)


        def on_key_press(sender, app_data):
            # handles key press (Del/Ins)
            key = app_data

            if key == dpg.mvKey_Delete:
                # REJECT
                condition = ((self.tidesub['Timestamp_shifted'] > self.rej_xmin) &
                             (self.tidesub['Timestamp_shifted'] < self.rej_xmax) &
                             (self.tidesub['Tide_shifted'] > self.rej_ymin) &
                             (self.tidesub['Tide_shifted'] < self.rej_ymax))

                self.tidesub.loc[condition, 'Tide_shifted'] = np.nan
                x = self.tidesub['Tide_shifted'].interpolate()
                self.tidesub.loc[:, 'Tide_shifted'] = x
                self.tidesub.loc[:, 'Tide_filtered'] = x

                update_plot()

            if key == dpg.mvKey_Insert:
                # RE-ACCEPT
                condition = ((self.tidesub['Timestamp_shifted'] > self.rej_xmin) &
                             (self.tidesub['Timestamp_shifted'] < self.rej_xmax) &
                             (self.tidesub['Tide'] > self.rej_ymin) &
                             (self.tidesub['Tide'] < self.rej_ymax))

                self.tidesub.loc[condition, 'Tide_shifted'] = self.tidesub.loc[condition, 'Tide']
                self.tidesub.loc[:, 'Tide_filtered'] = self.tidesub.loc[:, 'Tide_shifted']

                update_plot()


        def edit_settings(sender):
            if sender == 'fileformat_tag':
                self.FIELDFORMAT = dpg.get_value('fileformat_tag').split(',')
                print(self.FIELDFORMAT)
            if sender == 'dateformat_tag':
                self.DATETIMEFORMAT[0] = dpg.get_value('dateformat_tag')
            if sender == 'timeformat_tag':
                self.DATETIMEFORMAT[1] = dpg.get_value('timeformat_tag')


        def show_settings():
            # show configuration
            platf = platform.system()
            if platf == 'Linux':
                subprocess.call(['xdg-open', self.configfile])  # , check=True)
            if platf == 'Windows':
                os.startfile(self.configfile)


        def open_manual(sender):
            # open application manual/license
            to_open = self.manual if sender == 'manual_tag' else self.license
            platf = platform.system()
            if platf == 'Linux':
                subprocess.call(['xdg-open', to_open])  # , check=True)
            if platf == 'Windows':
                os.startfile(to_open)


        def drop(data, keys):
            # handles drag&drop files
            fNames = data
            # print(f'{fNames}')
            load_tides(fNames)


        def loadtidefiles(sender, app_data):
            # handles loading files selected in file dialog
            # print("Sender: ", sender)
            # print("App Data: ", app_data)
            fNames = list(app_data['selections'].values())
            # print(f'{fNames}')
            load_tides(fNames)


        def savetidefile(sender, app_data):
            # handles saving file selected in file dialog
            fName = app_data['file_path_name']

            if fName:
                if fName:
                    # Shifted DateTime from timestamp
                    self.tidesub['DateTime_Shifted'] = \
                        [datetime.fromtimestamp(x).strftime(f'{self.DATETIMEFORMAT[0]} {self.DATETIMEFORMAT[1]}') for x in
                         self.tidesub['Timestamp_shifted']]
                    # round 'Tide_filtered' 3 decimals
                    self.tidesub['Tide_filtered'] = self.tidesub['Tide_filtered'].apply(lambda x: round(x, 3))

                    self.tidesub.to_csv(fName, columns=['DateTime_Shifted', 'Tide_filtered'], index=False, header=False)

                    # messagepop('File exported')


        def load_tides(fNames):
            # handles loading dropped/selected files
            try:
                if len(fNames):
                    linestoskip = dpg.get_value('linestoskip_tag')
                    tides = []
                    for fName in fNames:
                        singletide = pd.read_csv(fName, sep=r',|;|\s|\t|,',
                                                 skiprows=[x for x in range(linestoskip)],
                                                 skip_blank_lines=True, header=None, names=self.FIELDFORMAT,
                                                 dtype='object', engine='python')

                        # #  add concatenated 'DateTime' col
                        # singletide['DateTime'] = singletide['Date'] + ' ' + singletide['Time']
                        # convert date column to datetime.date & time column to datetime.time
                        tidedate = pd.to_datetime(singletide['Date'],
                                                  format=self.DATETIMEFORMAT[0], errors='coerce').dt.date
                        tidetime = pd.to_datetime(singletide['Time'],
                                                  format=self.DATETIMEFORMAT[1], errors='coerce').dt.time
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

                    downsample()

            except:
                self.message = 'File(s) not loaded\nCheck config file, header, fields, etc.'
                dpg.set_value('messaget_text_tag', self.message)
                dpg.configure_item('Warning', show=True)


        def downsample():
            # tide downsampling
            # get variables
            downrate = dpg.get_value('downrate_tag')
            zshift = dpg.get_value('zshift_tag')
            tshift = dpg.get_value('tshift_tag')

            # shift original tide data
            self.tide['Tide_shifted'] = self.tide['Tide'] + zshift
            self.tide['Timestamp_shifted'] = self.tide['Timestamp'] + tshift

            # subsample Tide df
            self.tidesub = self.tide.iloc[::downrate]
            self.tidesub.reset_index(drop=True, inplace=True)
            self.tidesub['Tide'] = self.tidesub['Tide_shifted']

            update_plot()


        def run_filter():
            # filter downsampled tide
            filter_type = dpg.get_value('filter_type_tag')
            filter_value = dpg.get_value('filter_value_tag')

            if filter_type == 'Gauss':
                # Gaussian 1D filter
                gauss_sigma = filter_value
                self.filtered = gaussian_filter1d(self.tidesub['Tide_shifted'], gauss_sigma)
                self.tidesub['Tide_filtered'] = self.filtered

            elif filter_type == 'FIR':
                # FIR filter
                sample_rate = filter_value
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

            elif filter_type == 'Median':
                # Median filter / make kernel odd
                kernel = filter_value + 1 if filter_value % 2 == 0\
                    else filter_value

                self.filtered = medfilt(self.tidesub['Tide_shifted'], kernel)
                self.tidesub['Tide_filtered'] = self.filtered

            elif filter_type == 'Mean':
                # Mean filter
                kernel = filter_value
                self.filtered = np.convolve(self.tidesub['Tide_shifted'], np.ones(kernel), 'same') / kernel
                self.tidesub['Tide_filtered'] = self.filtered


            update_plot()


        def update_plot():
            # update tide plot
            if self.tide.empty or self.tidesub.empty:
                return

            xo, xs, xf = self.tide['Timestamp_shifted'], self.tidesub['Timestamp_shifted'], self.tidesub['Timestamp_shifted']
            yo, ys, yf = self.tide['Tide_shifted'], self.tidesub['Tide_shifted'], self.tidesub['Tide_filtered']

            dpg.set_value('tide_series_tag', [xo.tolist(), yo.tolist()])
            dpg.set_value('tidesub_series_tag', [xs.tolist(), ys.tolist()])
            dpg.set_value('tidefilt_series_tag', [xf.tolist(), yf.tolist()])

            dpg.fit_axis_data('x_axis_tag')
            dpg.fit_axis_data('y_axis_tag')


        def plot_query_callback(sender, app_data):
            # handles plotted query rectangle on Tide plot
            (self.rej_xmin, self.rej_ymin, self.rej_xmax, self.rej_ymax) = app_data[0]


        # Key press handler
        with dpg.handler_registry():
            dpg.add_key_press_handler(callback=on_key_press)

        # theme for line
        with dpg.theme() as filt_theme:
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(
                    dpg.mvPlotCol_Line,
                    (0, 153, 255, 255),  # Blue
                    category=dpg.mvThemeCat_Plots
                )
                dpg.add_theme_style(
                    dpg.mvPlotStyleVar_LineWeight,
                    3.0,  # Line width
                    category=dpg.mvThemeCat_Plots
                )

        # text entry theme
        with dpg.theme() as text_theme:
            with dpg.theme_component(dpg.mvInputText):
                # Change text color (Green)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 0, 255))
                # # Change background box color (Dark Gray)
                # dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (50, 50, 50, 255))


        # open files dialog
        with dpg.file_dialog(label='Load tide file(s)', directory_selector=False, show=False, callback=loadtidefiles,
                             file_count=10000000,
                             tag='open_tides_dialog', width=700 ,height=400):
            dpg.add_file_extension('.txt', color=(255, 150, 150, 255))
            dpg.add_file_extension('.csv', color=(255, 255, 0, 255))
            dpg.add_file_extension('.*', color=(255, 0, 255, 255))
        # save file dialog
        with dpg.file_dialog(label='Save tide file', directory_selector=False, show=False, callback=savetidefile,
                             tag='export_tide_dialog', width=700 ,height=400):
            dpg.add_file_extension('.csv', color=(255, 255, 0, 255))
            dpg.add_file_extension('.txt', color=(255, 150, 150, 255))
            dpg.add_file_extension('.*', color=(255, 0, 255, 255))


        # MAIN WINDOW
        with dpg.window(tag='Win_tag'):
            # Menu bar
            with dpg.menu_bar():
                with dpg.menu(label='Menu'):
                    dpg.add_menu_item(label="Load tide(s)...", callback=lambda: dpg.show_item('open_tides_dialog'))
                    dpg.add_menu_item(label="Save filtered...", callback=lambda: dpg.show_item('export_tide_dialog'))
                    dpg.add_menu_item(label="Show settings file...", callback=show_settings)
                    dpg.add_menu_item(label="Manual", tag='manual_tag', callback=open_manual)
                    dpg.add_menu_item(label="License", tag='license_tag', callback=open_manual)


            # Plot
            with dpg.plot(label='Tide', tag='tideplot_tag', use_24hour_clock=True, use_ISO8601 =True,
                          query=True, callback=plot_query_callback,
                          width=-1, height=-140):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label='Time', tag='x_axis_tag', scale=mvPlotScale_Time)
                dpg.add_plot_axis(dpg.mvYAxis, label='Tide', tag='y_axis_tag')
                dpg.add_line_series([], [], label='Tide', parent='x_axis_tag',
                                    tag='tide_series_tag')
                dpg.add_line_series([], [], label='Tide downsampled', parent='x_axis_tag',
                                    tag='tidesub_series_tag')
                filtered = dpg.add_line_series([], [], label='Tide filtered', parent='x_axis_tag',
                                               tag='tidefilt_series_tag')

                dpg.bind_item_theme(filtered, filt_theme)


            # Fields format
            ff = dpg.add_input_text(label='Data fields', tag='fileformat_tag', callback=edit_settings,
                                    default_value=','.join(self.FIELDFORMAT),
                                    width=782)
            dpg.bind_item_theme(ff, text_theme)

            with dpg.group(horizontal=True):
                # dpg.add_spacer(width=5)
                with dpg.group():
                    # Date fomat
                    df = dpg.add_input_text(label='Date format', tag='dateformat_tag', callback=edit_settings,
                                            default_value=self.DATETIMEFORMAT[0],
                                            width=120)
                    dpg.bind_item_theme(df, text_theme)

                    # Time fomat
                    tf = dpg.add_input_text(label='Time format', tag='timeformat_tag', callback=edit_settings,
                                            default_value=self.DATETIMEFORMAT[1],
                                            width=120)
                    dpg.bind_item_theme(tf, text_theme)

                dpg.add_spacer(width=50)
                with dpg.group():
                    # Lines to skip spinbox
                    dpg.add_input_int(label='Lines to skip', tag='linestoskip_tag', callback=downsample,
                                      default_value=self.LINESTOSKIP, min_value=0, max_value=1000,
                                      width=100)
                    # Downsample spinbox
                    dpg.add_input_int(label='Downsample rate', tag='downrate_tag', callback=downsample,
                                      default_value=self.SUBSAMPLE, min_value=1, max_value=1000,
                                      width=100)
                    # Z shift spinbox
                    dpg.add_input_float(label='Z shift (m)', tag='zshift_tag', callback=downsample,
                                        default_value=0, min_value=-9999, max_value=9999,
                                        width=100)
                    # T shift spinbox
                    dpg.add_input_int(label='T shift (s)', tag='tshift_tag', callback=downsample,
                                      default_value=0, min_value=-82800, max_value=82800,
                                      width=100)
                    # filter value spinbox
                    dpg.add_input_int(label='Filter value', tag='filter_value_tag',
                                      default_value=self.SIGMA, min_value=1, max_value=10000,
                                      width=100)

                dpg.add_spacer(width=50)
                with dpg.group():
                    # Filters RB
                    dpg.add_radio_button(label='Filter type', items=['Gauss', 'FIR', 'Median', 'Mean'],
                                         tag='filter_type_tag',
                                         default_value='Gauss')

                dpg.add_spacer(width=50)
                with dpg.group():
                    # Filter button
                    dpg.add_button(label='Filter', tag='run_filter_tag', width=120, height=50,
                                   callback=run_filter)
                    # Export button
                    dpg.add_button(label='Save', tag='save_tide_tag', width=120, height=50,
                                   callback=lambda: dpg.show_item('export_tide_dialog'))


        #  MESSAGEBOX
        with dpg.window(
                label='Warning', tag='Warning',
                modal=True,     # no collapse
                show=False,
                no_resize=True,
                # no_move=True,
                pos=(400, 200),
                width=300,
                height=120,):
            dpg.add_text(tag='messaget_text_tag')
            dpg.add_spacer(height=10)
            dpg.add_button(label="OK", width=75, callback=close_message)


        dpg.create_viewport(title=f'SimpleTideFilter v.3 - akayurin@gmail.com (c) 2026')
        dpg.set_viewport_small_icon(self.iconfile)
        dpg.set_viewport_large_icon(self.iconfile)
        dpg.set_exit_callback(on_exit_callback)

        dpg_dnd.set_drop(drop)                                  # !!!! enables files drag&drop
        dpg.setup_dearpygui()
        dpg.show_viewport()

        dpg.set_primary_window('Win_tag', True)     # !!!! tie window to viewport (maximize to viewport)
        dpg.start_dearpygui()
        dpg.destroy_context()


def main():
    parentfold = os.path.dirname(sys.argv[0])
    configfold = os.path.join(parentfold, '_internal')
    configfile = os.path.join(configfold, 'cfg.json')
    logfile = os.path.join(configfold, 'error.log')
    iconfile = os.path.join(configfold, 'icon_tide.ico')
    manual = os.path.join(configfold, 'manual.pdf')
    license = os.path.join(configfold, 'license.pdf')


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

    except:
        LASTFOLDER = parentfold
        LINESTOSKIP = 0
        FIELDFORMAT = ['Date', 'Time', 'Tide']
        EXPORTFORMAT = ['DateTime_shifted', 'Tide_filtered']
        DATETIMEFORMAT = ['%d/%m/%Y', '%H:%M:%S']
        SUBSAMPLE  = 10
        SIGMA  = 25


    stw = SimpleTideWindow(configfold, configfile, logfile, iconfile, manual, license,
                           LASTFOLDER, LINESTOSKIP, FIELDFORMAT, EXPORTFORMAT,
                           DATETIMEFORMAT, SUBSAMPLE, SIGMA,
                           )
    stw.create_window()


if __name__ == '__main__':
    main()