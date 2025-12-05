from typing import Optional,List
from sqlmodel import SQLModel, Field, Relationship
from utils.dominante import Pie
from utils.positions import Position
from utils.states import States

class Jugador():
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


class Estadistica_partido():
    id: Optional[int] = Field(default=None, primary_key=True)
    id_jugador: list["Jugador"] = Relationship(back_populates="jugador")
    id_partido: list["Partido"] = Relationship(back_populates="partido")
    tarjetas:int #no mayor a 2, es expulsion
    min_jugados:int
#debemos hacer estadisticas generales con esta tabla 


class Partido():
    pass


