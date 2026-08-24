# Programación de Videojuegos I - Repositorio de Proyectos

Este repositorio contiene la colección de videojuegos desarrollados durante la asignatura de Programación de Videojuegos 1. Cada juego está contenido en su propia carpeta y funciona de manera independiente, utilizando una base tecnológica compartida.

**Créditos del Código Base:** La estructura fundamental y el motor de los juegos toman como punto de partida los recursos provistos por el profesor en el repositorio oficial del curso: [R3mmurd/VideoGameProgrammingI](https://github.com/R3mmurd/VideoGameProgrammingI).

---

## Estructura del Repositorio

El repositorio está dividido en carpetas individuales para cada proyecto. Por ejemplo:
* `01-pong/`: Implementación del clásico Pong con Inteligencia Artificial predictiva y Modos de Juego.
* `02-flappy_bird/`: Version de Flappy Bird con generación procedural, patrón Strategy para Modos de Juego (Fácil/Difícil), obstáculos dinámicos y power-ups.
* *(Nuevos proyectos se irán añadiendo en sus respectivas carpetas)*.

---

## Requisitos del Sistema

Para garantizar la correcta ejecución de cualquiera de los juegos, asegúrate de cumplir con los siguientes requisitos:

*   **Python:** `3.11` o superior.
*   **Git:** Para clonar el repositorio en tu máquina local.

---

## Guía de Instalación Global

El proceso de instalación se realiza **una sola vez** en la raíz del repositorio. Sigue estos pasos para descargar, configurar y preparar el entorno virtual de forma segura.

### 1. Clonar el repositorio

Descarga el código fuente en tu máquina local abriendo una terminal y ejecutando:

```bash
git clone https://github.com/fgrim4227/Video_game_PR1.git
cd tu_repositorio

```

### 2. Crear y activar el entorno virtual

Es altamente recomendado usar un entorno virtual para instalar las dependencias del motor gráfico sin afectar tu sistema operativo.

**En Windows (Command Prompt / PowerShell):**

```cmd
python -m venv .venv
.\.venv\Scripts\activate

```

**En Linux / macOS / WSL:**

```bash
python3 -m venv .venv
source .venv/bin/activate

```

### 3. Instalar las dependencias

Con el entorno virtual activado `(venv)`, instala el motor `gale` y las librerías necesarias ejecutando:

```bash
pip install -r requirements.txt

```

---

## Cómo Ejecutar los Juegos

Una vez que el entorno virtual esté activado y las dependencias instaladas, puedes jugar a cualquier título del repositorio navegando a su carpeta y ejecutando su archivo principal.

Por ejemplo, para jugar **Flappy Bird**:

```bash
# 1. Entra a la carpeta del juego
cd 02-flappy_bird

# 2. Ejecuta el archivo principal
python main.py

```

Para cambiar de juego, simplemente vuelve a la raíz del repositorio y entra a la otra carpeta:

```bash
cd ..
cd 01-pong
python main.py

```

---

## Controles Rápidos

**Menús (General):**

* **Navegar:** Teclas `Flecha Izquierda`/`Flecha Derecha` o `W`/`S` (dependiendo del juego).


* **Confirmar:** `Enter`.



**Flappy Bird:**

* **Volar / Saltar:** Clic Izquierdo del Ratón
* **Pausa:** Tecla `P`
* **Modo Difícil (Movimiento Horizontal):** Teclas `A` y `D`

**Pong:**

* **Jugador 1:** `W` (Subir) y `S` (Bajar).


* **Jugador 2:** `Flecha Arriba` y `Flecha Abajo`.



**General:**

* **Cerrar cualquier juego:** Tecla `Esc`.
