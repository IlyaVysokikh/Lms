from contextlib import contextmanager
from typing import Generator
import psycopg2
from psycopg2 import errors


class Database:
    def __init__(self, url: str) -> None:
        self._url = url

    @contextmanager
    def get_cursor(self) -> Generator[psycopg2.extensions.cursor, None, None]:
        """
        Контекстный менеджер для получения курсора базы данных.
        :return: Генератор, возвращающий курсор базы данных.
        """
        with self.__get_connection__(self._url) as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except errors.Error as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()

    @contextmanager
    def __get_connection__(self) -> Generator[psycopg2.extensions.connection, None, None]:
        """
        Контекстный менеджер для получения соединения с базой данных.
        :return: Генератор, возвращающий соединение с базой данных.
        """
        conn = psycopg2.connect(self._url)
        try:
            yield conn
        except errors.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()