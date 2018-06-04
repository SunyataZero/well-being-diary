import datetime
import time
import logging
import re

import wbd.gui.date_time_dialog
import wbd.model
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from wbd import wbd_global
import wbd.gui.question_selection_dialog


MY_WIDGET_NAME_STR = "test-name"
BACKGROUND_IMAGE_PATH_STR = "Gerald-G-Yoga-Poses-stylized-1-300px-CC0.png"
#"Gerald-G-Yoga-Poses-stylized-CC0.svg"
NO_ENTRY_CLICKED_INT = -1


# noinspection PyArgumentList
class DiaryListCompositeWidget(QtWidgets.QWidget):
    """
    Inspiration for this class:
    http://stackoverflow.com/questions/20041385/python-pyqt-setting-scroll-area
    """

    context_menu_change_date_signal = QtCore.pyqtSignal()
    context_menu_delete_signal = QtCore.pyqtSignal()
    diary_entry_left_clicked_signal = QtCore.pyqtSignal(int)

    last_entry_clicked_id_it = NO_ENTRY_CLICKED_INT

    def __init__(self):
        super().__init__()

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        self.scroll_area_w3 = QtWidgets.QScrollArea()
        self.scroll_area_w3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area_w3.setWidgetResizable(True)
        self.scroll_area_w3.verticalScrollBar().rangeChanged.connect(self.move_scrollbar_to_bottom)
        self.scroll_list_widget_w4 = QtWidgets.QWidget()
        self.scroll_list_widget_w4.setObjectName(MY_WIDGET_NAME_STR)
        self.scroll_list_widget_w4.setStyleSheet("#" + MY_WIDGET_NAME_STR
                                                 + "{" + "background-image:url(\"" + wbd.wbd_global.background_image_path
                                                 + "\"); background-position:center; background-repeat:no-repeat" + "}")
        self.scroll_list_vbox_l5 = QtWidgets.QVBoxLayout()

        self.scroll_list_widget_w4.setLayout(self.scroll_list_vbox_l5)
        self.scroll_area_w3.setWidget(self.scroll_list_widget_w4)
        self.vbox_l2.addWidget(self.scroll_area_w3)
        self.setLayout(self.vbox_l2)

    def move_scrollbar_to_bottom(self, i_min_int, i_max_int):
        # -we must wait for rangeChange, before calling setValue. rangeChange is the signal that this
        # (move_scrollbar_to_bottom) method is connected to
        self.scroll_area_w3.verticalScrollBar().setValue(i_max_int)

    # The same function is used for all the "rows"
    def on_custom_label_mouse_pressed(self, i_qmouseevent, i_diary_id_it):
        logging.debug("button clicked: " + str(i_qmouseevent.button()))
        logging.debug("diary id: " + str(i_diary_id_it))
        self.last_entry_clicked_id_it = i_diary_id_it
        if i_qmouseevent.button() == QtCore.Qt.LeftButton:
            self.diary_entry_left_clicked_signal.emit(i_diary_id_it)

    # noinspection PyUnresolvedReferences
    def contextMenuEvent(self, i_qcontextmenuevent):
        """
        Overridden
        Docs: http://doc.qt.io/qt-5/qwidget.html#contextMenuEvent
        """
        self.right_click_menu = QtWidgets.QMenu()

        rename_action = QtWidgets.QAction("Rename")
        rename_action.triggered.connect(self.on_context_menu_rename)
        self.right_click_menu.addAction(rename_action)

        delete_action = QtWidgets.QAction("Delete")
        delete_action.triggered.connect(self.on_context_menu_delete)
        self.right_click_menu.addAction(delete_action)

        change_date_action = QtWidgets.QAction("Change date")
        change_date_action.triggered.connect(self.on_context_menu_change_date)
        self.right_click_menu.addAction(change_date_action)

        toggle_favorite_action = QtWidgets.QAction("Toggle favorite")
        toggle_favorite_action.triggered.connect(self.on_context_menu_toggle_favorite)
        self.right_click_menu.addAction(toggle_favorite_action)

        change_question_action = QtWidgets.QAction("Change question")
        change_question_action.triggered.connect(self.on_context_menu_change_question)
        self.right_click_menu.addAction(change_question_action)

        clear_question_action = QtWidgets.QAction("Clear question")
        clear_question_action.triggered.connect(self.on_context_menu_clear_question)
        self.right_click_menu.addAction(clear_question_action)

        self.right_click_menu.exec_(QtGui.QCursor.pos())

    def on_context_menu_clear_question(self):
        wbd.model.DiaryEntryM.clear_question(int(self.last_entry_clicked_id_it))
        self.update_gui()

    def on_context_menu_change_question(self):
        question_id_result_int = wbd.gui.question_selection_dialog.QuestionSelectionDialog.get_question_selection_dialog()
        if question_id_result_int is not None:
            wbd.model.DiaryEntryM.update_question(int(self.last_entry_clicked_id_it), question_id_result_int)
            self.update_gui()
        else:
            pass  # -do nothing

    def on_context_menu_delete(self):
        message_box_reply = QtWidgets.QMessageBox.question(
            self, "Remove diary entry?", "Are you sure that you want to remove this diary entry?"
        )
        if message_box_reply == QtWidgets.QMessageBox.Yes:
            wbd.model.DiaryEntryM.remove(int(self.last_entry_clicked_id_it))
            self.update_gui()
            self.context_menu_delete_signal.emit()
        else:
            pass  # -do nothing

    def on_context_menu_rename(self):
        last_clicked_row_dbkey_it = int(self.last_entry_clicked_id_it)
        diary_entry = wbd.model.DiaryEntryM.get(last_clicked_row_dbkey_it)
        text_input_dialog = QtWidgets.QInputDialog()
        new_text_qstring = text_input_dialog.getText(
            self, "Rename dialog", "New name: ", text=diary_entry.diary_text)
        # -Docs: http://doc.qt.io/qt-5/qinputdialog.html#getText
        if new_text_qstring[0]:
            logging.debug("new_text_qstring = " + str(new_text_qstring))
            wbd.model.DiaryEntryM.update_note(last_clicked_row_dbkey_it, new_text_qstring[0])
            self.update_gui()
        else:
            pass  # -do nothing

    def on_context_menu_change_date(self):
        last_clicked_row_dbkey_it = int(self.last_entry_clicked_id_it)
        diary_item = wbd.model.DiaryEntryM.get(last_clicked_row_dbkey_it)
        updated_time_unix_time_it = wbd.gui.date_time_dialog.DateTimeDialog.get_date_time_dialog(diary_item.date_added_it)
        if updated_time_unix_time_it != -1:
            wbd.model.DiaryEntryM.update_date(diary_item.id, updated_time_unix_time_it)
            self.update_gui()
            self.context_menu_change_date_signal.emit()
        else:
            pass  # -do nothing

    def on_context_menu_toggle_favorite(self):
        last_clicked_row_dbkey_it = int(self.last_entry_clicked_id_it)
        diary_item = wbd.model.DiaryEntryM.get(last_clicked_row_dbkey_it)

        is_favorite_int = diary_item.favorite_it
        logging.debug("is_favorite_int = " + str(is_favorite_int))

        if is_favorite_int == wbd.model.SQLITE_FALSE:
            is_favorite_int = wbd.model.SQLITE_TRUE
        elif is_favorite_int == wbd.model.SQLITE_TRUE:
            is_favorite_int = wbd.model.SQLITE_FALSE
        else:
            raise ValueError("This value should not be possible")

        wbd.model.DiaryEntryM.update_favorite(diary_item.id, is_favorite_int)

        self.context_menu_change_date_signal.emit()
        self.update_gui()

    def update_gui(self):
        clear_widget_and_layout_children(self.scroll_list_vbox_l5)

        diary_list = []
        if wbd_global.active_view_viewenum == wbd_global.ViewEnum.question_view:
            diary_list = wbd.model.DiaryEntryM.get_all_for_question(
                wbd_global.active_question_id_it,
                wbd.wbd_global.current_page_number_int
            )
        elif wbd_global.active_view_viewenum == wbd_global.ViewEnum.daily_overview:
            diary_list = wbd.model.DiaryEntryM.get_all_for_active_day()
        elif wbd_global.active_view_viewenum == wbd_global.ViewEnum.search_view:
            diary_list = wbd.model.DiaryEntryM.get_all_for_search_term(
                wbd.wbd_global.search_string_str,
                wbd.wbd_global.current_page_number_int
            )
        else:
            raise Exception("Can not get here")

        old_date_str = ""
        for diary_entry in diary_list:
            label_text_sg = diary_entry.diary_text.strip()

            hbox_l6 = QtWidgets.QHBoxLayout()
            self.scroll_list_vbox_l5.addLayout(hbox_l6)

            date_string_format_str = "%A"  # -weekday
            if wbd_global.active_view_viewenum == wbd_global.ViewEnum.daily_overview:
                date_string_format_str = "%H:%M"  # -hour, min
            elif diary_entry.date_added_it < time.time() - 60 * 60 * 24 * 7:
                date_string_format_str = "%-d %b"  # - jun 12
            date_str = datetime.datetime.fromtimestamp(diary_entry.date_added_it).strftime(
                date_string_format_str)

            time_qlabel = QtWidgets.QLabel("")
            question_title_sg = ""

            if old_date_str == date_str:
                time_qlabel.setText("")
            elif (is_same_day(diary_entry.date_added_it, time.time())
            and wbd_global.active_view_viewenum != wbd_global.ViewEnum.daily_overview):
                time_qlabel.setText("Today")
            else:
                time_qlabel.setText(date_str)
            old_date_str = date_str

            if wbd_global.active_view_viewenum == wbd_global.ViewEnum.question_view:
                pass
            elif wbd_global.active_view_viewenum == wbd_global.ViewEnum.daily_overview:
                if diary_entry.habit_ref_it != wbd.wbd_global.NO_ACTIVE_HABIT_INT:
                    questionm = wbd.model.HabitM.get(diary_entry.habit_ref_it)
                    question_title_sg = str(questionm.title_str)
                    # left_qlabel = QtWidgets.QLabel(question_title_sg)
                else:
                    pass
            else:
                pass

            hbox_l6.addWidget(time_qlabel, stretch=1)

            formatted_label_text_sg = label_text_sg
            if wbd_global.active_view_viewenum == wbd_global.ViewEnum.search_view:
                formatted_label_text_sg = re.sub("(" + wbd.wbd_global.search_string_str + ")",
                    r"<b>\1</b>", formatted_label_text_sg)
            if question_title_sg:
                formatted_label_text_sg = "<i>" + question_title_sg + " </i>" + formatted_label_text_sg
            formatted_label_text_sg = '<p style="font-size:'\
                + str(wbd.wbd_global.diary_text_size_ft) + 'pt;">'\
                + formatted_label_text_sg + "</p>"
            # -please note that we have to add pt after the number
            # -an alternative way to do this is to use qlabel.setfont
            # -more info here: http://www.qtcentre.org/threads/15175-How-to-change-font-size-in-QLabel(QLabel-created-from-Qdesigner)

            listitem_cqll = CustomQLabel(formatted_label_text_sg, diary_entry.id)
            listitem_cqll.setWordWrap(True)
            if diary_entry.rating_int == wbd.model.SQLITE_TRUE:
                # -TODO: Change to rating 1-3 here
                listitem_cqll.setStyleSheet("background-color:rgba(180,230,180,0.3);")  # #d0e8c9 rgba(0,255,0,0.3);
            listitem_cqll.mouse_pressed_signal.connect(self.on_custom_label_mouse_pressed)
            listitem_cqll.setTextInteractionFlags(
                QtCore.Qt.TextSelectableByMouse
            )

            hbox_l6.addWidget(listitem_cqll, stretch=5)

            hbox_l6.addWidget(QtWidgets.QLabel(""), stretch=1)

        self.scroll_list_vbox_l5.addStretch()


def is_same_day(i_first_date_it, i_second_date_it):
    first_date = datetime.datetime.fromtimestamp(i_first_date_it)
    second_date = datetime.datetime.fromtimestamp(i_second_date_it)
    return first_date.date() == second_date.date()  # - == operator works for "datetime" type


def clear_widget_and_layout_children(qlayout_or_qwidget):
    if qlayout_or_qwidget.widget():
        qlayout_or_qwidget.widget().deleteLater()
    elif qlayout_or_qwidget.layout():
        while qlayout_or_qwidget.layout().count():
            child_qlayoutitem = qlayout_or_qwidget.takeAt(0)
            clear_widget_and_layout_children(child_qlayoutitem)  # Recursive call


class CustomQLabel(QtWidgets.QLabel):
    NO_DIARY_ENTRY_SELECTED = -1
    diary_entry_id = NO_DIARY_ENTRY_SELECTED
    mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_diary_entry_id=NO_DIARY_ENTRY_SELECTED):
        super().__init__(i_text_sg)
        self.diary_entry_id = i_diary_entry_id

    # Overridden
    # Please note that this is the event handler (not an event!)
    def mousePressEvent(self, i_qmouseevent):
        super(CustomQLabel, self).mousePressEvent(i_qmouseevent)
        self.mouse_pressed_signal.emit(i_qmouseevent, self.diary_entry_id)
