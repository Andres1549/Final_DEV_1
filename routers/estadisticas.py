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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request})

# Estadisticas

@app.post("/estadisticas/", tags=["Estadisticas"])
def crear_nueva_estadistica(obj: EstadisticaCreate, session: Session = Depends(get_db)):
    return create_estadistica(session, obj)

@app.get("/estadisticas/", tags=["Estadisticas"])
def listar_todas_las_estadisticas(
    skip: int = 0,
    limit: int = Query(10, le=100),
    include_deleted: bool = Query(False, description="Incluir eliminados lógicamente"),
    session: Session = Depends(get_db)
):
    return listar_estadisticas(session, skip=skip, limit=limit, include_deleted=include_deleted)

@app.get("/estadisticas/deleted", tags=["Estadisticas"])
def listar_estadisticas_borradas(session: Session = Depends(get_db)):
    return listar_estadisticas_eliminadas(session)

@app.post("/estadisticas/{estadistica_id}/restore", tags=["Estadisticas"])
def restaurar_estadistica_por_id(estadistica_id: int, session: Session = Depends(get_db)):
    if restaurar_estadistica(session, estadistica_id):
        return {"message": "Estadística restaurada correctamente"}
    raise HTTPException(status_code=404, detail="No fue posible restaurar la estadística")

@app.get("/estadisticas/filter/jugador/", tags=["Estadisticas"])
def filtrar_estadisticas_por_jugador(jugador_id: int = Query(...), session: Session = Depends(get_db)):
    return filtrar_estadisticas_por_jugador(session, jugador_id)

@app.get("/estadisticas/filter/partido/", tags=["Estadisticas"])
def filtrar_estadisticas_por_partido(partido_id: int = Query(...), session: Session = Depends(get_db)):
    return filtrar_estadisticas_por_partido(session, partido_id)

@app.get("/estadisticas/filter/goles/", tags=["Estadisticas"])
def filtrar_estadisticas_por_goles_minimos(min_goles: int = Query(0, ge=0), session: Session = Depends(get_db)):
    return filtrar_estadisticas_por_goles(session, min_goles)

@app.get("/estadisticas/{estadistica_id}", tags=["Estadisticas"])
def obtener_estadistica_por_id(estadistica_id: int, session: Session = Depends(get_db)):
    return obtener_estadistica(session, estadistica_id)

@app.put("/estadisticas/{estadistica_id}", tags=["Estadisticas"])
def actualizar_datos_estadistica(estadistica_id: int, obj: EstadisticaUpdate, session: Session = Depends(get_db)):
    return actualizar_estadistica(session, estadistica_id, obj)

@app.delete("/estadisticas/{estadistica_id}", tags=["Estadisticas"])
def eliminar_estadistica_por_id(estadistica_id: int, session: Session = Depends(get_db)):
    if crud.eliminar_estadistica(session, estadistica_id):
        return {"message": "Estadística eliminada correctamente"}
    raise HTTPException(status_code=404, detail="Estadística no encontrada")
