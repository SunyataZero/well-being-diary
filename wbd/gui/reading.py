from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

import wbd.model
import wbd.wbd_global


class ReadingWidget(QtWidgets.QWidget):
    search_text_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        self.setMaximumWidth(240)

        vbox1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox1)

        self.view_radio_qbuttongroup = QtWidgets.QButtonGroup(self)
        # noinspection PyUnresolvedReferences
        self.view_radio_qbuttongroup.buttonToggled.connect(self.on_view_radio_button_toggled)
        self.daily_overview_qrb = QtWidgets.QRadioButton("Daily Overview")
        self.view_radio_qbuttongroup.addButton(
            self.daily_overview_qrb,
            wbd.wbd_global.ViewEnum.daily_overview.value)
        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox1.addLayout(hbox_l2)
        hbox_l2.addWidget(self.daily_overview_qrb)
        self.date_selection_qde = QtWidgets.QDateEdit()
        hbox_l2.addWidget(self.date_selection_qde)
        self.question_view_qrb = QtWidgets.QRadioButton("Question View")
        vbox1.addWidget(self.question_view_qrb)
        self.view_radio_qbuttongroup.addButton(
            self.question_view_qrb,
            wbd.wbd_global.ViewEnum.habit_view.value)
        self.search_view_qrb = QtWidgets.QRadioButton("Search")
        self.view_radio_qbuttongroup.addButton(
            self.search_view_qrb,
            wbd.wbd_global.ViewEnum.search_view.value)
        vbox1.addWidget(self.search_view_qrb)

        self.view_type_qll = QtWidgets.QLabel()
        vbox1.addWidget(self.view_type_qll)
        self.lock_view_qpb = QtWidgets.QPushButton("Lock view")
        self.lock_view_qpb.setCheckable(True)
        self.lock_view_qpb.clicked.connect(self.on_lock_view_clicked)
        vbox1.addWidget(self.lock_view_qpb)

        self.daily_overview_qrb.setChecked(True)

        self.search_qle = QtWidgets.QLineEdit()
        self.search_qle.textChanged.connect(self.on_search_text_changed)  # textEdited
        self.search_qle.setPlaceholderText("Search")
        vbox1.addWidget(self.search_qle)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox1.addLayout(hbox_l2)
        hbox_l2.addWidget(QtWidgets.QLabel("Rating"))
        self.rating_qsr = QtWidgets.QSlider()
        self.rating_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.rating_qsr.setMinimum(1)
        self.rating_qsr.setMaximum(3)
        self.rating_qsr.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.rating_qsr.setTickInterval(1)
        self.rating_qsr.setSingleStep(1)
        self.rating_qsr.setPageStep(1)
        hbox_l2.addWidget(self.rating_qsr)

        self.journals_qlw = QtWidgets.QListWidget()
        for journal in wbd.model.JournalM.get_all():
            self.journals_qlw.addItem(journal.title_str)
        vbox1.addWidget(self.journals_qlw)

        """
        # ..column 2
        self.hashtags_composite = TagBoxCompositeWidget("Hashtags", "#")
        vbox1.addWidget(self.hashtags_composite)
        self.hashtags_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)

        # ..calendar
        calendar_dock_qdw2 = QtWidgets.QDockWidget("Calendar", self)
        calendar_dock_qdw2.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        calendar_dock_qdw2.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.custom_calendar_w3 = wbd.gui.calendar.CompositeCalendarWidget()
        self.custom_calendar_w3.setFixedHeight(240)
        self.custom_calendar_w3.calendar_widget.selectionChanged.connect(self.on_calendar_selection_changed)
        # -TODO: Move this into the calendar widget class
        ### self.custom_calendar_w3.calendar_widget.currentPageChanged.connect(self.on_calendar_page_changed)
        calendar_dock_qdw2.setWidget(self.custom_calendar_w3)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, calendar_dock_qdw2)
        """

        # self.custom_calendar_w3.update_gui()

        """
        # Row 1
        hbox2 = QtWidgets.QHBoxLayout()
        vbox1.addLayout(hbox2)
        # ..column 1
        self.joy_composite = TagBoxCompositeWidget("Sources of joy", "[joy]")
        hbox2.addWidget(self.joy_composite)
        self.joy_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        # ..column 2
        self.friends_composite = TagBoxCompositeWidget("Friends (by time)", "@")
        hbox2.addWidget(self.friends_composite)
        self.friends_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        # Row 2
        hbox2 = QtWidgets.QHBoxLayout()
        vbox1.addLayout(hbox2)
        # ..column 1
        self.places_composite = TagBoxCompositeWidget("Places (by time)", "^")
        hbox2.addWidget(self.places_composite)
        self.places_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        # ..column 2
        self.hashtags_composite = TagBoxCompositeWidget("Hashtags", "#")
        hbox2.addWidget(self.hashtags_composite)
        self.hashtags_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        # Row 3
        hbox2 = QtWidgets.QHBoxLayout()
        vbox1.addLayout(hbox2)
        # ..column 1
        self.feelings_composite = TagBoxCompositeWidget("Feelings (pos and neg) (by time)", "*")
        hbox2.addWidget(self.feelings_composite)
        self.feelings_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        # ..column 2
        self.needs_composite = TagBoxCompositeWidget("Needs", "+")
        hbox2.addWidget(self.needs_composite)
        self.needs_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        """


        self.update_gui()

    def on_lock_view_clicked(self, i_checked: bool):
        wbd.wbd_global.diary_view_locked_bool = i_checked

    def on_tags_current_row_changed(self, i_search_text: str):
        self.search_qle.setText(i_search_text)

    def on_search_text_changed(self):
        wbd.wbd_global.active_view_viewenum = wbd.wbd_global.ViewEnum.search_view
        wbd.wbd_global.search_string_str = self.search_qle.text().strip()
        self.search_text_changed_signal.emit()

    def on_view_radio_button_toggled(self):
        if self.updating_gui_bool:
            return
        wbd.wbd_global.current_page_number_int = 0  # -resetting
        wbd.wbd_global.active_view_viewenum = wbd.wbd_global.ViewEnum(self.view_radio_qbuttongroup.checkedId())

        self.update_gui()
        self.search_text_changed_signal.emit()

    def update_gui(self):
        self.updating_gui_bool = True

        if wbd.wbd_global.active_view_viewenum == wbd.wbd_global.ViewEnum.daily_overview:
            self.view_type_qll.setText("<h3>Daily Overview</h3>")
            self.daily_overview_qrb.setChecked(True)
        elif wbd.wbd_global.active_view_viewenum == wbd.wbd_global.ViewEnum.habit_view:
            self.view_type_qll.setText("<h3>Habit View</h3>")
            self.question_view_qrb.setChecked(True)
        elif wbd.wbd_global.active_view_viewenum == wbd.wbd_global.ViewEnum.search_view:
            self.view_type_qll.setText("<h3>Search View</h3>")
            self.search_view_qrb.setChecked(True)
        else:
            raise Exception("Should not be able to get here")

        self.updating_gui_bool = False

        # reading tags from the db
        #self.hashtags_composite.update_gui()
        """
        self.feelings_composite.update_gui()
        self.needs_composite.update_gui()
        self.joy_composite.update_gui()
        self.friends_composite.update_gui()
        self.places_composite.update_gui()
        """


class TagBoxCompositeWidget(QtWidgets.QWidget):
    current_row_changed_signal = QtCore.pyqtSignal(str)

    def __init__(self, i_title: str, i_prefix: str):
        super().__init__()
        # , i_ref_search_qle

        self.prefix_str = i_prefix
        # self.ref_search_qle = i_ref_search_qle

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        self.tags_qll = QtWidgets.QLabel(i_title)
        vbox.addWidget(self.tags_qll)
        self.tags_qlw = QtWidgets.QListWidget()
        vbox.addWidget(self.tags_qlw)
        self.tags_qlw.currentRowChanged.connect(self.on_tags_current_row_changed)

    def on_tags_current_row_changed(self):
        current_row_int = self.tags_qlw.currentRow()
        current_row_qli = self.tags_qlw.item(current_row_int)
        search_text_str = current_row_qli.text() if current_row_qli else None
        # self.ref_search_qle.setText(search_text_str)
        self.current_row_changed_signal.emit(search_text_str)

    def update_gui(self):
        self.tags_qlw.clear()
        self.tags_qlw.addItems(
            [tag for (tag, id_list) in wbd.model.DiaryEntryM.get_all_tags_or_friends(self.prefix_str)]
        )


class CustomQLabel(QtWidgets.QLabel):
    NO_DIARY_ENTRY_SELECTED = -1
    question_entry_id = NO_DIARY_ENTRY_SELECTED  # -"static"
    mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_diary_entry_id=NO_DIARY_ENTRY_SELECTED):
        super().__init__(i_text_sg)
        self.question_entry_id = i_diary_entry_id

    # Overridden
    # Please note that this is the event handler (not an event!)
    def mousePressEvent(self, i_qmouseevent):
        super(CustomQLabel, self).mousePressEvent(i_qmouseevent)
        # -self is automatically sent as the 1st argument
        self.mouse_pressed_signal.emit(i_qmouseevent, self.question_entry_id)

