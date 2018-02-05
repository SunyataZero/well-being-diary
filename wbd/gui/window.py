import enum
import sys
import logging

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import wbd.gui.calendar
import wbd.gui.central
import wbd.model
import wbd.gui.questions
import wbd.gui.wisdom
import wbd.wbd_global
import wbd.gui.quotes
import wbd.gui.reminders
import wbd.gui.search_and_tags


class EventSource(enum.Enum):
    undefined = -1
    obs_selection_changed = 1
    obs_current_row_changed = 2
    practice_details = 3
    calendar_selection_changed = 4
    tags = 5


class WellBeingWindow(QtWidgets.QMainWindow):
    """
    The main window of the application
    Suffix explanation:
    _w: widget
    _l: layout
    _# (number): The level in the layout stack
    """
    # noinspection PyArgumentList,PyUnresolvedReferences
    def __init__(self):
        super().__init__()

        # Initializing window
        self.setGeometry(40, 30, 1100, 700)
        self.showMaximized()
        if wbd.wbd_global.testing_bool:
            data_storage_str = "{data stored in memory}"
        else:
            data_storage_str = "{data stored on hard drive}"
        self.setWindowTitle(wbd.wbd_global.BWB_APPLICATION_NAME_STR + " ["
                            + wbd.wbd_global.BWB_APPLICATION_VERSION_STR + "] "
                            + data_storage_str)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setStyleSheet("selection-background-color:#72ba5e")
        # self.setStyleSheet("selection-background-color:#72ba5e; font-size:10.5pt")

        # Setup of widgets..
        # ..calendar
        calendar_dock_qdw2 = QtWidgets.QDockWidget("Calendar", self)
        calendar_dock_qdw2.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        calendar_dock_qdw2.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.custom_calendar_w3 = wbd.gui.calendar.CompositeCalendarWidget()
        self.custom_calendar_w3.setFixedHeight(240)
        self.custom_calendar_w3.calendar_widget.selectionChanged.connect(self.on_calendar_selection_changed)
        self.custom_calendar_w3.calendar_widget.currentPageChanged.connect(self.on_calendar_page_changed)
        calendar_dock_qdw2.setWidget(self.custom_calendar_w3)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, calendar_dock_qdw2)
        # ..questions
        self.questions_dock_qw2 = QtWidgets.QDockWidget("Journal Questions", self) # "Daily questions"
        self.questions_dock_qw2.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable)
        self.questions_composite_w3 = wbd.gui.questions.PracticeCompositeWidget()
        self.questions_composite_w3.item_selection_changed_signal.connect(self.on_practice_item_selection_changed)
        self.questions_composite_w3.current_row_changed_signal.connect(self.on_question_current_row_changed)
        self.questions_dock_qw2.setWidget(self.questions_composite_w3)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.questions_dock_qw2)
        # ..central widget (which **holds the diary** etc)
        self.central_widget_w3 = wbd.gui.central.CompositeCentralWidget()
        self.setCentralWidget(self.central_widget_w3)
        self.central_widget_w3.journal_button_toggled_signal.connect(self.update_gui)
        self.central_widget_w3.text_added_to_diary_signal.connect(self.update_gui)

        self.central_widget_w3.diary_widget.context_menu_change_date_signal.connect(
            self.update_gui)
        self.central_widget_w3.diary_widget.context_menu_delete_signal.connect(
            self.update_gui)

        self.central_widget_w3.adding_text_to_diary_textedit_w6.key_press_0_9_for_question_list_signal\
            .connect(self.on_central_key_press_0_9_for_question_list)
        self.central_widget_w3.adding_text_to_diary_textedit_w6.key_press_up_for_question_list_signal\
            .connect(self.on_central_key_press_up_for_question_list)
        self.central_widget_w3.adding_text_to_diary_textedit_w6.key_press_down_for_question_list_signal\
            .connect(self.on_central_key_press_down_for_question_list)

        # ..reminders
        reminders_dock_qw2 = QtWidgets.QDockWidget("Reminders", self)
        self.reminders_composite_w3 = wbd.gui.reminders.CompositeRemindersWidget()
        reminders_dock_qw2.setWidget(self.reminders_composite_w3)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, reminders_dock_qw2)
        reminders_dock_qw2.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        reminders_dock_qw2.setFixedHeight(300)  # TODO: Change to dynamic
        # ..quotes
        quotes_dock_qw2 = QtWidgets.QDockWidget("Quotes", self)
        self.quotes_composite_w3 = wbd.gui.quotes.CompositeQuotesWidget()
        quotes_dock_qw2.setWidget(self.quotes_composite_w3)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, quotes_dock_qw2)
        quotes_dock_qw2.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)
        # ..tags
        tags_dock_qw2 = QtWidgets.QDockWidget("Search and Tags", self)
        self.tags_composite_w3 = wbd.gui.search_and_tags.SearchAndTagsCompositeWidget()
        self.tags_composite_w3.search_text_changed_signal.connect(self.on_search_text_changed)
        tags_dock_qw2.setWidget(self.tags_composite_w3)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, tags_dock_qw2)
        tags_dock_qw2.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)

        # Creating the menu bar..
        # ..setup of actions
        export_qaction = QtWidgets.QAction("Export", self)
        export_qaction.triggered.connect(wbd.model.export_all)
        exit_qaction = QtWidgets.QAction("Exit", self)
        exit_qaction.triggered.connect(lambda x: sys.exit())
        redraw_qaction = QtWidgets.QAction("Redraw", self)
        redraw_qaction.triggered.connect(self.update_gui)
        about_qaction = QtWidgets.QAction("About", self)
        about_qaction.triggered.connect(self.show_about_box)
        manual_qaction = QtWidgets.QAction("Manual", self)
        backup_qaction = QtWidgets.QAction("Backup db", self)
        backup_qaction.triggered.connect(wbd.model.backup_db_file)
        ### dear_buddha_qaction = QtWidgets.QAction("Prepend diary entries with \"Dear Buddha\"", self)
        ### dear_buddha_qaction.triggered.connect(self.toggle_dear_buddha_text)
        quotes_window_qaction = quotes_dock_qw2.toggleViewAction()
        reminder_window_qaction = reminders_dock_qw2.toggleViewAction()
        # ..adding menu items
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("&File")
        debug_menu = self.menu_bar.addMenu("Debu&g")
        ### tools_menu = self.menu_bar.addMenu("&Tools")
        help_menu = self.menu_bar.addMenu("&Help")
        window_menu = self.menu_bar.addMenu("&Window")
        file_menu.addAction(export_qaction)
        file_menu.addAction(backup_qaction)
        file_menu.addAction(exit_qaction)
        debug_menu.addAction(redraw_qaction)
        ### tools_menu.addAction(dear_buddha_qaction)
        help_menu.addAction(about_qaction)
        help_menu.addAction(manual_qaction)
        window_menu.addAction(quotes_window_qaction)
        window_menu.addAction(reminder_window_qaction)

        quotes_dock_qw2.hide()
        reminders_dock_qw2.hide()

        self.update_gui()

        """
        # ..practice details
        practice_details_dock_qw2 = QtWidgets.QDockWidget("Journal Details", self)
        self.practice_details_composite_w3 = bwb_practice_details.PracticeCompositeWidget()
        practice_details_dock_qw2.setWidget(self.practice_details_composite_w3)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, practice_details_dock_qw2)
        self.practice_details_composite_w3.time_of_day_state_changed_signal.connect(
            self.on_practice_details_time_of_day_state_changed)
        """
        # ..quotes
        # TODO: A stackedwidget, perhaps with two arrows above for going back and fwd (or just one to switch randomly)
        """
        # ..help
        help_dock_qw2 = QtWidgets.QDockWidget("Help", self)
        self.help_composite_w3 = bwb_help.HelpCompositeWidget()
        help_dock_qw2.setWidget(self.help_composite_w3)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, help_dock_qw2)
        """
        # ..wisdom
        """
        wisdom_dock_qw2 = QtWidgets.QDockWidget("Wisdom", self)
        self.wisdom_composite_w3 = wbd.wisdom.WisdomCompositeWidget()
        wisdom_dock_qw2.setWidget(self.wisdom_composite_w3)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, wisdom_dock_qw2)
        wisdom_dock_qw2.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        wisdom_dock_qw2.hide()
        """
        """
        # ..image
        image_qll = QtWidgets.QLabel()
        image_qll.setPixmap(QtGui.QPixmap("Gerald-G-Yoga-Poses-stylized-1-300px-CC0.png"))
        image_dock_qw2 = QtWidgets.QDockWidget("Image", self)
        image_dock_qw2.setWidget(image_qll)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, image_dock_qw2)
        """

    def on_search_text_changed(self):
        self.update_gui(EventSource.tags)

    def on_central_key_press_0_9_for_question_list(self, i_int):
        logging.debug("Entered on_central_key_press_for_question_list")
        self.questions_composite_w3.list_widget.setCurrentRow(i_int)

    def on_central_key_press_up_for_question_list(self):
        questions_current_row_int = self.questions_composite_w3.list_widget.currentRow()
        if questions_current_row_int <= 0:
            return
        self.questions_composite_w3.list_widget.setCurrentRow(questions_current_row_int - 1)

    def on_central_key_press_down_for_question_list(self):
        questions_current_row_int = self.questions_composite_w3.list_widget.currentRow()
        if questions_current_row_int >= self.questions_composite_w3.list_widget.count() - 1:
            return
        self.questions_composite_w3.list_widget.setCurrentRow(questions_current_row_int + 1)

    def keyPressEvent(self, iQKeyEvent):
        """
        Important: Some key presses are not captured when focusing on certain widgets. For example
        if the list widget has focus key_up and key_down will be captured by the list widget rather
        than here. However please note that that when using modifiers these will be considered as
        separate from the "plain" pressing of a button, so we can for example use alt+key_up even
        if the widget that has focus is a list widget
        :param iQKeyEvent: 
        :return: 
        """
        logging.debug("keyPressEvent in Main Window")

    def toggle_dear_buddha_text(self):
        old_text_str = self.central_widget_w3.adding_text_to_diary_textedit_w6.toPlainText()
        new_text_str = "Dear Buddha, "
        if old_text_str.startswith(new_text_str):
            new_text_str_length_int = len(new_text_str)
            new_text_str = old_text_str[new_text_str_length_int:]
        self.central_widget_w3.adding_text_to_diary_textedit_w6.setText(new_text_str)

    def on_calendar_selection_changed(self):
        logging.debug("Selected date: " + str(self.custom_calendar_w3.calendar_widget.selectedDate()))
        wbd.wbd_global.active_date_qdate = self.custom_calendar_w3.calendar_widget.selectedDate()
        self.update_gui(EventSource.calendar_selection_changed)

    def on_calendar_page_changed(self):
        wbd.wbd_global.shown_month_1to12_it = self.custom_calendar_w3.calendar_widget.monthShown()
        wbd.wbd_global.shown_year_it = self.custom_calendar_w3.calendar_widget.yearShown()
        self.update_gui(EventSource.calendar_selection_changed)

    def on_practice_details_time_of_day_state_changed(self):
        self.update_gui(EventSource.practice_details)

    def on_question_current_row_changed(self):
        # -"None" cannot be sent using the signal system since it is not an "int"

        if wbd.wbd_global.active_question_id_it is not None:
            question = wbd.model.QuestionM.get(wbd.wbd_global.active_question_id_it)
            self.central_widget_w3.question_title_qll.setText(question.title_str)
            self.central_widget_w3.question_descr_qll.setText(question.question_str)
        else:
            self.central_widget_w3.question_title_qll.setText("<i>title empty</i>")
            self.central_widget_w3.question_descr_qll.setText("<i>descr. empty</i>")

        self.update_gui(EventSource.obs_current_row_changed)

    def on_practice_item_selection_changed(self):
        pass
        ###self.update_gui(EventSource.obs_selection_changed)  # Showing habits for practice etc

    def show_about_box(self):
        message_box = QtWidgets.QMessageBox.about(
            self, "<html>About Buddhist Well-Being",
            ("Concept and programming by _____\n"
            'Photography (for icons) by Torgny Dellsén - <a href="torgnydellsen.zenfolio.com">asdf</a><br>'
            "Software License: GPLv3\n"
            "Photo license: CC BY-SA 4.0"
            "Art license: CC PD</html>")
        )

    def update_gui(self, i_event_source=EventSource.undefined):
        if i_event_source == EventSource.practice_details:
            return
        self.central_widget_w3.update_gui()
        self.custom_calendar_w3.update_gui()
        if i_event_source == EventSource.undefined or i_event_source == EventSource.calendar_selection_changed:
            self.questions_composite_w3.update_gui()
            # -it's important that we don't run this update when other widgets are selected, because
            # then we will loose the selection in the questions list

        if i_event_source != EventSource.tags:
            self.tags_composite_w3.update_gui()
