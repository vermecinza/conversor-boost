## Importando bibliotecas
import numpy as np
import matplotlib.pyplot as plt

## Definição dos parâmetros alterados - 
Vin = 48.0            # Tensão de entrada  (V) - bateria 48V
Vout = 200.0          # Tensão de saída  (V) - para sistema de 200V
Pout = 800.0          # Potência máxima na saída  (W)
Fs = 100e3            # Frequência de chaveamento  (Hz) - 100 kHz
Ts = 1 / Fs           # Período de chaveamento (s)
VIl = 0.25            # Ondulação da corrente no indutor  (%)
VVl = 0.015           # Ondulação da tensão no capacitor  (%)

## Cálculo dos valores nominais e dimensionamento de componentes
D = 1 - (Vin / Vout)      # Razão Cíclica para conversor Boost
Iout = Pout / Vout        # Corrente de saída
Iin = Pout / Vin          # Corrente de entrada
R = (Vout**2) / Pout      # Resistência da carga
L = (Vin * D) / (Fs * VIl * Iin)   # Indutância de entrada
C = (Iout * D) / (Fs * VVl * Vout) # Capacitância de saída

print(f"Parâmetros calculados:")
print(f"Razão cíclica D = {D:.3f}")
print(f"Indutor L = {L*1e6:.2f} µH")
print(f"Capacitor C = {C*1e6:.2f} µF")
print(f"Resistência R = {R:.2f} Ω")
print(f"Corrente de entrada Iin = {Iin:.2f} A")
print(f"Corrente de saída Iout = {Iout:.2f} A")

# Tempo de simulação: 15 ms para ver o amortecimento
t_end = 15e-3       # 15 ms
dt = Ts / 200       # subdividindo cada período em 200 passos
t = np.arange(0, t_end, dt)

# Vetores de simulação
iL = np.zeros_like(t)     # Corrente do indutor
vO = np.zeros_like(t)     # Tensão do capacitor/saída

# Condições iniciais
iL[0] = 0.0
vO[0] = 0.0

# Loop de simulação usando Euler Explícito
for k in range(len(t) - 1):
    t_cycle = t[k] % Ts
    
    # Determinar estado da chave (ON ou OFF)
    if t_cycle < D * Ts:
        # Estado ON: Chave fechada
        vL = Vin           # Tensão no indutor = Vin
        iC = -vO[k] / R   # Corrente no capacitor = - corrente na carga
    else:
        # Estado OFF: Chave aberta  
        vL = Vin - vO[k]   # Tensão no indutor = Vin - Vout
        iC = iL[k] - vO[k] / R  # Corrente no capacitor = iL - iR
    
    # Método de Euler Explícito para o indutor
    iL[k + 1] = iL[k] + (vL / L) * dt
    
    # Método de Euler Explícito para o capacitor
    vO[k + 1] = vO[k] + (iC / C) * dt

# Plot apenas da tensão de saída
plt.figure(figsize=(12, 6))
plt.plot(t * 1e3, vO, 'b-', linewidth=1.5, label='Tensão de Saída (vout)')
plt.axhline(Vout, color='red', linestyle='--', label=f'Tensão Desejada = {Vout:.1f} V')
plt.title(f'Resposta do Conversor Boost ({Vin} V → {Vout} V, {Pout} W)')
plt.xlabel('Tempo (ms)')
plt.ylabel('Tensão (V)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()