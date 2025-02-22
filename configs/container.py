from functools import lru_cache

import punq

from configs.settings import Settings
from internal.infrastructure.postgresql.database import Database
from internal.infrastructure.postgresql.repositories.token_repository import TokenRepository
from internal.infrastructure.postgresql.repositories.user_repository import UserRepository
from internal.services.identity.auth_service import AuthService
from internal.usecase.identity.login_usecase import LoginUseCase


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
            url=settings.build_pg_dns(),
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
            container.resolve(UserRepository),
            container.resolve(TokenRepository),
            settings
        )
    )

    container.register(
        LoginUseCase,
        scope=punq.Scope.transient,
        factory=lambda: LoginUseCase(
            container.resolve(AuthService),
        )
    )

    container.register(LoginUseCase, scope=punq.Scope.transient, instance=LoginUseCase())



    return container