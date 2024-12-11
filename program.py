import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


# ======= Сравнение поставок и потребления =======
def find_equal_volumes():
    try:
        suppliers = [supplier_entry.get() for supplier_entry in supplier_entries]
        supply_volumes = [float(volume_entry.get()) for volume_entry in supply_volume_entries]
        consumers = [consumer_entry.get() for consumer_entry in consumer_entries]
        consumption_volumes = [float(volume_entry.get()) for volume_entry in consumption_volume_entries]

        matches = []
        for i in range(len(suppliers)):
            for j in range(len(consumers)):
                if supply_volumes[i] == consumption_volumes[j]:
                    matches.append((suppliers[i], consumers[j], supply_volumes[i]))

        show_results(matches)
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные числовые значения.")


def show_results(matches):
    if not matches:
        messagebox.showinfo("Результат", "Нет совпадающих объёмов поставок и потребления.")
        return

    result_window = tk.Toplevel(root)
    result_window.title("Совпадающие объёмы")
    result_window.geometry("500x300")

    columns = ("Поставщик", "Потребитель", "Объём")
    tree = ttk.Treeview(result_window, columns=columns, show="headings", height=10)
    tree.heading("Поставщик", text="Поставщик")
    tree.heading("Потребитель", text="Потребитель")
    tree.heading("Объём", text="Объём")
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for match in matches:
        tree.insert("", "end", values=match)

    close_button = tk.Button(result_window, text="Закрыть", command=result_window.destroy, bg="lightblue")
    close_button.pack(pady=10)


def show_supply_comparison():
    clear_root()

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text="Поставщик", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame, text="Объём поставки", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(frame, text="Потребитель", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5)
    tk.Label(frame, text="Объём потребления", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=5, pady=5)

    global supplier_entries, supply_volume_entries, consumer_entries, consumption_volume_entries
    supplier_entries, supply_volume_entries = [], []
    consumer_entries, consumption_volume_entries = [], []

    for i in range(10):
        supplier_entry = tk.Entry(frame)
        supplier_entry.grid(row=i + 1, column=0, padx=5, pady=5)
        supplier_entries.append(supplier_entry)

        supply_volume_entry = tk.Entry(frame)
        supply_volume_entry.grid(row=i + 1, column=1, padx=5, pady=5)
        supply_volume_entries.append(supply_volume_entry)

        consumer_entry = tk.Entry(frame)
        consumer_entry.grid(row=i + 1, column=2, padx=5, pady=5)
        consumer_entries.append(consumer_entry)

        consumption_volume_entry = tk.Entry(frame)
        consumption_volume_entry.grid(row=i + 1, column=3, padx=5, pady=5)
        consumption_volume_entries.append(consumption_volume_entry)

    tk.Button(root, text="Найти совпадения", command=find_equal_volumes, width=20, bg="lightgreen").pack(pady=20)
    tk.Button(root, text="Вернуться в меню", command=show_main_menu, width=20, bg="lightblue").pack(pady=10)


# ======= Анализ выполнения плана =======
def calculate():
    try:
        codes = [code_entry.get() for code_entry in code_entries]
        plan_values = [float(plan_entry.get()) for plan_entry in plan_entries]
        real_values = [float(real_entry.get()) for real_entry in real_entries]

        results = []
        for i in range(len(plan_values)):
            if real_values[i] < plan_values[i]:
                underperformance = ((plan_values[i] - real_values[i]) / plan_values[i]) * 100
                results.append((codes[i], round(underperformance, 2)))

        for row in tree.get_children():
            tree.delete(row)

        if results:
            for result in results:
                tree.insert("", "end", values=result)
        else:
            tree.insert("", "end", values=("Все предприятия выполнили план", ""))
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные числовые значения.")


def show_plan_analysis():
    clear_root()

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text="Шифр", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame, text="Плановый показатель", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(frame, text="Реальный показатель", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5)

    global code_entries, plan_entries, real_entries, tree
    code_entries, plan_entries, real_entries = [], [], []

    for i in range(10):
        code_entry = tk.Entry(frame, justify="center")
        code_entry.grid(row=i + 1, column=0, padx=5, pady=5)
        code_entries.append(code_entry)

        plan_entry = tk.Entry(frame, justify="center")
        plan_entry.grid(row=i + 1, column=1, padx=5, pady=5)
        plan_entries.append(plan_entry)

        real_entry = tk.Entry(frame, justify="center")
        real_entry.grid(row=i + 1, column=2, padx=5, pady=5)
        real_entries.append(real_entry)

    tk.Button(root, text="Вычислить", command=calculate, width=20, bg="lightgreen").pack(pady=20)

    columns = ("Шифр", "Недовыполнение (%)")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
    tree.heading("Шифр", text="Шифр")
    tree.heading("Недовыполнение (%)", text="Недовыполнение (%)")
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    tk.Button(root, text="Вернуться в меню", command=show_main_menu, width=20, bg="lightblue").pack(pady=10)


# ======= Работа с банками =======
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


def update_bank_list():
    cursor.execute("SELECT name, rate FROM banks")
    banks = cursor.fetchall()

    listbox_banks.delete(0, tk.END)
    for bank in banks:
        listbox_banks.insert(tk.END, f"{bank[0]} - {bank[1]}%")


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


def show_bank_with_max_rate():
    cursor.execute("SELECT name, rate FROM banks ORDER BY rate DESC LIMIT 1")
    max_bank = cursor.fetchone()

    if max_bank:
        messagebox.showinfo("Банк с максимальной ставкой", f"Банк: {max_bank[0]}\nСтавка: {max_bank[1]}%")
    else:
        messagebox.showerror("Ошибка", "Данные не найдены")


def show_bank_menu():
    clear_root()

    frame = ttk.Frame(root, padding=10)
    frame.pack(pady=10, fill=tk.X)

    ttk.Label(frame, text="Название банка:").grid(row=0, column=0, padx=5, pady=5)
    global entry_bank_name
    entry_bank_name = ttk.Entry(frame, width=30)
    entry_bank_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Процентная ставка:").grid(row=1, column=0, padx=5, pady=5)
    global entry_rate
    entry_rate = ttk.Entry(frame, width=30)
    entry_rate.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(frame, text="Добавить банк", command=add_bank).grid(row=2, column=0, columnspan=2, pady=10)

    global listbox_banks
    listbox_banks = tk.Listbox(root, height=10, font=("Arial", 12))
    listbox_banks.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    update_bank_list()

    frame_buttons = ttk.Frame(root)
    frame_buttons.pack(pady=10)

    ttk.Button(frame_buttons, text="Банки со ставками ниже средней", command=show_banks_below_average).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_buttons, text="Банк с максимальной ставкой", command=show_bank_with_max_rate).pack(side=tk.LEFT, padx=10)

    ttk.Button(root, text="Вернуться в меню", command=show_main_menu).pack(pady=10)


# ======= Общие функции =======
def clear_root():
    for widget in root.winfo_children():
        widget.destroy()


def show_main_menu():
    clear_root()

    tk.Button(root, text="Сравнение поставок и потребления", command=show_supply_comparison, width=30).pack(pady=10)
    tk.Button(root, text="Анализ выполнения плана", command=show_plan_analysis, width=30).pack(pady=10)
    tk.Button(root, text="Работа с банками", command=show_bank_menu, width=30).pack(pady=10)


# ======= Главная программа =======
root = tk.Tk()
root.title("Главное меню")
root.geometry("800x800")

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

show_main_menu()
root.mainloop()
