import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from flask import Flask, render_template, request, redirect, url_for

def simular(Lx=1.0, Ly=1.0, Nx=50, Ny=50, alpha=1e-4, dt=0.1, frames=200, tFuente=600, tAmbiente=300, tInicial=300, fuenteX=0.5, fuenteY=0.5):
    
    # Función para actualizar las temperaturas
    def actualizaTemperatura(malla):
        nuevaMalla = [row[:] for row in malla]

        for x in range(1, Nx-1):
            for y in range(1, Ny-1):
                nuevaMalla[x][y] = malla[x][y] + r_x * (malla[x+1][y] + malla[x-1][y] - 2 * malla[x][y]) + r_y * (malla[x][y+1] + malla[x][y-1] - 2 * malla[x][y])

        # Aplicar la fuente de calor
        nuevaMalla[fuenteX][fuenteY] = tFuente

        return nuevaMalla
    
    # Función de animación
    def animar(frame):
        nonlocal malla
        malla = actualizaTemperatura(malla)
        im.set_data(malla)
        return [im]
    
    # Calcular paso espacial y coeficiente de estabilidad
    dx = Lx / (Nx - 1)
    dy = Ly / (Ny - 1)
    r_x = alpha * dt / dx**2  # Coeficiente en la dirección x
    r_y = alpha * dt / dy**2  # Coeficiente en la dirección y

    # Inicialización de la malla
    malla = [[tInicial for _ in range(Ny)] for _ in range(Nx)]

    # Condiciones de frontera: Temperatura ambiente en los bordes
    for i in range(Nx):
        malla[i][0] = tAmbiente  # Borde izquierdo
        malla[i][Ny-1] = tAmbiente  # Borde derecho
    for j in range(Ny):
        malla[0][j] = tAmbiente  # Borde superior
        malla[Nx-1][j] = tAmbiente  # Borde inferior

    # Fuente de calor
    fuenteX = int(fuenteX * (Nx - 1))  # Ajustar la fuente a las dimensiones de la malla
    fuenteY = int(fuenteY * (Ny - 1))

    # Configuración de la animación
    fig, ax = plt.subplots()
    im = ax.imshow(malla, cmap='coolwarm', origin='lower', extent=[0, Lx, 0, Ly], vmin=0, vmax=1000)
    plt.colorbar(im, ax=ax, label='Temperatura (K)')

    ani = FuncAnimation(fig, animar, frames=frames, interval=50, blit=True)

    # Guardar la animación como archivo GIF
    ani.save("static/animacion.gif", writer=PillowWriter(fps=20))

# Código

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        # Obtener variables del formulario
        Lx = float(request.form["Lx"])
        Ly = float(request.form["Ly"])
        Nx = int(request.form["Nx"])
        Ny = int(request.form["Ny"])
        alpha = float(request.form["alpha"])
        dt = float(request.form["dt"])
        frames = int(request.form["frames"])
        tFuente = float(request.form["tFuente"])
        tAmbiente = float(request.form["tAmbiente"])
        tInicial = float(request.form["tInicial"])
        fuenteX = float(request.form["fuenteX"])
        fuenteY = float(request.form["fuenteY"])

        simular(Lx, Ly, Nx, Ny, alpha, dt, frames, tFuente, tAmbiente, tInicial, fuenteX, fuenteY)
        
        return redirect(url_for('index'))

    return render_template("index.html")

if __name__ == "__main__":
    app.run('0.0.0.0', 8888, debug=True)
