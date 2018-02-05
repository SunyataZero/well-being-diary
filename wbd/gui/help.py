from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class HelpCompositeWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        helptext_qll = QtWidgets.QLabel("Please select one of the tabs to get access to more of tha application")
        helptext_qll.setWordWrap(True)

        vbox.addWidget(helptext_qll)
