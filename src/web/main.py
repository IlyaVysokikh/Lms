from fastapi import FastAPI


def create_app() -> FastAPI:
    application = FastAPI(
        title="Learning management system",
        docs_url="/api/docs",
        description="API for Learning management system",
        debug=True,
    )
    return application


app = create_app()