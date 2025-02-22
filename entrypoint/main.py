from fastapi import FastAPI

from internal.exceptions.identity.password_mismatch_exception import PasswordMismatchException
from internal.exceptions.identity.user_not_found import UserNotFoundException
from internal.handlers.identity.handlers import router as identity_router
from internal.handlers.identity.exception_handlers import user_not_found_exception_handler, \
    password_mismatch_exception_handler


def _add_exception_handlers(application: FastAPI):
    # identity exceptions handlers
    application.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    application.add_exception_handler(PasswordMismatchException, password_mismatch_exception_handler)

def create_app() -> FastAPI:
    application = FastAPI(
        title='Learning management system API',
        docs_url='/api/docs',
        description='Diploma project',
        debug=True,
    )

    application.include_router(identity_router)

    _add_exception_handlers(application)

    return application

app = create_app()
