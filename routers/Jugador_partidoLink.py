from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from database import get_session
from models import Jugador_partidoLink, Jugador, Partido

router = APIRouter()


@router.get("/", response_model=List[Jugador_partidoLink])
def listar_relaciones(session: Session = Depends(get_session)):
    return session.exec(select(Jugador_partidoLink)).all()


@router.post("/", response_model=Jugador_partidoLink, status_code=201)
def crear_relacion(link: Jugador_partidoLink, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, link.jugador_id)
    partido = session.get(Partido, link.partido_id)
    if not jugador or not partido:
        raise HTTPException(status_code=404, detail="Jugador o Partido no encontrado")
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


@router.delete("/{jugador_id}/{partido_id}")
def eliminar_relacion(jugador_id: int, partido_id: int, session: Session = Depends(get_session)):
    link = session.exec(
        select(Jugador_partidoLink).where(
            (Jugador_partidoLink.jugador_id == jugador_id) & (Jugador_partidoLink.partido_id == partido_id)
        )
    ).first()
    if not link:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    session.delete(link)
    session.commit()
    return {"mensaje": f"Relación Jugador {jugador_id} - Partido {partido_id} eliminada"}


@router.get("/jugador/{jugador_id}", response_model=List[Jugador_partidoLink])
def obtener_partidos_de_jugador(jugador_id: int, session: Session = Depends(get_session)):
    """Obtiene todas las relaciones de partidos de un jugador específico"""
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    links = session.exec(
        select(Jugador_partidoLink).where(Jugador_partidoLink.jugador_id == jugador_id)
    ).all()
    return links


@router.get("/partido/{partido_id}", response_model=List[Jugador_partidoLink])
def obtener_jugadores_de_partido(partido_id: int, session: Session = Depends(get_session)):
    """Obtiene todas las relaciones de jugadores de un partido específico"""
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    links = session.exec(
        select(Jugador_partidoLink).where(Jugador_partidoLink.partido_id == partido_id)
    ).all()
    return links
