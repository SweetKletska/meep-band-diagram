
import meep as mp

# Параметры геометрии
eps = 13
w = 1.2
r = 0.36
sy = 12
dpml = 1.0
resolution = 20

cell = mp.Vector3(1, sy)

geometry = [
    mp.Block(size=mp.Vector3(mp.inf, w, mp.inf), material=mp.Medium(epsilon=eps)),
    mp.Cylinder(radius=r, center=mp.Vector3(0, 0))
]

fcen = 0.25
df = 1.5
sources = [
    mp.Source(src=mp.GaussianSource(fcen, fwidth=df), 
              component=mp.Hz, 
              center=mp.Vector3(0.1234, 0))
]

symmetries = [mp.Mirror(direction=mp.Y, phase=-1)]
pml_layers = [mp.PML(dpml, direction=mp.Y)]

sim = mp.Simulation(
    cell_size=cell,
    geometry=geometry,
    sources=sources,
    symmetries=symmetries,
    boundary_layers=pml_layers,
    resolution=resolution,
)

print("Начинаем расчет для 19 k-точек...", flush=True)

k_points = mp.interpolate(19, [mp.Vector3(0), mp.Vector3(0.5)])

print("Запуск run_k_points...", flush=True)
sim.run_k_points(300, k_points)

print("Расчет завершен!", flush=True)