from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Query, HTTPException
from sqlalchemy.orm import Session
import models
import uvicorn
from utils.positions import Position
from utils.states import States


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request})

#Jugadores

@app.get("/jugadores")
def jugadores(request: Request, db: Session = Depends(get_db)):
    jugadores = get_jugadores(db)
    return templates.TemplateResponse("jugadores.html", {"request": request, "jugadores": jugadores})

@app.post("/jugadores/", tags=["Jugadores"])
def crear_nuevo_jugador(obj: JugadorCreate, session: Session = Depends(get_db)):
    return create_jugador(session, obj)

@app.get("/jugadores/", tags=["Jugadores"])
def listar_todos_los_jugadores(
    skip: int = 0,
    limit: int = Query(10, le=100),
    include_deleted: bool = Query(False, description="Incluir jugadores eliminados eliminados "),
    session: Session = Depends(get_db)
):
    return listar_jugadores(session, skip=skip, limit=limit, include_deleted=include_deleted)

@app.get("/jugadores/deleted", tags=["Jugadores"])
def listar_jugadores_borrados(session: Session = Depends(get_db)):
    return listar_jugadores_eliminados(session)

@app.post("/jugadores/{jugador_id}/restore", tags=["Jugadores"])
def restaurar_jugador_por_id(jugador_id: int, session: Session = Depends(get_db)):
    if restaurar_jugador(session, jugador_id):
        return {"message": "Jugador restaurado"}
    raise HTTPException(status_code=404, detail="No se pudo restaurar el jugador")

@app.get("/jugadores/search/", tags=["Jugadores"])
def buscar_jugador(nombre: str = Query(..., min_length=1), session: Session = Depends(get_db)):
    return buscar_jugador_por_nombre(session, nombre)

@app.get("/jugadores/filter/equipo/", tags=["Jugadores"])
def filtrar_jugadores_por_equipo(equipo: str = Query(..., min_length=1), session: Session = Depends(get_db)):
    return filtrar_jugadores_por_equipo(session, equipo)

@app.get("/jugadores/{jugador_id}", tags=["Jugadores"])
def obtener_jugador_por_id(jugador_id: int, session: Session = Depends(get_db)):
    return obtener_jugador(session, jugador_id)

@app.put("/jugadores/{jugador_id}", tags=["Jugadores"])
def actualizar_datos_jugador(jugador_id: int, obj: JugadorUpdate, session: Session = Depends(get_db)):
    return actualizar_jugador(session, jugador_id, obj)

@app.delete("/jugadores/{jugador_id}", tags=["Jugadores"])
def eliminar_jugador_por_id(jugador_id: int, session: Session = Depends(get_db)):
    if eliminar_jugador(session, jugador_id):
        return {"message": "Jugador eliminado"}
    raise HTTPException(status_code=404, detail="Jugador no encontrado")


