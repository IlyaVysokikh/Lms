from dataclasses import dataclass

import redis
from typing import Any, Dict

class RedisClient:

    def __init__(
            self,
            url: str
    ):
        self.client = redis.Redis.from_url(url=url)

    def set_key(
            self,
            key: str,
            value: Any,
            expire_time: int | None = None
    ) -> bool:
        """
        Установка значения ключа.

        :param key: Ключ
        :param value: Значение
        :param expire_time: Время жизни в секундах
        :return: Результат операции (True/False)
        """
        return self.client.set(key, value, ex=expire_time)

    def get_key(self, key: str) -> str | None:
        """
        Получение значения ключа.

        :param key: Ключ
        :return: Значение или None, если ключ не существует
        """
        return self.client.get(key)

    def delete_key(self, key: str) -> int:
        """
        Удаление ключа.

        :param key: Ключ
        :return: Количество удаленных ключей
        """
        return self.client.delete(key)

    def key_exists(self, key: str) -> bool:
        """
        Проверка существования ключа.

        :param key: Ключ
        :return: True/False
        """
        return self.client.exists(key) == 1

    def set_expire(self, key: str, expire_time: int) -> bool:
        """
        Установка времени жизни ключа.

        :param key: Ключ
        :param expire_time: Время жизни в секундах
        :return: True, если время установлено
        """
        return self.client.expire(key, expire_time)

    def close(self) -> None:
        """Закрытие соединения с Redis."""
        self.client.close()
