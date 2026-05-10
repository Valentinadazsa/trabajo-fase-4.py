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
# ================== SERVICIO ABSTRACTO ==================
class Servicio(Entidad):
    def __init__(self, id, nombre, tarifa_base):
        super().__init__(id)

        if not nombre:
            raise ServicioError("Nombre de servicio inválido")
        if tarifa_base <= 0:
            raise ServicioError("Tarifa base inválida")

        self._nombre = nombre
        self._tarifa_base = tarifa_base

    def mostrar(self):
        return f"{self._nombre} - Tarifa: {self._tarifa_base}"

    def convertir_a_horas(self, cantidad, unidad):
        try:
            if cantidad <= 0:
                raise ServicioError("Cantidad inválida")

            unidad = unidad.lower()

            if unidad == "horas":
                return cantidad
            elif unidad == "días" or unidad == "dias":
                return cantidad * 24
            elif unidad == "semanas":
                return cantidad * 24 * 7
            else:
                raise ServicioError("Unidad de tiempo no válida")

        except Exception as e:
            Logger.log(f"Error al convertir tiempo: {str(e)}")
            raise ServicioError("Error en conversión de tiempo") from e

    @abstractmethod
    def calcular_costo(self, cantidad, unidad):
        pass


# ================== SERVICIOS ==================
class ReservaSala(Servicio):
    def __init__(self, id, tarifa):
        super().__init__(id, "Reserva de Sala", tarifa)

    def calcular_costo(self, cantidad, unidad):
        horas = self.convertir_a_horas(cantidad, unidad)
        return self._tarifa_base * horas


class AlquilerEquipo(Servicio):
    def __init__(self, id, tarifa):
        super().__init__(id, "Alquiler de Equipo", tarifa)

    def calcular_costo(self, cantidad, unidad):
        horas = self.convertir_a_horas(cantidad, unidad)
        return self._tarifa_base * horas * 0.8


class Asesoria(Servicio):
    def __init__(self, id, tarifa):
        super().__init__(id, "Asesoría Especializada", tarifa)

    def calcular_costo(self, cantidad, unidad):
        horas = self.convertir_a_horas(cantidad, unidad)
        return self._tarifa_base * horas * 1.2

# ============= RESERVAS ============
class Reserva:

    def __init__(self, cliente, servicio, cantidad, tipo_tiempo):
        if cantidad <= 0:
            raise ReservaError("Tiempo inválido")

        self._cliente = cliente
        self._servicio = servicio
        self._cantidad = cantidad
        self._tipo_tiempo = tipo_tiempo
        self._estado = "pendiente"

    def confirmar(self):
        if self._estado != "pendiente":
            raise ReservaError("Solo reservas pendientes pueden confirmarse")
        self._estado = "confirmada"

    def procesar(self):
        try:
            self.confirmar()
            costo = self._servicio.calcular_costo(self._cantidad, self._tipo_tiempo)
            self._estado = "procesada"
            return costo
        except Exception as e:
            Logger.log(f"Error al procesar: {e}")
            raise ReservaError("Error en procesamiento") from e

    def mostrar(self):
        return f"{self._cliente.mostrar()} | {self._servicio.mostrar()} | Estado: {self._estado}"


# ================== SISTEMA ==================
class Sistema:
    def __init__(self):
        self.clientes = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def crear_reserva(self, reserva):
        self.reservas.append(reserva)
        

