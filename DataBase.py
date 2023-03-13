import sqlite3  # импорт движка базы данных
from sqlite3 import Error  # импортируем отдельно модуль ошибки (для удобства использования)
import sqlalchemy  # импортируем ORM
from sqlalchemy.orm import declarative_base, sessionmaker  # Импортируем необходимые модули дял сборки базы данных
from sqlalchemy import create_engine  # модуль который и будет производить сборку
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean  # Типы данных для бд
from sqlalchemy import Sequence  # Модуль для последовательности в бд
import os


def find_db_file(name: str, path: str) -> bool:  # Функция для создания файла (по факту проверка наличия файла, но работает некорректно)
    for root, dirs, files in os.walk(path):  # Проходимся по файлам в различных директориях
        if name in files:  # Проверяем наличие файла в списке файлов пути
            return True
        else:
            print('File does not exist in this directory')
            return False


if not find_db_file('main.db', '/Text_to_Audio'):  # Вызываем функцию проверки сущестования файла

    Base = declarative_base()  # Создание экземпляра декларативной базы (класса)
    engine = create_engine('sqlite:///main.db', echo=False)  # Движок для работы с бд
    Session = sessionmaker(bind=engine)  # Экземпляр класса для сессий


    class Users(Base):  # Класс-таблица пользователя 
        __tablename__ = 'users'  # Имя таблицы
        id = Column(Integer, Sequence('user_id_seq'), primary_key=True)  # ID которое будет иметь последовательное значение
        user_name = Column(String(80), nullable=False)  # Имя пользователя
        f_name = Column(String(80), nullable=False)  # Имя
        l_name = Column(String(80), nullable=False)  # Фамилия
        tmp_passwd = Column(String(16), nullable=False)  # временный пароль

        def __repr__(self):  # Конвертация данных в строку (Зачем? - я ленивый. А это текст для echo = True)
            return f'<User (user name = {self.user_name}, first name = {self.f_name})>'


    class File(Base):  # Класс - таблица файла
        __tablename__ = 'file'  # Название таблицы
        file_id = Column(Integer, Sequence('file_id_seq'), primary_key=True)  # ID файла
        file_name = Column(String, nullable=False)  # Имя файла
        # file_date = Column(Date)  # Дата создания файла (пока разбираюсь)
        file_owner = Column(Integer, ForeignKey('users.id'), nullable=False)  # Внешний ключ указывающий на id владельца

        def __repr__(self):
            return f'File (file name = {self.file_name} owner = {self.file_owner})'


    Base.metadata.create_all(engine)  # Создаем бд с методанными (последовательность, скрытые данные и т.д.)

    session = Session()  # Создаем сессию для записи в бд
    session.add_all([
        # test_user_n = Users(user_name='', f_name="", l_name="", tmp_passwd=""),
        Users(user_name='Alex_Klim', f_name="Alexey", l_name="Klimov", tmp_passwd="dota2_gamer"),
        Users(user_name='SimpleGM', f_name="Konstantin", l_name="Shalimov", tmp_passwd="tmp_password_747"),
        Users(user_name='AgDeSs', f_name="Nikita", l_name="Kolankov", tmp_passwd="2077_2077"),

        # test_file_n = File(file_name='', file_owner=''),
        File(file_name='Ведьмак_моды+читы', file_owner='1'),
        File(file_name='Плюсы и минусы системы GURPS', file_owner='2'),
        File(file_name='Java для начинающих', file_owner='3'),
        File(file_name='Квинт аккорды на восьмиструнной гитаре', file_owner='1')
    ])  # Закидываем записи в базу данных. Класс указывает на принадлежность к таблице данных
    session.commit()  # Загружаем все записи в бд


else:
    print(f'Data Base file already exist\n{find_db_file("main.db", "/Text_to_Audio")}')  # Файл уже существует, значит создавать не нужно

Database = sqlite3.connect('main.db')  # Подключаемся к бд

cur = Database.cursor()  # Экзепляр класса курсор/указатель

users = (cur.execute("SELECT * FROM users ORDER BY f_name ").fetchall())  # Выводим все данные пользователей с сортировкой по имени
for user in users:
    print(user)

print(cur.execute("SELECT * FROM file ORDER BY file_owner").fetchall())  # Выводим все данные файлов с сортировкой по id владельца
