
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys
import time


class DateTimeDialog(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_unix_time_it, i_parent = None):
        super(DateTimeDialog, self).__init__(i_parent)

        vbox = QtWidgets.QVBoxLayout(self)

        self.date_time_edit = QtWidgets.QDateTimeEdit(self)
        self.date_time_edit.setCalendarPopup(True)
        present_qdatetime = QtCore.QDateTime()
        present_qdatetime.setMSecsSinceEpoch(1000 * i_unix_time_it)
        self.date_time_edit.setDateTime(present_qdatetime)
        vbox.addWidget(self.date_time_edit)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

    def get_unix_time(self):
        datetime = self.date_time_edit.dateTime()
        unix_time_it = datetime.toMSecsSinceEpoch() // 1000
        return unix_time_it

    @staticmethod
    def get_date_time_dialog(i_unix_time_it):
        dialog = DateTimeDialog(i_unix_time_it)
        dialog_result = dialog.exec_()
        unix_time = -1
        if dialog_result == QtWidgets.QDialog.Accepted:
            unix_time = dialog.get_unix_time()
        return unix_time

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    result = DateTimeDialog.get_date_time_dialog(time.time())
    sys.exit(app.exec_())
