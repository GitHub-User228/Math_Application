import random
from itertools import chain
import operator



OPERATIONS = {"+": operator.add, "-": operator.sub, "∙": operator.mul, ":": operator.ifloordiv}
VARIABLES = ['x', 'y', 'a', 'm', 'n', 'q', 't']
DIVS = lambda n: chain(*((d, n // d) for d in range(1, int(n ** 0.5) + 1) if n % d == 0))
MAX_NUMBER_GENERATED = 1000
MIN_NUMBER_GENERATED = 2
K = 1



class BaseGenerator:
    def __init__(self):
        self.n_tasks = None
        self.complexity = None
        self.max_number = None

    def reset(self, n_tasks, conf3, max_number):
        self.n_tasks = n_tasks
        self.conf3 = conf3
        self.max_number = max_number

    def generate(self):
        tasks = []
        real_answers = []
        for k in range(self.n_tasks):
            task, ans = self.generate_single_task()
            tasks.append(task)
            real_answers.append(ans)
        return tasks, real_answers

    def generate_single_task(self):
        task = None
        ans = None
        return task, ans

    def validate_task(self, input):
        pass



class EquationsGenerator(BaseGenerator):

    def __init__(self):
        super().__init__()

    def generate_single_task(self):
        ans = random.randint(1, self.max_number)
        equation = ans
        task = VARIABLES[random.randint(0, len(VARIABLES) - 1)]
        while True:
            if type(self.conf3) == str:
                complexity = random.randint(1, 3)
            else:
                complexity = self.conf3
            for it in range(complexity):
                equation, task = self.step(equation, task)
                if not equation:
                    break
            if (it == complexity - 1) and (equation is not False):
                break
            equation = ans
            task = VARIABLES[random.randint(0, len(VARIABLES) - 1)]
        if (task[0] == '(') and (task[-1] == ')'):
            task = task[1:-1]
        task += ' = ' + str(equation['res'])
        return task, str(ans)

    def step(self, prev_equation, prev_task):
        '''
        I order:
        x +/-/:/* a = b
        II order:
        (x +/-/:/* a) +/-/:/* b = c
        III order:
        ((x +/-/:/* a) +/-/:/* b) +/-/:/* c = d
        '''
        task = 'POS1 OPERATION POS2'
        equation = {'pos1': None, 'operation': None, 'pos2': None, 'res': None}
        operation = list(OPERATIONS.keys())[random.randint(0, 3)]
        task = task.replace('OPERATION', operation)
        equation['operation'] = operation
        posx = random.randint(1, 2)
        try:
            equation[f'pos{posx}'] = prev_equation['res']
            if ((operation in ['∙', ':']) and (prev_equation['operation'] in ['∙', ':'])) and (posx == 2):
                task = task.replace(f'POS{posx}', f'({prev_task})')
            else:
                task = task.replace(f'POS{posx}', f'{prev_task}')
            if operation in ['+', '-']:
                task = '(' + task + ')'
        except:
            equation[f'pos{posx}'] = prev_equation
            task = task.replace(f'POS{posx}', f'{prev_task}')
            if operation in ['+', '-']:
                task = '(' + task + ')'
        iter = 0
        while True:
            if operation == ':' and posx == 2:
                equation[f'pos{1 if posx == 2 else 2}'] = equation[f'pos{posx}'] * random.randint(MIN_NUMBER_GENERATED,
                                                                                                  max(MIN_NUMBER_GENERATED + 1,
                                                                                                      self.max_number //
                                                                                                      equation[
                                                                                                          f'pos{posx}']))
            elif operation == ':' and posx == 1:
                dividers = list(DIVS(equation[f'pos{posx}']))
                equation[f'pos{1 if posx == 2 else 2}'] = dividers[random.randint(0, len(dividers) - 1)]
            else:
                equation[f'pos{1 if posx == 2 else 2}'] = random.randint(MIN_NUMBER_GENERATED, self.max_number)
            equation['res'] = OPERATIONS[operation](equation['pos1'], equation['pos2'])
            iter += 1
            if self.validate_task(equation):
                task = task.replace(f'POS{1 if posx == 2 else 2}', str(equation[f'pos{1 if posx == 2 else 2}']))
                break
            if iter == 100:
                return False, None
        equation[f'pos{posx}'] = prev_equation
        return equation, task

    def validate_task(self, equation):
        if any([v < 1 for v in [equation['pos1'], equation['pos2'], equation['res']]]):
            return False
        elif any([v >= self.max_number * K for v in [equation['pos1'], equation['pos2'], equation['res']]]):
            return False
        return True



UNITS1 = {'мкм': 1e+6,'мм': 1e+3, 'см': 1e+2, 'дм': 10, 'м': 1, 'км': 1e-3}
UNITS2 = {'мм2': 1e+6, 'см2': 1e+4, 'дм2': 1e+2, 'м2': 1, 'ар': 1e-2, 'гектар': 1e-4}
UNITS3 = {'с': 86400, 'мин': 1440, 'ч': 24, 'д': 1}
UNITS4 = {'мм3': 1e+9, 'см3': 1e+6, 'дм3': 1e+3, 'м3': 1}



class ConvertingTasksGenerator(BaseGenerator):

    def __init__(self):
        super().__init__()

    def generate_single_task(self):
        while True:
            subset = random.choice([UNITS1, UNITS2, UNITS3, UNITS4])
            try:
                task = {}
                units = random.sample(list(subset.keys()), random.randint(2, len(subset)))
                units = [v for v in subset.keys() if v in units]
                units = [units[k] for k in range(len(units) - 1, -1, -1)]
                dv = self.max_number
                for unit in units:
                    v = random.randint(1, int(dv / subset[units[-1]] * subset[unit] * 0.8))
                    task[unit] = v
                    dv -= v * subset[units[-1]] / subset[unit]
                break
            except Exception as e:
                pass
        units2 = [task[key] / subset[key] * subset[units[-1]] for key in task.keys()]
        ans1 = f'{int(sum(units2))}{units[-1]}'
        task1 = ' '.join([f'{b}{a}' for (a, b) in task.items()])
        task2 = f'{int(sum(units2))}{units[-1]}'
        ans2, units2_ = self.deconv(val=int(sum(units2)),
                                    unit=units[-1],
                                    subset=subset)
        task1 = f'Приведи к {list(task.keys())[-1]}:\n' + task1
        task2 = f'Разложи на {", ".join(units2_)}:\n' + task2
        if self.conf3 == 'Аггрегация':
            return task1, ans1
        elif self.conf3 == 'Разложение':
            return task2, ans2
        elif 'Люб' in self.conf3:
            if random.randint(0, 1) < 0.5:
                return task1, ans1
            return task2, ans2

    def deconv(self, val, unit, subset):
        keys = list(subset.keys())
        keys = keys[keys.index(unit):]
        new_ans = {}
        for key in reversed(keys):
            dv = subset[unit] / subset[key]
            v = int(val // dv)
            if v > 0:
                new_ans[key] = v
            val = val % dv
        new_ans_ = ' '.join([f'{b}{a}' for (a, b) in new_ans.items()])
        return new_ans_, list(new_ans.keys())



TASKS = {'P': {'Треугольник': ['сторона', 'сторона', 'сторона', 'периметр'],
               'Равнобедренный треугольник': ['боковая сторона', 'основание', 'периметр'],
               'Равносторонний треугольник': ['сторона', 'периметр'],
               'Квадрат': ['сторона', 'периметр'],
               'Прямоугольник': ['ширина', 'длина', 'периметр'],
               'Параллелограмм': ['боковая сторона', 'основание', 'периметр'],
               'Равнобедренная трапеция': ['боковая сторона',
                            'нижнее основание', 'верхнее основание',
                            'периметр'],
               'Ромб': ['сторона', 'периметр'],
               'Четырехугольник': ['сторона', 'сторона', 'сторона', 'сторона', 'периметр']},
        'S': {'Прямоугольный треугольник': ['катет', 'катет', 'площадь'],
              'Квадрат': ['сторона', 'площадь'],
              'Прямоугольник': ['ширина', 'длина', 'площадь']},
        'V': {'Куб': ['длина ребра', 'объем'],
              'Паралеллипипед': ['длина','ширина','высота', 'объем'],
              'Прямая призма': ['площадь основания', 'высота', 'объем'],
              'Цилиндр': ['площадь основания', 'высота', 'объем']}}


CONV = {'сторона': 'сторону',
        'периметр': 'периметр',
        'боковая сторона': 'боковую сторону',
        'основание': 'основание',
        'ширина': 'ширину',
        'длина': 'длину',
        'нижнее основание': 'нижнее основание',
        'верхнее основание': 'верхнее основание',
        'катет': 'катет',
        'площадь': 'площадь',
        'объем': 'объем',
        'площадь основания': 'площадь основания',
        'высота': 'высоту',
        'длина ребра': 'длину ребра'}

EQUATIONS = {'P': {'Треугольник': lambda a,b,c: a+b+c,
                   'Равнобедренный треугольник': lambda a,b: 2*a + b,
                   'Равносторонний треугольник': lambda a: 3*a,
                   'Квадрат': lambda a: a*4,
                   'Прямоугольник': lambda a,b: (a+b)*2,
                   'Параллелограмм': lambda a,b: (a+b)*2,
                   'Равнобедренная трапеция': lambda a,b,c: 2*a+b+c,
                   'Ромб': lambda a: a*4,
                   'Четырехугольник': lambda a,b,c,d: a+b+c+d},
            'S': {'Прямоугольный треугольник': lambda a,b: a*b/2,
                  'Квадрат':  lambda a: a**2,
                  'Прямоугольник': lambda a,b: a*b},
        'V': {'Куб': lambda a: a**3,
              'Паралеллипипед': lambda a,b,c: a*b*c,
              'Прямая призма': lambda a,b: a*b,
              'Цилиндр': lambda a,b: a*b,
              }}

LIMITS = {'P': {'Треугольник': lambda v: v/3,
                'Равнобедренный треугольник': lambda v: v/3,
                'Равносторонний треугольник': lambda v: v/3,
                'Квадрат': lambda v: v/4,
                'Прямоугольник': lambda v: v/4,
                'Параллелограмм': lambda v: v/4,
                'Равнобедренная трапеция': lambda v: v/4,
                'Ромб': lambda v: v/4,
                'Четырехугольник': lambda v: v/4},
         'S': {'Прямоугольный треугольник': lambda v: (v/2)**0.5,
               'Квадрат':  lambda v: (v/2)**0.5,
               'Прямоугольник': lambda v: v**0.5},
          'V': {'Куб': lambda v: v**(1/3),
                'Паралеллипипед': lambda v: v**(1/3),
                'Прямая призма': lambda v: v**(1/2),
                'Цилиндр': lambda v: v**(1/2),
                }}


class PSVTasksGenerator(BaseGenerator):

    def __init__(self):
        super().__init__()

    def generate_single_task(self):
        if self.conf3 == 'Периметр':
            subset1 = TASKS['P']
            subset2 = EQUATIONS['P']
            limits = LIMITS['P']
        elif self.conf3 == 'Площадь':
            subset1 = TASKS['S']
            subset2 = EQUATIONS['S']
            limits = LIMITS['S']
        elif self.conf3 == 'Объем':
            subset1 = TASKS['V']
            subset2 = EQUATIONS['V']
            limits = LIMITS['V']
        else:
            subset1 = TASKS['P']
            subset2 = EQUATIONS['P']
            limits = LIMITS['P']
        while True:
            task_ = random.choice(list(subset1.keys()))
            subtask1 = subset1[task_]
            while True:
                if subset1 == 'Треугольник':
                    values = [random.randint(1, int(limits[task_](self.max_number))) for _ in range(len(subtask1[:-2]))]
                    values.append(random.randint(1, sum(values)-1))
                elif subset1 == 'Равнобедренный треугольник':
                    values = [random.randint(1, int(limits[task_](self.max_number))) for _ in range(len(subtask1[:-2]))]
                    values.append(random.randint(1, sum(values)*2 - 1))
                elif subset1 == 'Равнобедренная трапеция':
                    values = [random.randint(1, int(limits[task_](self.max_number))) for _ in range(len(subtask1[:-2]))]
                    values.append(random.randint(1, values[-1] - 1))
                elif subset1 == 'Четырехугольник':
                    values = [random.randint(1, int(limits[task_](self.max_number))) for _ in range(len(subtask1[:-2]))]
                    values.append(random.randint(1, sum(values) - 1))
                else:
                    values = [random.randint(1, int(limits[task_](self.max_number))) for _ in range(len(subtask1[:-1]))]
                v = int(subset2[task_](*values))
                if (subset2[task_](*values) - v) == 0:
                    values.append(v)
                    break
            target_id = random.randint(0, len(subtask1)-1)
            ans = values[target_id]
            task = task_+'\n'+'\n'.join([f'{a[0].upper()+a[1:]}: {b} ' for k, (a,b) in enumerate(zip(subtask1, values)) if k!=target_id])
            task = task + f'\nНайти {CONV[subtask1[target_id]]}'
            if all([v <= self.max_number for v in values]):
                break
        return task, str(ans)



class SoLEqGenerator(BaseGenerator):

    def __init__(self):
        super().__init__()

    def generate_single_task(self):
        if type(self.conf3) == str:
            complexity = random.randint(2, 4)
        else:
            complexity = int(self.conf3)
        while True:
            A = [[random.randint(1, int(self.max_number/2**(complexity))) for _ in range(complexity)] for _ in range(complexity)]
            ans = [random.randint(0, int(self.max_number/2**(complexity))) for _ in range(complexity)]
            B = [sum([w1*w2 for (w1,w2) in zip(a, ans)]) for a in A]
            if all([b < self.max_number for b in B]):
                if len(set([str(k) for k in A])) == len(A):
                    break
        variables = random.sample(VARIABLES, complexity)
        task = [' '.join([f"{str(w) if w<0 else '+ '+str(w)}{var}" for (w, var) in zip(a, variables)])+f" = {b}" for (a, b) in zip(A, B)]
        for k in range(len(task)):
            if task[k][0] == '+':
                task[k] = task[k][1:]
        task = '\n'.join(task)
        task = task + f'\nВведите значения ' + ','.join(variables) + ' через пробел'
        return task, ' '.join([str(k) for k in ans])