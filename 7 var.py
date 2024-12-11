import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# Функция для обработки данных и вывода результатов
def find_equal_volumes():
    try:
        # Считывание данных с полей ввода
        suppliers = [supplier_entry.get() for supplier_entry in supplier_entries]
        supply_volumes = [float(volume_entry.get()) for volume_entry in supply_volume_entries]
        consumers = [consumer_entry.get() for consumer_entry in consumer_entries]
        consumption_volumes = [float(volume_entry.get()) for volume_entry in consumption_volume_entries]

        # Сравнение объёмов поставок и потребления
        matches = []
        for i in range(len(suppliers)):
            for j in range(len(consumers)):
                if supply_volumes[i] == consumption_volumes[j]:
                    matches.append((suppliers[i], consumers[j], supply_volumes[i]))

        # Отображение результатов
        show_results(matches)

    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные числовые значения.")


# Функция для отображения результатов в новом окне
def show_results(matches):
    if not matches:
        messagebox.showinfo("Результат", "Нет совпадающих объёмов поставок и потребления.")
        return

    # Создание нового окна
    result_window = tk.Toplevel(root)
    result_window.title("Совпадающие объёмы")
    result_window.geometry("500x300")

    # Создание таблицы
    columns = ("Поставщик", "Потребитель", "Объём")
    tree = ttk.Treeview(result_window, columns=columns, show="headings", height=10)
    tree.heading("Поставщик", text="Поставщик")
    tree.heading("Потребитель", text="Потребитель")
    tree.heading("Объём", text="Объём")
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Заполнение таблицы
    for match in matches:
        tree.insert("", "end", values=match)

    # Кнопка закрытия окна
    close_button = tk.Button(result_window, text="Закрыть", command=result_window.destroy, bg="lightblue")
    close_button.pack(pady=10)


# Создание основного окна
root = tk.Tk()
root.title("Сравнение поставщиков и потребителей")
root.geometry("700x600")

# Заголовки
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Поставщик", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame, text="Объём поставки", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame, text="Потребитель", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5)
tk.Label(frame, text="Объём потребления", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=5, pady=5)

# Поля ввода для поставщиков и потребителей
supplier_entries = []
supply_volume_entries = []
consumer_entries = []
consumption_volume_entries = []

for i in range(10):  # 10 строк для ввода данных
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

# Кнопка для выполнения поиска
find_button = tk.Button(root, text="Найти совпадения", command=find_equal_volumes, width=20, bg="lightgreen", font=("Arial", 10, "bold"))
find_button.pack(pady=20)

# Запуск приложения
root.mainloop()
