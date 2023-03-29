import datetime
import os

from peewee import MySQLDatabase, InternalError as PeeweeInternalError
from domain_models.book import Book
from repository.library import Library
from files.pdf_file import PdfFile


class ConsoleLibrary:

    def _input_year(self):

        while True:
            string_input = input("Введите год книги:" )
            if not string_input.isnumeric():
                print("Пожалуйста введите число: " )
            elif not 1 <= int(string_input) <= int(datetime.date.today().year):
                print("Ваше число не диапазоне. Попробуйте снова")
            else:

                year = int(string_input)
                return year

    def add_book(self):
        os.system("cls")
        #title = input("Введите название книги:" )

        title = input("ВВедите название книги (оставьте пустым что бы вернутся в меню): ")
        if title == "":
            return
        author = input("Введите имя автора:" )

        while len(author.strip()) == 0:
            author = input('Введите имя автора:')

        year = self._input_year()
        book = Book(title, year, author)
        change_option = input("Вы действительно хотите добавить книгу %s? 1-Да, 2-Нет: " % book )

        if change_option == '1':
            self.library.add(book=book)

        input("Нажмите ENTER что бы вернуться в главное меню" )

    def delete_book(self):
        os.system("cls")
        book_number = input("Введите номер книги для удаления:" )
        book = self.library.get_at(book_number)
        if not book:
            input("Книга не найдена... Нажмите ENTER что бы вернуться в главное меню" )
            return

        change_option = input("Вы действительно хотите удалить книгу %s? 1-Да, 2-Нет: " % book)

        if change_option == '1':
            self.library.remove_at(book_number)
            print("Книга удалена ", book)
            
        input("Нажмите ENTER что бы вернуться в главное меню" )

    def change_title(self, book_number, book):
        os.system("cls")
        title = input("ВВедите название книги (оставьте пустым что бы сохранить без изменений): ")
        if title == "" or book.title == title:
            input("Название не изменилось либо поле ввода пустое. Нажмите ENTER что бы вернуться в главное меню")
            return
        book.title = title
        change_option = input("Вы действительно хотите поменять название %s? 1-Да, 2-Нет: " % book)

        if change_option == '1':
            self.library.update_at(book_number, book)
            print("Информация о книге обновлена! ", book)

    def change_author(self, book_number, book):
        os.system("cls")
        author = input("Введите имя автора (оставьте пустым что бы сохранить без изменений): ")
        if author == "" or book.author == author:
            input("Имя автора не изменилось либо поле ввода пустое. Нажмите ENTER что бы вернуться в главное меню")
            return

        book.author = author
        change_option = input("Вы действительно хотите поменять имя автора %s? 1-Да, 2-Нет: " % book)

        if change_option == '1':
            self.library.update_at(book_number, book)
            print("Информация об авторе книги обновлена! ", book)

    def change_year(self, book_number, book):
        os.system("cls")

        year = self._input_year()

        if year == "" or book.year == year:
            input("Год книги не изменился либо поле ввода пустое. Нажмите ENTER что бы вернуться в главное меню")
            return
        book.year = year

        change_option = input("Вы действительно хотите обновть информацию о годе книги %s? 1-Да, 2-Нет: " % book)

        if change_option == '1':
            self.library.update_at(book_number, book)
            print("Информация о годе книги обновлена! ", book)

    def update_book(self):
        os.system("cls")
        book_id = input("Напишите номер книги для обновления данных: ")
        book = self.library.get_at(book_id)

        if not book:
            input("Книга не найдена. Нажмите ENTER что бы вернуться в главное меню")
            return

        print("Обновление информации ", book)
        change_option = input("Что вы хотите изменить? \n 1-Название \n 2-Автор \n 3-Год \n Оставьте поле пустым что бы вернуться в главное меню \n Ввод: ")

        if change_option == "1":
            self.change_title(book_id, book)
        elif change_option == "2":
            self.change_author(book_id, book)
        elif change_option == "3":
            self.change_year(book_id, book)

        input("Нажмите ENTER что бы вернуться в главное меню")

    def find_books_year(self):
        os.system("cls")
        year = self._input_year()
        book = self.library.find_by_year(year)
        print("Найдено: ", book)
        return book

    def find_books_author(self):
        os.system("cls")
        author = input("Введите имя автора для поиска: ")
        book = self.library.find_by_author(author)
        print("Найдено: ", book)
        return book

    def find_books_title(self):
        os.system("cls")
        title = input("Введите название книги для поиска: ")
        book = self.library.find_by_title(title)
        print("Найдено: ", book)
        return book

    def find_books(self):
        os.system("cls")
        search = input("Найти книгу по \n 1 - Году \n 2 - Автору \n 3 - Названию \n Ввод:")
        result = None
        if search == "1":
            result = self.find_books_year()
        elif search == "2":
            result = self.find_books_author()
        elif search == "3":
            result = self.find_books_title()
        input("Нажмите ENTER что бы вернуться в главное меню")
        return result

    def print_all_books(self):
        os.system("cls")
        pdf = PdfFile()
        books = self.library.get_all_books()
        pdf.save(books)
        input("Нажмите ENTER что бы вернуться в главное меню")

    def __init__(self):
        self.library = Library(data_base=MySQLDatabase('Library', user='user228', password='1234567890', host='localhost', port=3306))

        self.library.connect()

    def run(self):
        try:
            while True:
                os.system("cls")
                books = self.library.get_all_books()
                print("Колличество книг в Книготеке: ", len(books))
                command = input(
                    'Выберите необходимый пункт:\n 1-Добавление книги \n 2-Удаление книги \n 3-Обновление данных о книге \n 4-Поиск по номеру книги \n 5-Импорт библиотеки \n 0-Заверешение программы \n Ввод:')
                if command == "0":
                    break
                elif command == "1":
                    self.add_book()
                elif command == "2":
                    self.delete_book()
                elif command == "3":
                    self.update_book()
                elif command == "4":
                    self.find_books()
                elif command == "5":
                    self.print_all_books()

            self.library.close()
        except PeeweeInternalError as px:
            print(str(px))

        print("Консоль библиотеки закрыта!")
