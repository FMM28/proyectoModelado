import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from flask import Flask, render_template, request
from IPython.display import HTML

def simular(Lx=1.0, Ly=1.0, Nx=50, Ny=50, alpha=1e-4, dt=0.1, frames=200, tFuente=600, tAmbiente=300, tInicial=300, fuenteX=0.5, fuenteY=0.5):
    def actualizaTemperatura(malla):
        nuevaMalla = [row[:] for row in malla]
        for x in range(1, Nx-1):
            for y in range(1, Ny-1):
                nuevaMalla[x][y] = malla[x][y] + r_x * (malla[x+1][y] + malla[x-1][y] - 2 * malla[x][y]) + r_y * (malla[x][y+1] + malla[x][y-1] - 2 * malla[x][y])
        nuevaMalla[fuenteX][fuenteY] = tFuente
        return nuevaMalla
    
    def animar(frame):
        nonlocal malla
        malla = actualizaTemperatura(malla)
        im.set_data(malla)
        return [im]
    
    dx = Lx / (Nx - 1)
    dy = Ly / (Ny - 1)
    r_x = alpha * dt / dx**2
    r_y = alpha * dt / dy**2
    malla = [[tInicial for _ in range(Ny)] for _ in range(Nx)]
    for i in range(Nx):
        malla[i][0] = tAmbiente
        malla[i][Ny-1] = tAmbiente
    for j in range(Ny):
        malla[0][j] = tAmbiente
        malla[Nx-1][j] = tAmbiente
    fuenteX = int(fuenteX * (Nx - 1))
    fuenteY = int(fuenteY * (Ny - 1))
    
    fig, ax = plt.subplots()
    im = ax.imshow(malla, cmap='coolwarm', origin='lower', extent=[0, Lx, 0, Ly], vmin=0, vmax=1000)
    plt.colorbar(im, ax=ax, label='Temperatura (K)')

    ani = FuncAnimation(fig, animar, frames=frames, interval=50, blit=True)

    html_animation = HTML(ani.to_jshtml())  # Genera el HTML para la animación
    plt.close(fig)
    
    return html_animation.data 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    Lx = 1.0
    Ly = 1.0
    Nx = 50
    Ny = 50
    alpha = 1e-4
    dt = 0.1
    frames = 200
    tFuente = 600
    tAmbiente = 300
    tInicial = 300
    fuenteX = 0.5
    fuenteY = 0.5
    animacion_html = ""

    if request.method == "POST":
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

        animacion_html = simular(Lx, Ly, Nx, Ny, alpha, dt, frames, tFuente, tAmbiente, tInicial, fuenteX, fuenteY)

    return render_template("index.html", Lx=Lx, Ly=Ly, Nx=Nx, Ny=Ny, alpha=alpha, dt=dt, frames=frames, 
                           tFuente=tFuente, tAmbiente=tAmbiente, tInicial=tInicial, fuenteX=fuenteX, fuenteY=fuenteY, 
                           animacion_html=animacion_html)

if __name__ == "__main__":
    app.run('0.0.0.0', 8888, debug=True)