import sched
import threading
import time

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import wbd.model

ID_NOT_SET = -1
BUTTON_WIDTH_IT = 28


class PracticeCompositeWidget(QtWidgets.QWidget):
    time_of_day_state_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.id_it = ID_NOT_SET
        self.scheduler = sched.scheduler(time.time, time.sleep)

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        vbox.setAlignment(QtCore.Qt.AlignTop)

        # ..for details
        ### self.details_ll = QtWidgets.QLabel("-----")
        ### self.details_ll.setWordWrap(True)
        self.question_ll = QtWidgets.QLabel("<h4>Question</h4>")
        vbox.addWidget(self.question_ll)
        self.question_le = QtWidgets.QLineEdit()
        self.question_le.textChanged.connect(self.on_question_text_changed)
        vbox.addWidget(self.question_le)

    def on_time_of_day_statechanged(self, i_new_checked_state):
        self.update_db_time()

    def on_time_of_day_changed(self, i_qtime):
        self.update_db_time()

    def update_db_time(self):
        if self.id_it == ID_NOT_SET:
            return
        qtime = self.time_of_day_timeedit.time()
        if self.time_of_day_active_qcb.checkState() == QtCore.Qt.Checked:
            wbd.model.ReminderM.update_time_of_day(self.id_it, qtime.hour())

            # Set a scheduled task
            practice = wbd.model.ReminderM.get(self.id_it)
            self.set_reminder(qtime.hour(), practice.title)
        else:
            model.ReminderM.update_time_of_day(self.id_it, model.TIME_NOT_SET)
        self.time_of_day_state_changed_signal.emit()

    def set_reminder(self, i_hour_it, i_practice_title_sg):
        self.schedule_thread = threading.Thread(target=self.background_function, args=(i_hour_it, i_practice_title_sg), daemon=True)
        self.schedule_thread.start()

    def background_function(self, i_hour_it, i_practice_title_sg):
        now = time.time()
        reminder_time_qdatetime = QtCore.QDateTime.currentDateTime()
        reminder_time_qdatetime.setTime(QtCore.QTime(i_hour_it, 50))
        reminder_time_in_seconds_it = reminder_time_qdatetime.toMSecsSinceEpoch() / 1000
        logging.debug("reminder_time_in_seconds_it = " + str(reminder_time_in_seconds_it))
        self.scheduler.enterabs(reminder_time_in_seconds_it + 10, 1, self.popup_function, (i_practice_title_sg,))
        # -Several events can be scheduled, (the enterabs function adds an event rather than replacing)
        self.scheduler.run()  # blocking=False

    def popup_function(self, i_string):
        message_box = QtWidgets.QMessageBox.information(None, i_string, (i_string))


    def on_question_text_changed(self):
        if self.id_it == ID_NOT_SET:
            return
        model.ReminderM.update_question_text(
            self.id_it,
            self.question_le.text().strip()
        )

    def change_practice(self, i_practice_id_it):
        self.id_it = i_practice_id_it  # storing the id locally
        self.update_gui()

    def update_gui(self):
        ###time_of_day_cb_was_blocked_bl = self.time_of_day_active_qcb.blockSignals(True)
        ###time_of_day_timeedit_was_blocked_bl = self.time_of_day_timeedit.blockSignals(True)

        practice = model.ReminderM.get(self.id_it)
        ##self.details_ll.setText(practice.description)
        self.question_le.setText(practice.question)

        ###self.time_of_day_active_qcb.blockSignals(time_of_day_cb_was_blocked_bl)
        ###self.time_of_day_timeedit.blockSignals(time_of_day_timeedit_was_blocked_bl)
