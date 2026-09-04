# 4-bar Trajectory Calculations
# To start the calcs, needs b, d, e, (x_1,y_1), (x_2,y_2), and theta range

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, cos, sin, atan2, asin, pi

# ============================================================
# PARAMETERS - Edit these values
# ============================================================

# Fixed points
x1 = 0.0   # position for point 1
x2 = 5.0   # position for point 2
y1 = 0.0   # position for point 1
y2 = 0.0   # position for point 2

# Bar lengths
b = 5.0    # moving bar (from x2,y2)
d = 5.0    # bar representing the topshell (between s,t and m,n)
e = 5.0    # moving bar (from x1,y1)

# Theta range - edit these to change the angle range
theta_start = 0.0
theta_end = 2 * pi
theta_steps = 50

# ============================================================
# CALCULATION FUNCTION
# ============================================================

def calculate_4bar(x1, y1, x2, y2, b, d, e, theta):
    # Calculate base length a (distance between x1,y1 and x2,y2)
    a_val = sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    # Calculate diagonal c using law of cosines
    c_val = sqrt(a_val**2 + b**2 - 2 * a_val * b * cos(theta))
    
    # Calculate omega using law of cosines
    # Clamp the value to avoid domain errors in asin
    omega_arg = (c_val**2 + e**2 - d**2) / (2 * c_val * e)
    omega_arg = max(-1.0, min(1.0, omega_arg))
    omega_val = asin(omega_arg)
    
    # Calculate angle between a and horizontal x axis
    angle_ah = atan2(y1 - y2, x1 - x2)
    
    # Calculate point (s,t)
    s_val = x2 + b * cos(theta + angle_ah)
    t_val = y2 + b * sin(theta + angle_ah)
    
    # Calculate angle between a and c
    angle_ac_arg = (b * sin(theta)) / c_val
    angle_ac_arg = max(-1.0, min(1.0, angle_ac_arg))
    angle_ac = asin(angle_ac_arg)
    
    # Calculate angle between e and horizon
    angle_eh = omega_val + angle_ac - angle_ah
    
    # Calculate point (m,n)
    m_val = x1 + e * cos(angle_eh)
    n_val = y1 + e * sin(angle_eh)
    
    return s_val, t_val, m_val, n_val


# ============================================================
# MAIN CALCULATIONS
# ============================================================

# Generate theta range
theta_range = np.linspace(theta_start, theta_end, theta_steps)

# Initialize arrays to store results
all_s = []
all_t = []
all_m = []
all_n = []

# Calculate for each theta
for theta in theta_range:
    s, t, m, n = calculate_4bar(x1, y1, x2, y2, b, d, e, theta)
    all_s.append(s)
    all_t.append(t)
    all_m.append(m)
    all_n.append(n)

# ============================================================
# PLOTTING
# ============================================================

plt.figure(figsize=(12, 6))

# Plot 1: Trajectory
plt.subplot(1, 2, 1)

# Plot fixed points
plt.scatter([x1, x2], [y1, y2], color='red', label='Fixed Points', s=100, zorder=5)

# Plot trajectories
plt.plot(all_s, all_t, color='blue', label='Point (s,t) trajectory', linewidth=2)
plt.plot(all_m, all_n, color='green', label='Point (m,n) trajectory', linewidth=2)

# Plot the bar d (connection between s,t and m,n) for the last theta
plt.plot([all_s[-1], all_m[-1]], [all_t[-1], all_n[-1]], 
         color='purple', label='Bar d', linewidth=2, linestyle='--')

# Add labels and legend
plt.xlabel('X')
plt.ylabel('Y')
plt.title('4-bar Trajectory')
plt.legend()
plt.grid(True)
plt.axis('equal')

# Plot 2: Verification
plt.subplot(1, 2, 2)

# Calculate distances for verification
distances = []
for i in range(len(all_s)):
    dx = all_s[i] - all_m[i]
    dy = all_t[i] - all_n[i]
    dist = sqrt(dx**2 + dy**2)
    distances.append(dist)

plt.plot(theta_range, distances, label='Actual distance', linewidth=2)
plt.axhline(y=d, color='red', label=f'Expected (d={d})', linestyle='--')
plt.xlabel('Theta (radians)')
plt.ylabel('Distance')
plt.title('Verification: distance between (s,t) and (m,n)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# ============================================================
# VERIFICATION OUTPUT
# ============================================================

print("\n=== Verification ===")
print(f"Bar length d: {d}")
print(f"All distances approximately equal to d: {all(abs(d - np.array(distances)) < 0.01)}")
print(f"\nDistance stats:")
print(f"  Min: {min(distances):.4f}")
print(f"  Max: {max(distances):.4f}")
print(f"  Mean: {np.mean(distances):.4f}")
