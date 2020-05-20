from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt

from python.gui.widgets.tabs.dashboard import DashboardTab
from python.gui.widgets.tabs.logtab import LogTab
from python.gui.widgets.tabs.protocoltab import ProgramTab

"""
This script creates a TabManager that manages multiple tabs.

"""


class TabManager(QTabWidget):
    def __init__(self, status_bar):
        super().__init__()
        self.status_bar = status_bar

        self.active_tabs = []
        self.tabs = []
        for i in range(4):
            tab = QWidget()
            tab.layout = QHBoxLayout()
            tab.layout.setAlignment(Qt.AlignCenter)

            if i == 0:
                tab.setObjectName("Dashboard")
                tab1 = DashboardTab(self, tab)
                tab1.setObjectName("Dashboard")
            elif i == 1:
                tab.setObjectName("Log")
                tab1 = LogTab(self, tab)
                tab1.setObjectName("Log")
            else:
                tab.setObjectName(f"Program {i - 1}")
                tab1 = ProgramTab(self, tab)
                tab1.setObjectName(f"Program {i - 1}")
            self.tabs.append(tab1)
            self.addTab(tab, tab1.objectName())

        self.tabBarClicked.connect(lambda: self.check_active_tabs())
            # self.setTabsClosable(True)



    def addprogramtab(self):
        # Check how many ProgramTab are there
        num_ptab = []
        for i in self.tabs:
            if isinstance(i, ProgramTab):
                num_ptab.append(int(i.objectName().split(" ")[-1]))
        num_ptab.sort()
        j = 1
        for i in num_ptab:
            if j == i:
                j += 1
            else:
                break
        name = f"Program {j}"
        tab = QWidget()
        tab.setObjectName(name)
        tab.layout = QHBoxLayout()
        tab.layout.setAlignment(Qt.AlignCenter)
        tab1 = ProgramTab(self, tab)
        tab1.setObjectName(name)
        self.tabs.append(tab1)
        self.insertTab(j + 1, tab, name)  # .addTab(tab, name)

    def check_active_tabs(self):
        self.active_tabs = []
        for tb in self.tabs:
            if isinstance(tb, ProgramTab):
                self.active_tabs.append({tb.objectName(): tb.is_active})
        self.tabs[0].update_active_pgm()

    def reconstruct_program(self, data):
        # Check number of ProgramTabs
        num_pgtab = 0
        for tab in self.tabs:
            if isinstance(tab, ProgramTab):
                num_pgtab += 1
        # add tabs if needed
        for _ in range(len(data) - num_pgtab):
            self.addprogramtab()

        # reconstruct tabs
        for pg in data:
            for tab in self.tabs:
                if isinstance(tab, ProgramTab):
                    if tab.program_log["Program"] == pg["Program"]:
                        for key, val in pg.items():
                            tab.program_log[key] = val
                        tab.reset(tab.program_log)
        self.check_active_tabs()
