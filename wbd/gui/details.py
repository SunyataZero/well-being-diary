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

        # self.qframe = QtWidgets.QFrame()

        self.qtextedit = QtWidgets.QLabel()
        self.qtextedit.setWordWrap(True)
        new_font = self.qtextedit.font()
        new_font.setPointSize(15)
        self.qtextedit.setFont(new_font)
        self.qtextedit.setFrameStyle(QtWidgets.QFrame.Box)
        self.qtextedit.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        self.qtextedit.setAlignment(QtCore.Qt.AlignTop)
        vbox2.addWidget(self.qtextedit)

        """
        self.qtextedit = QtWidgets.QTextEdit()
        self.qtextedit.setFontPointSize(16)
        # self.qtextedit.textChanged.connect(self.on_textedit_changed)
        self.qtextedit.setReadOnly(True)
        vbox2.addWidget(self.qtextedit)
        """

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
        
            def on_link_activated(self, i_link: str):
        logging.debug("on_link_activated, i_link = " + i_link)
        self.adding_text_to_diary_textedit_w6.appendPlainText(i_link)

        """

    def question_current_row_changed(self):
        # TODO: Do we want to have this code as part of the update_gui method?

        # -"None" cannot be sent using the signal system since it is not an "int"

        if not wbd.wbd_global.diary_view_locked_bool:
            wbd.wbd_global.active_view_viewenum = wbd.wbd_global.ViewEnum.habit_view

        if wbd.wbd_global.active_question_id_it is not None:
            question = wbd.model.HabitM.get(wbd.wbd_global.active_question_id_it)

            description_str = question.description_str

            self.title_qll.setText('<span style="font-size: 14pt">' + question.title_str + '</span>')

            # new_description_str = wbd.wbd_global.create_links_using_delimiters(description_str, "<", ">")
            # new_description_str = re.sub(r'<(.*?)>', r'<a href="\1">\1</a>', description_str)
            new_description_str = description_str
            logging.debug("new_description_str = " + new_description_str)

            # html_str = ("<span>" + " " + new_description_str + "</span>")
            html_str = new_description_str
            # + " " + re.sub("(<[.]+>)", '<a href="$1>$1</a>', question.description_str)

            self.qtextedit.setText(html_str)

            # TODO: Move this code into the central widget

        """
        else:
            self.question_info_shared_qll.setText("<i>title empty</i>")
        """

    def on_textedit_changed(self):
        """
        wbd.model.QuestionM.update_description(
            wbd.wbd_global.active_question_id_it,
            self.qtextedit.toPlainText()
        )
        """
