import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# Функция для вычисления процента недовыполнения плана
def calculate():
    try:
        # Считывание данных с полей ввода
        codes = [code_entry.get() for code_entry in code_entries]
        plan_values = [float(plan_entry.get()) for plan_entry in plan_entries]
        real_values = [float(real_entry.get()) for real_entry in real_entries]

        # Список для результатов
        results = []
        for i in range(len(plan_values)):
            if real_values[i] < plan_values[i]:
                underperformance = ((plan_values[i] - real_values[i]) / plan_values[i]) * 100
                results.append((codes[i], round(underperformance, 2)))

        # Очищаем таблицу
        for row in tree.get_children():
            tree.delete(row)

        # Вывод результатов в таблицу
        if results:
            for result in results:
                tree.insert("", "end", values=result)
        else:
            tree.insert("", "end", values=("Все предприятия выполнили план", ""))

    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные числовые значения.")


# Создание основного окна
root = tk.Tk()
root.title("Анализ выполнения плана грузооборота")
root.geometry("650x600")

# Добавление меток и полей ввода для шифров, плановых и реальных показателей
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Шифр", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame, text="Плановый показатель", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame, text="Реальный показатель", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5)

code_entries = []
plan_entries = []
real_entries = []

for i in range(10):
    tk.Label(frame, text=f"Предприятие {i + 1}").grid(row=i + 1, column=0, padx=5, pady=5, sticky="w")

    code_entry = tk.Entry(frame, justify="center")
    code_entry.grid(row=i + 1, column=0, padx=5, pady=5)
    code_entries.append(code_entry)

    plan_entry = tk.Entry(frame, justify="center")
    plan_entry.grid(row=i + 1, column=1, padx=5, pady=5)
    plan_entries.append(plan_entry)

    real_entry = tk.Entry(frame, justify="center")
    real_entry.grid(row=i + 1, column=2, padx=5, pady=5)
    real_entries.append(real_entry)

# Кнопка для вычисления
calculate_button = tk.Button(root, text="Вычислить", command=calculate, width=15, bg="lightblue", font=("Arial", 10, "bold"))
calculate_button.pack(pady=10)

# Создание таблицы для вывода результатов
columns = ("Шифр", "Недовыполнение (%)")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
tree.heading("Шифр", text="Шифр")
tree.heading("Недовыполнение (%)", text="Недовыполнение (%)")
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Запуск приложения
root.mainloop()
