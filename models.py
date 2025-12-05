from typing import Optional
from sqlmodel import SQLModel, Field
from utils.dominante import Pie
from utils.positions import Position
from utils.states import States

class Jugador():
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    n_camiseta: int 
    año_nacimiento:int
    nacionalidad:str
    altura:int
    peso:int
    pie_dom: Pie
    posicion:Position
    año_ingreso:int
    estado: States


class Estadistica():
    pass


class Partido():
    pass


