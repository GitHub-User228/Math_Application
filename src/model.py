from src.TasksGenerator import EquationsGenerator, \
    ConvertingTasksGenerator, \
    PSVTasksGenerator, \
    SoLEqGenerator



class Model:
    def __init__(self):
        self.generator = None


    def reset_generator(self, configs):
        if configs['task_type'] == 'уравнения':
            self.generator = EquationsGenerator()
        if configs['task_type'] == 'ед.измерения':
            self.generator = ConvertingTasksGenerator()
        if configs['task_type'] == 'геометрия':
            self.generator = PSVTasksGenerator()
        if configs['task_type'] == 'сист.ур.':
            self.generator = SoLEqGenerator()
        self.generator.reset(**dict(list(configs.items())[1:]))


    def generate_tasks(self):
        tasks, real_answers = self.generator.generate()
        data = {}
        data['Task'] = tasks
        data['Answer'] = real_answers
        data['№'] = list(range(1, len(real_answers) + 1))
        data['YourAnswer'] = []
        data['Time'] = []
        return data
