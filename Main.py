import argparse
import json
import os
import datetime

# Функция для создания новой заметки
def create_note(title, message):
    note = {
        "id": len(notes) + 1,
        "title": title,
        "message": message,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notes.append(note)
    return note

# Функция для сохранения списка заметок в JSON файл
def save_notes():
    with open(notes_file, 'w') as file:
        json.dump(notes, file, indent=4)

# Функция для чтения списка заметок из JSON файла и фильтрации по дате
def read_notes(filter_date=None):
    if not os.path.exists(notes_file):
        return []

    with open(notes_file, 'r') as file:
        notes_data = json.load(file)

    if filter_date:
        return [note for note in notes_data if note['timestamp'].startswith(filter_date)]
    else:
        return notes_data

# Функция для редактирования заметки по идентификатору
def edit_note(note_id, new_title, new_message):
    for note in notes:
        if note["id"] == note_id:
            note["title"] = new_title
            note["message"] = new_message
            note["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True
    return False

# Функция для удаления заметки по идентификатору
def delete_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return True
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Консольное приложение для работы с заметками")
    parser.add_argument("command", choices=["add", "list", "edit", "delete"], help="Команда для выполнения")
    parser.add_argument("--title", help="Заголовок заметки")
    parser.add_argument("--msg", help="Текст заметки")
    parser.add_argument("--date", help="Дата для фильтрации (YYYY-MM-DD)")

    args = parser.parse_args()

    notes_file = "notes.json"

    if os.path.exists(notes_file):
        with open(notes_file, 'r') as file:
            notes = json.load(file)
    else:
        notes = []

    if args.command == "add":
        title = args.title
        message = args.msg
        if title and message:
            create_note(title, message)
            save_notes()
            print("Заметка успешно сохранена")
        else:
            print("Ошибка: Заголовок и текст заметки обязательны")

    elif args.command == "list":
        filter_date = args.date
        filtered_notes = read_notes(filter_date)
        if filtered_notes:
            print("Список заметок:")
            for note in filtered_notes:
                print(f"Идентификатор: {note['id']}")
                print(f"Заголовок: {note['title']}")
                print(f"Содержание: {note['message']}")
                print(f"Дата/время создания: {note['timestamp']}")
                print("-" * 20)
        else:
            print("Список заметок пуст")

    elif args.command == "edit":
        note_id = int(input("Введите идентификатор заметки, которую хотите отредактировать: "))
        new_title = input("Введите новый заголовок: ")
        new_message = input("Введите новый текст заметки: ")
        if edit_note(note_id, new_title, new_message):
            save_notes()
            print("Заметка успешно отредактирована")
        else:
            print("Заметка с таким идентификатором не найдена")

    elif args.command == "delete":
        note_id = int(input("Введите идентификатор заметки, которую хотите удалить: "))
        if delete_note(note_id):
            save_notes()
            print("Заметка успешно удалена")
        else:
            print("Заметка с таким идентификатором не найдена")
