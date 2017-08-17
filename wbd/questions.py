
import logging

import wbd.model
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

import wbd.wbd_global
import wbd.safe_confirmation_dialog


class PracticeCompositeWidget(QtWidgets.QWidget):
    item_selection_changed_signal = QtCore.pyqtSignal()
    current_row_changed_signal = QtCore.pyqtSignal()
    # -Please note: The int that is sent is not the current row number, but instead the id for the question
    new_practice_button_pressed_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.show_archived_questions_bool = False

        self.last_entry_clicked_id_int = wbd.wbd_global.NO_ACTIVE_QUESTION_INT

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        # Creating widgets
        # ..for ten practices (left column)
        ##habits_label = QtWidgets.QLabel("<h3>Journals</h3>")
        ##vbox_l2.addWidget(habits_label)
        self.list_widget = QtWidgets.QListWidget()
        ###self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        vbox_l2.addWidget(self.list_widget)
        self.list_widget.currentRowChanged.connect(self.on_current_row_changed)
        ###self.list_widget.itemPressed.connect(self.on_item_selection_changed)
        # -itemClicked didn't work, unknown why (it worked on the first click but never when running in debug mode)
        # -currentItemChanged cannot be used here since it is activated before the list of selected items is updated
        # ..for adding a new question
        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.adding_new_practice_qle = QtWidgets.QLineEdit()
        self.adding_new_practice_qle.setPlaceholderText("New question")
        hbox_l3.addWidget(self.adding_new_practice_qle)
        self.adding_new_practice_bn = QtWidgets.QPushButton("Add")
        hbox_l3.addWidget(self.adding_new_practice_bn)
        self.adding_new_practice_bn.clicked.connect(self.on_add_new_practice_button_pressed)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.show_archived_qpb = QtWidgets.QPushButton("Show archived")
        hbox_l3.addWidget(self.show_archived_qpb)
        self.show_archived_qpb.setCheckable(True)
        self.show_archived_qpb.toggled.connect(self.on_show_archived_button_toggled)

    def on_show_archived_button_toggled(self, i_new_state_bool):
        self.show_archived_questions_bool = i_new_state_bool
        self.update_gui()

    # noinspection PyUnresolvedReferences
    def contextMenuEvent(self, i_qcontextmenuevent):
        """
        Overridden
        Docs: http://doc.qt.io/qt-5/qwidget.html#contextMenuEvent
        """

        if self.last_entry_clicked_id_int == wbd.wbd_global.NO_ACTIVE_QUESTION_INT:
            return

        self.right_click_menu = QtWidgets.QMenu()

        change_title_action = QtWidgets.QAction("Change title")
        change_title_action.triggered.connect(self.on_context_menu_change_title)
        self.right_click_menu.addAction(change_title_action)

        change_description_action = QtWidgets.QAction("Change question description")
        change_description_action.triggered.connect(self.on_context_menu_change_description)
        self.right_click_menu.addAction(change_description_action)

        if self.show_archived_qpb.isChecked():
            delete_action = QtWidgets.QAction("Delete")
            delete_action.triggered.connect(self.on_context_menu_delete)
            self.right_click_menu.addAction(delete_action)

        if not self.show_archived_qpb.isChecked():
            archive_action = QtWidgets.QAction("Archive")
            archive_action.triggered.connect(self.on_context_menu_archive)
            self.right_click_menu.addAction(archive_action)

        if not self.show_archived_qpb.isChecked():
            move_up_action = QtWidgets.QAction("Move up")
            move_up_action.triggered.connect(self.on_context_menu_move_up)
            self.right_click_menu.addAction(move_up_action)

        if not self.show_archived_qpb.isChecked():
            move_down_action = QtWidgets.QAction("Move down")
            move_down_action.triggered.connect(self.on_context_menu_move_down)
            self.right_click_menu.addAction(move_down_action)

        self.right_click_menu.exec_(QtGui.QCursor.pos())

    def on_context_menu_move_up(self):
        wbd.model.QuestionM.update_active_sort_order_move_up_down(
            self.last_entry_clicked_id_int, wbd.model.MoveDirectionEnum.up)
        self.update_gui()

    def on_context_menu_move_down(self):
        wbd.model.QuestionM.update_active_sort_order_move_up_down(
            self.last_entry_clicked_id_int, wbd.model.MoveDirectionEnum.down)
        self.update_gui()

    def on_context_menu_change_description(self):
        if self.last_entry_clicked_id_int != wbd.wbd_global.NO_ACTIVE_QUESTION_INT:
            question = wbd.model.QuestionM.get(self.last_entry_clicked_id_int)
            text_input_dialog = QtWidgets.QInputDialog()
            new_text_qstring = text_input_dialog.getText(
                self, "Change description dialog", "New description: ", text=question.question_str)
            # -Docs: http://doc.qt.io/qt-5/qinputdialog.html#getText
            if new_text_qstring[0]:
                logging.debug("new_text_qstring = " + str(new_text_qstring))
                wbd.model.QuestionM.update_description(self.last_entry_clicked_id_int, new_text_qstring[0])
                self.update_gui()
            else:
                pass  # -do nothing
        else:
            raise Exception("Should not be possible to get here")

    def on_context_menu_change_title(self):
        if self.last_entry_clicked_id_int != wbd.wbd_global.NO_ACTIVE_QUESTION_INT:
            question = wbd.model.QuestionM.get(self.last_entry_clicked_id_int)
            text_input_dialog = QtWidgets.QInputDialog()
            new_text_qstring = text_input_dialog.getText(
                self, "Rename dialog", "New name: ", text=question.title_str)
            # -Docs: http://doc.qt.io/qt-5/qinputdialog.html#getText
            if new_text_qstring[0]:
                logging.debug("new_text_qstring = " + str(new_text_qstring))
                wbd.model.QuestionM.update_title(self.last_entry_clicked_id_int, new_text_qstring[0])
                self.update_gui()
            else:
                pass  # -do nothing
        else:
            raise Exception("Should not be possible to get here")

    def on_context_menu_archive(self):
        if self.last_entry_clicked_id_int != wbd.wbd_global.NO_ACTIVE_QUESTION_INT:
            message_box_reply = QtWidgets.QMessageBox.question(
                self, "Archive entry?", "Are you sure that you want to archive this entry?"
            )
            if message_box_reply == QtWidgets.QMessageBox.Yes:
                wbd.model.QuestionM.update_archived(int(self.last_entry_clicked_id_int), True)
                self.update_gui()
                ### self.context_menu_delete_signal.emit()
        else:
            raise Exception("Should not be possible to get here")

    def on_context_menu_delete(self):
        if self.last_entry_clicked_id_int != wbd.wbd_global.NO_ACTIVE_QUESTION_INT:
            active_question = wbd.model.QuestionM.get(wbd.wbd_global.active_question_id_it)
            conf_result_bool = wbd.safe_confirmation_dialog.SafeConfirmationDialog.get_safe_confirmation_dialog(
                "Are you sure that you want to remove this entry?<br><i>Please type the name to confirm</i>",
                active_question.title_str
            )

            if conf_result_bool:
                self.list_widget.clearSelection()
                wbd.wbd_global.active_question_id_it = None
                self.current_row_changed_signal.emit()

                wbd.model.QuestionM.remove(int(self.last_entry_clicked_id_int))
                self.update_gui()
                ### self.context_menu_delete_signal.emit()
        else:
            raise Exception("Should not be possible to get here")

    def on_add_new_practice_button_pressed(self):
        text_sg = self.adding_new_practice_qle.text().strip()  # strip is needed to remove a newline at the end (why?)
        if not (text_sg and text_sg.strip()):
            return
        wbd.model.QuestionM.add(text_sg, "long question text")
        self.adding_new_practice_qle.clear()
        self.update_gui()

    def on_practice_new_button_pressed_signal(self, i_practice_text_sg):
        wbd.model.QuestionM.add(i_practice_text_sg, "question unfilled")
        self.update_gui()

    def on_current_row_changed(self):
        ###self.current_row_changed_signal.emit(self.list_widget.currentRow())

        current_row_int = self.list_widget.currentRow()
        # if current_row_int != NO_QUESTION_INT:
        current_question_qli = self.list_widget.item(current_row_int)
        customqlabel_widget = self.list_widget.itemWidget(current_question_qli)
        wbd.wbd_global.active_question_id_it = customqlabel_widget.question_entry_id
        self.current_row_changed_signal.emit()
        # else:
        # pass
        ######wbd.bwbglobal.active_question_id_it = None

    """
    def on_item_selection_changed(self, i_qlistwidget_item):
        logging.debug("self.list_widget.currentRow() = " + str(self.list_widget.currentRow()))

        current_row_it = self.list_widget.currentRow()
        if current_row_it == -1:
            # We might get here when a karma item has been clicked
            return

        self.item_selection_changed_signal.emit()
    """

    # The same function is used for all the "rows"
    def on_list_row_label_mouse_pressed(self, i_qmouseevent, i_diary_id_it):
        logging.debug("button clicked: " + str(i_qmouseevent.button()))
        logging.debug("diary id: " + str(i_diary_id_it))
        self.last_entry_clicked_id_int = i_diary_id_it

    def update_gui(self):
        logging.debug("questions - update_gui() entered")
        current_row_int = self.list_widget.currentRow()
        self.list_widget.clear()
        self.list_widget.clearSelection()

        """
        row_item = QtWidgets.QListWidgetItem()
        self.list_widget.addItem(row_item)
        question_title_qll = CustomQLabel("<i>no question</i>", wbd.bwbglobal.NO_ACTIVE_QUESTION_INT)
        self.list_widget.setItemWidget(row_item, question_title_qll)
        """

        for question in wbd.model.QuestionM.get_all(self.show_archived_questions_bool):
            row_item = QtWidgets.QListWidgetItem()

            question_title_str = question.title_str
            all_for_active_day_list = wbd.model.DiaryEntryM.get_for_question_and_active_day(question.id_int)
            if len(all_for_active_day_list) > 0:
                question_title_str = "<b>" + question.title_str + "</b>"

            question_title_qll = CustomQLabel(question_title_str, question.id_int)
            question_title_qll.mouse_pressed_signal.connect(self.on_list_row_label_mouse_pressed)
            self.list_widget.addItem(row_item)
            self.list_widget.setItemWidget(row_item, question_title_qll)

        ###current_row_signal_was_blocked_bl = self.list_widget.blockSignals(True)
        ###self.list_widget.item(1).setSelected(False)
        ###self.list_widget.setCurrentRow(current_row_int)
        ###self.list_widget.blockSignals(current_row_signal_was_blocked_bl)
        self.list_widget.clearSelection()
        logging.debug("questions - clearselection")


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


