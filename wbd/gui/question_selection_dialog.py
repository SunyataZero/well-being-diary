
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys
import time
import wbd.model


class QuestionSelectionDialog(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_parent = None):
        super(QuestionSelectionDialog, self).__init__(i_parent)

        vbox = QtWidgets.QVBoxLayout(self)

        self.list_widget = QtWidgets.QListWidget()
        vbox.addWidget(self.list_widget)
        self.populate_list()

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

    def populate_list(self):
        for question in wbd.model.HabitM.get_all():
            ###question_title_qlwi = QtWidgets.QListWidgetItem(question.title_str)
            ###self.list_widget.addItem(question_title_qlwi)

            row_item = QtWidgets.QListWidgetItem()
            question_title_qll = CustomQLabel(question.title_str, question.id_int)
            self.list_widget.addItem(row_item)
            self.list_widget.setItemWidget(row_item, question_title_qll)

    @staticmethod
    def get_question_selection_dialog():
        dialog = QuestionSelectionDialog()
        dialog_result = dialog.exec_()
        question_id_result_int = None
        if dialog_result == QtWidgets.QDialog.Accepted:
            current_item = dialog.list_widget.currentItem()
            custom_label = dialog.list_widget.itemWidget(current_item)
            question_id_result_int = custom_label.question_entry_id
        return question_id_result_int


class CustomQLabel(QtWidgets.QLabel):
    NO_DIARY_ENTRY_SELECTED = -1  # "static"
    question_entry_id = NO_DIARY_ENTRY_SELECTED

    def __init__(self, i_text_sg, i_diary_entry_id=NO_DIARY_ENTRY_SELECTED):
        super().__init__(i_text_sg)
        self.question_entry_id = i_diary_entry_id


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    question_id_result_int = QuestionSelectionDialog.get_question_selection_dialog()
    print("question_id_result_int = " + str(question_id_result_int))
    sys.exit(app.exec_())


