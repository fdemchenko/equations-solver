import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from polynomial import Polynomial
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np


class GUIBuilder:
    grid_columns_count, grid_rows_count = 12, 13
    coefficients_labels = []
    coefficients_entries = []
    
    
    @classmethod
    def draw_widgets(cls, master):
        labelProgramTitle = tk.Label(master, text='Розв\'язання нелінійних алгебраїчних рівнянь',
                                        justify='center', font='Arial 25')
        labelProgramTitle.grid(column=0, row=0, columnspan=cls.grid_columns_count, padx=220, pady=10)

        for index in range(cls.grid_columns_count - 2):
            power = 10 - index
            if power == 10:
                label_text = f'x{Polynomial.superscript_digits[1]}{Polynomial.superscript_digits[0]}'
            elif power == 1:
                label_text = 'x'
            else:
                label_text = f'x{Polynomial.superscript_digits[power]}'

            cls.coefficients_labels.append(tk.Label(master, text=label_text, font='Arial 18'))
            cls.coefficients_labels[-1].grid(row=1, column=index, pady=(15, 0), padx=(10, 0))

        for index in range(cls.grid_columns_count - 1):
            cls.coefficients_entries.append(ttk.Entry(master, font='Arial 16', width=6))
            cls.coefficients_entries[-1].grid(row=2, column=index, padx=(10, 0))

        cls.coefficients_labels.append(ttk.Label(master, text='= 0 ', font='Arial 16'))
        cls.coefficients_labels[-1].grid(row=2, column=cls.grid_columns_count - 1)

        cls.radio_buttons_group_var = tk.StringVar(master, 'Newton')

        bisection_method_choice = tk.Radiobutton(master, text='Метод бісекції', 
                            variable=cls.radio_buttons_group_var, value='Bisection', font='Arial 16', justify='left')
        bisection_method_choice.grid(row=3, column=0, columnspan=3, pady=(10, 5), padx=(15, 70))
        bisection_method_options_label = ttk.Label(master, 
                            text='Два значення х, на яких функція\nприймає значення різних знаків:', font='Arial 15')
        bisection_method_options_label.grid(row=4, column=0, columnspan=4, padx=(50, 15), pady=(0, 10))
        cls.bisection_method_options_entry_first = ttk.Entry(master, font='Arial 16', width=8)
        cls.bisection_method_options_entry_first.grid(row=5, column=0, columnspan=2, padx=(30, 0))
        cls.bisection_method_options_entry_second = ttk.Entry(master, font='Arial 16', width=8)
        cls.bisection_method_options_entry_second.grid(row=5, column=2, columnspan=2, padx=(0, 50))


        newton_method_choice = tk.Radiobutton(master, text='Метод Ньютона', 
                            variable=cls.radio_buttons_group_var, value='Newton', font='Arial 16', justify='left')
        newton_method_choice.grid(row=6, column=0, columnspan=3, pady=(10, 5), padx=(15, 60))
        bisection_method_options_label = ttk.Label(master, text='Наближене значення кореня:', font='Arial 15')
        bisection_method_options_label.grid(row=7, column=0, columnspan=4, padx=(55, 50), pady=(0, 10))
        cls.newton_method_options_entry_first = ttk.Entry(master, font='Arial 16', width=8)
        cls.newton_method_options_entry_first.grid(row=8, column=0, columnspan=2, padx=(30, 0))
        


        secants_method_choice = tk.Radiobutton(master, text='Метод cічних', 
                            variable=cls.radio_buttons_group_var, value='Secants', font='Arial 16', justify='left')
        secants_method_choice.grid(row=9, column=0, columnspan=3, pady=(10, 5), padx=(15, 80))
        bisection_method_options_label = ttk.Label(master, text='Наближене значення кореня:', font='Arial 15')
        bisection_method_options_label.grid(row=10, column=0, columnspan=4, padx=(60, 50), pady=(0, 10))
        cls.secants_method_options_entry_first = ttk.Entry(master, font='Arial 16', width=8)
        cls.secants_method_options_entry_first.grid(row=11, column=0, columnspan=2, padx=(30, 0))

        matplotlib.rcParams.update({"axes.grid" : True, "grid.color": "#000000"})
        cls.figure = plt.Figure(figsize=(6,4), dpi=100, facecolor='#9999ff')
        cls.ax = cls.figure.add_subplot(111)
 
        cls.chart_type = FigureCanvasTkAgg(cls.figure, master)
        cls.chart_type.get_tk_widget().grid(row=3, column=5, rowspan=8, columnspan=7, pady=20)
        cls.ax.set_facecolor('#eeeeee')
        cls.ax.set_xlim([-10, 10])
        cls.ax.set_ylim([-7, 7])

        toolbarFrame = tk.Frame(master=master)
        toolbarFrame.grid(row=11,column=5, columnspan=4)
        toolbar = NavigationToolbar2Tk(cls.chart_type, toolbarFrame)

        precision_label = ttk.Label(master, text='Точність', font='Arial 16')
        precision_label.grid(row=12, column=0, columnspan=2, padx=(25, 40), pady=(20, 0))

        cls.precision_entry = ttk.Entry(master, font='Arial 16', width=8)
        cls.precision_entry.grid(row=12, column=2, pady=(20, 0))
        cls.precision_entry.insert(tk.END, '0.001')

        plot_graph_button = tk.Button(master, text='Побудувати графік', font='Arial 16', width=20, command=cls.build_graph)
        plot_graph_button.grid(row=12, column=5, columnspan=3, pady=(20, 0))

        cls.solve_equation_button = tk.Button(master, text='Розв\'язати рівняння', font='Arial 16', width=20)
        cls.solve_equation_button.grid(row=12, column=8, columnspan=3, pady=(20, 0))

    @classmethod
    def build_graph(cls):
        try:
            entries_text = [entry.get() for entry in cls.coefficients_entries]
            entries_text.reverse()

            polynomial = Polynomial([element if element else 0 for element in entries_text])

            x = np.linspace(-1000, 1000, 100000)
            cls.ax.clear()
            cls.ax.set_title(f'f(x) = {polynomial}')
            cls.ax.plot(x, [polynomial.get_value(point) for point in x])
            cls.ax.set_xlim([-10, 10])
            cls.ax.set_ylim([-7, 7])
            cls.chart_type.draw()
        except TypeError:
            showerror('Помилка', 'Неправильні коефіцієнти рівняння')
