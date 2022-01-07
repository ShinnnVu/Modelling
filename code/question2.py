import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
choose = int(input("SIR or SIRD? Press 1 to choose SIR, otherwise press 2\n"))
# Number of people
N = float(input("Number of individuals: "))
# Time t
t = int(input("Time: "))
#Beta, gamma
beta = float(input("Beta: "))
gamma = float(input("Gamma: "))
if (choose == 2):
    phi = float(input("Phi: "))
# Initial cases of infected I0 and recovered R0 individuals
I0 = float(input("Initial number of Infected: "))
R0 = float(input("Initial number of Recovered: "))
D0 = 0
if (choose == 2):
    D0 = float(input("Initial number of Deceased: "))
S0 = float(N-I0-R0)


def SIR(y, t, N, beta, gamma):
    S, I, R = y
    dS_dt = -(beta/N) * I * S
    dI_dt = (beta/N) * I * S - gamma * I
    dR_dt = gamma * I
    # return dS_dt, dI_dt, dR_dt
    return dS_dt, dI_dt, dR_dt


def SIRD(y, t, N, beta, gamma, phi):
    S, I, R, D = y
    dS_dt = -(beta/N) * I * S
    dI_dt = (beta/N) * I * S - (gamma * I) - (phi * I)
    dR_dt = gamma * I
    dD_dt = phi * I
    # return dS_dt, dI_dt, dR_dt
    return dS_dt, dI_dt, dR_dt, dD_dt


t = np.linspace(0, t, t+1)
if (choose == 1):
    y0 = S0, I0, R0
    result = odeint(SIR, y0, t, args=(N, beta, gamma))
    S, I, R = result.T
else:
    y0 = S0, I0, R0, D0
    result = odeint(SIRD, y0, t, args=(N, beta, gamma, phi))
    S, I, R, D = result.T

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered')
if (choose == 2):
    ax.plot(t, D, 'y', alpha=0.5, lw=2, label='Deceased')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number')
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()