
import logging

import wbd.model
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

import wbd.wbd_global
import wbd.gui.safe_confirmation_dialog


class HabitCompositeWidget(QtWidgets.QWidget):
    item_selection_changed_signal = QtCore.pyqtSignal()
    current_row_changed_signal = QtCore.pyqtSignal()
    new_practice_button_pressed_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.show_archived_questions_bool = False
        self.last_entry_clicked_id_int = wbd.wbd_global.NO_ACTIVE_HABIT_INT
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        # Creating widgets
        # ..for habits
        self.habit_qlw = QtWidgets.QListWidget()
        self.habit_qlw.currentRowChanged.connect(self.on_current_row_changed)
        vbox_l2.addWidget(self.habit_qlw)
        ###self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        ###self.list_widget.itemPressed.connect(self.on_item_selection_changed)
        # -itemClicked didn't work, unknown why (it worked on the first click but never when running in debug mode)
        # -currentItemChanged cannot be used here since it is activated before the list of selected items is updated

        # ..for adding a new question
        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.adding_new_practice_qle = QtWidgets.QLineEdit()
        self.adding_new_practice_qle.setPlaceholderText("New habit")
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

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.edit_texts_qpb = QtWidgets.QPushButton()
        self.edit_texts_qpb.setIcon(QtGui.QIcon(wbd.wbd_global.get_icon_path("pencil-2x.png")))
        self.edit_texts_qpb.setToolTip(self.tr("Edit the selected question"))
        self.edit_texts_qpb.clicked.connect(self.on_edit_clicked)
        hbox_l3.addWidget(self.edit_texts_qpb)

        self.move_to_top_qpb = QtWidgets.QPushButton()
        self.move_to_top_qpb.setIcon(QtGui.QIcon(wbd.wbd_global.get_icon_path("data-transfer-upload-2x.png")))
        self.move_to_top_qpb.setToolTip(self.tr("Move the selected breathing phrase to top"))
        #####self.move_to_top_qpb.clicked.connect(self.on_move_to_top_clicked)
        hbox_l3.addWidget(self.move_to_top_qpb)

        self.move_up_qpb = QtWidgets.QPushButton()
        self.move_up_qpb.setIcon(QtGui.QIcon(wbd.wbd_global.get_icon_path("arrow-top-2x.png")))
        self.move_up_qpb.setToolTip(self.tr("Move the selected breathing phrase up"))
        self.move_up_qpb.clicked.connect(self.on_context_menu_move_up)
        hbox_l3.addWidget(self.move_up_qpb)
        self.move_down_qpb = QtWidgets.QPushButton()
        self.move_down_qpb.setIcon(QtGui.QIcon(wbd.wbd_global.get_icon_path("arrow-bottom-2x.png")))
        self.move_down_qpb.setToolTip(self.tr("Move the selected breathing phrase down"))
        self.move_down_qpb.clicked.connect(self.on_context_menu_move_down)
        hbox_l3.addWidget(self.move_down_qpb)
        hbox_l3.addStretch(1)

        self.archive_phrase_qpb = QtWidgets.QPushButton()
        self.archive_phrase_qpb.setIcon(QtGui.QIcon(wbd.wbd_global.get_icon_path("box-2x.png")))
        self.archive_phrase_qpb.setToolTip(self.tr("Archive the selected question"))
        self.archive_phrase_qpb.clicked.connect(self.on_context_menu_archive)
        hbox_l3.addWidget(self.archive_phrase_qpb)

        self.delete_phrase_qpb = QtWidgets.QPushButton()
        self.delete_phrase_qpb.setIcon(QtGui.QIcon(wbd.wbd_global.get_icon_path("trash-2x.png")))
        self.delete_phrase_qpb.setToolTip(self.tr("Delete the selected breathing phrase"))
        self.delete_phrase_qpb.clicked.connect(self.on_context_menu_delete)
        hbox_l3.addWidget(self.delete_phrase_qpb)

    def on_current_row_changed(self):
        current_row_int = self.habit_qlw.currentRow()
        # if current_row_int != NO_QUESTION_INT:
        current_question_qli = self.habit_qlw.item(current_row_int)
        customqlabel_widget = self.habit_qlw.itemWidget(current_question_qli)
        if customqlabel_widget is not None:
            wbd.wbd_global.active_question_id_it = customqlabel_widget.question_entry_id
            self.current_row_changed_signal.emit()

    def on_edit_clicked(self):
        self.show_edit_dialog()

    def show_edit_dialog(self):
        id_int = wbd.wbd_global.active_question_id_it
        if id_int != wbd.wbd_global.NO_ACTIVE_HABIT_INT:
            self.edit_dialog = EditDialog()
            self.edit_dialog.finished.connect(self.on_edit_dialog_finished)
            self.edit_dialog.show()

    def on_edit_dialog_finished(self, i_result: int):
        if i_result == QtWidgets.QDialog.Accepted:
            # assert mc.mc_global.active_phrase_id_it != wbd.wbd_global.NO_PHRASE_SELECTED_INT
            # question = wbd.model.QuestionM.get(wbd.wbd_global.active_question_id_it)
            wbd.model.HabitM.update_title(
                wbd.wbd_global.active_question_id_it,
                self.edit_dialog.question_title_qle.text()
            )
            if self.edit_dialog.is_sheduled_bool:
                hour_int = self.edit_dialog.hour_qte.time().hour()
            else:
                hour_int = wbd.model.TIME_NOT_SET
            wbd.model.HabitM.update_hour(wbd.wbd_global.active_question_id_it, hour_int)
            plain_text_str = self.edit_dialog.description_qpte.toPlainText()
            wbd.model.HabitM.update_description(
                wbd.wbd_global.active_question_id_it,
                plain_text_str
            )
        else:
            pass
        ### self.phrase_changed_signal.emit(True)
        self.update_gui(True)

    def on_show_archived_button_toggled(self, i_new_state_bool):
        self.show_archived_questions_bool = i_new_state_bool
        self.update_gui()

    def update_db_sort_order_for_all_rows(self):
        logging.debug("update_db_sort_order_for_all_rows")
        i = 0
        while i < self.habit_qlw.count():
            q_list_item_widget = self.habit_qlw.item(i)
            custom_label = self.habit_qlw.itemWidget(q_list_item_widget)
            id_int = custom_label.question_entry_id
            row_int = self.habit_qlw.row(q_list_item_widget)
            wbd.model.HabitM.update_sort_order(
                id_int,
                row_int
            )
            logging.debug("id_int = " + str(id_int) + ", row_int = " + str(row_int))
            i += 1

    def move_current_row_up_down(self, i_move_direction: wbd.wbd_global.MoveDirectionEnum) -> None:
        current_row_int = self.habit_qlw.currentRow()
        current_list_widget_item = self.habit_qlw.item(current_row_int)
        item_widget = self.habit_qlw.itemWidget(current_list_widget_item)
        self.habit_qlw.takeItem(current_row_int)
        # -IMPORTANT: item is removed from list only after the item widget has been extracted.
        #  The reason for this is that if we take the item away from the list the associated
        #  widget (in our case a CustomLabel) will not come with us (which makes sense
        #  if the widget is stored in the list somehow)
        if i_move_direction == wbd.wbd_global.MoveDirectionEnum.up:
            # if main_sort_order_int == 0 or main_sort_order_int > len(QuestionM.get_all()):
            if current_row_int >= 0:
                self.habit_qlw.insertItem(current_row_int - 1, current_list_widget_item)
                self.habit_qlw.setItemWidget(current_list_widget_item, item_widget)
                self.habit_qlw.setCurrentRow(current_row_int - 1)
        elif i_move_direction == wbd.wbd_global.MoveDirectionEnum.down:
            # if main_sort_order_int < 0 or main_sort_order_int >= len(QuestionM.get_all()):
            if current_row_int < self.habit_qlw.count():
                self.habit_qlw.insertItem(current_row_int + 1, current_list_widget_item)
                self.habit_qlw.setItemWidget(current_list_widget_item, item_widget)
                self.habit_qlw.setCurrentRow(current_row_int + 1)

        self.update_db_sort_order_for_all_rows()

    """
            row_item = QtWidgets.QListWidgetItem()

            question_title_str = question.title_str
            all_for_active_day_list = wbd.model.DiaryEntryM.get_for_question_and_active_day(question.id_int)
            if len(all_for_active_day_list) > 0:
                question_title_str = "<b>" + question.title_str + "</b>"

            question_title_qll = CustomQLabel(question_title_str, question.id_int)
            question_title_qll.mouse_pressed_signal.connect(
                self.on_list_row_label_mouse_pressed
            )
            self.list_widget.addItem(row_item)
            self.list_widget.setItemWidget(row_item, question_title_qll)

    """

    # noinspection PyUnresolvedReferences
    def contextMenuEvent(self, i_qcontextmenuevent):
        """
        Overridden
        Docs: http://doc.qt.io/qt-5/qwidget.html#contextMenuEvent
        """

        if self.last_entry_clicked_id_int == wbd.wbd_global.NO_ACTIVE_HABIT_INT:
            return

        self.right_click_menu = QtWidgets.QMenu()

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
        """
        wbd.model.QuestionM.update_active_sort_order_move_up_down(
            self.last_entry_clicked_id_int, wbd.model.MoveDirectionEnum.up)
        """
        self.move_current_row_up_down(wbd.wbd_global.MoveDirectionEnum.up)
        self.update_gui()

    def on_context_menu_move_down(self):
        """
        wbd.model.QuestionM.update_active_sort_order_move_up_down(
            self.last_entry_clicked_id_int, wbd.model.MoveDirectionEnum.down)
        """
        self.move_current_row_up_down(wbd.wbd_global.MoveDirectionEnum.down)
        self.update_gui()

    def on_context_menu_archive(self):
        if not self.show_archived_qpb.isChecked():
            if self.last_entry_clicked_id_int != wbd.wbd_global.NO_ACTIVE_HABIT_INT:
                message_box_reply = QtWidgets.QMessageBox.question(
                    self, "Archive entry?", "Are you sure that you want to archive this entry?"
                )
                if message_box_reply == QtWidgets.QMessageBox.Yes:
                    wbd.model.HabitM.update_archived(int(self.last_entry_clicked_id_int), True)
                    self.update_gui()
                    ### self.context_menu_delete_signal.emit()
            else:
                raise Exception("Should not be possible to get here")
        else:
            message_box_reply = QtWidgets.QMessageBox.question(
                self, "Un-archive entry?", "Are you sure that you want to un-archive this entry?"
            )
            if message_box_reply == QtWidgets.QMessageBox.Yes:
                wbd.model.HabitM.update_archived(int(self.last_entry_clicked_id_int), False)
                self.update_gui()

    def on_context_menu_delete(self):
        if self.last_entry_clicked_id_int != wbd.wbd_global.NO_ACTIVE_HABIT_INT:
            active_question = wbd.model.HabitM.get(wbd.wbd_global.active_question_id_it)
            conf_result_bool = wbd.gui.safe_confirmation_dialog.SafeConfirmationDialog.get_safe_confirmation_dialog(
                "Are you sure that you want to remove this entry?<br><i>Please type the name to confirm</i>",
                active_question.title_str
            )

            if conf_result_bool:
                self.habit_qlw.clearSelection()
                wbd.wbd_global.active_question_id_it = wbd.wbd_global.NO_ACTIVE_HABIT_INT
                self.current_row_changed_signal.emit()

                wbd.model.HabitM.remove(self.last_entry_clicked_id_int)
                self.update_gui()
                ### self.context_menu_delete_signal.emit()
        else:
            raise Exception("Should not be possible to get here")

    def on_add_new_practice_button_pressed(self):
        text_sg = self.adding_new_practice_qle.text().strip()  # strip is needed to remove a newline at the end (why?)
        if not (text_sg and text_sg.strip()):
            return
        wbd.wbd_global.active_question_id_it = wbd.model.HabitM.add(text_sg, "")

        self.adding_new_practice_qle.clear()
        self.update_gui()

        self.show_edit_dialog()

    # The same function is used for all the "rows"
    def on_list_row_label_mouse_pressed(self, i_qmouseevent, i_diary_id_it):
        logging.debug("button clicked: " + str(i_qmouseevent.button()))
        logging.debug("diary id: " + str(i_diary_id_it))
        self.last_entry_clicked_id_int = i_diary_id_it

    def update_gui(self, i_reset_current_row:bool=False):
        logging.debug("questions - update_gui() entered")

        self.habit_qlw.clear()
        self.habit_qlw.clearSelection()

        for question in wbd.model.HabitM.get_all(self.show_archived_questions_bool):
            row_item = QtWidgets.QListWidgetItem()

            question_title_str = question.title_str
            if question.hour_int != wbd.model.TIME_NOT_SET:
                hour_str = str(question.hour_int).zfill(2)
                question_title_str = "[" + hour_str + "] " + question_title_str
            all_for_active_day_list = wbd.model.DiaryEntryM.get_for_question_and_active_day(question.id_int)
            if len(all_for_active_day_list) > 0:
                question_title_str = "<b>" + question_title_str + "</b>"

            question_title_qll = CustomQLabel(question_title_str, question.id_int)
            question_title_qll.mouse_pressed_signal.connect(
                self.on_list_row_label_mouse_pressed
            )

            self.habit_qlw.addItem(row_item)
            self.habit_qlw.setItemWidget(row_item, question_title_qll)

            if i_reset_current_row and wbd.wbd_global.active_question_id_it == question.id_int:
                self.habit_qlw.setCurrentItem(row_item)


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


class EditDialog(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_parent=None):
        super(EditDialog, self).__init__(i_parent)

        self.setModal(True)

        self.setMinimumWidth(400)
        self.setMinimumHeight(600)

        self.updating_gui_bool = False

        """
        # If a phrase is not selected, default to phrase with id 1
        if mc.mc_global.active_phrase_id_it == mc.mc_global.NO_PHRASE_SELECTED_INT:
            mc.mc_global.active_phrase_id_it = 1
        """

        question = wbd.model.HabitM.get(wbd.wbd_global.active_question_id_it)
        self.is_sheduled_bool = question.hour_int != wbd.model.TIME_NOT_SET

        vbox = QtWidgets.QVBoxLayout(self)
        spacing_int = 20

        vbox.addWidget(QtWidgets.QLabel(self.tr("Title")))
        self.question_title_qle = QtWidgets.QLineEdit()
        vbox.addWidget(self.question_title_qle)
        vbox.addSpacing(spacing_int)

        vbox.addWidget(QtWidgets.QLabel(self.tr("Description")))
        self.description_qpte = QtWidgets.QPlainTextEdit()
        self.description_qpte.setPlaceholderText("Please enter a description")
        vbox.addWidget(self.description_qpte)

        # descr_help_str = """You can enclose text inside < and > to make it clickable """
        """so that it is added to the edit area when clicking it"""
        # self.description_help_qll = QtWidgets.QLabel(descr_help_str)
        # self.description_help_qll.setWordWrap(True)
        # vbox.addWidget(self.description_help_qll)

        vbox.addSpacing(spacing_int)

        self.is_scheduled_qcb = QtWidgets.QCheckBox("Scheduled")
        self.is_scheduled_qcb.toggled.connect(self.on_is_scheduled_toggled)
        vbox.addWidget(self.is_scheduled_qcb)

        vbox.addWidget(QtWidgets.QLabel(self.tr("Hour")))
        self.hour_qte = QtWidgets.QTimeEdit()
        vbox.addWidget(self.hour_qte)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

        self.update_gui()

    def on_is_scheduled_toggled(self, i_checked: bool):
        self.is_sheduled_bool = i_checked
        self.update_gui_hour_details()

    def update_gui_hour_details(self):
        question = wbd.model.HabitM.get(wbd.wbd_global.active_question_id_it)
        self.hour_qte.setEnabled(self.is_sheduled_bool)
        if self.is_sheduled_bool:
            qtime = QtCore.QTime(question.hour_int, 0)
            self.hour_qte.setTime(qtime)

    def update_gui(self):
        self.updating_gui_bool = True

        question = wbd.model.HabitM.get(wbd.wbd_global.active_question_id_it)

        self.question_title_qle.setText(question.title_str)
        self.description_qpte.setPlainText(question.description_str)

        self.is_scheduled_qcb.setChecked(self.is_sheduled_bool)

        self.update_gui_hour_details()

        self.adjustSize()

        self.updating_gui_bool = False


