

import random
import pandas as pd



def cuadrados_medios_siguiente(x, digitos=4):
    """Da UN paso del método de cuadrados medios a partir del estado x.
    Devuelve (nuevo_x, r, detalle) donde detalle muestra el cálculo interno."""
    cuadrado_relleno = str(x ** 2).zfill(digitos * 2)
    inicio = (len(cuadrado_relleno) - digitos) // 2
    nuevo_x = int(cuadrado_relleno[inicio:inicio + digitos])
    r = nuevo_x / (10 ** digitos)
    detalle = {
        "X anterior": x,
        "X al cuadrado (relleno a 8 dígitos)": cuadrado_relleno,
        "Dígitos centrales extraídos": nuevo_x
    }
    return nuevo_x, r, detalle


def congruencia_siguiente(x, a=7141, c=54773, m=259200):
    """Da UN paso del método de congruencia lineal a partir del estado x."""
    operacion = a * x + c
    nuevo_x = operacion % m
    r = nuevo_x / m
    detalle = {
        "X anterior": x,
        "a·X + c": operacion,
        "mod m": m,
        "X nuevo": nuevo_x
    }
    return nuevo_x, r, detalle


def generar_semilla_4_digitos():
    """'Tomamos un generador al azar' para sacar la semilla de 4 dígitos."""
    return random.randint(1000, 9999)


def secuencia_larga(metodo, semilla, n=200):
    """Genera n números R (0 a 1) seguidos con el método indicado,
    útil para las gráficas de dispersión."""
    estado = semilla
    valores = []
    for _ in range(n):
        if metodo == "cuadrado_medio":
            estado, r, _detalle = cuadrados_medios_siguiente(estado)
        else:
            estado, r, _detalle = congruencia_siguiente(estado)
        valores.append(r)
    return valores


class Persona:
    def __init__(self, nombre, metodo, semilla):
        self.nombre = nombre
        self.metodo = metodo  # "cuadrado_medio" o "congruencial"
        self.estado = semilla
        self.semilla_inicial = semilla
        self.historial_r = []        # números R (0 a 1) generados
        self.historial_fuerza = []   # fuerza (0 a 1) generados
        self.historial_proceso = []  # detalle paso a paso (proceso visible)

    def siguiente_fuerza(self):
        if self.metodo == "cuadrado_medio":
            self.estado, r, detalle = cuadrados_medios_siguiente(self.estado)
        else:
            self.estado, r, detalle = congruencia_siguiente(self.estado)
        fuerza = round(r, 2)
        self.historial_r.append(r)
        self.historial_fuerza.append(fuerza)

        fila = {"Ronda": len(self.historial_fuerza)}
        fila.update(detalle)
        fila["R (0 a 1)"] = round(r, 4)
        fila["Fuerza (0 a 1)"] = fuerza
        self.historial_proceso.append(fila)

        return fuerza

    def tabla_proceso(self):
        """Tabla con el cálculo interno de cada ronda para esta persona."""
        return pd.DataFrame(self.historial_proceso)
def von_neuman(seed):
    seeds_len=len(str(seed))
    temp=str(seed**2)
    if len(temp)<seeds_len*2:
        temp=temp.zfill(seeds_len*2)
    new_seed=temp[seeds_len//2:seeds_len//2+seeds_len]
    return int(new_seed)
def linear_congruential(seed,a,c,m):
    new_seed=(a*seed+c)%m
    return new_seed
