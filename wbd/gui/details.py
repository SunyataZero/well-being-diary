import logging
import wbd.model
import re
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import wbd.wbd_global


class CompositeDetailsWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        vbox2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox2)

        self.title_qll = QtWidgets.QLabel()
        vbox2.addWidget(self.title_qll)

        self.qtextedit = QtWidgets.QTextEdit()
        self.qtextedit.setFontPointSize(16)
        self.qtextedit.textChanged.connect(self.on_textedit_changed)
        vbox2.addWidget(self.qtextedit)

        """
        # ..shared info
        self.question_info_shared_qll = QtWidgets.QLabel()
        palette = self.question_info_shared_qll.palette()
        palette.setColor(QtGui.QPalette.Link, QtGui.QColor("#009900"))
        self.question_info_shared_qll.setPalette(palette)
        # self.question_info_shared_qll.setStyleSheet("color: palette(link);")
        self.question_info_shared_qll.linkActivated.connect(self.on_link_activated)
        self.vbox_l2.addWidget(self.question_info_shared_qll)
        self.question_info_shared_qll.setWordWrap(True)
        """


    def question_current_row_changed(self):
        # TODO: Do we want to have this code as part of the update_gui method?

        # -"None" cannot be sent using the signal system since it is not an "int"

        if not wbd.wbd_global.diary_view_locked_bool:
            wbd.wbd_global.active_view_viewenum = wbd.wbd_global.ViewEnum.question_view

        if wbd.wbd_global.active_question_id_it is not None:
            question = wbd.model.QuestionM.get(wbd.wbd_global.active_question_id_it)

            question_str = question.question_str

            self.title_qll.setText('<span style="font-size: 14pt">' + question.title_str + '</span>')

            # new_question_str = wbd.wbd_global.create_links_using_delimiters(question_str, "<", ">")
            new_question_str = re.sub(r'<(.*?)>', r'<a href="\1">\1</a>', question_str)
            logging.debug("new_question_str = " + new_question_str)

            # html_str = ("<span>" + " " + new_question_str + "</span>")
            html_str = new_question_str
            # + " " + re.sub("(<[.]+>)", '<a href="$1>$1</a>', question.question_str)

            self.qtextedit.setText(html_str)

            # TODO: Move this code into the central widget

        else:
            self.question_info_shared_qll.setText("<i>title empty</i>")

    def on_textedit_changed(self):
        wbd.model.QuestionM.update_description(
            wbd.wbd_global.active_question_id_it,
            self.qtextedit.toPlainText()
        )
