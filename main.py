import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = 'expenses.json'

# Загрузка данных
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Сохранение данных
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Инициализация данных
expenses = load_data()

# Основное окно
root = tk.Tk()
root.title("Expense Tracker")

# Ввод данных
tk.Label(root, text="Сумма").grid(row=0, column=0, padx=5, pady=5)
amount_var = tk.StringVar()
entry_amount = tk.Entry(root, textvariable=amount_var)
entry_amount.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Категория").grid(row=0, column=2, padx=5, pady=5)
categories = ['Еда', 'Транспорт', 'Развлечения', 'Другое']
category_var = tk.StringVar(value=categories[0])
category_menu = ttk.Combobox(root, textvariable=category_var, values=categories, state='readonly')
category_menu.grid(row=0, column=3, padx=5, pady=5)

tk.Label(root, text="Дата (ГГГГ-ММ-ДД)").grid(row=0, column=4, padx=5, pady=5)
date_var = tk.StringVar()
entry_date = tk.Entry(root, textvariable=date_var)
entry_date.grid(row=0, column=5, padx=5, pady=5)

# Кнопка добавления
def add_expense():
    try:
        amount = float(amount_var.get())
        if amount <= 0:
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Введите положительное число для суммы")
        return
    date_str = date_var.get()
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except:
        messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД")
        return
    expense = {
        'amount': amount,
        'category': category_var.get(),
        'date': date_str
    }
    expenses.append(expense)
    save_data(expenses)
    update_table()
    update_total()
    # Очистка полей
    amount_var.set('')
    date_var.set('')

tk.Button(root, text="Добавить расход", command=add_expense).grid(row=0, column=6, padx=5, pady=5)

# Фильтры
tk.Label(root, text="Фильтр по категории").grid(row=1, column=0, padx=5, pady=5)
filter_category_var = tk.StringVar(value='Все')
categories_with_all = ['Все'] + categories
filter_category_menu = ttk.Combobox(root, textvariable=filter_category_var, values=categories_with_all, state='readonly')
filter_category_menu.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Период с").grid(row=1, column=2, padx=5, pady=5)
filter_start_date_var = tk.StringVar()
entry_start_date = tk.Entry(root, textvariable=filter_start_date_var)
entry_start_date.grid(row=1, column=3, padx=5, pady=5)

tk.Label(root, text="по").grid(row=1, column=4, padx=5, pady=5)
filter_end_date_var = tk.StringVar()
entry_end_date = tk.Entry(root, textvariable=filter_end_date_var)
entry_end_date.grid(row=1, column=5, padx=5, pady=5)

# Таблица расходов
columns = ('Сумма', 'Категория', 'Дата')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=2, column=0, columnspan=7, padx=5, pady=5)

# Общая сумма
total_label = tk.Label(root, text="Общая сумма: 0")
total_label.grid(row=3, column=0, padx=5, pady=5)

# Обновление таблицы
def update_table(filtered_expenses=None):
    for row in tree.get_children():
        tree.delete(row)
    data = filtered_expenses if filtered_expenses is not None else expenses
    for exp in data:
        tree.insert('', 'end', values=(exp['amount'], exp['category'], exp['date']))

# Обновление суммы
def update_total():
    total = sum(exp['amount'] for exp in expenses)
    total_label.config(text=f"Общая сумма: {total:.2f}")

# Фильтрация данных
def apply_filters():
    filtered = expenses
    # Категория
    cat_filter = filter_category_var.get()
    if cat_filter != 'Все':
        filtered = [exp for exp in filtered if exp['category'] == cat_filter]
    # Даты
    start_str = filter_start_date_var.get()
    end_str = filter_end_date_var.get()
    try:
        if start_str:
            start_date = datetime.strptime(start_str, '%Y-%m-%d')
        else:
            start_date = None
        if end_str:
            end_date = datetime.strptime(end_str, '%Y-%m-%d')
        else:
            end_date = None
    except:
        messagebox.showerror("Ошибка", "Введите даты в формате ГГГГ-ММ-ДД")
        return
    if start_date:
        filtered = [exp for exp in filtered if datetime.strptime(exp['date'], '%Y-%m-%d') >= start_date]
    if end_date:
        filtered = [exp for exp in filtered if datetime.strptime(exp['date'], '%Y-%m-%d') <= end_date]
    update_table(filtered)

# Обновление суммы по фильтру
def update_filtered_total():
    filtered = expenses
    cat_filter = filter_category_var.get()
    if cat_filter != 'Все':
        filtered = [exp for exp in filtered if exp['category'] == cat_filter]
    start_str = filter_start_date_var.get()
    end_str = filter_end_date_var.get()
    try:
        if start_str:
            start_date = datetime.strptime(start_str, '%Y-%m-%d')
        else:
            start_date = None
        if end_str:
            end_date = datetime.strptime(end_str, '%Y-%m-%d')
        else:
            end_date = None
    except:
        messagebox.showerror("Ошибка", "Введите даты в формате ГГГГ-ММ-ДД")
        return
    if start_date:
        filtered = [exp for exp in expenses if datetime.strptime(exp['date'], '%Y-%m-%d') >= start_date]
    else:
        filtered = expenses
    if end_date:
        filtered = [exp for exp in filtered if datetime.strptime(exp['date'], '%Y-%m-%d') <= end_date]
    update_table(filtered)
    total = sum(exp['amount'] for exp in filtered)
    total_label.config(text=f"Общая сумма: {total:.2f}")

# Кнопки фильтрации
tk.Button(root, text="Применить фильтр", command=apply_filters).grid(row=1, column=6, padx=5, pady=5)
tk.Button(root, text="Сбросить фильтр", command=lambda: [filter_category_var.set('Все'), filter_start_date_var.set(''), filter_end_date_var.set(''), update_table(), update_total()]).grid(row=1, column=7, padx=5, pady=5)

# Изначальное отображение
update_table()
update_total()

root.mainloop()
