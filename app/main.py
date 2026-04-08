from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from routers import index


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"))


app.include_router(index.router)
