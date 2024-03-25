# ALTITUDE IS IN METERS
# VELOCITY IS IN M/S
# MASS IN KILOGRAMS
# TIME IN SECONDS

######################### QUESTIONS ##############################
# - before, after, or including motor burnout?
# - based on prev. answer, what's the mass(es) of the rocket?
# - should altitude-based drag also be factored in?
# - what's the time step?
# - for the flight sim, continue to loop through (progressing in time) until d2 < d1?
##################################################################


# master list of data
data = [["alt, vel, best_angle"]]


def get_data(data):
    # runs through all possible altitudes
    for alt in range(0, 25):  # 0,250
        # runs through all possible velocities
        for vel in range(0, 10):  # 0,100
            # finds optimal angle
            best_angle = find_optimal_angle(alt, vel)
            # adds the altitude, velocity, and optimal angle to the end of the master data list
            data += [[alt, vel, best_angle]]


def find_optimal_angle(alt, vel):
    # creates variables
    alt_goal = 244
    opt_ang = 0

    # runs through all possible airbrake angles
    for ang in range(0, 9):  # 0,90
        # simulates flight and finds the predicted apogee
        apogee = flight_sim(alt, vel, ang)
        # updates what the optimal angle would be
        diff = alt_goal - diff
        if diff < smallest_diff:
            smallest_diff = diff
            opt_ang = ang

    return opt_ang


def flight_sim(alt, vel, ang):
    # "run the physics simulation with the starting altitude and velocity conditions. Air breaks are set at a constant deployment value"
    vel = 25
    alt = 100
    ang = 45

    # FORCE
    mass = 2  # in kg AND needs to be changed
    g = -9.81 * mass
    drag = -1 * airbrake_drag(vel, ang)
    motor = 30  # NEEDS TO BE CHANGED
    force = g + drag + motor
    print("force is", force)

    # ACCELERATION
    acc = force / mass
    print("acc is", acc)

    # VELOCITY
    t = 0.01  # WHATS THE TIME STEP AND WHAT UNIT
    v1 = vel  # initial velocity
    print("vel is", vel)
    v2 = (acc * t) + v1  # derived from acc. equation
    print("v2 one is", v2)

    # curr_vel = prev_vel + (acc * t)
    # prev_vel = curr_vel

    # POSITION
    d1 = alt  # initial altitude
    print("alt is", alt)
    d2 = (v2 * t) + d1
    if d2 < 0:
        d2 = 0
    print("d2 is", d2)
    print("here")

    import time
    time.sleep(2)

    while d2 <= 244:
        # reset variables for next time step calculation
        print("d2 is", d2, "d1", d1)
        v1 = v2
        d1 = d2

        t += t

        # calculate next vel and alt
        v2 = (acc * t) + v1
        d2 = (v2 * t) + d1
        if d2 < 0:
            d2 = 0

        print("now here")
        print("AND NOW d2 is", d2, "d1", d1)
    predicted_apogee = d1

    return predicted_apogee


def airbrake_drag(vel, ang):
    # find the drag from the airbrakes at a given angle and velocity (based on CFD data)
    cf = [0.00000000e+00, 9.74016773e-04, -1.81889130e-05, 1.86864541e-03,
          9.05051660e-05, 3.65178982e-09, -5.18226152e-07, 8.97878717e-08]
    x = vel  # m/s
    y = ang  # airbrake angle
    val = (cf[0] * (x ** 0 * y ** 0)) + (cf[1] * (x * y)) + (cf[2] * (x * y ** 2)) + (cf[3] * (x ** 2 * y ** 0)) + (
                cf[4] * (x ** 2 * y)) + (cf[5] * (x ** 3 * y ** 2)) + (cf[6] * (x ** 3 * y)) + (
                      cf[7] * (x ** 0 * y ** 3))
    return val


# runs the code
get_data(data)
print(get_data(data))

# exports data to a CSV file called angle_data
# import csv
# with open('angle_data.csv', 'w') as file:
#    write = csv.writer(file)
#    write.writerows(data)
