import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Функция для добавления банка в базу данных
def add_bank():
    name = entry_bank_name.get()
    try:
        rate = float(entry_rate.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Процентная ставка должна быть числом.")
        return

    if not name or rate < 0:
        messagebox.showerror("Ошибка", "Введите корректные данные.")
        return

    cursor.execute("INSERT INTO banks (name, rate) VALUES (?, ?)", (name, rate))
    conn.commit()

    entry_bank_name.delete(0, tk.END)
    entry_rate.delete(0, tk.END)

    update_bank_list()
    messagebox.showinfo("Успех", f"Банк '{name}' добавлен!")


# Функция для обновления списка банков
def update_bank_list():
    cursor.execute("SELECT name, rate FROM banks")
    banks = cursor.fetchall()

    listbox_banks.delete(0, tk.END)
    for bank in banks:
        listbox_banks.insert(tk.END, f"{bank[0]} - {bank[1]}%")


# Функция для расчёта средней ставки и отображения банков ниже неё
def show_banks_below_average():
    cursor.execute("SELECT AVG(rate) FROM banks")
    avg_rate = cursor.fetchone()[0]

    cursor.execute("SELECT name, rate FROM banks WHERE rate < ?", (avg_rate,))
    banks = cursor.fetchall()

    result_window = tk.Toplevel(root)
    result_window.title("Банки со ставками ниже средней")
    result_window.geometry("400x300")

    ttk.Label(result_window, text=f"Средняя ставка: {avg_rate:.2f}%").pack(pady=5)

    for bank in banks:
        ttk.Label(result_window, text=f"{bank[0]} - {bank[1]}%").pack()


# Функция для отображения банка с максимальной ставкой
def show_bank_with_max_rate():
    cursor.execute("SELECT name, rate FROM banks ORDER BY rate DESC LIMIT 1")
    max_bank = cursor.fetchone()

    if max_bank:
        messagebox.showinfo("Банк с максимальной ставкой",
                            f"Банк: {max_bank[0]}\nСтавка: {max_bank[1]}%")
    else:
        messagebox.showerror("Ошибка", "Данные не найдены")


# Создание базы данных
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE banks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rate REAL NOT NULL
)
""")

# Создание главного окна
root = tk.Tk()
root.title("Информация о банках")
root.geometry("600x500")

# Ввод данных о банке
frame_input = ttk.Frame(root, padding=10)
frame_input.pack(pady=10, fill=tk.X)

ttk.Label(frame_input, text="Название банка:").grid(row=0, column=0, padx=5, pady=5)
entry_bank_name = ttk.Entry(frame_input, width=30)
entry_bank_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Процентная ставка:").grid(row=1, column=0, padx=5, pady=5)
entry_rate = ttk.Entry(frame_input, width=30)
entry_rate.grid(row=1, column=1, padx=5, pady=5)

btn_add = ttk.Button(frame_input, text="Добавить банк", command=add_bank)
btn_add.grid(row=2, column=0, columnspan=2, pady=10)

# Список банков
frame_list = ttk.Frame(root, padding=10)
frame_list.pack(pady=10, fill=tk.BOTH, expand=True)

ttk.Label(frame_list, text="Список банков:").pack(anchor=tk.W)
listbox_banks = tk.Listbox(frame_list, height=10, font=("Arial", 12))
listbox_banks.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Кнопки действий
frame_buttons = ttk.Frame(root, padding=10)
frame_buttons.pack(pady=10)

btn_show_below_average = ttk.Button(frame_buttons, text="Банки с ставками ниже средней",
                                    command=show_banks_below_average)
btn_show_below_average.pack(side=tk.LEFT, padx=10)

btn_show_max_rate = ttk.Button(frame_buttons, text="Банк с максимальной ставкой",
                               command=show_bank_with_max_rate)
btn_show_max_rate.pack(side=tk.LEFT, padx=10)

# Запуск программы
root.mainloop()
