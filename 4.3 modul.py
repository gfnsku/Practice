import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime

# Хранилище данных
homework = {}  # Домашние задания по предметам
grades = {}  # Журнал успеваемости
students = []  # Список студентов
subjects = ["Математика", "Физика", "Информатика"]  # Базовые предметы
schedule = {}  # График работы преподавателя
archive = {}  # Архив успеваемости


# Функции для обработки данных
def add_student():
    student_group = entry_student_group.get()  # Группа студента
    student_name = entry_student.get()  # Имя студента
    if student_group and student_name:
        student_info = f"{student_group} - {student_name}"
        if student_info not in students:
            students.append(student_info)
            grades[student_info] = {}
            combobox_student["values"] = students  # Обновление списка студентов
            combobox_student_performance["values"] = students  # Обновление списка студентов для успеваемости
            update_group_combobox()  # Обновление списка групп
            messagebox.showinfo("Успех", f"Студент '{student_name}' добавлен в группу '{student_group}'.")
        else:
            messagebox.showerror("Ошибка", f"Студент '{student_name}' уже существует.")
    else:
        messagebox.showerror("Ошибка", "Введите группу и имя студента.")
    entry_student.delete(0, tk.END)
    entry_student_group.delete(0, tk.END)


def update_group_combobox():
    groups = list(set([student.split(" - ")[0] for student in students]))
    combobox_group["values"] = groups


def add_homework():
    subject = combobox_subject.get()
    task = entry_homework.get()
    date_assigned = date_entry.get_date().strftime("%Y-%m-%d")
    if subject and task:
        if subject not in homework:
            homework[subject] = []
        homework[subject].append((task, date_assigned))
        messagebox.showinfo("Успех",
                            f"Домашнее задание '{task}' добавлено для предмета '{subject}' на дату {date_assigned}.")
    else:
        messagebox.showerror("Ошибка", "Выберите предмет и введите задание.")
    entry_homework.delete(0, tk.END)

def edit_homework():
    subject = combobox_subject.get()
    task = entry_homework.get()
    new_task = entry_new_homework.get()
    new_date_assigned = date_new_entry.get_date().strftime("%Y-%m-%d")
    if subject and task and new_task:
        if subject in homework:
            for i, (current_task, date_assigned) in enumerate(homework[subject]):
                if current_task == task:
                    homework[subject][i] = (new_task, new_date_assigned)
                    messagebox.showinfo("Успех", f"Домашнее задание '{task}' изменено на '{new_task}' с датой {new_date_assigned}.")
                    entry_homework.delete(0, tk.END)
                    entry_new_homework.delete(0, tk.END)
                    return
            messagebox.showerror("Ошибка", f"Домашнее задание '{task}' не найдено.")
        else:
            messagebox.showerror("Ошибка", f"Предмет '{subject}' не найден.")
    else:
        messagebox.showerror("Ошибка", "Заполните все поля для редактирования задания.")

def delete_homework():
    subject = combobox_subject.get()
    task = entry_homework.get()
    if subject and task:
        if subject in homework:
            homework[subject] = [(t, d) for t, d in homework[subject] if t != task]
            messagebox.showinfo("Успех", f"Домашнее задание '{task}' удалено.")
            entry_homework.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", f"Предмет '{subject}' не найден.")
    else:
        messagebox.showerror("Ошибка", "Выберите предмет и введите задание для удаления.")


def add_grade():
    student_name = combobox_student.get()
    subject = combobox_grade_subject.get()
    task = combobox_task.get()
    grade = entry_grade_value.get()
    date_completed = date_completion_entry.get_date().strftime("%Y-%m-%d")
    if student_name and subject and task and grade:
        if student_name not in grades:
            messagebox.showerror("Ошибка", f"Студент '{student_name}' не найден.")
        else:
            if subject not in grades[student_name]:
                grades[student_name][subject] = {}
            grades[student_name][subject][task] = (grade, date_completed)
            messagebox.showinfo("Успех",
                                f"Оценка {grade} добавлена студенту '{student_name}' за задание '{task}' по предмету '{subject}' на дату {date_completed}.")
    else:
        messagebox.showerror("Ошибка", "Заполните все поля для оценки.")
    entry_grade_value.delete(0, tk.END)


def update_task_list(*args):
    subject = combobox_grade_subject.get()
    if subject in homework:
        combobox_task["values"] = [task[0] for task in homework[subject]]
    else:
        combobox_task["values"] = []


def display_data():
    output.delete(1.0, tk.END)
    output.insert(tk.END, "Домашние задания:\n")
    for subject, tasks in homework.items():
        output.insert(tk.END, f"- {subject}: {', '.join([f'{task[0]} ({task[1]})' for task in tasks])}\n")
    output.insert(tk.END, "\nЖурнал успеваемости:\n")
    for student, subjects in grades.items():
        output.insert(tk.END, f"- {student}:\n")
        for subject, tasks in subjects.items():
            output.insert(tk.END, f"  {subject}: {tasks}\n")
    output.insert(tk.END, "\nСписок студентов:\n")
    output.insert(tk.END, ", ".join(students) + "\n")
    output.insert(tk.END, "\nГрафик работы преподавателя:\n")
    for day, time in schedule.items():
        output.insert(tk.END, f"{day}: {time}\n")


def open_schedule_window():
    def save_schedule():
        day = combobox_day.get()
        time = entry_time.get()
        if day and time:
            schedule[day] = time
            messagebox.showinfo("Успех", f"График на {day} сохранён: {time}.")
        else:
            messagebox.showerror("Ошибка", "Заполните день и время.")
        entry_time.delete(0, tk.END)

    schedule_window = tk.Toplevel(root)
    schedule_window.title("График работы")

    tk.Label(schedule_window, text="День недели").grid(row=0, column=0, pady=5)
    combobox_day = ttk.Combobox(schedule_window, values=["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"],
                                state="readonly")
    combobox_day.grid(row=0, column=1, pady=5)

    tk.Label(schedule_window, text="Время работы").grid(row=1, column=0, pady=5)
    entry_time = tk.Entry(schedule_window)
    entry_time.grid(row=1, column=1, pady=5)

    tk.Button(schedule_window, text="Сохранить", command=save_schedule).grid(row=2, column=0, columnspan=2, pady=10)


# Функции для поиска и сортировки
def search_task():
    subject = combobox_subject_search.get()
    task = entry_task_search.get()
    if subject in homework:
        if task in [t[0] for t in homework[subject]]:
            messagebox.showinfo("Результат поиска", f"Задание '{task}' найдено по предмету '{subject}'.")
        else:
            messagebox.showerror("Результат поиска", f"Задание '{task}' не найдено по предмету '{subject}'.")
    else:
        messagebox.showerror("Ошибка", f"По предмету '{subject}' заданий не найдено.")
    entry_task_search.delete(0, tk.END)


def list_tasks_sorted_by_avg_grade():
    subject = combobox_subject_sort.get()
    if subject in homework:
        tasks = homework[subject]
        task_grades = {}
        for task in tasks:
            task_name = task[0]
            grades_list = [
                int(grades[student][subject][task_name][0])
                for student in grades
                if subject in grades[student] and task_name in grades[student][subject]
            ]
            avg_grade = sum(grades_list) / len(grades_list) if grades_list else 0
            task_grades[task_name] = avg_grade
        sorted_tasks = sorted(task_grades.items(), key=lambda x: x[1], reverse=True)
        result = "\n".join([f"{task}: {avg_grade:.2f}" for task, avg_grade in sorted_tasks])
        messagebox.showinfo("Задания по предмету", f"Задания по '{subject}' (по среднему баллу):\n{result}")
    else:
        messagebox.showerror("Ошибка", f"По предмету '{subject}' заданий не найдено.")


def list_performance_by_group_and_period():
    group = combobox_group.get()
    start_date = start_date_entry.get_date().strftime("%Y-%m-%d")
    end_date = end_date_entry.get_date().strftime("%Y-%m-%d")
    students_in_group = [student for student in students if student.startswith(group)]
    if not students_in_group:
        messagebox.showerror("Ошибка", f"Группа '{group}' не найдена.")
        return

    result = ""
    for student in students_in_group:
        student_grades = grades.get(student, {})
        for subject, tasks in student_grades.items():
            for task, (grade, date_completed) in tasks.items():
                task_date = next((t[1] for t in homework[subject] if t[0] == task), None)
                if task_date and start_date <= task_date <= end_date:
                    result += f"Студент: {student}, Предмет: {subject}, Задание: {task}, Дата выполнения: {date_completed}, Оценка: {grade}\n"

    if result:
        messagebox.showinfo("Успеваемость по группе и периоду", result)
    else:
        messagebox.showinfo("Успеваемость по группе и периоду", "Нет данных для выбранных параметров.")


def calculate_task_count():
    counts = {subject: len(tasks) for subject, tasks in homework.items()}
    result = "\n".join([f"{subject}: {count}" for subject, count in counts.items()])
    messagebox.showinfo("Количество заданий по предметам", result)


def add_subject():
    new_subject = entry_new_subject.get()
    if new_subject and new_subject not in subjects:
        subjects.append(new_subject)
        combobox_subject["values"] = subjects
        combobox_grade_subject["values"] = subjects
        combobox_subject_search["values"] = subjects
        combobox_subject_sort["values"] = subjects
        combobox_remove_subject["values"] = subjects
        messagebox.showinfo("Успех", f"Предмет '{new_subject}' добавлен.")
    else:
        messagebox.showerror("Ошибка", "Введите название предмета или предмет уже существует.")
    entry_new_subject.delete(0, tk.END)


def remove_subject():
    subject_to_remove = combobox_remove_subject.get()
    if subject_to_remove in subjects:
        subjects.remove(subject_to_remove)
        if subject_to_remove in homework:
            del homework[subject_to_remove]
        for student in grades:
            if subject_to_remove in grades[student]:
                del grades[student][subject_to_remove]
        combobox_subject["values"] = subjects
        combobox_grade_subject["values"] = subjects
        combobox_subject_search["values"] = subjects
        combobox_subject_sort["values"] = subjects
        combobox_remove_subject["values"] = subjects
        messagebox.showinfo("Успех", f"Предмет '{subject_to_remove}' удален.")
    else:
        messagebox.showerror("Ошибка", "Предмет не найден.")
    combobox_remove_subject.set('')


def identify_difficult_tasks():
    difficult_tasks = {}
    for subject, tasks in homework.items():
        for task, _ in tasks:
            total_students = len(students)
            not_completed = sum(
                1 for student in grades if subject in grades[student] and task not in grades[student][subject]
            )
            if total_students > 0 and not_completed / total_students > 0.5:  # Более 50% студентов не выполнили задание
                if subject not in difficult_tasks:
                    difficult_tasks[subject] = []
                difficult_tasks[subject].append(task)

    if difficult_tasks:
        result = "Сложные задания (не выполнило >50% студентов):\n"
        for subject, tasks in difficult_tasks.items():
            result += f"{subject}: {', '.join(tasks)}\n"
        messagebox.showinfo("Сложные задания", result)
    else:
        messagebox.showinfo("Сложные задания", "Нет сложных заданий.")


def archive_old_records():
    current_year = datetime.now().year
    for student, subjects in list(grades.items()):
        for subject, tasks in list(subjects.items()):
            for task, (grade, date_completed) in list(tasks.items()):
                task_year = datetime.strptime(date_completed, "%Y-%m-%d").year
                if task_year < current_year:
                    if student not in archive:
                        archive[student] = {}
                    if subject not in archive[student]:
                        archive[student][subject] = {}
                    archive[student][subject][task] = grades[student][subject].pop(task)
                    if not grades[student][subject]:
                        del grades[student][subject]
                    if not grades[student]:
                        del grades[student]
    messagebox.showinfo("Архивирование",
                        "Журнал успеваемости за истекший год перемещен в архив и удален из текущей базы данных.")

# Создание графического интерфейса
root = tk.Tk()
root.title("АРМ Учителя")
root.geometry("1000x850")

# Разделим экран на два фрейма
frame_left = tk.Frame(root)
frame_left.grid(row=0, column=0, padx=20, pady=10, sticky='n')

frame_right = tk.Frame(root)
frame_right.grid(row=0, column=1, padx=20, pady=10, sticky='n')

# Левый фрейм - добавление студента и оценок
tk.Label(frame_left, text="Добавить студента").grid(row=0, column=0, columnspan=2, pady=5)
tk.Label(frame_left, text="Группа студента").grid(row=1, column=0)
entry_student_group = tk.Entry(frame_left)
entry_student_group.grid(row=1, column=1)
tk.Label(frame_left, text="Имя студента").grid(row=2, column=0)
entry_student = tk.Entry(frame_left)
entry_student.grid(row=2, column=1)
tk.Button(frame_left, text="Добавить студента", command=add_student).grid(row=3, column=0, columnspan=2, pady=5)

# Добавление домашнего задания
tk.Label(frame_left, text="Добавить домашнее задание").grid(row=4, column=0, columnspan=2, pady=5)
tk.Label(frame_left, text="Предмет").grid(row=5, column=0)
combobox_subject = ttk.Combobox(frame_left, values=subjects, state="readonly")
combobox_subject.grid(row=5, column=1)
tk.Label(frame_left, text="Задание").grid(row=6, column=0)
entry_homework = tk.Entry(frame_left)
entry_homework.grid(row=6, column=1)
tk.Label(frame_left, text="Дата выдачи").grid(row=7, column=0)
date_entry = DateEntry(frame_left, width=12, background='darkblue', foreground='white', borderwidth=2, year=datetime.now().year,
                       month=datetime.now().month, day=datetime.now().day)
date_entry.grid(row=7, column=1)
tk.Button(frame_left, text="Добавить задание", command=add_homework).grid(row=8, column=0, columnspan=2, pady=5)

# Редактирование домашнего задания
tk.Label(frame_left, text="Новое задание").grid(row=9, column=0)
entry_new_homework = tk.Entry(frame_left)
entry_new_homework.grid(row=9, column=1)
tk.Label(frame_left, text="Новая дата выдачи").grid(row=10, column=0)
date_new_entry = DateEntry(frame_left, width=12, background='darkblue', foreground='white', borderwidth=2, year=datetime.now().year,
                           month=datetime.now().month, day=datetime.now().day)
date_new_entry.grid(row=10, column=1)
tk.Button(frame_left, text="Редактировать задание", command=edit_homework).grid(row=11, column=0, columnspan=2, pady=5)

# Удаление домашнего задания
tk.Button(frame_left, text="Удалить задание", command=delete_homework).grid(row=12, column=0, columnspan=2, pady=5)

# Добавление оценок
tk.Label(frame_left, text="Добавить оценку").grid(row=13, column=0, columnspan=2, pady=5)
tk.Label(frame_left, text="Студент").grid(row=14, column=0)
combobox_student = ttk.Combobox(frame_left, values=students, state="readonly")
combobox_student.grid(row=14, column=1)
tk.Label(frame_left, text="Предмет").grid(row=15, column=0)
combobox_grade_subject = ttk.Combobox(frame_left, values=subjects, state="readonly")
combobox_grade_subject.grid(row=15, column=1)
combobox_grade_subject.bind("<<ComboboxSelected>>", update_task_list)
tk.Label(frame_left, text="Задание").grid(row=16, column=0)
combobox_task = ttk.Combobox(frame_left, state="readonly")
combobox_task.grid(row=16, column=1)
tk.Label(frame_left, text="Оценка").grid(row=17, column=0)
entry_grade_value = tk.Entry(frame_left)
entry_grade_value.grid(row=17, column=1)
tk.Label(frame_left, text="Дата выполнения").grid(row=18, column=0)
date_completion_entry = DateEntry(frame_left, width=12, background='darkblue', foreground='white', borderwidth=2, year=datetime.now().year,
                                  month=datetime.now().month, day=datetime.now().day)
date_completion_entry.grid(row=18, column=1)
tk.Button(frame_left, text="Добавить оценку", command=add_grade).grid(row=19, column=0, columnspan=2, pady=5)

# Вывод данных
tk.Button(frame_left, text="Показать данные", command=display_data).grid(row=20, column=0, columnspan=2, pady=5)
output = tk.Text(frame_left, height=20, width=50)
output.grid(row=21, column=0, columnspan=2, pady=5)

# Правый фрейм - управление предметами, заданиями и анализ успеваемости
# Добавление и удаление предметов
tk.Label(frame_right, text="Добавить новый предмет").grid(row=0, column=0, columnspan=2, pady=5)
entry_new_subject = tk.Entry(frame_right)
entry_new_subject.grid(row=1, column=0, padx=5)
tk.Button(frame_right, text="Добавить", command=add_subject).grid(row=1, column=1, padx=5)

tk.Label(frame_right, text="Удалить предмет").grid(row=2, column=0, columnspan=2, pady=5)
combobox_remove_subject = ttk.Combobox(frame_right, values=subjects, state="readonly")
combobox_remove_subject.grid(row=3, column=0, padx=5)
tk.Button(frame_right, text="Удалить", command=remove_subject).grid(row=3, column=1, padx=5)

# Поиск задания
tk.Label(frame_right, text="Поиск задания").grid(row=4, column=0, columnspan=2, pady=5)
tk.Label(frame_right, text="Предмет").grid(row=5, column=0)
combobox_subject_search = ttk.Combobox(frame_right, values=subjects, state="readonly")
combobox_subject_search.grid(row=5, column=1)
tk.Label(frame_right, text="Задание").grid(row=6, column=0)
entry_task_search = tk.Entry(frame_right)
entry_task_search.grid(row=6, column=1)
tk.Button(frame_right, text="Найти задание", command=search_task).grid(row=7, column=0, columnspan=2, pady=5)

# Сортировка заданий
tk.Label(frame_right, text="Сортировка заданий по среднему баллу").grid(row=8, column=0, columnspan=2, pady=5)
tk.Label(frame_right, text="Предмет").grid(row=9, column=0)
combobox_subject_sort = ttk.Combobox(frame_right, values=subjects, state="readonly")
combobox_subject_sort.grid(row=9, column=1)
tk.Button(frame_right, text="Сортировать задания", command=list_tasks_sorted_by_avg_grade).grid(row=10, column=0, columnspan=2, pady=5)

# Успеваемость по группе и периоду
tk.Label(frame_right, text="Успеваемость по группе и периоду").grid(row=11, column=0, columnspan=2, pady=5)
tk.Label(frame_right, text="Группа").grid(row=12, column=0)
combobox_group = ttk.Combobox(frame_right, state="readonly")
combobox_group.grid(row=12, column=1)
tk.Label(frame_right, text="Дата начала").grid(row=13, column=0)
start_date_entry = DateEntry(frame_right, width=12, background='darkblue', foreground='white', borderwidth=2)
start_date_entry.grid(row=13, column=1)
tk.Label(frame_right, text="Дата конца").grid(row=14, column=0)
end_date_entry = DateEntry(frame_right, width=12, background='darkblue', foreground='white', borderwidth=2)
end_date_entry.grid(row=14, column=1)
tk.Button(frame_right, text="Показать успеваемость", command=list_performance_by_group_and_period).grid(row=15, column=0, columnspan=2, pady=5)

# Подсчёт заданий
tk.Button(frame_right, text="Рассчитать количество заданий", command=calculate_task_count).grid(row=16, column=0, columnspan=2, pady=5)

# Выявление сложных заданий
tk.Button(frame_right, text="Выявить сложные задания", command=identify_difficult_tasks).grid(row=17, column=0, columnspan=2, pady=5)

# Архивирование данных
tk.Button(frame_right, text="Архивировать данные", command=archive_old_records).grid(row=18, column=0, columnspan=2, pady=5)

# Добавление информации о создателе
creator_info = tk.Label(root, text="Создатель программы: Халтурин Алексей Владмирович, группа 1225С9-1")
creator_info.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
