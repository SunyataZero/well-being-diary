from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class WisdomCompositeWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.qtreewidget = QtWidgets.QTreeWidget()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.qtreewidget)
        self.setLayout(vbox)

        self.qtreewidget.setColumnCount(2)
        self.qtreewidget.setHeaderLabels(["Wisdom"])
        self.qtreewidget.setItemsExpandable(True)


        growth_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Growth"])
        growth_faith_qtwi = QtWidgets.QTreeWidgetItem(growth_qtwi, ["Faith"])
        growth_virtue_qtwi = QtWidgets.QTreeWidgetItem(growth_qtwi, ["Virtue"])
        growth_generosity_qtwi = QtWidgets.QTreeWidgetItem(growth_qtwi, ["Generosity"])
        growth_wisdom_qtwi = QtWidgets.QTreeWidgetItem(growth_qtwi, ["Wisdom"])

        QtWidgets.QTreeWidgetItem(growth_virtue_qtwi, ["Not to kill"])
        QtWidgets.QTreeWidgetItem(growth_virtue_qtwi, ["Not to steal"])
        QtWidgets.QTreeWidgetItem(growth_virtue_qtwi, ["Avoiding sexual misconduct"])
        QtWidgets.QTreeWidgetItem(growth_virtue_qtwi, ["Not to lie"])
        QtWidgets.QTreeWidgetItem(growth_virtue_qtwi, ["Avoiding intoxicants"])

        QtWidgets.QTreeWidgetItem(growth_wisdom_qtwi, ["Wants to see monks"])
        QtWidgets.QTreeWidgetItem(growth_wisdom_qtwi, ["Wants to hear the good Dharma"])
        QtWidgets.QTreeWidgetItem(growth_wisdom_qtwi, ["Retains in mind the teachings he has heard"])
        QtWidgets.QTreeWidgetItem(growth_wisdom_qtwi,
            ["Examines the meaning of the teachings that have been retained in mind"])
        QtWidgets.QTreeWidgetItem(growth_wisdom_qtwi,
            ["Understands the meaning of the Dharma and then practices in accordance with the Dharma"])




        efforts_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Four Right Efforts"])
        efforts_first_qtwi = QtWidgets.QTreeWidgetItem(efforts_qtwi, ["First"])
        efforts_second_qtwi = QtWidgets.QTreeWidgetItem(efforts_qtwi, ["Second"])

        self.qtreewidget.setItemWidget(efforts_first_qtwi, 1, QtWidgets.QPushButton("Filter"))

        four_est_mindfulness_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Four Est. of Mindfulness"])
        four_est_mindfulness_body_qtwi = QtWidgets.QTreeWidgetItem(four_est_mindfulness_qtwi, ["Body"])
        four_est_mindfulness_feelings_qtwi = QtWidgets.QTreeWidgetItem(four_est_mindfulness_qtwi, ["Feelings"])
        four_est_mindfulness_mind_qtwi = QtWidgets.QTreeWidgetItem(four_est_mindfulness_qtwi, ["Mind"])
        four_est_mindfulness_objects_qtwi = QtWidgets.QTreeWidgetItem(four_est_mindfulness_qtwi, ["Objects of Mind"])

        four_immeasurable_minds_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Four Immeasurable Minds"])
        four_immeasurable_kindness_qtwi = QtWidgets.QTreeWidgetItem(four_immeasurable_minds_qtwi, ["Loving Kindness"])
        four_immeasurable_compassion_qtwi = QtWidgets.QTreeWidgetItem(four_immeasurable_minds_qtwi, ["Compassion"])
        four_immeasurable_joy_qtwi = QtWidgets.QTreeWidgetItem(four_immeasurable_minds_qtwi, ["Sympathetic Joy"])
        four_immeasurable_equanimity_qtwi = QtWidgets.QTreeWidgetItem(four_immeasurable_minds_qtwi, ["Equanimity"])

        noble_eightfold_path_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Noble Eightfold Path"])
        noble_eightfold_path_view_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right View"])
        noble_eightfold_path_thinking_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Thinking"])
        noble_eightfold_path_speech_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Speech"])
        noble_eightfold_path_action_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Action"])
        noble_eightfold_path_livelihood_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Livelihood"])
        noble_eightfold_path_effort_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Effort (Diligence)"])
        noble_eightfold_path_mindfulness_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Mindfulness"])
        noble_eightfold_path_concentration_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Concentration"])

        four_noble_truths_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Four Noble Truths"])
        four_noble_truths_suffering_qtwi = QtWidgets.QTreeWidgetItem(four_noble_truths_qtwi, ["Suffering"])
        four_noble_truths_causes_qtwi = QtWidgets.QTreeWidgetItem(four_noble_truths_qtwi, ["Causes of Suffering"])
        four_noble_truths_cessation_qtwi = QtWidgets.QTreeWidgetItem(four_noble_truths_qtwi, ["Cessation of Suffering"])
        four_noble_truths_path_qtwi = QtWidgets.QTreeWidgetItem(four_noble_truths_qtwi, ["Path to the Cessaction of Suffering"])

        self.qtreewidget.expandAll()
        self.qtreewidget.resizeColumnToContents(0)
        self.qtreewidget.resizeColumnToContents(1)

        self.qtreewidget.collapseItem(growth_virtue_qtwi)
        self.qtreewidget.collapseItem(growth_wisdom_qtwi)

        """
        self.qtoolbox = QtWidgets.QToolBox()

        self.four_noble_truths_qlw = QtWidgets.QListWidget()
        self.four_noble_truths_qlw.addItems(
            ["Suffering", "Causes of Suffering", "Cessation of Suffering", "Path to the Cessaction of Suffering"])
        self.qtoolbox.addItem(self.four_noble_truths_qlw, "Four Noble Truths")

        self.householder_wellbeing_qlw = QtWidgets.QListWidget()
        self.householder_wellbeing_qlw.addItems(["Faith", "Virtue", "Generosity", "Wisdom"])
        self.qtoolbox.addItem(self.householder_wellbeing_qlw, QtGui.QIcon("icon.png"),
            "Spiritual Progress for Householders")

        self.factors_awakening_qlw = QtWidgets.QListWidget()
        self.factors_awakening_qlw.addItems(["Mindfulness", "Investigation of Mind Objects", "Energy",
            "Joy", "Tranquility", "Concentration", "Equanimity"])
        self.qtoolbox.addItem(self.factors_awakening_qlw, "Seven Factors of Awakening")

        self.powers_qlw = QtWidgets.QListWidget()
        self.powers_qlw.addItems(["Faith", "Diligence (Effort)", "Mindfulness",
            "Concentration", "Insight / Understanding / Wisdom"])
        self.qtoolbox.addItem(self.powers_qlw, "<b>Five Powers</b>")
        """


        """
        # ..blessings
        blessings_dock_qw2 = QtWidgets.QDockWidget("Blessings", self)
        self.blessings_qlw = QtWidgets.QListWidget()
        blessings_list = []
        blessings_list.append("Not to associate with fools")
        blessings_list.append("To associate with the wise")
        blessings_list.append("To pay respects where they are due")
        blessings_list.append("To reside in a suitable location")
        blessings_list.append("To have previously done meritorious deeds")
        blessings_list.append("To be heading in the right direction")
        blessings_list.append("To have much learning")
        blessings_list.append("To be skilled and knowledgeable")
        blessings_list.append("To be restrained by a moral code")
        blessings_list.append("To have beautiful speech")
        blessings_list.append("To be a support for your parents")
        blessings_list.append("The cherishing of wife")
        blessings_list.append("The cherishing of children")
        blessings_list.append("To make one's livelihood without difficulty")
        blessings_list.append("To make gifts")
        blessings_list.append("To live in accord with the Dhamma")
        blessings_list.append("To cherish one's relatives")
        blessings_list.append("To do blameless actions")
        blessings_list.append("To cease and abstain from evil")
        blessings_list.append("To refrain from intoxicants")
        blessings_list.append("Not to be heedless of the Dhamma")
        blessings_list.append("To be respectful")
        blessings_list.append("To be humble")
        blessings_list.append("To be content")
        blessings_list.append("To have gratitude")
        blessings_list.append("To hear the Dhamma at the right time")
        blessings_list.append("To have patience")
        blessings_list.append("To be easy to admonish")
        blessings_list.append("The sight of monks")
        blessings_list.append("To discuss the Dhamma at a suitable time")
        blessings_list.append("To practice austerities")
        blessings_list.append("To lead the Holy Life")
        blessings_list.append("Seeing the Noble Truths")
        blessings_list.append("The realization of Nibbana")
        blessings_list.append("A mind unshaken by contact with the world")
        blessings_list.append("Sorrowlessness")
        blessings_list.append("Stainlessness")
        blessings_list.append("Secure")
        self.blessings_qlw.addItems(blessings_list)
        blessings_dock_qw2.setWidget(self.blessings_qlw)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, blessings_dock_qw2)
        """