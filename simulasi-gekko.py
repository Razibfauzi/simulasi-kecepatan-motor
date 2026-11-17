"""Pemodelan & Simulasi Kecepatan Sepeda Motor """
import os
import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO

os.makedirs('gambar', exist_ok=True)

m_, c, rho, Cd, A, Crr, g = 170.0, 2.0, 1.2, 0.7, 0.6, 0.015, 9.81

m = GEKKO(remote=False)
ts = np.linspace(0, 150, 1501)
m.time = ts

ustep = np.zeros(1501)
ustep[50:500]   = 50.0
ustep[500:1000] = 100.0
u = m.Param(value=ustep)                   # bukaan gas (%)

v = m.Var(0.0)                             # kecepatan (m/s)
x = m.Var(0.0)                             # jarak (m)
k = 0.5 * rho * Cd * A
m.Equation(m_ * v.dt() == c * u - k * v**2 - Crr * m_ * g * m.tanh(v / 0.05))
m.Equation(x.dt() == v)

m.options.IMODE = 4
m.solve(disp=False)

plt.figure(figsize=(9, 5))
plt.subplot(2, 1, 1)
plt.plot(m.time, np.array(v.value) * 3.6, 'b-')
plt.ylabel('Kecepatan $v(t)$, (km/jam)'); plt.grid(True)
plt.subplot(2, 1, 2)
plt.plot(m.time, u.value, 'r--')
plt.ylabel('Bukaan Gas $u(t)$, (%)'); plt.xlabel('$t$, (s)'); plt.grid(True)
plt.tight_layout()
plt.savefig('gambar/grafik3_gekko.png', dpi=150)
plt.show()

# Bandingkan dengan hasil odeint
try:
    hasil = np.load('hasil_odeint.npy')
    selisih = np.max(np.abs(hasil[1] - np.array(v.value)))
    print(f'Selisih maksimum v (GEKKO vs odeint): {selisih:.4f} m/s')
except FileNotFoundError:
    print('Jalankan simulasi_odeint.py dahulu untuk membandingkan hasil.')"""Pemodelan & Simulasi Kecepatan Sepeda Motor - Metode GEKKO (IMODE=4, simulasi)"""
import os
import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO

os.makedirs('gambar', exist_ok=True)

m_, c, rho, Cd, A, Crr, g = 170.0, 2.0, 1.2, 0.7, 0.6, 0.015, 9.81

m = GEKKO(remote=False)
ts = np.linspace(0, 150, 1501)
m.time = ts

ustep = np.zeros(1501)
ustep[50:500]   = 50.0
ustep[500:1000] = 100.0
u = m.Param(value=ustep)                   # bukaan gas (%)

v = m.Var(0.0)                             # kecepatan (m/s)
x = m.Var(0.0)                             # jarak (m)
k = 0.5 * rho * Cd * A
m.Equation(m_ * v.dt() == c * u - k * v**2 - Crr * m_ * g * m.tanh(v / 0.05))
m.Equation(x.dt() == v)

m.options.IMODE = 4
m.solve(disp=False)

plt.figure(figsize=(9, 5))
plt.subplot(2, 1, 1)
plt.plot(m.time, np.array(v.value) * 3.6, 'b-')
plt.ylabel('Kecepatan $v(t)$, (km/jam)'); plt.grid(True)
plt.subplot(2, 1, 2)
plt.plot(m.time, u.value, 'r--')
plt.ylabel('Bukaan Gas $u(t)$, (%)'); plt.xlabel('$t$, (s)'); plt.grid(True)
plt.tight_layout()
plt.savefig('gambar/grafik3_gekko.png', dpi=150)
plt.show()

# Bandingkan dengan hasil odeint
try:
    hasil = np.load('hasil_odeint.npy')
    selisih = np.max(np.abs(hasil[1] - np.array(v.value)))
    print(f'Selisih maksimum v (GEKKO vs odeint): {selisih:.4f} m/s')
except FileNotFoundError:
    print('Jalankan simulasi_odeint.py dahulu untuk membandingkan hasil.')
