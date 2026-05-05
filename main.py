import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Предопределённые курсы валют (примерные)
exchange_rates = {
    'USD': {'EUR': 0.85, 'RUB': 75.0, 'GBP': 0.75, 'JPY': 110.0},
    'EUR': {'USD': 1.18, 'RUB': 88.0, 'GBP': 0.88, 'JPY': 129.0},
    'RUB': {'USD': 0.013, 'EUR': 0.011, 'GBP': 0.009, 'JPY': 1.45},
    'GBP': {'USD': 1.33, 'EUR': 1.14, 'RUB': 111.0, 'JPY': 147.0},
    'JPY': {'USD': 0.0091, 'EUR': 0.0077, 'RUB': 0.69, 'GBP': 0.0068}
}

currencies = list(exchange_rates.keys())

# Загрузка истории
if os.path.exists('history.json'):
    with open('history.json', 'r') as f:
        try:
            history = json.load(f)
        except:
            history = []
else:
    history = []

def save_history():
    with open('history.json', 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def convert():
    from_curr = combo_from.get()
    to_curr = combo_to.get()
    amount_str = entry_amount.get()

    # Проверка корректности ввода
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Введите положительное число")
        return

    # Получение курса из словаря
    try:
        rate = exchange_rates[from_curr][to_curr]
    except KeyError:
        messagebox.showerror("Ошибка", "Курс не найден")
        return

    result = amount * rate
    result_str = f"{amount} {from_curr} = {result:.4f} {to_curr}"
    label_result.config(text=result_str)

    # Записываем в историю
    entry = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'from': from_curr,
        'to': to_curr,
        'amount': amount,
        'rate': rate,
        'result': result
    }
    history.append(entry)
    save_history()
    update_history_table()

def update_history_table():
    for row in tree.get_children():
        tree.delete(row)
    for item in reversed(history):
        tree.insert('', 'end', values=(
            item['time'],
            f"{item['amount']} {item['from']}",
            f"{item['result']:.4f} {item['to']} (курс {item['rate']})"
        ))

# Создаем окно
root = tk.Tk()
root.title("Currency Converter (Без API)")
root.geometry("700x500")

# Верхняя панель
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Из:").grid(row=0, column=0, padx=5)
combo_from = ttk.Combobox(frame_top, values=currencies, state='readonly')
combo_from.current(0)
combo_from.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="В:").grid(row=0, column=2, padx=5)
combo_to = ttk.Combobox(frame_top, values=currencies, state='readonly')
combo_to.current(1)
combo_to.grid(row=0, column=3, padx=5)

tk.Label(frame_top, text="Сумма:").grid(row=0, column=4, padx=5)
entry_amount = tk.Entry(frame_top, width=15)
entry_amount.grid(row=0, column=5, padx=5)

# Кнопка
btn = tk.Button(root, text="Конвертировать", command=convert)
btn.pack(pady=10)

# Результат
label_result = tk.Label(root, text="", font=('Arial', 14))
label_result.pack()

# История
tk.Label(root, text="История:").pack(pady=5)
columns = ('time', 'details', 'result')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('time', text='Время')
tree.heading('details', text='Из/в')
tree.heading('result', text='Результат')
tree.pack(fill='both', expand=True)

update_history_table()

root.mainloop()