from src.ui.MenuScreen import MenuScreen
from src.ui.TaskScreen import TaskScreen
from src.ui.ResultsScreen import ResultScreen
from src.ui.LogSelectionScreen import LogSelectionScreen
from src.ui.LogManagingScreen import LogManagingcreen
from kivy.uix.screenmanager import ScreenManager



class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.add_widget(MenuScreen(name='menu'))
        self.add_widget(TaskScreen(name='task'))
        self.add_widget(ResultScreen(name='result'))
        self.add_widget(LogSelectionScreen(name='logs'))
        self.add_widget(LogManagingcreen(name='logs_manager'))