import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from polynomial import Polynomial
from solver import Solver
from validator import Validator
from guibuilder import GUIBuilder


class EquationSolver(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Equations Solver')
        self.geometry('1150x700')
        self.resizable(False, False)

        GUIBuilder.draw_widgets(self)
        GUIBuilder.solve_equation_button['command'] = self.solve_equation


    @staticmethod
    def solve_equation():
        try:
            entries = [entry.get() for entry in GUIBuilder.coefficients_entries]
            entries.reverse()

            polynomial = Polynomial([value if value else 0 for value in entries])
        except TypeError:
            showerror('Помилка', 'Неправильні коефіцієнти рівняння')
            return

        if all(map(lambda value: value == 0, polynomial.coefficients)):
            showinfo('Інформація', 'Рівняння має безліч коренів!')
            return

        if all(map(lambda value: value == 0, polynomial.coefficients[1:])) and polynomial.coefficients[0] != 0:
            showinfo('Інформація', 'Рівняння не має коренів!')
            return

        if GUIBuilder.radio_buttons_group_var.get() == 'Bisection':
            first_option = GUIBuilder.bisection_method_options_entry_first.get()
            second_option = GUIBuilder.bisection_method_options_entry_second.get()
            precision = GUIBuilder.precision_entry.get()
            
            if not Validator.validate_float_number(first_option):
                showerror('Помилка', 'Введіть правильне значення для першої точки')
                return

            if not Validator.validate_float_number(second_option):
                showerror('Помилка', 'Введіть правильне значення для другої точки')
                return

            if not Validator.validate_float_number(precision) or float(precision) <= 0:
                showerror('Помилка', 'Введіть правильне значення точності')
                return

            results = Solver.bisection_method_solver(float(first_option), float(second_option), float(precision), polynomial)

            if not results['root']:
                showerror('Помилка', 'На кінцях даного відрізка функція приймає однаковий знак')
            else:
                showinfo('Результати', f'Знайдений корінь: {round(results["root"], 6)}\nТочність: {precision}\nКількість ітерацій: {results["iterations_count"]}')
                FileSaver.save_results(polynomial, results, precision)


        elif GUIBuilder.radio_buttons_group_var.get() == 'Newton':
            approximate_root = GUIBuilder.newton_method_options_entry_first.get()
            precision = GUIBuilder.precision_entry.get()

            if not Validator.validate_float_number(approximate_root):
                showerror('Помилка', 'Введіть правильне значення для наближеного кореня')
                return

            if not Validator.validate_float_number(precision) or float(precision) <= 0:
                showerror('Помилка', 'Введіть правильне значення точності')
                return

            results = Solver.newton_method_solver(float(approximate_root), float(precision), polynomial)
            if not results['root']:
                showerror('Помилка', 'Ділення на нуль!')
            else:
                showinfo('Результати', f'Знайдений корінь: {round(results["root"], 6)}\nТочність: {precision}\nКількість ітерацій: {results["iterations_count"]}')
                FileSaver.save_results(polynomial, results, precision)
             
        elif GUIBuilder.radio_buttons_group_var.get() == 'Secants':
            approximate_root = GUIBuilder.secants_method_options_entry_first.get()
            precision = GUIBuilder.precision_entry.get()

            if not Validator.validate_float_number(approximate_root):
                showerror('Помилка', 'Введіть правильне значення для наближеного кореня')
                return

            if not Validator.validate_float_number(precision) or float(precision) <= 0:
                showerror('Помилка', 'Введіть правильне значення точності')
                return

            results = Solver.secants_method_solver(float(approximate_root), float(precision), polynomial)
            if not results['root']:
                showerror('Помилка', 'Ділення на нуль!')
            else:
                showinfo('Результати', f'Знайдений корінь: {round(results["root"], 6)}\nТочність: {precision}\nКількість ітерацій: {results["iterations_count"]}')
                FileSaver.save_results(polynomial, results, precision)
        else:
            raise RuntimeError('Impossible')



class FileSaver:
    @staticmethod
    def save_results(polynomial, results, eps, filename='solve-info.txt'):
        try:
            with open(filename, 'w') as file:
                file.write(f'Equation: {polynomial} = 0\n\n')
                file.write(f'Approximate root: {results["root"]}\n')
                file.write(f'Precision: {eps}\n')
                file.write(f'Iterations count: {results["iterations_count"]}\n\n')

                file.write(f'Approximate roots:\n')
                for approximate_root in results["approximate_roots"]:
                    file.write(f'  {approximate_root}\n')
        except:
            print('Error while open file to write results')


if __name__ == '__main__':
    app = EquationSolver()
    app.mainloop()

