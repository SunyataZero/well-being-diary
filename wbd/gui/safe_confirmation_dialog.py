
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys
import time


class SafeConfirmationDialog(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_description_str, i_parent = None):
        super(SafeConfirmationDialog, self).__init__(i_parent)

        vbox = QtWidgets.QVBoxLayout(self)

        self.description_qll = QtWidgets.QLabel(i_description_str)
        vbox.addWidget(self.description_qll)

        self.line_edit = QtWidgets.QLineEdit(self)
        vbox.addWidget(self.line_edit)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

    @staticmethod
    def get_safe_confirmation_dialog(i_description_str, i_comparison_str):
        dialog = SafeConfirmationDialog(i_description_str)
        dialog_result = dialog.exec_()
        confirmation_result_bool = False
        if dialog_result == QtWidgets.QDialog.Accepted and dialog.line_edit.text() == i_comparison_str:
            confirmation_result_bool = True
        return confirmation_result_bool


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    confirmation_result_bool = SafeConfirmationDialog.get_safe_confirmation_dialog("experimental description", "asdf")
    print("confirmation_result_bool = " + str(confirmation_result_bool))
    sys.exit(app.exec_())
