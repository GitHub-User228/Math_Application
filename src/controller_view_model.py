import re
import time
from datetime import datetime
from functools import partial
from src.helpers import os, read_yaml, read, save, time_converter, time_diff, get_project_dir


PATH_TO_CONFIGS = os.path.join(get_project_dir(), 'configs')
CONFIGS_UI = read_yaml(path=PATH_TO_CONFIGS, filename='configs_ui')
SCR_RES = read_yaml(path=PATH_TO_CONFIGS, filename='screen_resolution')
CONFIGS_MODEL = read_yaml(path=PATH_TO_CONFIGS, filename='configs_model')


from kivy.config import Config
Config.set('graphics', 'width', SCR_RES['width'])
Config.set('graphics', 'height', SCR_RES['height'])
from kivy.app import App
from src.ui.ScreenManager import Manager
from src.ui.CustomWidgets import ConfigsArea
from src.model import Model
from kivy.clock import Clock


class ControllerViewModel(App):

    def build(self):
        ### Model and ViewManager
        self.model = Model()
        self.main = Manager()
        self.counter = 0
        ### Clock
        self.old_text = ''
        self.timer = {'clock': None, 'dts': None,
                      'times': None, 'start': None}
        ### binding functions to buttons and inputs
        self.bind_all_buttons()
        self.main.get_screen('task').input.bind(text = self.on_text_task_input)
        self.main.get_screen('logs').popup.input.bind(text = self.on_text_password)
        ### initial configs
        self.configs = {}
        self.configs['task_type'] = 'уравнения'
        self.configs['n_tasks'] = CONFIGS_MODEL[self.configs['task_type']]['n_tasks']['value']
        self.configs['max_number'] = CONFIGS_MODEL[self.configs['task_type']]['max_number']['value']
        self.configs['conf3'] = CONFIGS_MODEL[self.configs['task_type']]['conf3']['value']
        self.current_configs = self.configs.copy()
        return self.main


    def bind_all_buttons(self):
        ### binding functions to buttons from main screen
        self.main.get_screen('menu').btn13.on_press = self.on_press_to_task
        self.main.get_screen('menu').btn11.on_press = self.on_press_to_result
        self.main.get_screen('menu').btn31.on_press = self.on_press_menu_1
        self.main.get_screen('menu').btn32.on_press = self.on_press_menu_2
        self.main.get_screen('menu').btn33.on_press = self.on_press_menu_3
        self.main.get_screen('menu').area.btn1.on_press = self.on_press_menu_4
        self.main.get_screen('menu').area.btn2.on_press = self.on_press_menu_5
        for key in self.main.get_screen('menu').dropdown.buttons.keys():
            self.main.get_screen('menu').dropdown.buttons[key].on_press = partial(self.on_press_menu_dropdown, key)
        ### binding functions to buttons from task screen
        self.main.get_screen('task').btn12.on_press = self.on_press_to_menu
        self.main.get_screen('task').btn11.on_press = self.on_press_to_result
        self.main.get_screen('task').btn42.on_press = self.clear_input_answer
        self.main.get_screen('task').btn41.on_press = self.on_press_task_next
        ### binding functions to buttons from result screen
        self.main.get_screen('result').btn2.on_press = self.on_press_to_menu
        self.main.get_screen('result').btn3.on_press = self.on_press_to_task
        ### binding functions to buttons from logs screen
        self.main.get_screen('logs').btn1.on_press = self.on_press_to_result2
        self.main.get_screen('logs').btn2.on_press = self.on_press_logs_open_popup
        self.main.get_screen('logs').popup.btn1.on_press = self.on_press_logs_close_popup
        self.main.get_screen('logs').popup.btn2.on_press = self.on_press_logs_popup_clear_textinput
        self.main.get_screen('logs').btn3.on_press = self.on_press_logs_select_last_res
        for i in range(len(self.main.get_screen('logs').table.buttons)):
            for j in range(len(self.main.get_screen('logs').table.headers)):
                self.main.get_screen('logs').table.buttons[i][j].on_press = partial(self.on_press_logs_select_data, i)
        ### binding functions to buttons from logs_manager screen
        self.main.get_screen('logs_manager').btn1.on_press = self.on_press_logs_manager_close
        self.main.get_screen('logs_manager').dropdown.buttons['Выбрать всё'].on_press = self.on_press_logs_manager_select_all_data
        self.main.get_screen('logs_manager').dropdown.buttons['Убрать выделение'].on_press = self.on_press_logs_manager_remove_selection
        self.main.get_screen('logs_manager').dropdown.buttons['Удалить'].on_press = self.on_press_logs_manager_delete_selected
        for i in range(len(self.main.get_screen('logs_manager').table.buttons)):
            for j in range(len(self.main.get_screen('logs_manager').table.headers)):
                self.main.get_screen('logs_manager').table.buttons[i][j].on_press = partial(self.on_press_logs_manager_select_data, i)


    def unbind_all_buttons(self):
        ### unbinding functions from main screen buttons
        self.main.get_screen('menu').btn13.on_press = None
        self.main.get_screen('menu').btn11.on_press = None
        self.main.get_screen('menu').btn31.on_press = None
        self.main.get_screen('menu').btn32.on_press = None
        self.main.get_screen('menu').btn33.on_press = None
        self.main.get_screen('menu').area.btn1.on_press = None
        self.main.get_screen('menu').area.btn2.on_press = None
        for key in self.main.get_screen('menu').dropdown.buttons.keys():
            self.main.get_screen('menu').dropdown.buttons[key].on_press = None
        ### unbinding functions from task screen buttons
        self.main.get_screen('task').btn12.on_press = None
        self.main.get_screen('task').btn11.on_press = None
        self.main.get_screen('task').btn42.on_press = None
        self.main.get_screen('task').btn41.on_press = None
        ### unbinding functions from result screen buttons
        self.main.get_screen('result').btn2.on_press = None
        self.main.get_screen('result').btn3.on_press = None
        ### unbinding functions from logs screen buttons
        self.main.get_screen('logs').btn1.on_press = None
        self.main.get_screen('logs').btn2.on_press = None
        self.main.get_screen('logs').popup.btn1.on_press = None
        self.main.get_screen('logs').popup.btn2.on_press = None
        self.main.get_screen('logs').btn3.on_press = None
        for i in range(len(self.main.get_screen('logs').table.buttons)):
            for j in range(len(self.main.get_screen('logs').table.headers)):
                self.main.get_screen('logs').table.buttons[i][j].on_press = None
        ### unbinding functions from logs_manager screen buttons
        self.main.get_screen('logs_manager').btn1.on_press = None
        self.main.get_screen('logs_manager').dropdown.buttons['Выбрать всё'].on_press = None
        self.main.get_screen('logs_manager').dropdown.buttons['Убрать выделение'].on_press = None
        self.main.get_screen('logs_manager').dropdown.buttons['Удалить'].on_press = None
        for i in range(len(self.main.get_screen('logs_manager').table.buttons)):
            for j in range(len(self.main.get_screen('logs_manager').table.headers)):
                self.main.get_screen('logs_manager').table.buttons[i][j].on_press = None


    def button_timeout(func):
        def wrapper(self, arg=None):
            self.unbind_all_buttons()
            try:
                func(self)
            except:
                func(self, arg)
            self.bind_all_buttons()
        return wrapper


    def start_timer(self):
        self.timer['clock'] = Clock.schedule_interval(self.update_timer, 1/30)


    def stop_timer(self):
        self.timer['clock'].cancel()


    def update_timer(self, dt):
        dt = time_converter((datetime.now() - self.timer['start']).total_seconds())
        self.main.get_screen('task').label22.text = dt


    @button_timeout
    def on_press_menu_dropdown(self, task_type):
        self.main.get_screen('menu').btn31.background_color = CONFIGS_UI['button']['background_color']['default']
        self.configs['task_type'] = task_type
        self.configs['n_tasks'] = CONFIGS_MODEL[self.configs['task_type']]['n_tasks']['value']
        self.configs['max_number'] = CONFIGS_MODEL[self.configs['task_type']]['max_number']['value']
        self.configs['conf3'] = CONFIGS_MODEL[self.configs['task_type']]['conf3']['actual_values'] \
            [CONFIGS_MODEL[self.configs['task_type']]['conf3']['value']]
        self.main.get_screen('menu').area = ConfigsArea(task=task_type)


    @button_timeout
    def on_press_menu_1(self):
        ### update coloring
        self.main.get_screen('menu').btn31.background_color = CONFIGS_UI['button']['background_color']['if_clicked']
        self.main.get_screen('menu').btn32.background_color =  CONFIGS_UI['button']['background_color']['default']
        self.main.get_screen('menu').btn33.background_color = CONFIGS_UI['button']['background_color']['default']
        ### erasing data in area
        try:
            self.main.get_screen('menu').row2.remove_widget(self.main.get_screen('menu').area)
            self.main.get_screen('menu').row2.add_widget(self.main.get_screen('menu').dummy)
        except:
            pass


    @button_timeout
    def on_press_menu_2(self):
        ### update coloring
        self.main.get_screen('menu').btn31.background_color = CONFIGS_UI['button']['background_color']['default']
        self.main.get_screen('menu').btn32.background_color =  CONFIGS_UI['button']['background_color']['if_clicked']
        self.main.get_screen('menu').btn33.background_color = CONFIGS_UI['button']['background_color']['default']
        try:
            self.main.get_screen('menu').row2.remove_widget(self.main.get_screen('menu').dummy)
            self.main.get_screen('menu').row2.add_widget(self.main.get_screen('menu').area)
            self.main.get_screen('menu').area.task_type.text = f"Тип: {self.configs['task_type']}"
            self.main.get_screen('menu').area.slider1.value = self.configs['n_tasks']
            self.main.get_screen('menu').area.slider2.value = self.configs['max_number']
            self.main.get_screen('menu').area.slider3.value = self.configs['complexity']
            self.main.get_screen('menu').area.label32.text = str(self.configs['n_tasks'])
            self.main.get_screen('menu').area.label42.text = str(self.configs['max_number'])
            self.main.get_screen('menu').area.label52.text = str(self.configs['complexity'])
        except:
            pass


    @button_timeout
    def on_press_menu_3(self):
        ### update coloring
        self.main.get_screen('menu').btn31.background_color = CONFIGS_UI['button']['background_color']['default']
        self.main.get_screen('menu').btn32.background_color =  CONFIGS_UI['button']['background_color']['default']
        self.main.get_screen('menu').btn33.background_color = CONFIGS_UI['button']['background_color']['if_clicked']
        ### erasing data in area
        try:
            self.main.get_screen('menu').row2.remove_widget(self.main.get_screen('menu').area)
            self.main.get_screen('menu').row2.add_widget(self.main.get_screen('menu').dummy)
        except:
            pass
        self.model.reset_generator(configs=self.configs)
        self.current_configs = self.configs.copy()
        self.data = self.model.generate_tasks()
        self.counter = 0
        self.main.get_screen('result').reset_data(nrows=self.counter,
                                                  data=self.data)
        self.main.get_screen('task') \
            .reset_task_ui(task=self.data['Task'][self.counter],
                           number=self.data['№'][self.counter],
                           n_tasks=len(self.data['Task']))
        self.main.current = 'task'
        self.timer = {'clock': None, 'dts': [],
                      'times': [], 'start': None}
        try:
            time.sleep(0.3)
            self.stop_timer()
        except:
            pass
        self.timer['start'] = datetime.now()
        self.start_timer()


    @button_timeout
    def on_press_menu_4(self):
        ### update coloring
        self.main.get_screen('menu').btn32.background_color = CONFIGS_UI['button']['background_color']['default']
        ### get new configs
        self.configs['n_tasks'] = int(self.main.get_screen('menu').area.label32.text)
        self.configs['max_number'] = int(self.main.get_screen('menu').area.label42.text)
        try:
            self.configs['conf3'] = int(self.main.get_screen('menu').area.label52.text)
        except:
            self.configs['conf3'] = str(self.main.get_screen('menu').area.label52.text)
        ### erasing data in area
        self.main.get_screen('menu').row2.remove_widget(self.main.get_screen('menu').area)
        self.main.get_screen('menu').row2.add_widget(self.main.get_screen('menu').dummy)


    @button_timeout
    def on_press_menu_5(self):
        ### update coloring
        self.main.get_screen('menu').btn32.background_color = CONFIGS_UI['button']['background_color']['default']
        ### erasing data in area
        self.main.get_screen('menu').row2.remove_widget(self.main.get_screen('menu').area)
        self.main.get_screen('menu').row2.add_widget(self.main.get_screen('menu').dummy)


    @button_timeout
    def on_press_to_menu(self):
        self.main.current = 'menu'
        self.main.get_screen('result').btn1.on_press = self.on_press_to_result


    @button_timeout
    def on_press_to_task(self):
        self.main.current = 'task'
        self.main.get_screen('result').btn1.on_press = self.on_press_to_result


    @button_timeout
    def on_press_to_result(self):
        self.main.current = 'result'
        self.main.get_screen('result').btn1.on_press = self.on_press_to_logs


    @button_timeout
    def on_press_to_result2(self):
        self.main.current = 'result'


    @button_timeout
    def on_press_to_logs(self):
        self.main.current = 'logs'


    @button_timeout
    def clear_input_answer(self):
        self.main.get_screen('task').input.text = ''


    @button_timeout
    def on_press_task_next(self):
        if self.counter + 1 <= len(self.data['№']):
            ans = str(self.main.get_screen('task').input.text)
            if any([str(k) in ans for k in range(10)]):
                time_ = self.main.get_screen('task').label22.text
                self.timer['times'].append(time_)
                try:
                    dt = time_diff(self.timer['times'][-2], self.timer['times'][-1])
                except:
                    dt = self.timer['times'][-1]
                self.data['Time'].append(dt)
                self.data['YourAnswer'].append(ans)
                self.main.get_screen('result').reset_data(nrows=self.counter+1,
                                                          data=self.data)
                self.counter += 1
                try:
                    self.main.get_screen('task') \
                        .reset_task_ui(task=self.data['Task'][self.counter],
                                       number=self.data['№'][self.counter],
                                       n_tasks=len(self.data['Task']))
                except:
                    pass
        if self.counter == len(self.data['№']):
                self.main.get_screen('task') \
                    .reset_task_ui(task='Все задания выполнены',
                                   number=len(self.data['№']),
                                   n_tasks=len(self.data['Task']))
                self.stop_timer()
                save(data=self.data, configs=self.configs, start_time=self.timer['start'])
                self.main.get_screen('logs').reset_data()
                self.main.get_screen('logs_manager').reset_data()

        for i in range(len(self.main.get_screen('logs').table.buttons)):
            for j in range(len(self.main.get_screen('logs').table.headers)):
                self.main.get_screen('logs').table.buttons[i][j].background_color = CONFIGS_UI['table4']['background_color']['default']


    @button_timeout
    def on_press_logs_select_data(self, id_):
        filenames = list(sorted(os.listdir('logs'), reverse=True))
        data_new = read(filenames[id_])
        self.main.get_screen('result').reset_data(nrows=len(data_new[list(data_new.keys())[0]]),
                                                  data=data_new)
        for i in range(len(self.main.get_screen('logs').table.buttons)):
            for j in range(len(self.main.get_screen('logs').table.headers)):
                self.main.get_screen('logs').table.buttons[i][j].background_color = CONFIGS_UI['table4']['background_color']['default']
        for j in range(len(self.main.get_screen('logs').table.headers)):
            self.main.get_screen('logs').table.buttons[id_][j].background_color = CONFIGS_UI['table4']['background_color']['selected']


    @button_timeout
    def on_press_logs_select_last_res(self):
        try:
            self.main.get_screen('result').reset_data(nrows=len(self.data['YourAnswer']),
                                                      data=self.data)
        except:
            self.main.get_screen('result').reset_data(nrows=0,
                                                      data=None)
        for i in range(len(self.main.get_screen('logs').table.buttons)):
            for j in range(len(self.main.get_screen('logs').table.headers)):
                self.main.get_screen('logs').table.buttons[i][j].background_color = CONFIGS_UI['table4']['background_color']['default']


    @button_timeout
    def on_press_logs_open_popup(self):
        self.main.get_screen('logs').popup.popup.open()


    @button_timeout
    def on_press_logs_close_popup(self):
        password = self.main.get_screen('logs').popup.input.text
        if password == str(CONFIGS_UI['screen']['logs_managing']['popup']['password']):
            self.main.get_screen('logs').popup.input.text = ''
            self.main.get_screen('logs').popup.popup.dismiss()
            self.main.current = 'logs_manager'
        else:
            self.main.get_screen('logs').popup.input.text = ''


    @button_timeout
    def on_press_logs_popup_clear_textinput(self):
        self.main.get_screen('logs').popup.input.text = ''


    @button_timeout
    def on_press_logs_manager_close(self):
        self.main.current = 'logs'


    @button_timeout
    def on_press_logs_manager_select_data(self, id_):
        filename = list(sorted(os.listdir('logs'), reverse=True))[id_]
        if filename in self.main.get_screen('logs_manager').selected:
            self.main.get_screen('logs_manager').selected.remove(filename)
            for j in range(len(self.main.get_screen('logs_manager').table.headers)):
                self.main.get_screen('logs_manager').table.buttons[id_][j].background_color = CONFIGS_UI['table4']['background_color']['default']
        else:
            self.main.get_screen('logs_manager').selected.append(filename)
            for j in range(len(self.main.get_screen('logs_manager').table.headers)):
                self.main.get_screen('logs_manager').table.buttons[id_][j].background_color = CONFIGS_UI['table4']['background_color']['selected']


    @button_timeout
    def on_press_logs_manager_select_all_data(self):
        self.main.get_screen('logs_manager').selected = list(sorted(os.listdir('logs'), reverse=True))
        for i in range(len(self.main.get_screen('logs_manager').table.buttons)):
            for j in range(len(self.main.get_screen('logs_manager').table.headers)):
                self.main.get_screen('logs_manager').table.buttons[i][j].background_color = CONFIGS_UI['table4']['background_color']['selected']


    @button_timeout
    def on_press_logs_manager_remove_selection(self):
        self.main.get_screen('logs_manager').selected = []
        for i in range(len(self.main.get_screen('logs_manager').table.buttons)):
            for j in range(len(self.main.get_screen('logs_manager').table.headers)):
                self.main.get_screen('logs_manager').table.buttons[i][j].background_color = CONFIGS_UI['table4']['background_color']['default']


    @button_timeout
    def on_press_logs_manager_delete_selected(self):
        for filename in self.main.get_screen('logs_manager').selected:
            os.remove(os.path.join(get_project_dir(), f'logs/{filename}'))
        self.main.get_screen('logs').reset_data()
        self.main.get_screen('logs_manager').reset_data()
        self.main.get_screen('logs_manager').selected = []
        try:
            self.main.get_screen('result').reset_data(nrows=len(self.data['YourAnswer']),
                                                      data=self.data)
        except:
            self.main.get_screen('result').reset_data(nrows=0,
                                                      data=None)


    def on_text_task_input(self, instance, text):
        if len(text) > len(self.old_text):
            if self.old_text != text[:-1]:
                instance.text = self.old_text
            else:
                if self.current_configs['task_type'] in ['уравнения','геометрия']:
                    if len(text) > 0:
                        if str(text[-1]) not in '0123456789':
                            instance.text = text[:-1]
                if self.current_configs['task_type'] == 'сист.ур.':
                    if len(text) > 0:
                        if len(text) == 1:
                            if text not in '0123456789':
                                instance.text = ''
                        else:
                            if '  ' in text:
                                instance.text = text[:-1]
                            elif sum([k == ' ' for k in text]) > len(self.data['Answer'][self.counter].split(' ')) - 1:
                                instance.text = text[:-1]
                            elif str(text[-1]) not in ' 0123456789':
                                instance.text = text[:-1]
                if self.current_configs['task_type'] == 'ед.измерения':
                    units = self.data['Answer'][self.counter].split(' ')
                    units = ''.join([re.sub('[0-9]', '', unit) for unit in units])
                    if len(text) > 0:
                        if len(text) == 1:
                            if text not in '0123456789':
                                instance.text = ''
                        else:
                            if '  ' in text:
                                instance.text = text[:-1]
                            elif sum([k == ' ' for k in text]) > len(self.data['Answer'][self.counter].split(' ')) - 1:
                                instance.text = text[:-1]
                            elif str(text[-1]) not in ' 0123456789'+units:
                                instance.text = text[:-1]
        elif len(text) == len(self.old_text) - 1:
            if self.old_text[:-1] != text:
                instance.text = self.old_text
        self.old_text = instance.text[:]


    def on_text_password(self, instance, text):
        if len(text) > 0:
            if str(text[-1]) not in '0123456789':
                instance.text = text[:-1]