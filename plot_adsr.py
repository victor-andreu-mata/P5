import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('img', exist_ok=True)

SR = 44100

def make_adsr(A, D, S, R, t_hold, t_total):
    n_total = int(t_total * SR)
    n_A     = int(A * SR)
    n_D     = int(D * SR)
    n_hold  = int(t_hold * SR)
    n_R     = int(R * SR)

    env = np.zeros(n_total)

    # Calcular nivel en cada muestra
    for n in range(n_total):
        if n < n_A:
            env[n] = n / max(n_A, 1)
        elif n < n_A + n_D:
            env[n] = 1.0 - (1.0 - S) * (n - n_A) / max(n_D, 1)
        else:
            env[n] = S

    # Calcular nivel exacto cuando se suelta la tecla
    release_start = env[min(n_hold, n_total - 1)]

    # Aplicar release desde t_hold
    for n in range(n_hold, min(n_hold + n_R, n_total)):
        env[n] = release_start * (1.0 - (n - n_hold) / max(n_R, 1))
    for n in range(n_hold + n_R, n_total):
        env[n] = 0.0

    t = np.arange(n_total) / SR
    return t, env


fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle('Envolventes ADSR', fontsize=14, fontweight='bold')

# ── 1. Genérica ───────────────────────────────────────────────────────────────
ax = axes[0, 0]
A, D, S, R = 0.10, 0.15, 0.6, 0.20
t_hold = 0.50
t, env = make_adsr(A, D, S, R, t_hold, t_hold + R + 0.05)
ax.plot(t, env, color='steelblue', linewidth=2)
ax.axvline(t_hold, color='gray', linestyle='--', linewidth=1, label='Key release')
ax.annotate('', xy=(A, 1.02), xytext=(0, 1.02),
            arrowprops=dict(arrowstyle='<->', color='tomato'))
ax.text(A/2, 1.07, f'A={A}s', ha='center', color='tomato', fontsize=9)
ax.annotate('', xy=(A+D, S-0.07), xytext=(A, S-0.07),
            arrowprops=dict(arrowstyle='<->', color='green'))
ax.text(A+D/2, S-0.15, f'D={D}s', ha='center', color='green', fontsize=9)
ax.axhline(S, color='purple', linestyle=':', linewidth=1)
ax.text(0.01, S+0.04, f'S={S}', color='purple', fontsize=9)
ax.annotate('', xy=(t_hold+R, -0.08), xytext=(t_hold, -0.08),
            arrowprops=dict(arrowstyle='<->', color='darkorange'))
ax.text(t_hold+R/2, -0.16, f'R={R}s', ha='center', color='darkorange', fontsize=9)
ax.set_title('1. Envolvente genérica')
ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud')
ax.set_ylim(-0.25, 1.2); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

# ── 2. Percusivo — extinción natural ─────────────────────────────────────────
ax = axes[0, 1]
A, D, S, R = 0.005, 0.35, 0.0, 0.01
t_hold = 0.80   # tecla pulsada mucho tiempo, el sonido ya se ha apagado
t, env = make_adsr(A, D, S, R, t_hold, 0.85)
ax.plot(t, env, color='steelblue', linewidth=2)
ax.axvline(t_hold, color='gray', linestyle='--', linewidth=1, label='Key release (tarde)')
ax.annotate('', xy=(A+D, -0.10), xytext=(A, -0.10),
            arrowprops=dict(arrowstyle='<->', color='green'))
ax.text(A+D/2, -0.18, f'D={D}s (extinción natural)', ha='center', color='green', fontsize=8)
ax.text(0.10, 0.55, 'S=0\n(sin mantenimiento)', color='purple', fontsize=9)
ax.set_title('2. Percusivo — extinción natural')
ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud')
ax.set_ylim(-0.28, 1.2); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

# ── 3. Percusivo — nota cortada antes de extinción ───────────────────────────
ax = axes[1, 0]
A, D, S, R = 0.005, 0.60, 0.0, 0.05
t_hold = 0.20
t, env = make_adsr(A, D, S, R, t_hold, t_hold + R + 0.10)
ax.plot(t, env, color='steelblue', linewidth=2)
ax.axvline(t_hold, color='gray', linestyle='--', linewidth=1, label='Key release (pronto)')
# Flecha señalando la caída
idx_hold = int(t_hold * SR)
ax.annotate('Caída abrupta\nal soltar tecla',
            xy=(t_hold + 0.01, env[idx_hold + int(0.01*SR)]),
            xytext=(t_hold + 0.04, env[idx_hold] + 0.15),
            arrowprops=dict(arrowstyle='->', color='tomato'),
            fontsize=9, color='tomato')
ax.set_title('3. Percusivo — nota cortada antes de extinción')
ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud')
ax.set_ylim(-0.15, 1.2); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

# ── 4. Plano (violín/viento) ──────────────────────────────────────────────────
ax = axes[1, 1]
A, D, S, R = 0.08, 0.0, 1.0, 0.08
t_hold = 0.50
t, env = make_adsr(A, D, S, R, t_hold, t_hold + R + 0.05)
ax.plot(t, env, color='steelblue', linewidth=2)
ax.axvline(t_hold, color='gray', linestyle='--', linewidth=1, label='Key release')
ax.annotate('', xy=(A, 1.02), xytext=(0, 1.02),
            arrowprops=dict(arrowstyle='<->', color='tomato'))
ax.text(A/2, 1.07, f'A={A}s', ha='center', color='tomato', fontsize=8)
ax.axhline(S, color='purple', linestyle=':', linewidth=1)
ax.text(0.01, S+0.04, f'S={S} (nivel plano)', color='purple', fontsize=9)
ax.text(0.25, 0.5, 'D=0\n(sin caída)', color='green', fontsize=9)
ax.annotate('', xy=(t_hold+R, -0.08), xytext=(t_hold, -0.08),
            arrowprops=dict(arrowstyle='<->', color='darkorange'))
ax.text(t_hold+R/2, -0.16, f'R={R}s', ha='center', color='darkorange', fontsize=8)
ax.set_title('4. Instrumento plano (violín/viento)')
ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud')
ax.set_ylim(-0.25, 1.2); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('img/adsr_envelopes.png', dpi=150, bbox_inches='tight')
print("Guardado en img/adsr_envelopes.png")