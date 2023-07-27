from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from src.helpers import read_yaml, get_project_dir, os


PATH_TO_TTF = os.path.join(get_project_dir(), 'data/ttf')
PATH_TO_CONFIGS = os.path.join(get_project_dir(), 'configs')
CONFIGS_UI = read_yaml(path=PATH_TO_CONFIGS, filename='configs_ui')
SCR_RES = read_yaml(path=PATH_TO_CONFIGS, filename='screen_resolution')
CONFIGS_MODEL = read_yaml(path=PATH_TO_CONFIGS, filename='configs_model')
HEIGHT = SCR_RES['height']
WIDTH = SCR_RES['width']



class CustomButton(Button):
    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.background_color = CONFIGS_UI['button']['background_color']['default']
        self.background_normal = ''
        self.color = CONFIGS_UI['button']['color']['default']
        self.font_name = os.path.join(PATH_TO_TTF, f"{CONFIGS_UI['button']['font_name']}.ttf")
        self.font_size = HEIGHT * CONFIGS_UI['button']['font_size_factor']



class CustomButton2(Button):
    def __init__(self, **kwargs):
        super(CustomButton2, self).__init__(**kwargs)
        self.background_color = CONFIGS_UI['button']['background_color']['if_clicked']
        self.background_normal = ''
        self.color = CONFIGS_UI['button']['color']['default']
        self.font_name = os.path.join(PATH_TO_TTF, f"{CONFIGS_UI['button']['font_name']}.ttf")
        self.font_size = HEIGHT * CONFIGS_UI['button']['font_size_factor']



class CustomButton3(Button):
    def __init__(self, **kwargs):
        super(CustomButton3, self).__init__(**kwargs)
        self.background_color = CONFIGS_UI['button']['background_color']['drop_down']
        self.background_normal = ''
        self.color = CONFIGS_UI['button']['color']['drop_down']
        self.font_name = os.path.join(PATH_TO_TTF, f"{CONFIGS_UI['button']['font_name']}.ttf")
        self.font_size = HEIGHT * CONFIGS_UI['button']['font_size_factor']
        self.height = CONFIGS_UI['button']['height']['drop_down']



class CustomLabelAppName(Label):
    def __init__(self, margin=[0, 0], **kwargs):
        super(CustomLabelAppName, self).__init__(**kwargs)
        self.text = CONFIGS_UI['appname']['text']
        self.color = CONFIGS_UI['appname']['color']
        self.font_name = os.path.join(PATH_TO_TTF, f"{CONFIGS_UI['appname']['font_name']}.ttf")
        self.font_size = HEIGHT * CONFIGS_UI['appname']['font_size_factor']
        self.bg = [0, 0, 0, 0]
        self.margin = margin

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg)
            Rectangle(pos=[a+b for (a,b) in zip(self.pos, self.margin)],
                      size=[a-2*b for (a,b) in zip(self.size, self.margin)])



class CustomLabel1(Label):
    def __init__(self, bg=[0, 0, 0, 0], margin=[0, 0], **kwargs):
        super(CustomLabel1, self).__init__(**kwargs)
        self.color = CONFIGS_UI['label']['color']
        self.font_name = os.path.join(PATH_TO_TTF, f"{CONFIGS_UI['label']['font_name']}.ttf")
        self.font_size = HEIGHT * CONFIGS_UI['label']['font_size_factor']
        self.bg = bg
        self.margin = margin

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg)
            Rectangle(pos=[a+b for (a,b) in zip(self.pos, self.margin)],
                      size=[a-2*b for (a,b) in zip(self.size, self.margin)])



class CustomLabel2(Label):
    def __init__(self, **kwargs):
        super(CustomLabel2, self).__init__(**kwargs)
        self.color = CONFIGS_UI['task_field']['foreground_color']
        self.font_name = os.path.join(PATH_TO_TTF, f"{CONFIGS_UI['task_field']['font_name']}.ttf")
        self.font_size = HEIGHT * CONFIGS_UI['task_field']['font_size_factor']
        self.bg = CONFIGS_UI['task_field']['background_color']

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg)
            Rectangle(pos=self.pos, size=self.size)



class CustomTextInput1(TextInput):
    def __init__(self, **kwargs):
        super(CustomTextInput1, self).__init__(**kwargs)
        self.background_color = CONFIGS_UI['text_input']['background_color']
        self.background_normal = ''
        self.foreground_color = CONFIGS_UI['text_input']['foreground_color']
        self.font_name = os.path.join(PATH_TO_TTF, f"{CONFIGS_UI['text_input']['font_name']}.ttf")
        self.font_size = HEIGHT * CONFIGS_UI['text_input']['font_size_factor']
        self.halign = CONFIGS_UI['text_input']['halign']

    def on_size(self, *args):
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]



class CustomDropDown(DropDown):
    def __init__(self, topics=None, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        if topics is None:
            topics = list(CONFIGS_MODEL.keys())
        self.buttons = dict(zip(topics, [None for _ in topics]))
        for key in self.buttons.keys():
            self.buttons[key] = CustomButton3(text=key, size_hint_y=None)
            self.buttons[key].bind(on_release=self.dismiss)
            self.add_widget(self.buttons[key])



class ConfigsArea(BoxLayout):
    def __init__(self, task, **kwargs):
        super(ConfigsArea, self).__init__(**kwargs)
        self.configs_model = CONFIGS_MODEL[task]
        self.configs = CONFIGS_UI['screen']['main']['configs_area']
        self.orientation = 'vertical'
        self.pos = [CONFIGS_UI['screen']['main']['padding'],
                    CONFIGS_UI['screen']['main']['padding'] + (1-self.configs['frac'])/2 * \
                    (HEIGHT - CONFIGS_UI['screen']['main']['padding']*2)]
        self.size = [WIDTH - CONFIGS_UI['screen']['main']['padding']*2,
                     self.configs['frac'] * (HEIGHT - CONFIGS_UI['screen']['main']['padding']*2)]
        with self.canvas.before:
            Color(*self.configs['background_color'])
            Rectangle(pos=[self.pos[0], self.pos[1]+self.size[1]*2/7],
                      size=[self.size[0], self.size[1]*4/7])

        # Row 1 (empty)
        self.add_widget(Widget())

        # Row 2 (task type)
        self.row2 = BoxLayout(orientation='horizontal', spacing=self.configs['spacing2'])
        self.row2.add_widget(Widget())
        self.task_type = CustomLabel1(text=task)
        self.row2.add_widget(self.task_type)
        self.row2.add_widget(Widget())
        self.add_widget(self.row2)


        # Row 3 (Number of Tasks)
        self.row3 = BoxLayout(orientation='horizontal', spacing=self.configs['spacing1'])
        ## Col 1
        self.label31 = CustomLabel1(text='Кол-во заданий', size_hint_x=self.configs['fracs'][0])
        self.row3.add_widget(self.label31)
        ## Col 2
        self.slider1 = Slider(orientation='horizontal',
                              min=self.configs_model['n_tasks']['min'],
                              max=self.configs_model['n_tasks']['max'],
                              value=self.configs_model['n_tasks']['value'],
                              step=self.configs_model['n_tasks']['step'],
                              size_hint_x=self.configs['fracs'][1])
        self.slider1.fbind('value', self.update_slider1_val)
        self.row3.add_widget(self.slider1)
        ## Col 3
        self.label32 = CustomLabel1(text=str(self.configs_model['n_tasks']['value']),
                                    size_hint_x=self.configs['fracs'][2])
        self.row3.add_widget(self.label32)
        self.add_widget(self.row3)

        # Row 4 (Numbers Range)
        self.row4 = BoxLayout(orientation='horizontal', spacing=self.configs['spacing1'])
        ## Col 1
        self.label41 = CustomLabel1(text='Макс. число', size_hint_x=self.configs['fracs'][0])
        self.row4.add_widget(self.label41)
        ## Col 2
        self.slider2 = Slider(orientation='horizontal',
                              min=self.configs_model['max_number']['min'],
                              max=self.configs_model['max_number']['max'],
                              value=self.configs_model['max_number']['value'],
                              step=self.configs_model['max_number']['step'],
                              size_hint_x=self.configs['fracs'][1])
        self.slider2.fbind('value', self.update_slider2_val)
        self.row4.add_widget(self.slider2)
        ## Col 3
        self.label42 = CustomLabel1(text=str(self.configs_model['max_number']['value']),
                                    size_hint_x=self.configs['fracs'][2])
        self.row4.add_widget(self.label42)
        self.add_widget(self.row4)

        # Row 5 (Complexity)
        self.row5 = BoxLayout(orientation='horizontal', spacing=self.configs['spacing1'])
        ## Col 1
        self.label51 = CustomLabel1(text=self.configs_model['conf3']['name'],
                                    size_hint_x=self.configs['fracs'][0])
        self.row5.add_widget(self.label51)
        ## Col 2
        self.slider3 = Slider(orientation='horizontal',
                              min=self.configs_model['conf3']['min'],
                              max=self.configs_model['conf3']['max'],
                              value=self.configs_model['conf3']['value'],
                              step=self.configs_model['conf3']['step'],
                              size_hint_x=self.configs['fracs'][1])
        self.slider3.fbind('value', self.update_slider3_val)
        self.row5.add_widget(self.slider3)
        ## Col 3
        self.label52 = CustomLabel1(text=str(self.configs_model['conf3']['actual_values'] \
                                                 [self.configs_model['conf3']['value']]),
                                    size_hint_x=self.configs['fracs'][2])
        self.row5.add_widget(self.label52)
        self.add_widget(self.row5)

        # Row 6 (update button)
        self.row6 = BoxLayout(orientation='horizontal', spacing=self.configs['spacing2'])
        self.row6.add_widget(Widget())
        self.btn1 = CustomButton2(text='Применить')
        self.row6.add_widget(self.btn1)
        self.btn2 = CustomButton2(text='Отменить')
        self.row6.add_widget(self.btn2)
        self.row6.add_widget(Widget())
        self.add_widget(self.row6)

        # Row 7 (empty)
        self.add_widget(Widget())



    def update_slider1_val(self, instance, val):
        self.label32.text = str(int(val))


    def update_slider2_val(self, instance, val):
        self.label42.text = str(int(val))


    def update_slider3_val(self, instance, val):
        self.label52.text = str(self.configs_model['conf3']['actual_values'][val])



class Table2(BoxLayout):
    def __init__(self, nrows, data=None, **kwargs):
        super(Table2, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = CONFIGS_UI['table2']['spacing_between']['header_and_items']
        self.padding = (CONFIGS_UI['table2']['padding']['x'],
                        CONFIGS_UI['table2']['padding']['y'],
                        CONFIGS_UI['table2']['padding']['x'],
                        CONFIGS_UI['table2']['padding']['y'])

        ### Header Row
        self.header = BoxLayout(orientation='horizontal',
                                spacing=CONFIGS_UI['table2']['spacing_between']['header_and_items'],
                                size_hint=(1, CONFIGS_UI['table2']['fracs']['header']))
        for k, header in enumerate(['№', 'Время', 'Заданиe|Ответ|Твой ответ']):
            self.header.add_widget(CustomLabel1(text=header,
                                                size_hint_x=CONFIGS_UI['table2']['column_fracs'][k],
                                                bg=CONFIGS_UI['table2']['background_color']['header']))
        self.add_widget(self.header)

        ### Items
        self.items = ScrollView(scroll_type=['content'],
                                size_hint=(1, CONFIGS_UI['table2']['fracs']['items']))

        ### Defining dictionary with items
        if data is not None:
            self.shape = (nrows, len(data))
            self.reset_table_ui(items=data)
        self.add_widget(self.items)


    def reset_table_ui(self, items):
        n_lines = [len(('\n'.join(map(lambda x: f'• {x}', [items[key][it] for key in ['Task',
                                                                                       'Answer',
                                                                                       'YourAnswer']]))).split('\n')) \
                   for it in range(self.shape[0])]
        height_fracs = [CONFIGS_UI['table2']['row_height_default'] + \
                        CONFIGS_UI['table2']['row_height_factor_per_line']*n for n in n_lines]
        self.rows = GridLayout(cols=1, size_hint=(1, None),
                               height=sum(height_fracs)*HEIGHT)
        total = sum(height_fracs)
        height_fracs = [k/total for k in height_fracs]
        for it in range(self.shape[0]):
            row = BoxLayout(orientation='horizontal',
                            spacing=CONFIGS_UI['table2']['spacing_between']['columns'],
                            size_hint=(1, height_fracs[it]))
            bg = CONFIGS_UI['table']['background_color']['item']['correct']
            if items['YourAnswer'][it] != items['Answer'][it]:
                bg = CONFIGS_UI['table']['background_color']['item']['not_correct']

            ### index item
            row.add_widget(CustomLabel1(text=str(items['№'][it]),
                                        size_hint=(CONFIGS_UI['table2']['column_fracs'][0], 1),
                                        bg=CONFIGS_UI['table2']['background_color']['index'],
                                        margin=[0, CONFIGS_UI['table2']['spacing_between']['rows']/2]))
            ### time item
            row.add_widget(CustomLabel1(text=str(items['Time'][it]),
                                        size_hint=(CONFIGS_UI['table2']['column_fracs'][1], 1),
                                        bg=bg,
                                        margin=[0, CONFIGS_UI['table2']['spacing_between']['rows']/2]))
            ### task, answer, true answer
            row.add_widget(CustomLabel1(text='\n'.join(map(lambda x: '• '+str(x.replace("\n", "\n  ")),
                                                           [items[key][it] for key in ['Task',
                                                                                       'Answer',
                                                                                       'YourAnswer']])),
                                        size_hint=(CONFIGS_UI['table2']['column_fracs'][2], 1),
                                        bg=bg,
                                        margin=[0, CONFIGS_UI['table2']['spacing_between']['rows']/2]))
            self.rows.add_widget(row)
        self.items.add_widget(self.rows)



class Table4(BoxLayout):
    def __init__(self, **kwargs):
        super(Table4, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = CONFIGS_UI['table4']['spacing_between']['header_and_items']
        self.padding = (CONFIGS_UI['table4']['padding']['x'],
                        CONFIGS_UI['table4']['padding']['y'],
                        CONFIGS_UI['table4']['padding']['x'],
                        CONFIGS_UI['table4']['padding']['y'])
        ### Loading filenames
        path = 'logs'
        filenames = list(sorted(os.listdir(path), reverse=True))
        converter = dict([(f'{it}', key) for (it, key) in enumerate(CONFIGS_MODEL.keys())])
        files = {'Дата': [f"{filename.split('_')[0]}\n{filename.split('_')[1]}" for  filename in filenames],
                 'Тип': [converter[filename.split('_')[2]] for filename in filenames],
                 'Кол-во': [filename.split('_')[4] for filename in filenames],
                 'Конфигурация': [str(CONFIGS_MODEL[converter[filename.split('_')[2]]]['conf3']['actual_values'] \
                                          [int(filename.split('_')[-1].split('.')[0])]) for filename in filenames],
                 '%': [str(round(int(filename.split('_')[3])/int(filename.split('_')[4])*100)) for filename in filenames],
                 }

        ### Defining the table
        self.headers = list(files.keys())

        ### Header Row
        self.header = BoxLayout(orientation='horizontal',
                                spacing=CONFIGS_UI['table4']['spacing_between']['header_and_items'],
                                size_hint=(1, CONFIGS_UI['table4']['fracs']['header']))
        for k, header in enumerate(self.headers):
            self.header.add_widget(CustomLabel1(text=header,
                                                size_hint_x=CONFIGS_UI['table4']['column_fracs'][k],
                                                bg=CONFIGS_UI['table4']['background_color']['header']))
        self.add_widget(self.header)

        ### Items
        self.items = ScrollView(scroll_type=['content'],
                                size_hint=(1, CONFIGS_UI['table4']['fracs']['items']))

        ### Defining dictionary with items
        self.shape = (len(filenames), len(self.headers))
        self.reset_table_ui(items=files)
        self.add_widget(self.items)


    def reset_table_ui(self, items):
        self.rows = GridLayout(cols=1, size_hint=(1, None),
                               height=CONFIGS_UI['table4']['row_height_factor']*HEIGHT*self.shape[0],
                               padding=[0, 10, 0, 10])
        self.buttons = [[] for _ in range(self.shape[0])]
        for it in range(self.shape[0]):
            row = BoxLayout(orientation='horizontal',
                            spacing=CONFIGS_UI['table4']['spacing_between']['columns'],
                            size_hint=(1, 1/self.shape[0]))

            for k, header in enumerate(self.headers):
                button = CustomButton(text=items[header][it],
                                      size_hint=(CONFIGS_UI['table4']['column_fracs'][k], 1))
                button.background_color = CONFIGS_UI['table4']['background_color']['default']
                row.add_widget(button)
                self.buttons[it].append(button)
            self.rows.add_widget(row)
        self.items.add_widget(self.rows)



class CustomPopup:
    def __init__(self):
        self.content = BoxLayout(orientation='vertical')
        self.label = CustomLabel1(text='Введите пароль')
        self.input = CustomTextInput1(text='',
                                      password=True,
                                      password_mask='*')
        self.btns = BoxLayout(orientation='horizontal')
        self.btn1 = CustomButton(text='Ввод')
        self.btn2 = CustomButton(text='Стереть')
        self.btns.add_widget(self.btn1)
        self.btns.add_widget(self.btn2)
        self.content.add_widget(self.label)
        self.content.add_widget(self.input)
        self.content.add_widget(self.btns)
        self.popup = Popup(title='',
                           content=self.content,
                           size_hint=CONFIGS_UI['screen']['logs_managing']['popup']['size_hint'])