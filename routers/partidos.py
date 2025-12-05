from fastapi import FastAPI, Request, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import SessionLocal
from models import Partido
from utils.partido import Victoria
from schemas import PartidoCreate, PartidoUpdate

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

# Partidos

@app.get("/partidos")
def partidos(request: Request, db: Session = Depends(get_db)):
    partidos_list = listar_partidos(db, skip=0, limit=100, include_deleted=False)
    return templates.TemplateResponse("partidos.html", {"request": request, "partidos": partidos_list})

@app.post("/partidos/", tags=["Partidos"])
def crear_nuevo_partido(obj: PartidoCreate, session: Session = Depends(get_db)):
    return create_partido(session, obj)

@app.get("/partidos/", tags=["Partidos"])
def listar_todos_los_partidos(
    skip: int = 0,
    limit: int = Query(10, le=100),
    include_deleted: bool = Query(False, description="Incluir eliminados lógicamente"),
    session: Session = Depends(get_db)
):
    return listar_partidos(session, skip=skip, limit=limit, include_deleted=include_deleted)

@app.get("/partidos/deleted", tags=["Partidos"])
def listar_partidos_borrados(session: Session = Depends(get_db)):
    return listar_partidos_eliminados(session)

@app.post("/partidos/{partido_id}/restore", tags=["Partidos"])
def restaurar_partido_por_id(partido_id: int, session: Session = Depends(get_db)):
    if restaurar_partido(session, partido_id):
        return {"message": "Partido restaurado correctamente"}
    raise HTTPException(status_code=404, detail="No fue posible restaurar el partido")

@app.get("/partidos/search/", tags=["Partidos"])
def buscar_partido_por_rival(rival: str = Query(..., min_length=1), session: Session = Depends(get_db)):
    return buscar_partido_por_rival(session, rival)

@app.get("/partidos/filter/local/", tags=["Partidos"])
def filtrar_partidos_locales(es_local: bool = Query(True), session: Session = Depends(get_db)):
    return filtrar_partidos_por_local(session, es_local)

@app.get("/partidos/filter/fecha/", tags=["Partidos"])
def filtrar_partidos_por_fecha(fecha_inicio: date = Query(...), fecha_fin: date = Query(...), session: Session = Depends(get_db)):
    return filtrar_partidos_por_fecha(session, fecha_inicio, fecha_fin)

@app.get("/partidos/filter/victoria/", tags=["Partidos"])
def filtrar_partidos_con_victoria(session: Session = Depends(get_db)):
    return filtrar_partidos_victorias(session)

@app.get("/partidos/{partido_id}", tags=["Partidos"])
def obtener_partido_por_id(partido_id: int, session: Session = Depends(get_db)):
    return obtener_partido(session, partido_id)

@app.put("/partidos/{partido_id}", tags=["Partidos"])
def actualizar_datos_partido(partido_id: int, obj: PartidoUpdate, session: Session = Depends(get_db)):
    return actualizar_partido(session, partido_id, obj)

@app.delete("/partidos/{partido_id}", tags=["Partidos"])
def eliminar_partido_por_id(partido_id: int, session: Session = Depends(get_db)):
    if eliminar_partido(session, partido_id):
        return {"message": "Partido eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Partido no encontrado")