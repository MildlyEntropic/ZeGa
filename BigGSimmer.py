import scipy.integrate

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


# Constants
c = 3.00e8
G_newton = 6.6740000000e-11
G_qing_li = 6.6741840000e-11
G_ferreira = 6.6743000000e-11
m = 0.5e-3
initial_distance = 0.1

# Label constants
NEWTON_G_LABEL = "Newton's G"
QING_LI_G_LABEL = "Qing Li et al.'s G"
FERREIRA_G_LABEL = "Ferreira's G"
BRANS_DICKE_G_LABEL = "Brans-Dicke's G"
PENROSE_G_LABEL = "Penrose's G"

V = 1.7
I = 0.02
efficiency = 0.3

Pe = I * V

radius_LED = 0.0015
radius_circuit = 0.03
A_LED = np.pi * radius_LED**2
A_Light = np.pi * radius_circuit**2
r = 0.0035
R = 0.8

Int_m = Pe * efficiency * (A_LED / A_Light)

A_m = np.pi * r**2

F_l = (1 + R) * Int_m * A_m / c

def g_brans_dicke(r):
    G0 = G_newton
    delta_phi = 1e-10
    phi_0 = 1
    return G0 * (1 + (delta_phi / phi_0) * r)

def g_penrose(t):
    G0 = G_newton
    delta_t = 1e-16
    return G0 * (1 + delta_t * t)

def derivatives(y, g_value):
    v_y, r_y, v_x, r_x = y
    r_v = 0.115
    cos_theta = 1 if r_x == 0 else r_v / np.sqrt(r_v**2 + r_x**2)
    f_l_adjusted = (1 + R) * Int_m * A_m / c * cos_theta
    a_y = g_value * m / r_y**2
    a_x = f_l_adjusted / m
    return [a_y, -v_y, a_x, v_x]

def derivatives_brans_dicke(t, y):
    v_y, r_y, v_x, r_x = y
    r_v = 0.115
    cos_theta = 1 if r_x == 0 else r_v / np.sqrt(r_v**2 + r_x**2)
    g_current = g_brans_dicke(r_y)
    f_l_adjusted = (1 + R) * Int_m * A_m / c * cos_theta
    a_y = g_current * m / r_y**2
    a_x = f_l_adjusted / m
    return [a_y, -v_y, a_x, v_x]

def derivatives_penrose(t, y):
    v_y, r_y, v_x, r_x = y
    r_v = 0.115
    cos_theta = 1 if r_x == 0 else r_v / np.sqrt(r_v**2 + r_x**2)
    g_current = g_penrose(t)
    f_l_adjusted = (1 + R) * Int_m * A_m / c * cos_theta
    a_y = g_current * m / r_y**2
    a_x = f_l_adjusted / m
    return [a_y, -v_y, a_x, v_x]

# Initial conditions and integration parameters
initial_conditions = [0, initial_distance, 0, 0]
t_span = (0, 192250)
t_eval_points = np.concatenate([
    np.linspace(t_span[0], t_span[1] * 0.9, 3, endpoint=False),
    np.linspace(t_span[1] * 0.9, t_span[1], 7)
])

# Define the range for distance (cluster towards smaller distances)
distance_min = 0.007
distance_max = 0.1
num_points = 10
distances = distance_min + (distance_max - distance_min) * np.exp(-np.linspace(0, 5, num_points))

# Solve the differential equations for all G values
solution_newton = scipy.integrate.solve_ivp(
    fun=lambda t, y: derivatives(y, G_newton),
    t_span=t_span,
    y0=initial_conditions,
    method='RK45',
    t_eval=t_eval_points
)

solution_qing_li = scipy.integrate.solve_ivp(
    fun=lambda t, y: derivatives(y, G_qing_li),
    t_span=t_span,
    y0=initial_conditions,
    method='RK45',
    t_eval=t_eval_points
)

solution_ferreira = scipy.integrate.solve_ivp(
    fun=lambda t, y: derivatives(y, G_ferreira),
    t_span=t_span,
    y0=initial_conditions,
    method='RK45',
    t_eval=t_eval_points
)

solution_brans_dicke = scipy.integrate.solve_ivp(
    fun=derivatives_brans_dicke,
    t_span=t_span,
    y0=initial_conditions,
    method='RK45',
    t_eval=t_eval_points
)

solution_penrose = scipy.integrate.solve_ivp(
    fun=derivatives_penrose,
    t_span=t_span,
    y0=initial_conditions,
    method='RK45',
    t_eval=t_eval_points
)

# Calculate acceleration vs. distance for Brans-Dicke's and Penrose's G
acceleration_newton = G_newton * m / distances**2
acceleration_qing_li = G_qing_li * m / distances**2
acceleration_ferreira = G_ferreira * m / distances**2
acceleration_brans_dicke = g_brans_dicke(distances) * m / distances**2
acceleration_penrose = g_penrose(t_eval_points[-1]) * m / distances**2

# Define end_points for zooming on the last portion of data
end_points = len(distances) // 2  # Show last half of the distance points

# Plotting - Zoomed on End Points with Detailed Labels
fig, axs_zoomed_end_labeled = plt.subplots(3, 1, figsize=(15, 10))
# Acceleration vs. Distance - Zoomed on End Points with Detailed Labels
axs_zoomed_end_labeled[0].plot(distances[end_points:], acceleration_newton[end_points:], label=NEWTON_G_LABEL, color='blue', marker='o')
axs_zoomed_end_labeled[0].plot(distances[end_points:], acceleration_qing_li[end_points:], label=QING_LI_G_LABEL, color='red', linestyle='--', marker='x')
axs_zoomed_end_labeled[0].plot(distances[end_points:], acceleration_ferreira[end_points:], label=FERREIRA_G_LABEL, color='green', linestyle=':', marker='s')
axs_zoomed_end_labeled[0].plot(distances[end_points:], acceleration_brans_dicke[end_points:], label=BRANS_DICKE_G_LABEL, color='purple', linestyle='-.', marker='^')
axs_zoomed_end_labeled[0].plot(distances[end_points:], acceleration_penrose[end_points:], label=PENROSE_G_LABEL, color='orange', linestyle='-.', marker='*')

# Acceleration vs. Distance - Zoomed on End Points with Detailed Labels
axs_zoomed_end_labeled[0].plot(distances[end_points:], acceleration_newton[end_points:], label=NEWTON_G_LABEL, color='blue', marker='o')
axs_zoomed_end_labeled[0].plot(distances[end_points:], acceleration_qing_li[end_points:], label=QING_LI_G_LABEL, color='red', linestyle='--', marker='x')
axs_zoomed_end_labeled[0].plot(distances[end_points:], acceleration_ferreira[end_points:], label=FERREIRA_G_LABEL, color='green', linestyle=':', marker='s')
axs_zoomed_end_labeled[0].plot(distances[end_points:], acceleration_brans_dicke[end_points:], label=BRANS_DICKE_G_LABEL, color='purple', linestyle='-.', marker='^')
axs_zoomed_end_labeled[0].plot(distances[end_points:], acceleration_penrose[end_points:], label=PENROSE_G_LABEL, color='orange', linestyle='-.', marker='*')
axs_zoomed_end_labeled[0].set_title('Acceleration vs. Distance (Zoomed on End Points with Detailed Labels)')
axs_zoomed_end_labeled[0].set_xlabel('Distance (m)')
axs_zoomed_end_labeled[0].set_ylabel('Acceleration (m/s²)')
axs_zoomed_end_labeled[0].invert_xaxis()
axs_zoomed_end_labeled[0].grid(True)
axs_zoomed_end_labeled[0].legend()
# Velocity vs. Time - Zoomed on End Points with Detailed Labels
axs_zoomed_end_labeled[1].plot(solution_newton.t[end_points:], solution_newton.y[0][end_points:], label=NEWTON_G_LABEL, color='blue', marker='o')
axs_zoomed_end_labeled[1].plot(solution_qing_li.t[end_points:], solution_qing_li.y[0][end_points:], label=QING_LI_G_LABEL, color='red', linestyle='--', marker='x')
axs_zoomed_end_labeled[1].plot(solution_ferreira.t[end_points:], solution_ferreira.y[0][end_points:], label=FERREIRA_G_LABEL, color='green', linestyle=':', marker='s')
axs_zoomed_end_labeled[1].plot(solution_brans_dicke.t[end_points:], solution_brans_dicke.y[0][end_points:], label=BRANS_DICKE_G_LABEL, color='purple', linestyle='-.', marker='^')
axs_zoomed_end_labeled[1].plot(solution_penrose.t[end_points:], solution_penrose.y[0][end_points:], label=PENROSE_G_LABEL, color='orange', linestyle='-.', marker='*')

# Velocity vs. Time - Zoomed on End Points with Detailed Labels
axs_zoomed_end_labeled[1].plot(solution_newton.t[end_points:], solution_newton.y[0][end_points:], label=NEWTON_G_LABEL, color='blue', marker='o')
axs_zoomed_end_labeled[1].plot(solution_qing_li.t[end_points:], solution_qing_li.y[0][end_points:], label=QING_LI_G_LABEL, color='red', linestyle='--', marker='x')
axs_zoomed_end_labeled[1].plot(solution_ferreira.t[end_points:], solution_ferreira.y[0][end_points:], label=FERREIRA_G_LABEL, color='green', linestyle=':', marker='s')
axs_zoomed_end_labeled[1].plot(solution_brans_dicke.t[end_points:], solution_brans_dicke.y[0][end_points:], label=BRANS_DICKE_G_LABEL, color='purple', linestyle='-.', marker='^')
axs_zoomed_end_labeled[1].plot(solution_penrose.t[end_points:], solution_penrose.y[0][end_points:], label=PENROSE_G_LABEL, color='orange', linestyle='-.', marker='*')
axs_zoomed_end_labeled[1].set_title('Velocity vs. Time (Zoomed on End Points with Detailed Labels)')
axs_zoomed_end_labeled[1].set_xlabel('Time (s)')
axs_zoomed_end_labeled[1].set_ylabel('Velocity (m/s)')
axs_zoomed_end_labeled[1].grid(True)
axs_zoomed_end_labeled[1].legend()
# Position vs. Time - Zoomed on End Points with Detailed Labels
axs_zoomed_end_labeled[2].plot(solution_newton.t[end_points:], solution_newton.y[1][end_points:], label=NEWTON_G_LABEL, color='blue', marker='o')
axs_zoomed_end_labeled[2].plot(solution_qing_li.t[end_points:], solution_qing_li.y[1][end_points:], label=QING_LI_G_LABEL, color='red', linestyle='--', marker='x')
axs_zoomed_end_labeled[2].plot(solution_ferreira.t[end_points:], solution_ferreira.y[1][end_points:], label=FERREIRA_G_LABEL, color='green', linestyle=':', marker='s')
axs_zoomed_end_labeled[2].plot(solution_brans_dicke.t[end_points:], solution_brans_dicke.y[1][end_points:], label=BRANS_DICKE_G_LABEL, color='purple', linestyle='-.', marker='^')
axs_zoomed_end_labeled[2].plot(solution_penrose.t[end_points:], solution_penrose.y[1][end_points:], label=PENROSE_G_LABEL, color='orange', linestyle='-.', marker='*')

# Position vs. Time - Zoomed on End Points with Detailed Labels
axs_zoomed_end_labeled[2].plot(solution_newton.t[end_points:], solution_newton.y[1][end_points:], label=NEWTON_G_LABEL, color='blue', marker='o')
axs_zoomed_end_labeled[2].plot(solution_qing_li.t[end_points:], solution_qing_li.y[1][end_points:], label=QING_LI_G_LABEL, color='red', linestyle='--', marker='x')
axs_zoomed_end_labeled[2].plot(solution_ferreira.t[end_points:], solution_ferreira.y[1][end_points:], label=FERREIRA_G_LABEL, color='green', linestyle=':', marker='s')
axs_zoomed_end_labeled[2].plot(solution_brans_dicke.t[end_points:], solution_brans_dicke.y[1][end_points:], label=BRANS_DICKE_G_LABEL, color='purple', linestyle='-.', marker='^')
axs_zoomed_end_labeled[2].plot(solution_penrose.t[end_points:], solution_penrose.y[1][end_points:], label=PENROSE_G_LABEL, color='orange', linestyle='-.', marker='*')
axs_zoomed_end_labeled[2].set_title('Position vs. Time (Zoomed on End Points with Detailed Labels)')
axs_zoomed_end_labeled[2].set_xlabel('Time (s)')
axs_zoomed_end_labeled[2].set_ylabel('Position (m)')
axs_zoomed_end_labeled[2].grid(True)
axs_zoomed_end_labeled[2].legend()

plt.tight_layout()
plt.show()

# Create DataFrames and calculate differences
data_acceleration = {
    "Distance (m)": distances[end_points:],
    "Newton's G (Acceleration)": acceleration_newton[end_points:],
    "Qing Li's G (Acceleration)": acceleration_qing_li[end_points:],
    "Ferreira's G (Acceleration)": acceleration_ferreira[end_points:],
    "Brans-Dicke's G (Acceleration)": acceleration_brans_dicke[end_points:],
    "Penrose's G (Acceleration)": acceleration_penrose[end_points:]
}

data_velocity = {
    "Time (s)": solution_newton.t[end_points:],
    "Newton's G (Velocity)": solution_newton.y[0][end_points:],
    "Qing Li's G (Velocity)": solution_qing_li.y[0][end_points:],
    "Ferreira's G (Velocity)": solution_ferreira.y[0][end_points:],
    "Brans-Dicke's G (Velocity)": solution_brans_dicke.y[0][end_points:],
    "Penrose's G (Velocity)": solution_penrose.y[0][end_points:]
}

data_position = {
    "Time (s)": solution_newton.t[end_points:],
    "Newton's G (Position)": solution_newton.y[1][end_points:],
    "Qing Li's G (Position)": solution_qing_li.y[1][end_points:],
    "Ferreira's G (Position)": solution_ferreira.y[1][end_points:],
    "Brans-Dicke's G (Position)": solution_brans_dicke.y[1][end_points:],
    "Penrose's G (Position)": solution_penrose.y[1][end_points:]
}

# Calculating differences from Newton's values
for key in ["Qing Li's G (Acceleration)", "Ferreira's G (Acceleration)", "Brans-Dicke's G (Acceleration)", "Penrose's G (Acceleration)"]:
    data_acceleration[f"Difference from Newton ({key})"] = data_acceleration[key] - data_acceleration["Newton's G (Acceleration)"]

for key in ["Qing Li's G (Velocity)", "Ferreira's G (Velocity)", "Brans-Dicke's G (Velocity)", "Penrose's G (Velocity)"]:
    data_velocity[f"Difference from Newton ({key})"] = data_velocity[key] - data_velocity["Newton's G (Velocity)"]

for key in ["Qing Li's G (Position)", "Ferreira's G (Position)", "Brans-Dicke's G (Position)", "Penrose's G (Position)"]:
    data_position[f"Difference from Newton ({key})"] = data_position[key] - data_position["Newton's G (Position)"]

# Creating DataFrames
df_acceleration = pd.DataFrame(data_acceleration)
df_velocity = pd.DataFrame(data_velocity)
df_position = pd.DataFrame(data_position)

# Displaying the DataFrames to the user
print("Acceleration Data:")
print(df_acceleration)
print("\nVelocity Data:")
print(df_velocity)
print("\nPosition Data:")
print(df_position)