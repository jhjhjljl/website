from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from routers import pages


app = FastAPI(openapi_url=None)


app.mount("/static", StaticFiles(directory="static"))


app.include_router(pages.router)
