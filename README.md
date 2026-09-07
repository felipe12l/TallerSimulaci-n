# Taller de simulación

Simulación de un juego de tira y afloja entre dos equipos. Cada persona genera
una fuerza pseudoaleatoria usando uno de dos métodos de generación de números
aleatorios:

- **Cuadrados medios** (método de von Neumann).
- **Congruencia lineal**.

El programa registra el cálculo interno de cada persona, actualiza la posición
de la cuerda ronda por ronda, determina el equipo ganador y guarda los
resultados en archivos CSV y gráficas de dispersión.

## Requisitos

- Python 3.
- `pandas`.
- `matplotlib`.

No hay un `requirements.txt` en el proyecto. Las dependencias pueden instalarse
con:

```bash
python -m pip install pandas matplotlib
```

Se recomienda trabajar dentro de un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate
python -m pip install pandas matplotlib
```

En Windows, la activación equivalente es:

```powershell
venv\Scripts\activate
```

## Ejecución

Desde la raíz del repositorio:

```bash
python src/main.py
```

El programa imprime en la terminal:

1. Las cuatro semillas generadas.
2. La tabla general de cada ronda.
3. La tabla de fuerzas de cada equipo.
4. El proceso interno de generación de cada persona.
5. El ganador, el número de rondas y la posición final de la cuerda.
6. La carpeta donde se guardaron los resultados.

Cada ejecución genera una carpeta nueva con la fecha y hora dentro de
`src/resultados/`, usando el formato:

```text
src/resultados/YYYY-MM-DD_HH-MM-SS/
```

Las semillas se generan aleatoriamente con valores enteros de cuatro dígitos,
por lo que dos ejecuciones normalmente producen resultados diferentes.

## Reglas de la simulación

La configuración actual crea cuatro personas y dos equipos:

| Persona | Método | Equipo |
| --- | --- | --- |
| Persona1 | Cuadrados medios | Izquierdo |
| Persona2 | Congruencia lineal | Izquierdo |
| Persona3 | Cuadrados medios | Derecho |
| Persona4 | Congruencia lineal | Derecho |

En cada ronda:

1. Cada persona genera un número `R` entre 0 y 1.
2. La fuerza de la persona es `R` redondeado a dos decimales.
3. Se suman las fuerzas de cada equipo.
4. La posición de la cuerda se actualiza con:

	 ```text
	 nueva_posición = posición_actual + suma_izquierda - suma_derecha
	 ```

5. La posición se limita al intervalo `[-5, 5]`.

El equipo izquierdo gana cuando la posición llega a `5`. El equipo derecho gana
cuando llega a `-5`. Si ningún equipo alcanza su meta, la simulación termina
después de 200 rondas y el resultado queda como **No definido**.

## Métodos de generación

### Cuadrados medios

Partiendo de una semilla de cuatro dígitos `X`:

1. Se calcula `X²`.
2. El resultado se rellena con ceros hasta tener ocho dígitos.
3. Se extraen los cuatro dígitos centrales para obtener el nuevo estado.
4. Se calcula `R = nuevo_estado / 10⁴`.

Ejemplo del proceso almacenado en los CSV:

```text
X anterior = 1754
X²         = 03076516
central    = 0765
R          = 0.0765
fuerza     = 0.08
```

### Congruencia lineal

El método usa los parámetros fijos:

```text
a = 7141
c = 54773
m = 259200
```

En cada paso se calcula:

```text
X nuevo = (a * X anterior + c) mod m
R       = X nuevo / m
```

La fuerza usada en el juego vuelve a redondearse a dos decimales.

## Archivos generados

Cada ejecución guarda los siguientes archivos en su carpeta de resultados:

### `tabla_general.csv`

Contiene una fila por ronda:

| Columna | Descripción |
| --- | --- |
| `Ronda` | Número de ronda. |
| `Suma Equipo Izquierdo` | Fuerza total del equipo izquierdo. |
| `Suma Equipo Derecho` | Fuerza total del equipo derecho. |
| `Posición cuerda` | Posición acumulada después de la ronda. |

### `tabla_equipo_izquierdo.csv` y `tabla_equipo_derecho.csv`

Contienen la fuerza de cada persona y la suma del equipo por ronda. Por
ejemplo, el archivo del equipo izquierdo incluye `Ronda`, `Persona1`,
`Persona2` y `Suma`.

### `proceso_persona1.csv` a `proceso_persona4.csv`

Exponen el detalle de cada paso del generador usado por la persona. Incluyen
la ronda, el estado anterior, la operación realizada, el valor `R` y la fuerza
redondeada. Las columnas de la operación cambian según el método:

- Cuadrados medios: `X al cuadrado (relleno a 8 dígitos)` y
	`Dígitos centrales extraídos`.
- Congruencia lineal: `a·X + c`, `mod m` y `X nuevo`.

### Gráficas PNG

También se generan dos gráficas de dispersión de pares consecutivos
`(Rᵢ, Rᵢ₊₁)` a partir de secuencias de 200 valores:

- `dispersion_cuadrados_medios.png`.
- `dispersion_congruencia_lineal.png`.

Las gráficas usan la semilla de `Persona1` para cuadrados medios y la de
`Persona2` para congruencia lineal. Sirven para observar visualmente la
distribución y posibles patrones entre valores consecutivos.

## Estructura del proyecto

```text
.
├── README.md
└── src/
		├── __init__.py
		├── main.py
		├── controller/
		│   └── simulationController.py
		├── model/
		│   └── methods.py
		├── resultados/
		│   └── YYYY-MM-DD_HH-MM-SS/
		│       ├── tabla_general.csv
		│       ├── tabla_equipo_izquierdo.csv
		│       ├── tabla_equipo_derecho.csv
		│       ├── proceso_persona1.csv
		│       ├── proceso_persona2.csv
		│       ├── proceso_persona3.csv
		│       ├── proceso_persona4.csv
		│       ├── dispersion_cuadrados_medios.png
		│       └── dispersion_congruencia_lineal.png
		└── views/
```

### Responsabilidades principales

- `src/main.py`: coordina la ejecución, la simulación, la impresión y la
	exportación de resultados.
- `src/model/methods.py`: implementa los generadores, la clase `Persona` y las
	tablas del proceso interno.
- `src/controller/simulationController.py`: contiene actualmente un método
	`simulate` sin implementación.
- `src/views/`: está reservado para vistas y actualmente no contiene una
	interfaz implementada.
- `test/`: está reservado para pruebas y actualmente está vacío.

## Notas de desarrollo

- La posición inicial de la cuerda es `0`.
- El objetivo está fijado en `5` unidades hacia cualquiera de los lados.
- El máximo de rondas está fijado en `200`.
- Los valores usados como fuerza son los valores `R` redondeados a dos
	decimales; el proceso interno conserva `R` con cuatro decimales.
- Las carpetas de `src/resultados/` son salidas de ejecuciones anteriores.
- `venv/` está ignorado por Git mediante `.gitignore`.

## Estado actual

La simulación principal funciona ejecutando `src/main.py`. La separación en
controlador y vistas todavía está preparada como estructura, pero la ejecución
actual se concentra en `main.py`. No existe todavía una batería automatizada de
pruebas ni una configuración de empaquetado del proyecto.
