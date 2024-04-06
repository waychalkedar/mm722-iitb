import matplotlib.pyplot as plt

data = open("dump_4.file", "r")
lines = data.readlines()
time = []
count = 0

x = []
y = []
z = []
n_1 = []
n_2 = []
n = []
num_atoms = 4
box_len = 10.0

for line in lines:
    # the below statements isolate timesteps
    if "TIMESTEP" in line.split():
        time.append(int(lines[count + 1]))
    # the below statements extract position information
    if 'xu' in line.split():
        x_pos = float(lines[count+1].split()[2])
        y_pos = float(lines[count+1].split()[3])
        z_pos = float(lines[count+1].split()[4])
        x.append(x_pos)
        y.append(y_pos)
        z.append(z_pos)
        n1 = 0
        n2 = 0

        for j in range(num_atoms):
            if float(lines[count+j+1].split()[2]) < box_len/2:
                n1 += 1
            else:
                n2 += 1
        n_1.append(n1)
        n_2.append(n2)
        n.append(n1+n2)

    count += 1

data.close()

# Plotting the required variables ---------------------------------------------------------------
plt.plot(time, n_1, label="n1 - Number of molecules in LHS")
# plt.plot(time, n_2, label="n2 - Number of molecules in RHS")
plt.plot(time, n, label="n - Total number of molecules in the box")
plt.xlabel("Time")
plt.ylabel("Number of atoms")
plt.title("Number of atoms in LHS and RHS of the box using Y=L/2 Plane")
plt.ylim([0, num_atoms+10])
plt.legend()
plt.show()

# plt.plot(time, x ,label = "X - Position")
# plt.plot(time, y, label = "Y - Position")
# plt.plot(time, z, label = "Z - Position")
# plt.title("Trajectory for Atom 1")
# plt.xlabel("Time")
# plt.ylabel("Position")
plt.legend()
plt.show()