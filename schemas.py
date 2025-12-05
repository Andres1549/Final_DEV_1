from pydantic import BaseModel
from typing import Optional
from utils.dominante import Pie
from utils.positions import Position
from utils.states import States
from utils.partido import Victoria

class JugadorCreate(BaseModel):
    nombre: str
    n_camiseta: int
    año_nacimiento: int
    nacionalidad: str
    altura: int
    peso: int
    pie_dom: Pie
    posicion: Position
    año_ingreso: int
    estado: States


class JugadorUpdate(BaseModel):
    nombre: Optional[str] = None
    n_camiseta: Optional[int] = None
    año_nacimiento: Optional[int] = None
    nacionalidad: Optional[str] = None
    altura: Optional[int] = None
    peso: Optional[int] = None
    pie_dom: Optional[Pie] = None
    posicion: Optional[Position] = None
    año_ingreso: Optional[int] = None
    estado: Optional[States] = None

class EstadisticaCreate(BaseModel):
    id_jugador: int
    id_partido: int
    tarjetas: int
    min_jugados: int
    goles: int


class EstadisticaUpdate(BaseModel):
    id_jugador: Optional[int] = None
    id_partido: Optional[int] = None
    tarjetas: Optional[int] = None
    min_jugados: Optional[int] = None
    goles: Optional[int] = None

class PartidoCreate(BaseModel):
    rival: str
    goles_sigmo: int
    goles_rival: int
    penales: bool
    penal_sig: Optional[int] = None
    penal_rival: Optional[int] = None
    resultado: Victoria


class PartidoUpdate(BaseModel):
    rival: Optional[str] = None
    goles_sigmo: Optional[int] = None
    goles_rival: Optional[int] = None
    penales: Optional[bool] = None
    penal_sig: Optional[int] = None
    penal_rival: Optional[int] = None
    resultado: Optional[Victoria] = None
