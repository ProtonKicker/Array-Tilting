import sys
import numpy as np


def trajectory(b, d, e, x_1, y_1, x_2, y_2, theta):

    # bars
    b = b  # moving bar
    d = d  # bar representing the topshell
    e = e  # moving bar

    # bottom vertices
    x_1 = x_1  # position for point 1
    y_1 = y_1  # position for point 1
    x_2 = x_2  # position for point 2
    y_2 = y_2  # position for point 2

    ## INPUT PARAM, array
    theta = np.array(theta)  # angle between a and b

    # process calcs

    a = np.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)  # fixed bottom bar
    c = np.sqrt(a ** 2 + b ** 2 - 2 * a * b * np.cos(theta))  # non existant diagonal line, output as a matrix

    omega = np.arcsin((c ** 2 + e ** 2 - d ** 2) / (2 * c * e))  # angle between c and e, array

    # find (s,t) and (m,n)

    angle_ah = np.arctan((y_1 - y_2) / (x_1 - x_2))  # between a and horizontal x axis

    s = x_2 + b * np.cos(theta + angle_ah)  # array
    t = y_2 + b * np.sin(theta + angle_ah)  # array

    angle_ac = np.arcsin(b * np.sin(theta) / c)  # angle between a and c, array
    angle_eh = omega + angle_ac - angle_ah  # angle between e and horizon, on the left of e, array

    m = x_1 + e * np.cos(angle_eh)
    n = y_1 + e * np.sin(angle_eh)

    # print and verify

    print("(" + str(s) + "," + str(t) + ")")
    print("(" + str(m) + "," + str(n) + ")")

    if np.allclose(d, np.sqrt((s - m) ** 2 + (t - n) ** 2)):
        print('pass')


if __name__ == "__main__":
    args = [float(x) for x in sys.argv[1:8]]
    theta_start = float(sys.argv[8])
    theta_step = float(sys.argv[9])
    theta_stop = float(sys.argv[10])
    theta_vals = np.arange(theta_start, theta_stop + theta_step, theta_step)
    trajectory(*args, theta_vals)