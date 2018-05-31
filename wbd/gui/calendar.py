from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import wbd.model
import wbd.wbd_global


class CompositeCalendarWidget(QtWidgets.QWidget):
    """
    IMPORTANT:
    At the time of writing the signals
    selectionChanged
    and
    currentPageChanged
    are handled in main_window.py rather than here (this is because it's easier to do, maybe this will be changed later)
    """

    def __init__(self):
        super().__init__()

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        hbox_l3 = QtWidgets.QHBoxLayout()
        self.setLayout(self.vbox_l2)

        self.calendar_widget = QtWidgets.QCalendarWidget()
        self.vbox_l2.addWidget(self.calendar_widget)
        htf = self.calendar_widget.headerTextFormat()
        htf.setFontPointSize(7.0)
        self.calendar_widget.setHeaderTextFormat(htf)
        cf = self.calendar_widget.font()
        cf.setPointSize(7.0)
        self.calendar_widget.setFont(cf)
        self.calendar_widget.setGridVisible(True)

        #if self.calendar_widget is not None:
        #    self.calendar_widget.deleteLater()
        #self.calendar_widget = None
        #self.update_gui()
        #self.calendar_widget.currentPageChanged.connect(self.on_calendar_current_page_changed)
        #self.calendar_widget.selectionChanged.connect(self.on_calendar_selection_changed)

        self.today_qpb = QtWidgets.QPushButton("Today")
        self.vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(self.today_qpb)
        self.today_qpb.clicked.connect(self.on_today_button_clicked)

    def update_gui(self):
        self.calendar_widget.setDateTextFormat(QtCore.QDate(), QtGui.QTextCharFormat())
        # -using the "null date" to clear

        date_qtextcharformat = QtGui.QTextCharFormat()
        date_qtextcharformat.setFontWeight(QtGui.QFont.Bold)
        for diarym in wbd.model.DiaryEntryM.get_all():
            qdatetime = QtCore.QDateTime.fromMSecsSinceEpoch(diarym.date_added_it * 1000)
            self.calendar_widget.setDateTextFormat(qdatetime.date(), date_qtextcharformat)


    """
    def on_calendar_selection_changed(self):
        self.update_gui()
        self.change_signal.emit()

    def on_calendar_current_page_changed(self, i_year_int, i_month_int):
        logging.debug("year: " + str(i_year_int) + " month: " + str(i_month_int))
        self.update_gui()
        self.change_signal.emit()
    """

    def on_today_button_clicked(self):
        self.calendar_widget.setSelectedDate(QtCore.QDate.currentDate())
        """
        if wbd.bwbglobal.active_view_viewenum == wbd.bwbglobal.ViewEnum.diary_daily_overview:
            self.calendar_widget.setSelectedDate(QtCore.QDate.currentDate())
        else:
            self.calendar_widget.showToday()
        """
        self.update_gui()

        # TODO: We may also want to switch to daily overview, alternatively we could
        # 1. change the button when we're in the monthly view or
        # 2. display two buttons, which both changes the view as well as the day/month selected
        # Please note though that there is a difference between the month and day views in that
        # month views are not selecting a month, only viewing

