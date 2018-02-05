from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

import wbd.model
import wbd.wbd_global


class SearchAndTagsCompositeWidget(QtWidgets.QWidget):
    search_text_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setMaximumWidth(380)

        vbox1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox1)

        self.search_qle = QtWidgets.QLineEdit()
        vbox1.addWidget(self.search_qle)
        self.search_qle.textChanged.connect(self.on_search_text_changed)  # textEdited
        self.search_qle.setPlaceholderText("Search")

        # Row 1
        hbox2 = QtWidgets.QHBoxLayout()
        vbox1.addLayout(hbox2)
        # ..column 1
        self.joy_composite = TagBoxCompositeWidget("Sources of joy", "[joy]")
        hbox2.addWidget(self.joy_composite)
        self.joy_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        # ..column 2
        self.friends_composite = TagBoxCompositeWidget("Friends (by time)", "@")
        hbox2.addWidget(self.friends_composite)
        self.friends_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        # Row 2
        hbox2 = QtWidgets.QHBoxLayout()
        vbox1.addLayout(hbox2)
        # ..column 1
        self.places_composite = TagBoxCompositeWidget("Places (by time)", "^")
        hbox2.addWidget(self.places_composite)
        self.places_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        # ..column 2
        self.hashtags_composite = TagBoxCompositeWidget("Hashtags", "#")
        hbox2.addWidget(self.hashtags_composite)
        self.hashtags_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        # Row 3
        hbox2 = QtWidgets.QHBoxLayout()
        vbox1.addLayout(hbox2)
        # ..column 1
        self.feelings_composite = TagBoxCompositeWidget("Feelings (pos and neg) (by time)", "*")
        hbox2.addWidget(self.feelings_composite)
        self.feelings_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)
        # ..column 2
        self.needs_composite = TagBoxCompositeWidget("Needs", "+")
        hbox2.addWidget(self.needs_composite)
        self.needs_composite.current_row_changed_signal.connect(self.on_tags_current_row_changed)

        self.update_gui()

    def on_tags_current_row_changed(self, i_search_text: str):
        self.search_qle.setText(i_search_text)

    def on_search_text_changed(self):
        wbd.wbd_global.active_view_viewenum = wbd.wbd_global.ViewEnum.search_view
        wbd.wbd_global.search_string_str = self.search_qle.text().strip()
        self.search_text_changed_signal.emit()

    def update_gui(self):
        # reading tags from the db
        self.hashtags_composite.update_gui()
        self.feelings_composite.update_gui()
        self.needs_composite.update_gui()
        self.joy_composite.update_gui()
        self.friends_composite.update_gui()
        self.places_composite.update_gui()


class TagBoxCompositeWidget(QtWidgets.QWidget):
    current_row_changed_signal = QtCore.pyqtSignal(str)

    def __init__(self, i_title: str, i_prefix: str):
        super().__init__()
        # , i_ref_search_qle

        self.prefix_str = i_prefix
        # self.ref_search_qle = i_ref_search_qle

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        self.tags_qll = QtWidgets.QLabel(i_title)
        vbox.addWidget(self.tags_qll)
        self.tags_qlw = QtWidgets.QListWidget()
        vbox.addWidget(self.tags_qlw)
        self.tags_qlw.currentRowChanged.connect(self.on_tags_current_row_changed)

    def on_tags_current_row_changed(self):
        current_row_int = self.tags_qlw.currentRow()
        current_row_qli = self.tags_qlw.item(current_row_int)
        search_text_str = current_row_qli.text()
        # self.ref_search_qle.setText(search_text_str)
        self.current_row_changed_signal.emit(search_text_str)

    def update_gui(self):
        self.tags_qlw.clear()
        self.tags_qlw.addItems(
            [tag for (tag, id_list) in wbd.model.DiaryEntryM.get_all_tags_or_friends(self.prefix_str)]
        )


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

