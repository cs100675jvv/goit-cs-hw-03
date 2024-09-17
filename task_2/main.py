from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure

# Підключення до MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")  # Замість localhost може бути ваш MongoDB URI
    db = client["cat_database"]
    collection = db["cats"]
    # Перевірка з'єднання
    client.admin.command('ismaster')
    print("MongoDB підключено успішно")
except ConnectionFailure:
    print("Не вдалося підключитися до MongoDB, перевірте з'єднання")


def create_document():
    """Створення нового запису"""
    try:
        name = input("Введіть ім'я тварини: ")
        age = int(input("Введіть вік тварини: "))
        features = input("Введіть особливості через кому: ").split(", ")
        document = {
            "name": name,
            "age": age,
            "features": features
        }
        collection.insert_one(document)
        print("Документ створено.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")
    except ValueError as e:
        print(f"Помилка введення: {e}")


def read_all_documents():
    """Виведення всіх записів"""
    try:
        documents = collection.find()
        for doc in documents:
            print(doc)
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")


def read_document_by_name():
    """Пошук запису за ім'ям"""
    try:
        name = input("Введіть ім'я тварини для пошуку: ")
        document = collection.find_one({"name": name})
        if document:
            print(document)
        else:
            print("Документ не знайдено.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")


def update_document_age():
    """Оновлення віку тварини за ім'ям"""
    try:
        name = input("Введіть ім'я тварини: ")
        new_age = int(input("Введіть новий вік тварини: "))
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print(f"Вік тварини '{name}' оновлено до {new_age}")
        else:
            print(f"Тварина з ім'ям '{name}' не знайдена.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")
    except ValueError as e:
        print(f"Помилка введення: {e}")


def add_feature_to_document():
    """Додавання нової характеристики до запису тварини"""
    try:
        name = input("Введіть ім'я тварини: ")
        new_feature = input("Введіть нову характеристику: ")
        result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.matched_count:
            print(f"Характеристика додана до тварини '{name}'")
        else:
            print(f"Тварина з ім'ям '{name}' не знайдена.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")


def delete_document():
    """Видалення запису за ім'ям"""
    try:
        name = input("Введіть ім'я тварини для видалення: ")
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"Тварина '{name}' видалена.")
        else:
            print(f"Тварина з ім'ям '{name}' не знайдена.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")


def delete_all_documents():
    """Видалення всіх записів"""
    try:
        confirmation = input("Ви впевнені, що хочете видалити всі документи? (так/ні): ")
        if confirmation.lower() == 'так':
            result = collection.delete_many({})
            print(f"Всі документи видалені. Видалено записів: {result.deleted_count}")
        else:
            print("Операцію скасовано.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")


def main():
    """Основне меню для вибору операцій"""
    while True:
        print("\nДоступні дії:")
        print("1 - Створити запис про тварину")
        print("2 - Показати всі записи")
        print("3 - Пошук запису за ім'ям тварини")
        print("4 - Оновити вік тварини")
        print("5 - Додати особливість до тварини")
        print("6 - Видалити запис про тварину")
        print("7 - Видалити всі записи")
        print("8 - Вийти")
        choice = input("Виберіть дію: ")

        if choice == "1":
            create_document()
        elif choice == "2":
            read_all_documents()
        elif choice == "3":
            read_document_by_name()
        elif choice == "4":
            update_document_age()
        elif choice == "5":
            add_feature_to_document()
        elif choice == "6":
            delete_document()
        elif choice == "7":
            delete_all_documents()
        elif choice == "8":
            break
        else:
            print("Некоректний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()