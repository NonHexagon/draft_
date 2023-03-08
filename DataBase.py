import sqlite3  # импорт движка базы данных
from sqlite3 import Error  # импортируем отдельно модуль ошибки (для удобства использования)
import sqlalchemy  # импортируем ORM
from sqlalchemy.orm import declarative_base, sessionmaker  # Импортируем необходимые модули дял сборки базы данных
from sqlalchemy import create_engine  # модуль который и будет производить сборку
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean  # Типы данных для бд
from sqlalchemy import Sequence  # Вот что это - не помню
import os


def find_db_file(name: str, path: str) -> bool:
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
        else:
            print('File does not exist in this directory')
            return False


if not find_db_file('main.db', '/Text_to_Audio'):

    Base = declarative_base()
    engine = create_engine('sqlite:///main.db', echo=False)
    Session = sessionmaker(bind=engine)


    class Users(Base):
        __tablename__ = 'users'
        id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
        user_name = Column(String(80), nullable=False)
        f_name = Column(String(80), nullable=False)
        l_name = Column(String(80), nullable=False)
        tmp_passwd = Column(String(16), nullable=False)

        def __repr__(self):
            return f'<User (user name = {self.user_name}, first name = {self.f_name})>'


    class File(Base):
        __tablename__ = 'file'
        file_id = Column(Integer, Sequence('file_id_seq'), primary_key=True)
        file_name = Column(String, nullable=False)
        # file_date = Column(Date)
        file_owner = Column(Integer, ForeignKey('users.id'), nullable=False)

        def __repr__(self):
            return f'File (file name = {self.file_name} owner = {self.file_owner})'


    Base.metadata.create_all(engine)

    session = Session()
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
    ])
    session.commit()


else:
    print(f'Data Base file already exist\n{find_db_file("main.db", "/Text_to_Audio")}')

Database = sqlite3.connect('main.db')

cur = Database.cursor()

users = (cur.execute("SELECT * FROM users ORDER BY f_name ").fetchall())
for user in users:
    print(user)

print(cur.execute("SELECT * FROM file ORDER BY file_owner").fetchall())
