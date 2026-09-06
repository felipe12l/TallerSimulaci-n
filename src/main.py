
import os
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

from model.methods import Persona, generar_semilla_4_digitos, secuencia_larga

CARPETA_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
MARCA_TIEMPO = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
CARPETA_SALIDA = os.path.join(CARPETA_BASE, MARCA_TIEMPO)
os.makedirs(CARPETA_SALIDA, exist_ok=True)



def actualizar_posicion(posicion, suma_izq, suma_der, meta=5):
    """Mueve la cuerda según la diferencia de fuerzas.
    Si Izq > Der, la posición sube (hacia +5). Si Der > Izq, baja (hacia -5).
    La recta va de 5 a 0 a 5 (simétrica): la posición nunca puede pasarse
    de esos límites, así que se recorta (clamp) a [-meta, meta]."""
    diferencia = suma_izq - suma_der
    nueva_posicion = posicion + diferencia
    nueva_posicion = max(-meta, min(meta, nueva_posicion))
    return nueva_posicion


def jugar(personas_izq, personas_der, meta=5, max_rondas=200):
    posicion = 0
    filas_general = []
    ganador = None
    rondas_jugadas = 0

    for ronda in range(1, max_rondas + 1):
        fuerzas_izq = [p.siguiente_fuerza() for p in personas_izq]
        fuerzas_der = [p.siguiente_fuerza() for p in personas_der]

        suma_izq = sum(fuerzas_izq)
        suma_der = sum(fuerzas_der)

        posicion = actualizar_posicion(posicion, suma_izq, suma_der, meta)
        rondas_jugadas = ronda

        filas_general.append({
            "Ronda": ronda,
            "Suma Equipo Izquierdo": round(suma_izq, 2),
            "Suma Equipo Derecho": round(suma_der, 2),
            "Posición cuerda": round(posicion, 2)
        })

        if posicion >= meta:
            ganador = "Equipo Izquierdo"
            break
        elif posicion <= -meta:
            ganador = "Equipo Derecho"
            break

    if ganador is None:
        ganador = "No definido (se alcanzó el máximo de rondas)"

    tabla_general = pd.DataFrame(filas_general)
    return tabla_general, ganador, rondas_jugadas


def tabla_equipo(personas, nombre_equipo):
    """Tabla de 4 columnas por equipo: Ronda | Persona1 | Persona2 | Suma"""
    n = len(personas[0].historial_fuerza)
    filas = []
    for i in range(n):
        p1 = personas[0].historial_fuerza[i]
        p2 = personas[1].historial_fuerza[i]
        filas.append({
            "Ronda": i + 1,
            personas[0].nombre: p1,
            personas[1].nombre: p2,
            "Suma": round(p1 + p2, 2)
        })
    return pd.DataFrame(filas)



def diagrama_dispersion(numeros, titulo, archivo_salida):
    x = numeros[:-1]
    y = numeros[1:]
    plt.figure(figsize=(5, 5))
    plt.scatter(x, y, s=18, alpha=0.7, color="#3B6FA0")
    plt.title(titulo)
    plt.xlabel("Ri")
    plt.ylabel("Ri+1")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=150)
    plt.close()



if __name__ == "__main__":


    semilla_p1 = generar_semilla_4_digitos()
    semilla_p2 = generar_semilla_4_digitos()
    semilla_p3 = generar_semilla_4_digitos()
    semilla_p4 = generar_semilla_4_digitos()

    print("Semillas generadas (4 dígitos, una por persona):")
    print(f"  Persona 1 (impar -> Cuadrados Medios): {semilla_p1}")
    print(f"  Persona 2 (par   -> Congruencial):      {semilla_p2}")
    print(f"  Persona 3 (impar -> Cuadrados Medios): {semilla_p3}")
    print(f"  Persona 4 (par   -> Congruencial):      {semilla_p4}\n")

    persona1 = Persona("Persona1", "cuadrado_medio", semilla_p1)
    persona2 = Persona("Persona2", "congruencial", semilla_p2)
    persona3 = Persona("Persona3", "cuadrado_medio", semilla_p3)
    persona4 = Persona("Persona4", "congruencial", semilla_p4)

    equipo_izquierdo = [persona1, persona2]
    equipo_derecho = [persona3, persona4]


    tabla_general, ganador, rondas = jugar(equipo_izquierdo, equipo_derecho)

    print("=" * 70)
    print("TABLA GENERAL DEL JUEGO (4 columnas)")
    print("=" * 70)
    print(tabla_general.to_string(index=False))
    print(f"\n>> Ganador: {ganador}  |  Rondas jugadas: {rondas}\n")


    tabla_izq = tabla_equipo(equipo_izquierdo, "Izquierdo")
    tabla_der = tabla_equipo(equipo_derecho, "Derecho")

    print("=" * 70)
    print("TABLA EQUIPO IZQUIERDO (Persona1=Cuadrado Medio, Persona2=Congruencial)")
    print("=" * 70)
    print(tabla_izq.to_string(index=False))

    print("\n" + "=" * 70)
    print("TABLA EQUIPO DERECHO (Persona3=Cuadrado Medio, Persona4=Congruencial)")
    print("=" * 70)
    print(tabla_der.to_string(index=False))

    print("\n" + "=" * 70)
    print("PROCESO INTERNO POR PERSONA (para que sea visible el cálculo)")
    print("=" * 70)
    for p in [persona1, persona2, persona3, persona4]:
        tabla_proc = p.tabla_proceso()
        print(f"\n--- {p.nombre} ({p.metodo}, semilla inicial={p.semilla_inicial}) ---")
        print(tabla_proc.to_string(index=False))
        tabla_proc.to_csv(os.path.join(CARPETA_SALIDA, f"proceso_{p.nombre.lower()}.csv"), index=False)

  
    tabla_general.to_csv(os.path.join(CARPETA_SALIDA, "tabla_general.csv"), index=False)
    tabla_izq.to_csv(os.path.join(CARPETA_SALIDA, "tabla_equipo_izquierdo.csv"), index=False)
    tabla_der.to_csv(os.path.join(CARPETA_SALIDA, "tabla_equipo_derecho.csv"), index=False)

    seq_cuadrado_medio = secuencia_larga("cuadrado_medio", semilla_p1, n=200)
    seq_congruencial = secuencia_larga("congruencial", semilla_p2, n=200)

    diagrama_dispersion(seq_cuadrado_medio, "Dispersión - Cuadrados Medios",
                         os.path.join(CARPETA_SALIDA, "dispersion_cuadrados_medios.png"))
    diagrama_dispersion(seq_congruencial, "Dispersión - Congruencia Lineal",
                         os.path.join(CARPETA_SALIDA, "dispersion_congruencia_lineal.png"))

    print(f"\nArchivos de esta corrida guardados en: {CARPETA_SALIDA}")
    print(f"(Cada corrida crea su propia carpeta con fecha y hora dentro de: {CARPETA_BASE})")

    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    if ganador == "Equipo Izquierdo":
        print("#" + " Gana: EQUIPO IZQUIERDO (Persona1 y Persona2)".center(68) + "#")
    elif ganador == "Equipo Derecho":
        print("#" + "Gana EQUIPO DERECHO (Persona3 y Persona4)".center(68) + "#")
    else:
        print("#" + f"   {ganador}".center(68) + "#")
    print("#" + " " * 68 + "#")
    print(f"#   Rondas jugadas: {rondas}".ljust(69) + "#")
    print(f"#   Posición final de la cuerda: {tabla_general['Posición cuerda'].iloc[-1]}".ljust(69) + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)
