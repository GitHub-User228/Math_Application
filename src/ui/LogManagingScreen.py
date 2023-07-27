from kivy.graphics import Rectangle
from src.ui.CustomWidgets import Table4 as Table
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from src.ui.CustomWidgets import CustomButton, CustomDropDown
from src.helpers import read_yaml, get_project_dir, os


PATH_TO_SCREEN_BG = os.path.join(get_project_dir(), 'data/images/screen_bg.png')
PATH_TO_CONFIGS = os.path.join(get_project_dir(), 'configs')
CONFIGS_UI = read_yaml(path=PATH_TO_CONFIGS, filename='configs_ui')
SCR_RES = read_yaml(path=PATH_TO_CONFIGS, filename='screen_resolution')
CONFIGS_MODEL = read_yaml(path=PATH_TO_CONFIGS, filename='configs_model')
HEIGHT = SCR_RES['height']
WIDTH = SCR_RES['width']



class LogManagingcreen(Screen):

    def __init__(self, **kwargs):
        super(LogManagingcreen, self).__init__(**kwargs)
        self.size = [WIDTH, HEIGHT]
        self.layout = BoxLayout(orientation='vertical',
                                spacing=0,
                                padding=0,
                                size=self.size,
                                pos=self.pos)

        with self.layout.canvas:
            Rectangle(source=PATH_TO_SCREEN_BG,
                      size=self.size,
                      pos=self.pos)

        # Row 1
        self.row1 = BoxLayout(orientation='horizontal',
                              spacing=0,
                              size_hint_y=CONFIGS_UI['screen']['logs_managing']['fracs'][0])
        self.btn1 = CustomButton(text='Назад')
        self.btn1.background_color = CONFIGS_UI['button']['background_color']['current_screen']
        self.btn2 = CustomButton(text='Действие')
        self.dropdown = CustomDropDown(topics=['Выбрать всё', 'Убрать выделение', 'Удалить'])
        self.btn2.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.btn2, 'text', x))
        self.btn2.background_color = CONFIGS_UI['button']['background_color']['current_screen']
        self.row1.add_widget(self.btn1)
        self.row1.add_widget(self.btn2)
        self.layout.add_widget(self.row1)

        # Row 2
        self.table = None
        self.reset_data()
        self.add_widget(self.layout)
        self.selected = []


    def reset_data(self):
        try:
            self.layout.remove_widget(self.table)
        except:
            pass
        self.table = Table(size_hint_y=CONFIGS_UI['screen']['logs']['fracs'][1])
        self.layout.add_widget(self.table)