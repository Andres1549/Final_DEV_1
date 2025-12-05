from typing import Optional,List
from sqlmodel import SQLModel, Field, Relationship
from utils.dominante import Pie
from utils.positions import Position
from utils.states import States
from utils.partido import Victoria


class Jugador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    n_camiseta: int #1 a 99 no se puede repetir
    año_nacimiento:int
    nacionalidad:str
    altura:int
    peso:int
    pie_dom: Pie
    posicion:Position
    año_ingreso:int
    estado: States


class Estadistica_partido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_jugador: list["Jugador"] = Relationship(back_populates="jugador")
    id_partido: list["Partido"] = Relationship(back_populates="partido")
    tarjetas:int #no mayor a 2, es expulsion
    min_jugados:int
    goles:int
#debemos hacer estadisticas generales con esta tabla 

class Jugador_partidoLink(SQLModel, table=True):
    jugador_id: Optional[int]= Field(default=None, foreign_key="jugador.id", primary_key=True)
    partido_id: Optional[int]= Field(default=None, foreign_key="partido.id", primary_key=True)

class Partido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rival: str
    goles_sigmo:int
    goles_rival:int
    penales:bool
    penal_sig:Optional[int]
    penal_rival:Optional[int]
    resultado:Victoria



