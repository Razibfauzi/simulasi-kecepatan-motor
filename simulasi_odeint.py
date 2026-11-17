"""Pemodelan & Simulasi Sistem Dinamik: Kecepatan Sepeda Motor dengan Hambatan Udara
Metode: SciPy odeint
Persamaan: m dv/dt = c*u - 0.5*rho*Cd*A*v^2 - Crr*m*g ;  dx/dt = v
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

os.makedirs('gambar', exist_ok=True)

# ---------- Parameter ----------
m   = 170.0   # massa motor + pengendara (kg)
c   = 2.0     # konstanta gaya dorong (N per % bukaan gas)
rho = 1.2     # massa jenis udara (kg/m^3)
Cd  = 0.7     # koefisien hambat aerodinamis
A   = 0.6     # luas frontal (m^2)
Crr = 0.015   # koefisien hambatan gelinding
g   = 9.81    # percepatan gravitasi (m/s^2)

# ---------- Model ----------
def motor(z, t, u, Cd=Cd):
    v, x = z
    F_dorong = c * u                       # gaya dorong mesin (N)
    F_udara  = 0.5 * rho * Cd * A * v**2   # gaya hambat udara (N)
    F_roda   = Crr * m * g                 # hambatan gelinding (N)
    dvdt = (F_dorong - F_udara - F_roda) / m
    if v <= 0 and dvdt < 0:                # motor diam tidak bergerak mundur
        dvdt = 0.0
    dxdt = v
    return [dvdt, dxdt]

# ---------- Waktu & input bukaan gas ----------
ts = np.linspace(0, 150, 1501)             # 0-150 s, setiap 0.1 s
u = np.zeros(1501)
u[50:500]   = 50.0                         # 5 s - 50 s  : gas 50%
u[500:1000] = 100.0                        # 50 s - 100 s: gas 100%
                                           # 100 s - 150 s: gas dilepas (0%)

# ---------- Simulasi ----------
z0 = [0.0, 0.0]                            # v(0)=0 m/s, x(0)=0 m
v = np.zeros(1501)
x = np.zeros(1501)
for i in range(1500):
    y = odeint(motor, z0, [0, 0.1], args=(u[i],))
    z0 = y[-1]
    v[i + 1], x[i + 1] = z0

# ---------- Plot ----------
plt.figure(figsize=(9, 8))
plt.subplot(3, 1, 1)
plt.plot(ts, v * 3.6, 'b-')
plt.ylabel('Kecepatan $v(t)$, (km/jam)'); plt.grid(True)
plt.subplot(3, 1, 2)
plt.plot(ts, x / 1000, 'g-')
plt.ylabel('Jarak $x(t)$, (km)'); plt.grid(True)
plt.subplot(3, 1, 3)
plt.plot(ts, u, 'r--')
plt.ylabel('Bukaan Gas $u(t)$, (%)'); plt.xlabel('$t$, (s)'); plt.grid(True)
plt.tight_layout()
plt.savefig('gambar/grafik1_simulasi_utama.png', dpi=150)
plt.show()

# ---------- Kecepatan steady state (hitungan analitik) ----------
for ub in (50, 100):
    vss = np.sqrt((c * ub - Crr * m * g) / (0.5 * rho * Cd * A))
    print(f'u = {ub}% -> v_ss = {vss:.2f} m/s = {vss*3.6:.1f} km/jam')
print(f'Kecepatan pada t=50 s : {v[500]*3.6:.1f} km/jam')
print(f'Kecepatan pada t=100 s: {v[1000]*3.6:.1f} km/jam')
print(f'Kecepatan pada t=150 s: {v[1500]*3.6:.1f} km/jam')
print(f'Jarak total           : {x[-1]/1000:.2f} km')

# ---------- Pengaruh koefisien hambat Cd (gas 100% tetap) ----------
ts2 = np.linspace(0, 100, 1001)
plt.figure(figsize=(8, 4.5))
for Cd_var, gaya, lbl in [(0.5, 'r-', 'Cd = 0.5'), (0.7, 'b--', 'Cd = 0.7'), (0.9, 'g:', 'Cd = 0.9')]:
    sol = odeint(motor, [0, 0], ts2, args=(100.0, Cd_var))
    plt.plot(ts2, sol[:, 0] * 3.6, gaya, label=lbl)
plt.xlabel('$t$, (s)'); plt.ylabel('Kecepatan $v(t)$, (km/jam)')
plt.legend(frameon=False); plt.grid(True); plt.tight_layout()
plt.savefig('gambar/grafik2_variasi_Cd.png', dpi=150)
plt.show()

np.save('hasil_odeint.npy', np.vstack([ts, v, x, u]))
