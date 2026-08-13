from PySide6 import QtWidgets
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import QFileDialog
import pyqtgraph as pg
import _UI_Control


class View(QtWidgets.QMainWindow, _UI_Control.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # set up le validators
        self.le_filt_val.setValidator(QIntValidator())
        self.le_zshift.setValidator(QDoubleValidator())
        self.le_tshift.setValidator(QIntValidator())

        # set up dataplot
        self.dataplot.setMenuEnabled(False)
        self.setAcceptDrops(True)
        self.vb_dataplot = self.dataplot.plotItem.vb  # for correct mouse tracking
        self.h_axis = pg.DateAxisItem(orientation='bottom')
        self.dataplot.setAxisItems({'bottom': self.h_axis})
        self.dataplot.showGrid(x=True, y=True)

        # set signals
        self.dataplot.scene().sigMouseMoved.connect(self.mouse_moved)
        self.sp_subsample.valueChanged.connect(self.stz_val_changed)
        self.le_tshift.textChanged.connect(self.stz_val_changed)
        self.le_zshift.textChanged.connect(self.stz_val_changed)
        self.b_augment.clicked.connect(self.augment_btn_pressed)
        self.b_align.clicked.connect(self.align_btn_pressed)
        self.b_reject.clicked.connect(self.reject_btn_pressed)
        self.b_run.clicked.connect(self.runfilter_btn_pressed)
        self.b_export.clicked.connect(self.savetide_btn_pressed)
        self.b_Yup.clicked.connect(self.scale_changed)
        self.b_Ydown.clicked.connect(self.scale_changed)
        self.b_Yall.clicked.connect(self.scale_changed)
        self.actionLoad.triggered.connect(self.selectfile)
        self.actionExport.triggered.connect(self.savetide_btn_pressed)
        self.actionEdit_config.triggered.connect(self.editconfig)
        self.actionShow_config.triggered.connect(self.showdoc)
        self.actionManual.triggered.connect(self.showdoc)
        self.actionLicense.triggered.connect(self.showdoc)
        for rb in [self.rb_Gauss, self.rb_FIR, self.rb_Median, self.rb_Mean, ]:
            rb.toggled.connect(self.setfiltertype)


        # set plot items
        self.parent_box = pg.PlotDataItem()
        self.dataplot.addItem(self.parent_box)
        self.plotlegend = self.dataplot.addLegend()
        # adding empty data graphs to plot parent_box
        # tide
        self.tidecurve = pg.PlotDataItem(x=[], y=[],
                                         pen=pg.mkPen((51, 153, 255, 255), width=0.5))
        # downsampled tide
        self.tidecurvesub = pg.PlotDataItem(x=[], y=[],
                                            pen=pg.mkPen((205, 205, 0, 255), width=1))
        # filtered tide
        self.flt = pg.PlotDataItem(x=[], y=[],
                                   pen=pg.mkPen((255, 0, 255, 255), width=4))
        # reject rectangle
        self.reject_rect = pg.PlotCurveItem([], [],
                                            pen=pg.mkPen(color='r', width=2))
        self.reject_rect.setVisible(False)
        # align start mark
        self.align_start = pg.PlotDataItem([], [],
                                           symbol='x', symbolSize=15, symbolBrush='red')
        self.align_start.setVisible(False)
        # align line
        self.align_line = pg.PlotDataItem([], [],
                                           pen=pg.mkPen(color='r', width=2))
        self.align_line.setVisible(False)

        self.tidecurve.setParentItem(self.parent_box)
        self.tidecurvesub.setParentItem(self.parent_box)
        self.flt.setParentItem(self.parent_box)
        self.reject_rect.setParentItem(self.parent_box)
        self.align_start.setParentItem(self.parent_box)
        self.align_line.setParentItem(self.parent_box)

        self.plotlegend.addItem(self.tidecurve, 'Raw')
        self.plotlegend.addItem(self.tidecurvesub, 'Raw Downsampled')
        self.plotlegend.addItem(self.flt, 'Filtered')


    def subscribe_controller(self, controller) -> None:
        self._controller = controller


    def closeEvent(self, e):
        self._controller.handle_close_ui()


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        fNames = e.mimeData().text().strip().replace('file:///', '')
        if fNames:
            self._controller.handle_loadtide(fNames.split('\n'))


    def mousePressEvent(self, e):
        self._controller.handle_mouse_pressed(e)


    def mouseReleaseEvent(self, e):
        self._controller.handle_mouse_released(e)


    def keyPressEvent(self, e):
        self._controller.handle_key_pressed(e)


    def showdoc(self):
        _sender = self.sender().objectName()
        self._controller.handle_showdoc(_sender)


    def editconfig(self):
        self._controller.handle_editconfig()


    def mouse_moved(self, e):
        self._controller.handle_mouse_moved(e)


    def selectfile(self):
        fNames, _ = QFileDialog.getOpenFileNames(self, 'Load tide file',
                                                 f'{self._controller._LASTFOLDER}',
                                               'ASCII tide files (*.*)')
        if fNames:
            self._controller.handle_loadtide(fNames)


    def savetide_btn_pressed(self):
        fName, _ = QFileDialog.getSaveFileName(self, 'Export filtered tide',
                                               f'{self._controller._LASTFOLDER}',
                                               'csv file (*.csv);;All Files (*.*)')
        if fName:
            self._controller.handle_savetide(fName)


    def stz_val_changed(self):
        _downrate = self.sp_subsample.value()
        _zshift = float(self.le_zshift.text())
        _tshift = int(self.le_tshift.text())
        self._controller.stz_tide(_downrate, _zshift, _tshift)


    def setfiltertype(self):
        if self.rb_Gauss.isChecked():
            self.l_filt_parameter.setText('Sigma')
        elif self.rb_FIR.isChecked():
            self.l_filt_parameter.setText('Samples')
        elif self.rb_Median.isChecked():
            self.l_filt_parameter.setText('Kernel')
        elif self.rb_Mean.isChecked():
            self.l_filt_parameter.setText('Window')


    def scale_changed(self):
        _aspect = self.dataplot.getViewBox().getAspectRatio()
        _sender = self.sender().objectName()
        self._controller.handle_scaleview(_aspect, _sender)


    def augment_btn_pressed(self):
        self._controller.handle_augment()


    def align_btn_pressed(self):
        self._controller.handle_align()


    def runfilter_btn_pressed(self):
        self._controller.handle_runfilter()


    def reject_btn_pressed(self):
        self._controller.handle_reject()
