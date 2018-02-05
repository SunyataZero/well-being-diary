import logging

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import wbd.model

NO_ENTRY_CLICKED_INT = -1


class CompositeRemindersWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.last_entry_clicked_id_int = NO_ENTRY_CLICKED_INT

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        self.reminder_list_qlw = QtWidgets.QListWidget()
        vbox.addWidget(self.reminder_list_qlw)
        self.reminder_list_qlw.currentRowChanged.connect(self.on_current_row_changed)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        self.adding_new_reminder_qle = QtWidgets.QLineEdit()
        self.adding_new_reminder_qle.setPlaceholderText("New reminder")
        hbox.addWidget(self.adding_new_reminder_qle)
        self.adding_new_reminder_bn = QtWidgets.QPushButton("Add")
        hbox.addWidget(self.adding_new_reminder_bn)
        self.adding_new_reminder_bn.clicked.connect(self.on_add_new_reminder_button_pressed)

        self.reminder_details_qll = QtWidgets.QLabel()
        vbox.addWidget(self.reminder_details_qll)
        self.reminder_details_qll.setWordWrap(True)
        self.reminder_details_qll.setTextFormat(QtCore.Qt.RichText)

        self.update_gui()

        self.reminder_list_qlw.setCurrentRow(0)

    def on_current_row_changed(self):
        current_row_int = self.reminder_list_qlw.currentRow()
        if current_row_int != -1:
            current_reminder_qli = self.reminder_list_qlw.item(current_row_int)
            customqlabel_widget = self.reminder_list_qlw.itemWidget(current_reminder_qli)
            ###reminder_id_int = current_reminder_qli.data(QtCore.Qt.UserRole)
            reminderm = wbd.model.ReminderM.get(customqlabel_widget.diary_entry_id)
            self.reminder_details_qll.setText("<big>" + reminderm.reminder_str + "</big>")
            # "<b>bold text</b> <i>italics</i> normal text <h2>h2 title text</h2>"

    def on_add_new_reminder_button_pressed(self):
        wbd.model.ReminderM.add(self.adding_new_reminder_qle.text(), "-")
        self.adding_new_reminder_qle.clear()
        self.update_gui()
        ## self.reminder_list_qlw.setCurrentRow()

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
        self.right_click_menu.exec_(QtGui.QCursor.pos())

    def on_context_menu_rename(self):
        pass

    def on_context_menu_delete(self):
        message_box_reply = QtWidgets.QMessageBox.question(
            self, "Remove entry?", "Are you sure that you want to remove this entry?"
        )
        if message_box_reply == QtWidgets.QMessageBox.Yes:
            wbd.model.ReminderM.remove(int(self.last_entry_clicked_id_int))
            self.update_gui()
            ### self.context_menu_delete_signal.emit()

    # The same function is used for all the "rows"
    def on_list_row_label_mouse_pressed(self, i_qmouseevent, i_diary_id_it):
        logging.debug("button clicked: " + str(i_qmouseevent.button()))
        logging.debug("diary id: " + str(i_diary_id_it))
        self.last_entry_clicked_id_int = i_diary_id_it

    def update_gui(self):
        self.reminder_list_qlw.clear()
        for reminder in wbd.model.ReminderM.get_all():
            row_item = QtWidgets.QListWidgetItem()
            ##row_item = CustomQListWidgetItem()
            reminder_title_qll = CustomQLabel(reminder.title_str, reminder.id_int)
            ##reminder_title_qll = QtWidgets.QLabel(reminder.title_str)
            reminder_title_qll.mouse_pressed_signal.connect(self.on_list_row_label_mouse_pressed)
            ##row_item.mouse_pressed_signal.connect(self.on_list_row_label_mouse_pressed)
            self.reminder_list_qlw.addItem(row_item)
            self.reminder_list_qlw.setItemWidget(row_item, reminder_title_qll)
            ### row_item.setData(QtCore.Qt.UserRole, reminder.id_int)


class CustomQLabel(QtWidgets.QLabel):
    NO_DIARY_ENTRY_SELECTED = -1  # "static"
    #diary_entry_id = NO_DIARY_ENTRY_SELECTED
    mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_diary_entry_id=NO_DIARY_ENTRY_SELECTED):
        super().__init__(i_text_sg)
        self.diary_entry_id = i_diary_entry_id

    # Overridden
    # Please note that this is the event handler (not an event!)
    def mousePressEvent(self, i_qmouseevent):
        super(CustomQLabel, self).mousePressEvent(i_qmouseevent)
        # -self is automatically sent as the 1st argument
        self.mouse_pressed_signal.emit(i_qmouseevent, self.diary_entry_id)

"""
class CustomQListWidgetItem(QtWidgets.QListWidgetItem):
    NO_DIARY_ENTRY_SELECTED = -1  # "static"
    diary_entry_id = NO_DIARY_ENTRY_SELECTED
    mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_diary_entry_id=NO_DIARY_ENTRY_SELECTED):
        super().__init__()
        self.diary_entry_id = i_diary_entry_id

    # Overridden
    # Please note that this is the event handler (not an event!)
    def itemPressed(self, i_qlistwidgetitem):
        super(CustomQListWidgetItem, self).itemPressed(i_qlistwidgetitem)
        # -self is automatically sent as the 1st argument
        self.mouse_pressed_signal.emit(i_qlistwidgetitem, self.diary_entry_id)
"""
