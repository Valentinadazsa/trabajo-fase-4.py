import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
import datetime

# ================== LOGGER ==================
class Logger:
    @staticmethod
    def log(mensaje):
        with open("logs.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} - {mensaje}\n")


# ================== EXCEPCIONES ==================
class SistemaError(Exception):
    pass

class ClienteError(SistemaError):
    pass

class ServicioError(SistemaError):
    pass

class ReservaError(SistemaError):
    pass


# ================== CLASE ABSTRACTA ==================
class Entidad(ABC):
    def __init__(self, id):
        self._id = id

    @abstractmethod
    def mostrar(self):
        pass


# ================== CLIENTE ==================
class Cliente(Entidad):
    def __init__(self, id, nombre, email):
        super().__init__(id)
        if not nombre:
            raise ClienteError("Nombre inválido")
        if "@" not in email:
            raise ClienteError("Email inválido")

        self.__nombre = nombre
        self.__email = email

    def mostrar(self):
        return f"{self.__nombre} ({self.__email})"

    def get_nombre(self):
        return self.__nombre

