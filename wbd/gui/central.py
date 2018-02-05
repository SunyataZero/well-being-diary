import logging
import wbd.gui.diary
import wbd.model

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

import wbd.wbd_global

ADD_NEW_HEIGHT_IT = 100
JOURNAL_BUTTON_GROUP_ID_INT = 1
NO_DIARY_ENTRY_EDITING_INT = -1
ADD_DIARY_BN_TEXT_STR = "Add new diary entry"
ADD_AND_NEXT_DIARY_BN_TEXT_STR = "Add and next"
EDIT_DIARY_BN_TEXT_STR = "Edit diary entry"
EDIT_AND_NEXT_DIARY_BN_TEXT_STR = "Edit and next"


class CompositeCentralWidget(QtWidgets.QWidget):

    journal_button_toggled_signal = QtCore.pyqtSignal()
    text_added_to_diary_signal = QtCore.pyqtSignal()
    # set_calendar_to_date_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        self.editing_diary_entry_int = NO_DIARY_ENTRY_EDITING_INT

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox_l2)

        hbox_l3 = QtWidgets.QHBoxLayout()
        self.vbox_l2.addLayout(hbox_l3)
        self.view_type_qll = QtWidgets.QLabel()
        hbox_l3.addWidget(self.view_type_qll)

        hbox_l3.addStretch()
        self.view_radio_qbuttongroup = QtWidgets.QButtonGroup(self)
        # noinspection PyUnresolvedReferences
        self.view_radio_qbuttongroup.buttonToggled.connect(self.on_view_radio_button_toggled)
        self.daily_overview_qrb = QtWidgets.QRadioButton("Daily Overview")
        self.view_radio_qbuttongroup.addButton(
            self.daily_overview_qrb,
            wbd.wbd_global.ViewEnum.daily_overview.value)
        hbox_l3.addWidget(self.daily_overview_qrb)
        self.question_view_qrb = QtWidgets.QRadioButton("Question View")
        hbox_l3.addWidget(self.question_view_qrb)
        self.view_radio_qbuttongroup.addButton(
            self.question_view_qrb,
            wbd.wbd_global.ViewEnum.question_view.value)
        self.search_view_qrb = QtWidgets.QRadioButton("Search")
        self.view_radio_qbuttongroup.addButton(
            self.search_view_qrb,
            wbd.wbd_global.ViewEnum.search_view.value)
        hbox_l3.addWidget(self.search_view_qrb)
        self.lock_view_qpb = QtWidgets.QPushButton("Lock view")
        self.lock_view_qpb.setCheckable(True)
        self.lock_view_qpb.clicked.connect(self.on_lock_view_clicked)
        hbox_l3.addWidget(self.lock_view_qpb)
        self.prev_page_qpb = QtWidgets.QPushButton("<")
        self.prev_page_qpb.setFixedWidth(30)
        self.prev_page_qpb.clicked.connect(self.on_prev_page_button_clicked)
        hbox_l3.addWidget(self.prev_page_qpb)
        self.next_page_qpb = QtWidgets.QPushButton(">")
        self.next_page_qpb.setFixedWidth(30)
        self.next_page_qpb.clicked.connect(self.on_next_page_button_clicked)
        hbox_l3.addWidget(self.next_page_qpb)

        # **Adding the diary list**
        self.diary_widget = wbd.gui.diary.DiaryListCompositeWidget()
        ##diary_widget.add_text_to_diary_button_pressed_signal.connect(self.on_diary_add_entry_button_pressed)
        self.diary_widget.context_menu_change_date_signal.connect(self.on_diary_context_menu_change_date)
        self.diary_widget.context_menu_delete_signal.connect(self.on_diary_context_menu_delete)
        self.diary_widget.diary_entry_left_clicked_signal.connect(self.on_diary_entry_left_clicked)
        self.vbox_l2.addWidget(self.diary_widget)

        # Adding new diary entry..
        adding_area_hbox_l3 = QtWidgets.QHBoxLayout()
        # ..title
        self.question_title_qll = QtWidgets.QLabel()
        self.vbox_l2.addWidget(self.question_title_qll)
        new_font = QtGui.QFont()
        new_font.setPointSize(16)
        self.question_title_qll.setFont(new_font)
        self.question_title_qll.setWordWrap(True)
        # self.question_label.setFixedWidth(200)
        # ..question
        self.question_descr_qll = QtWidgets.QLabel()
        new_font = QtGui.QFont()
        new_font.setPointSize(11)
        self.question_descr_qll.setFont(new_font)
        self.question_descr_qll.setWordWrap(True)
        # self.question_label.setFixedWidth(200)
        self.vbox_l2.addWidget(self.question_descr_qll)
        # ..text input area
        self.adding_text_to_diary_textedit_w6 = CustomQTextEdit(self)
        new_font = QtGui.QFont()
        new_font.setPointSize(12)
        self.adding_text_to_diary_textedit_w6.setFont(new_font)
        self.adding_text_to_diary_textedit_w6.setStyleSheet("background-color:#d0e8c9")
        ###self.adding_text_to_diary_textedit_w6.setText("<i>New diary entry</i>")
        self.adding_text_to_diary_textedit_w6.setFixedHeight(ADD_NEW_HEIGHT_IT)
        adding_area_hbox_l3.addWidget(self.adding_text_to_diary_textedit_w6)
        # .."add new buttons"
        edit_diary_entry_vbox_l4 = QtWidgets.QVBoxLayout()
        ###diary_entry_label = QtWidgets.QLabel("<h4>New diary entry </h4>")
        ###edit_diary_entry_vbox_l4.addWidget(diary_entry_label)
        self.add_bn_w3 = QtWidgets.QPushButton(ADD_DIARY_BN_TEXT_STR)
        self.add_bn_w3.setFixedHeight(50)
        edit_diary_entry_vbox_l4.addWidget(self.add_bn_w3)
        # noinspection PyUnresolvedReferences
        self.add_bn_w3.clicked.connect(self.on_add_text_to_diary_button_clicked)
        self.add_and_next_qbn_w3 = QtWidgets.QPushButton(ADD_AND_NEXT_DIARY_BN_TEXT_STR)
        edit_diary_entry_vbox_l4.addWidget(self.add_and_next_qbn_w3)
        self.cancel_editing_qbn_w3 = QtWidgets.QPushButton("Cancel editing")
        self.cancel_editing_qbn_w3.clicked.connect(self.on_cancel_clicked)
        self.cancel_editing_qbn_w3.hide()
        edit_diary_entry_vbox_l4.addWidget(self.cancel_editing_qbn_w3)
        adding_area_hbox_l3.addLayout(edit_diary_entry_vbox_l4)

        self.vbox_l2.addLayout(adding_area_hbox_l3)

        self.daily_overview_qrb.setChecked(True)

        self.update_gui()

    """
    def update_gui_journal_buttons(self):
        journalm_list = bwb_model.JournalM.get_all()
    """

    def on_lock_view_clicked(self, i_checked: bool):
        wbd.wbd_global.diary_view_locked_bool = i_checked

    def on_cancel_clicked(self):
        self.adding_text_to_diary_textedit_w6.clear()
        self.editing_diary_entry_int = NO_DIARY_ENTRY_EDITING_INT
        self.update_gui()

    def on_diary_entry_left_clicked(self, i_diary_entry_id: int):
        if self.adding_text_to_diary_textedit_w6.toPlainText().strip():
            return  # -we don't want to clear away text that has been entered
        self.editing_diary_entry_int = i_diary_entry_id

        diary_entry = wbd.model.DiaryEntryM.get(i_diary_entry_id)
        self.adding_text_to_diary_textedit_w6.setPlainText(diary_entry.diary_text)

        self.update_gui()  # -so that the button texts are updated

    def on_next_page_button_clicked(self):
        wbd.wbd_global.current_page_number_int += 1
        self.update_gui()

    def on_prev_page_button_clicked(self):
        wbd.wbd_global.current_page_number_int -= 1
        self.update_gui()

    def on_view_radio_button_toggled(self):
        if self.updating_gui_bool:
            return
        wbd.wbd_global.current_page_number_int = 0  # -resetting
        wbd.wbd_global.active_view_viewenum = wbd.wbd_global.ViewEnum(self.view_radio_qbuttongroup.checkedId())
        self.update_gui()

    def on_journal_button_toggled(self):
        wbd.wbd_global.active_question_id_it = self.journal_qbuttongroup.checkedId()
        self.update_gui()
        self.journal_button_toggled_signal.emit()

    def update_gui(self):
        self.updating_gui_bool = True

        if wbd.wbd_global.active_view_viewenum == wbd.wbd_global.ViewEnum.daily_overview:
            self.view_type_qll.setText("<h3>Daily Overview</h3>")
            self.daily_overview_qrb.setChecked(True)
        elif wbd.wbd_global.active_view_viewenum == wbd.wbd_global.ViewEnum.question_view:
            self.view_type_qll.setText("<h3>Question View</h3>")
            self.question_view_qrb.setChecked(True)
        elif wbd.wbd_global.active_view_viewenum == wbd.wbd_global.ViewEnum.search_view:
            self.view_type_qll.setText("<h3>Search View</h3>")
            self.search_view_qrb.setChecked(True)
        else:
            raise Exception("Should not be able to get here")

        if self.editing_diary_entry_int != NO_DIARY_ENTRY_EDITING_INT:
            self.add_bn_w3.setText(EDIT_DIARY_BN_TEXT_STR)
            self.add_and_next_qbn_w3.setText(EDIT_AND_NEXT_DIARY_BN_TEXT_STR)
            self.cancel_editing_qbn_w3.show()
        else:
            self.add_bn_w3.setText(ADD_DIARY_BN_TEXT_STR)
            self.add_and_next_qbn_w3.setText(ADD_AND_NEXT_DIARY_BN_TEXT_STR)
            self.cancel_editing_qbn_w3.hide()

        self.diary_widget.update_gui()

        self.updating_gui_bool = False

    def on_diary_context_menu_change_date(self):
        self.update_gui()
        # TODO: Update the calendar as well

    def on_diary_context_menu_delete(self):
        self.update_gui()
        # TODO: Update the calendar as well

    def on_add_text_to_diary_button_clicked(self):
        self.add_text_to_diary()

    def add_text_to_diary(self):
        notes_sg = self.adding_text_to_diary_textedit_w6.toPlainText().strip()

        if self.editing_diary_entry_int != NO_DIARY_ENTRY_EDITING_INT:
            # -editing a diary entry
            wbd.model.DiaryEntryM.update_note(self.editing_diary_entry_int, notes_sg)
            self.editing_diary_entry_int = NO_DIARY_ENTRY_EDITING_INT
        else:
            # -adding a new diary entry
            if wbd.wbd_global.active_date_qdate == QtCore.QDate.currentDate():
                time_qdatetime = QtCore.QDateTime.currentDateTime()
                unix_time_it = time_qdatetime.toMSecsSinceEpoch() // 1000
            else:
                unix_time_it = wbd.wbd_global.qdate_to_unixtime(wbd.wbd_global.active_date_qdate)
            logging.debug("t_unix_time_it = " + str(unix_time_it))

            wbd.model.DiaryEntryM.add(
                unix_time_it, wbd.model.SQLITE_FALSE,
                notes_sg,
                wbd.wbd_global.active_question_id_it)

        self.adding_text_to_diary_textedit_w6.clear()
        # self.update_gui()
        self.text_added_to_diary_signal.emit()


class CustomQTextEdit(QtWidgets.QPlainTextEdit):
    # -for now only plain text input is used. TODO: Maybe we want the change this in the future
    ref_central = None
    key_press_0_9_for_question_list_signal = QtCore.pyqtSignal(int)
    key_press_up_for_question_list_signal = QtCore.pyqtSignal()
    key_press_down_for_question_list_signal = QtCore.pyqtSignal()

    def __init__(self, i_ref_central):
        super().__init__()
        self.ref_central = i_ref_central

    def keyPressEvent(self, iQKeyEvent):
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            if iQKeyEvent.key() == QtCore.Qt.Key_Enter or iQKeyEvent.key() == QtCore.Qt.Key_Return:
                logging.debug("CtrlModifier + Enter/Return")
                self.ref_central.add_text_to_diary()
                self.key_press_down_for_question_list_signal.emit()
                # -TODO: Change name of signals to focus on goal rather than origin
                return
        elif QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.AltModifier:
            if iQKeyEvent.key() == QtCore.Qt.Key_Down:
                logging.debug("AltModifier + Key_Down")
                self.key_press_down_for_question_list_signal.emit()
                return
            elif iQKeyEvent.key() == QtCore.Qt.Key_Up:
                logging.debug("AltModifier + Key_Up")
                self.key_press_up_for_question_list_signal.emit()
                return
            elif iQKeyEvent.key() >= QtCore.Qt.Key_1 or iQKeyEvent.key() >= QtCore.Qt.Key_9:
                logging.debug("AltModifier + Key_0-9")
                new_row_int = 0
                if iQKeyEvent.key() == QtCore.Qt.Key_1:
                    new_row_int = 0
                elif iQKeyEvent.key() == QtCore.Qt.Key_2:
                    new_row_int = 1
                elif iQKeyEvent.key() == QtCore.Qt.Key_3:
                    new_row_int = 2
                elif iQKeyEvent.key() == QtCore.Qt.Key_4:
                    new_row_int = 3
                elif iQKeyEvent.key() == QtCore.Qt.Key_5:
                    new_row_int = 4
                elif iQKeyEvent.key() == QtCore.Qt.Key_6:
                    new_row_int = 5
                elif iQKeyEvent.key() == QtCore.Qt.Key_7:
                    new_row_int = 6
                elif iQKeyEvent.key() == QtCore.Qt.Key_8:
                    new_row_int = 7
                elif iQKeyEvent.key() == QtCore.Qt.Key_9:
                    new_row_int = 8
                ### self.questions_composite_w3.list_widget.setCurrentRow(new_row_int)
                self.key_press_0_9_for_question_list_signal.emit(new_row_int)
                return
        elif QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            pass
        else: # -no keyboard modifier
            if iQKeyEvent.key() == QtCore.Qt.Key_Enter or iQKeyEvent.key() == QtCore.Qt.Key_Return:
                # -http://doc.qt.io/qt-5/qguiapplication.html#keyboardModifiers
                # -Please note that the modifiers are placed directly in the QtCore.Qt namespace
                # Alternatively:
                # if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
                # -using bitwise and to find out if the shift key is pressed
                logging.debug("enter or return key pressed in textedit area")
                self.ref_central.add_text_to_diary()
                return

        QtWidgets.QPlainTextEdit.keyPressEvent(self, iQKeyEvent)
        # -if we get here it means that the key has not been captured elsewhere (or possibly
        # (that the key has been captured but that we want "double handling" of the key event)

"""
class CustomPushButton(QtWidgets.QWidget):
    def __init__(self, i_journal_name_str, i_journal_id_int):
        super.__init__(self, i_journal_name_str)
        self.journal_id_it = i_journal_id_int
"""
