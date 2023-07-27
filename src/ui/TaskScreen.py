from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from src.helpers import read_yaml, get_project_dir, os
from src.ui.CustomWidgets import CustomButton, CustomLabel1, CustomTextInput1, CustomLabel2


PATH_TO_SCREEN_BG = os.path.join(get_project_dir(), 'data/images/screen_bg.png')
PATH_TO_CONFIGS = os.path.join(get_project_dir(), 'configs')
CONFIGS_UI = read_yaml(path=PATH_TO_CONFIGS, filename='configs_ui')
SCR_RES = read_yaml(path=PATH_TO_CONFIGS, filename='screen_resolution')
CONFIGS_MODEL = read_yaml(path=PATH_TO_CONFIGS, filename='configs_model')
HEIGHT = SCR_RES['height']
WIDTH = SCR_RES['width']



class TaskScreen(Screen):

    def __init__(self, **kwargs):
        super(TaskScreen, self).__init__(**kwargs)
        self.configs = CONFIGS_UI['screen']['task']
        self.size = [WIDTH, HEIGHT]

        self.layout = BoxLayout(orientation='vertical',
                                spacing=self.configs['spacing'],
                                padding=self.configs['padding'],
                                size=self.size,
                                pos=self.pos)
        with self.layout.canvas:
            Rectangle(source=PATH_TO_SCREEN_BG,
                      size=self.size,
                      pos=self.pos)

        # Row 1
        self.row1 = BoxLayout(orientation='horizontal',
                              spacing=self.configs['inner_spacing'][0],
                              size_hint_y=self.configs['fracs'][0])
        self.btn11 = CustomButton(text='Результаты')
        self.btn11.color = CONFIGS_UI['button']['color']['other_screen']
        self.btn12 = CustomButton(text='Меню')
        self.btn12.color = CONFIGS_UI['button']['color']['other_screen']
        self.btn13 = CustomButton(text='Задания')
        self.btn13.background_color = CONFIGS_UI['button']['background_color']['current_screen']
        self.row1.add_widget(self.btn11)
        self.row1.add_widget(self.btn12)
        self.row1.add_widget(self.btn13)
        self.layout.add_widget(self.row1)

        # Row 2 (task counter and timer)
        self.row2 = BoxLayout(orientation='horizontal',
                              spacing=self.configs['inner_spacing'][1],
                              size_hint_y=self.configs['fracs'][1])
        self.label21 = CustomLabel1(text='Задание 0 из 0')
        self.row2.add_widget(self.label21)
        self.label22 = CustomLabel1(text='00:00:00')
        self.row2.add_widget(self.label22)
        self.layout.add_widget(self.row2)

        # Row 3 (task field)
        self.row3 = CustomLabel2(text="",
                                 size_hint_y=self.configs['fracs'][2])
        self.layout.add_widget(self.row3)

        # Row 4 (answer and submission)
        self.row4 = BoxLayout(orientation='horizontal',
                              spacing=self.configs['inner_spacing'][3],
                              size_hint_y=self.configs['fracs'][3])
        self.input = CustomTextInput1(multiline=False,
                                      size_hint_x=self.configs['answer_row_fracs'][0])
        self.row4.add_widget(self.input)
        ## Col 2
        self.btn41 = CustomButton(text='Ответить',
                                  size_hint_x=self.configs['answer_row_fracs'][1])
        self.row4.add_widget(self.btn41)
        ## Col 3
        self.btn42 = CustomButton(text='Cтереть',
                                 size_hint_x=self.configs['answer_row_fracs'][2])
        self.row4.add_widget(self.btn42)
        self.layout.add_widget(self.row4)
        self.add_widget(self.layout)


    def reset_task_ui(self, task, number, n_tasks):
        self.label21.text = f"Заданиe {number} из {n_tasks}"
        self.row3.text = str(task)
        self.input.text = ''