import uuid
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP_SSL, SMTPException

from configs.settings import SMTPSettings
from internal.infrastructure.postgresql.repositories.notification_repository import NotificationRepository
from internal.infrastructure.redis.redis_client import RedisClient
from internal.models.social.enums.notification_type import NotificationType
from internal.models.social.notification_template import NotificationTemplate


@dataclass
class NotificationService:
    smtp_settings: SMTPSettings
    notification_repository: NotificationRepository
    redis_client: RedisClient

    def send_verification_email(self, to_email: str, name: str, surname: str) -> None:
        """
        Отправляет пользователю письмо с подтверждением аккаунта.

        :param to_email: Электронная почта пользователя
        :param name: Имя получателя
        :param surname: Фамилия получателя
        """
        verification_token = uuid.uuid4().hex
        # todo изменить
        verification_link = f"http://localhost:8000/api/v1/identity/verify-email?token={verification_token}"
        subject = "Подтверждение аккаунта"

        notification_template: NotificationTemplate | None = self.notification_repository.get_notification_by_type(
            NotificationType.ACCOUNT_VERIFICATION.value
        )

        if not notification_template:
            raise ValueError("Шаблон уведомления не найден.")

        body = notification_template.body.format(
            name=name,
            surname=surname,
            verification_link=verification_link
        )

        message: MIMEMultipart = self.__build_message__(to_email=to_email, subject=subject, body=body)

        try:
            # Используем SMTP_SSL для безопасного подключения
            with SMTP_SSL(self.smtp_settings.SMTP_HOST, self.smtp_settings.SMTP_PORT) as server:
                server.login(
                    user=self.smtp_settings.SMTP_USER,
                    password=self.smtp_settings.SMTP_PASSWORD
                )
                server.sendmail(
                    from_addr=self.smtp_settings.SMTP_USER,
                    to_addrs=to_email,
                    msg=message.as_string()
                )

        except SMTPException as e:
            raise RuntimeError(f"Ошибка при отправке email: {str(e)}") from e

        self.redis_client.set_key(key=to_email, value=verification_token, expire_time=86400)

    def __build_message__(self, to_email: str, subject: str, body: str) -> MIMEMultipart:
        """
        Создает и возвращает объект MIMEMultipart для отправки email-сообщения.
        :param to_email: Email-адрес получателя
        :param subject: Тема письма
        :param body: Тело письма в формате HTML.
        :return: Объект MIMEMultipart, содержащий сформированное сообщение.
        """
        message = MIMEMultipart('alternative')
        message["From"] = self.smtp_settings.SMTP_USER
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        return message
