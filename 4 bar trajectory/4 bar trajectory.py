
# to start the calcs, needs b,d,e, (x_1,y_1), (x_2,y_2), and theta



# params

    a = None # fixed bottom bar
b = None # moving bar

c = None # non existant diagonal line

d = None # bar representing the topshell
e = None # moving bar

x_1 = None # position for point 1
y_1 = None # position for point 1

x_2 = None # position for point 2
y_2 = None # position for point 2

theta = None # angle between a and b
    omega = None # angle between c and e


# process calcs

a = sqrt ( (x_1 - x_2)^2 - (y_1-y_2)^2 )
c = sqrt ( a ^ 2 + b ^ 2 - 2 * a * b * cos(theta) )

omega = arcsin ( ( c ^ 2 + e ^ 2 - d ^ 2 ) / ( 2 * c * e ) )



# find (s,t) and (m,n)


angle_ah = arctan ( ( y_1 - y_2) / (x_1 - x_2) ) # between a and horizontal x axis

s = x_2 + b * cos ( theta + angle_ah )
t = y_2 + b * sin ( theta + angle_ah )

angle_ac = arcsin ( b * sin (theta) / c ) # angle between a and c
angle_eh = omega + angle_ac - angle_ah # angle between e and horizon, on the left of e

m = x_1 + e * cos ( angle_eh )
n = y_1 + e * sin ( angle_eh)



# verify

d - sqrt ( ( s - m ) ^ 2 + ( t - n) ^ 2 ) # should yield 0
