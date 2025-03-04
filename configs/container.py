from functools import lru_cache

import punq

from configs.settings import Settings
from internal.infrastructure.postgresql.database import Database
from internal.infrastructure.postgresql.repositories.notification_repository import NotificationRepository
from internal.infrastructure.postgresql.repositories.token_repository import TokenRepository
from internal.infrastructure.postgresql.repositories.user_repository import UserRepository
from internal.infrastructure.redis.redis_client import RedisClient
from internal.services.identity.auth_service import AuthService
from internal.services.identity.user_service import UserService
from internal.services.social.notification_service import NotificationService
from internal.usecase.identity.login_usecase import LoginUseCase
from internal.usecase.identity.register_usecase import RegisterUseCase
from internal.usecase.identity.verify_email_usecase import VerifyEmailUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _init_container()


def _init_container():
    container = punq.Container()

    container.register(Settings, scope=punq.Scope.singleton, instance=Settings())

    settings: Settings = container.resolve(Settings)

    container.register(
        Database,
        scope=punq.Scope.singleton,
        factory=lambda: Database(
            url=settings.postgres_settings.build_pg_dns(),
        ),
    )


    container.register(
        UserRepository,
        scope=punq.Scope.transient,
        factory= lambda: UserRepository(
            container.resolve(Database)
        )
    )

    container.register(
        TokenRepository,
        scope=punq.Scope.transient,
        factory=lambda: TokenRepository(
            container.resolve(Database)
        )
    )

    container.register(
        AuthService,
        scope=punq.Scope.transient,
        factory=lambda: AuthService(
            container.resolve(TokenRepository),
            settings.auth_settings
        )
    )

    container.register(
        UserService,
        scope=punq.Scope.transient,
        factory=lambda: UserService(
            container.resolve(UserRepository),
        )
    )

    container.register(
        NotificationRepository,
        scope=punq.Scope.transient,
        factory=lambda: NotificationRepository(
            database=container.resolve(Database),
        )
    )

    container.register(
        RedisClient,
        scope=punq.Scope.singleton,
        factory=lambda: RedisClient(settings.redis_url)
    )

    container.register(
        NotificationService,
        scope=punq.Scope.transient,
        factory=lambda: NotificationService(
            settings.smtp_settings,
            container.resolve(NotificationRepository),
            container.resolve(RedisClient),
        )
    )

    container.register(
        LoginUseCase,
        scope=punq.Scope.transient,
        factory=lambda: LoginUseCase(
            container.resolve(AuthService),
            container.resolve(UserService),
        )
    )

    container.register(
        RegisterUseCase,
        scope=punq.Scope.transient,
        factory=lambda: RegisterUseCase(
            container.resolve(UserService),
            container.resolve(AuthService),
            container.resolve(NotificationService),
        )
    )

    container.register(
        VerifyEmailUseCase,
        scope=punq.Scope.transient,
        factory=lambda: VerifyEmailUseCase(
            redis_client=container.resolve(RedisClient),
            user_service=container.resolve(UserService),
        )
    )

    return container