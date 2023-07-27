from src.helpers import read_yaml, get_project_dir, os



PATH_TO_SCREEN_BG = os.path.join(get_project_dir(), 'data/images/screen_bg.png')
PATH_TO_CONFIGS = os.path.join(get_project_dir(), 'configs')
CONFIGS_UI = read_yaml(path=PATH_TO_CONFIGS, filename='configs_ui')
SCR_RES = read_yaml(path=PATH_TO_CONFIGS, filename='screen_resolution')
CONFIGS_MODEL = read_yaml(path=PATH_TO_CONFIGS, filename='configs_model')
HEIGHT = SCR_RES['height']
WIDTH = SCR_RES['width']



from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from src.ui.CustomWidgets import CustomButton, CustomDropDown, ConfigsArea, CustomLabelAppName



class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.configs = CONFIGS_UI['screen']['main']
        self.size = [WIDTH, HEIGHT]

        self.layout = BoxLayout(orientation='vertical',
                                 spacing=self.configs['spacing'],
                                 padding=self.configs['padding'],
                                 size=self.size,
                                 pos=self.pos)
        with self.layout.canvas:
            Rectangle(source=PATH_TO_SCREEN_BG,
                      size=self.layout.size,
                      pos=self.layout.pos)

        # Row 1
        self.row1 = BoxLayout(orientation='horizontal',
                              spacing=self.configs['inner_spacing'],
                              size_hint_y=(1-self.configs['configs_area']['frac'])/2)
        self.btn11 = CustomButton(text='Результаты')
        self.btn11.color = CONFIGS_UI['button']['color']['other_screen']
        self.btn12 = CustomButton(text='Меню')
        self.btn12.background_color = CONFIGS_UI['button']['background_color']['current_screen']
        self.btn13 = CustomButton(text='Задания')
        self.btn13.color = CONFIGS_UI['button']['color']['other_screen']
        self.row1.add_widget(self.btn11)
        self.row1.add_widget(self.btn12)
        self.row1.add_widget(self.btn13)
        self.layout.add_widget(self.row1)

        # Row 2
        self.row2 = BoxLayout(orientation='vertical',
                              size_hint_y=self.configs['configs_area']['frac'])
        self.area = ConfigsArea(task='уравнения')
        self.dummy = CustomLabelAppName()
        self.row2.add_widget(self.dummy)
        self.layout.add_widget(self.row2)

        # Row 3
        self.row3 = BoxLayout(orientation='horizontal',
                              spacing=self.configs['inner_spacing'],
                              size_hint_y=(1-self.configs['configs_area']['frac'])/2)
        self.btn31 = CustomButton(text='Тип задания')
        self.dropdown = CustomDropDown()
        self.btn31.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.btn31, 'text', x))
        self.btn32 = CustomButton(text='Настройки')
        self.btn33 = CustomButton(text='Старт')
        self.row3.add_widget(self.btn31)
        self.row3.add_widget(self.btn32)
        self.row3.add_widget(self.btn33)
        self.layout.add_widget(self.row3)
        self.add_widget(self.layout)
