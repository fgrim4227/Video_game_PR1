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

---
**Pong:**

* **Jugador 1:** `W` (Subir) y `S` (Bajar).


* **Jugador 2:** `Flecha Arriba` y `Flecha Abajo`.
---
**Flappy Bird:**

* **Volar / Saltar:** Clic Izquierdo del Ratón
* **Pausa:** Tecla `P`
* **Modo Difícil (Movimiento Horizontal):** Teclas `A` y `D`
---
**Breakout:**
**Flechas Izquierda / Derecha:** Mover la paleta.
* **Enter:** Iniciar el juego / Confirmar selecciones / Sacar la pelota.
* **G:** Pausar / Reanudar el juego.
* **Espacio:** Disparar la pelota atrapada (Power-Up: Captura de Pelota).
* **D:** Disparar misiles (Power-Up: Cañones).
* **F:** Activar la cámara lenta (Power-Up: Manipulación Temporal).
* **Escape:** Salir del juego.

---

## ✨ Sistema de Power-Ups de BreakOut

Durante el juego, al destruir ladrillos, existe la posibilidad de que caigan diversos ítems. La interfaz en la esquina superior izquierda te indicará visualmente cuáles tienes activos y cuánto tiempo te queda de uso mediante una barra de progreso.

### 1. Two More Balls (Clásico)
Añade instantáneamente dos pelotas adicionales a la partida, con trayectorias y velocidades aleatorias, facilitando la limpieza rápida de la pantalla. No tiene duración límite, las pelotas extra permanecen hasta que caen al vacío.

### 2. Captura de Pelota (Grab Balls)
Permite que la paleta adquiera propiedades magnéticas durante 7 segundos. 
* **Efecto:** Al impactar contra la paleta, la pelota no rebota, sino que queda adherida y copia el movimiento horizontal del jugador.
* **Uso:** Presiona la tecla **Espacio** para volver a lanzar la pelota con un nuevo ángulo cuando consideres oportuno, toma en cuenta tu dirreccion y velocidad.

### 3. Cañones Perforadores (Missiles)
Equipa la paleta con un par de cañones en los extremos durante 8 segundos.
* **Efecto:** Al presionar la tecla **D**, se disparan dos misiles verticales simultáneos. Estos proyectiles destruyen todos los bloques que encuentren en su trayectoria de forma consecutiva hasta impactar con el techo.
* **Regla:** Solo puede haber un par de misiles activos en pantalla a la vez.

### 4. Manipulación Temporal ⏳ (Slow Time) - *[Power-Up Adicional]*
Un ítem táctico de doble fase que permite ralentizar el tiempo.
* **Fase 1 (Reserva):** Al recoger el ítem, tendrás una ventana de 30 segundos donde el poder estará "guardado" y listo para usarse.
* **Fase 2 (Ejecución):** Al presionar la tecla **F** dentro de esa ventana de tiempo, se activa una cámara lenta de 6 segundos. La velocidad de las pelotas se reduce drásticamente, permitiendo al jugador alcanzar ángulos difíciles o reaccionar a situaciones de peligro, mientras que la paleta mantiene su velocidad normal de respuesta.

**General:**

* **Cerrar cualquier juego:** Tecla `Esc`.
---
**Match 3:**
* **Intercambiar Piezas (Drag & Drop):** Mantén presionado el Clic Izquierdo sobre una pieza y arrástrala hacia una posición adyacente para intercambiarla, el intercambio sera valido si es un match de al menos 3 tiles, sino la tile se devolvera a su posicion original con el sonido de error.
* **Activar Power-Up Manualmente:** Clic Izquierdo directamente sobre la pieza especial sin arrastrarla.
* **Alternar Casos de Prueba (si se descomenta el manejo del input):** Tecla `R` para rotar entre los escenarios de demostración (Tablero Normal, Match-4, Reacción en Cadena, Sin Movimientos y Explosión Masiva).
---
---

## Mecánicas y Power-Ups de Match 3

### 1. Sistema de Asistencia y Rescate
* **Pistas Visuales (Hint):** Si el jugador pasa 10 segundos sin realizar un movimiento o sin dar click, un recuadro dorado titilante resaltará la posición exacta de un movimiento válido.
* **Auto-Activación y Reinicio:** Si el tablero se queda sin movimientos posibles, el sistema buscará los Power-Ups que hayan quedado en el tablero y los detonará en cadena para intentar generar nuevas combinaciones. Si tras la explosión sigue sin haber movimientos, la pantalla mostrará una alerta y el tablero se reiniciará automáticamente (tambien pausara el temporizador mientras se esta en la transicion para no descontar tiempo injustamente).

### 2. Limpia-Líneas (Match-4)
* **Generación:** Se crea automáticamente al lograr una coincidencia de exactamente 4 baldosas en la casilla de la pieza movida por el player para el match o si fue por caida en cualquiera de las casillas usadas para hacer el match.
* **Efecto:** Al activarse mediante un clic directo o al ser combinado con su color, dispara una explosión en cruz que destruye por completo toda su fila y su columna activando power ups antes de destruirlos si fueron alcanzados.

### 3. Bomba de Color (Match-5+)
* **Generación:** Se crea al lograr una coincidencia de 5 o más baldosas.
* **Efecto:** Al detonarse, rastrea el tablero y destruye absolutamente todas las baldosas que compartan su color. Si la explosión de esta bomba alcanza a un "Limpia-Líneas" u otro Power-Up, estos también se activarán, generando reacciones en cadena masivas.
