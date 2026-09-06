fun trajectory ( b, d , e, x_1, y_1, x_2, y_2, theta)

    # bars
b = None # moving bar
d = None # bar representing the topshell
e = None # moving bar

    # bottom vertices
x_1 = None # position for point 1
y_1 = None # position for point 1
x_2 = None # position for point 2
y_2 = None # position for point 2

    ## INPUT PARAM, array
theta = None # angle between a and b



# process calcs

a = sqrt ( (x_1 - x_2)^2 - (y_1-y_2)^2 )   # fixed bottom bar
c = sqrt ( a ^ 2 + b ^ 2 - 2 * a * b * cos(theta) )   # non existant diagonal line, output as a matrix

omega = arcsin ( ( c ^ 2 + e ^ 2 - d ^ 2 ) / ( 2 * c * e ) )   # angle between c and e, array



# find (s,t) and (m,n)


angle_ah = arctan ( ( y_1 - y_2) / (x_1 - x_2) ) # between a and horizontal x axis

s = x_2 + b * cos ( theta + angle_ah ) # array
t = y_2 + b * sin ( theta + angle_ah ) # array

angle_ac = arcsin ( b * sin (theta) / c ) # angle between a and c, array
angle_eh = omega + angle_ac - angle_ah # angle between e and horizon, on the left of e, array

m = x_1 + e * cos ( angle_eh ) 
n = y_1 + e * sin ( angle_eh)



# print and verify

print( "(" + s + "," + t + ")")
print( "(" + m + "," + n + ")")

if d - sqrt ( ( s - m ) ^ 2 + ( t - n) ^ 2 ) == 0 print ( 'pass' )
