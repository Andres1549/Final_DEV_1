from fastapi import FastAPI
from routers import *
app = FastAPI(title="sigmotoa FC")
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
async def root():
    return {"message": "sigmotoa FC data"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Bienvenido a sigmotoa FC {name}"}


app.include_router(jugadores, prefix="/jugadores", tags=["Jugadores"])
app.include_router(partidos, prefix="/partidos", tags=["Partidos"])
app.include_router(estadisticas, prefix="/estadisticas", tags=["Estadisticas"])
