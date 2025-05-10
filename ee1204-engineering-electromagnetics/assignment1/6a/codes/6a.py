import matplotlib.pyplot as plt 
import numpy as np 

N = 20 # the grid on which we will plot the vector will have order N

r_1 = np.array([1, 0]).reshape(-1, 1)   # positive charge
r_2 = np.array([-1, 0]).reshape(-1, 1)  # positive charge
r_3 = np.array([0, 1]).reshape(-1, 1)   # negative charge
r_4 = np.array([0, -1]).reshape(-1, 1)  # negative charge

k = 8.99 * 1e9  # Coulomb constant

x_points = np.linspace(-2, 2, N) # create N uniformly distribured points from -2 to 2
y_points = np.linspace(-2, 2, N) # create N uniformly distribured points from -2 to 2)

fig, ax = plt.subplots(figsize=(8, 6))
position_x = list()
position_y = list()
field_strength = list()
field_directions_x = list()
field_directions_y = list()

for x in x_points:
    for y in y_points:
        if ((x != 1 or y != 0) and (x != -1 or y != 0) and
            (x != 0 or y != 1) and (x != 0 or y != -1)):
            position_vector = np.array([x, y]).reshape(-1, 1)
            
            field_r1 = -(k / (((r_1 - position_vector).T @ (r_1 - position_vector)) ** 1.5)) * (position_vector - r_1) # field at position_vector due to charge at r_1
            field_r2 = -(k / (((r_2 - position_vector).T @ (r_2 - position_vector)) ** 1.5)) * (position_vector - r_2) # field at position_vector due to charge at r_2
            field_r3 = -(k / (((r_3 - position_vector).T @ (r_3 - position_vector)) ** 1.5)) * (r_3 - position_vector) # field at position_vector due to charge at r_3
            field_r4 = -(k / (((r_4 - position_vector).T @ (r_4 - position_vector)) ** 1.5)) * (r_4 - position_vector) # field at position_vector due to charge at r_4
            
            net_field = field_r1 + field_r2 + field_r3 + field_r4
            strength = np.sqrt(net_field.T @ net_field)[0, 0] 
            
            position_x.append(position_vector[0, 0])
            position_y.append(position_vector[1, 0])
            
            field_strength.append(strength)
            
            # Normalize vectors to have equal length
            if strength != 0:
                unit_vector = net_field / strength
                field_directions_x.append(unit_vector[0, 0])
                field_directions_y.append(unit_vector[1, 0])
            else:
                field_directions_x.append(0)
                field_directions_y.append(0)

# used to normalize color map
max_field_strength = max(field_strength)
min_field_strength = min(field_strength)

quiver = ax.quiver(position_x, position_y, field_directions_x, field_directions_y, field_strength, cmap=plt.cm.plasma, norm=plt.Normalize(vmin=min_field_strength, vmax=max_field_strength))

# Add colorbar
cbar = plt.colorbar(quiver, ax=ax)
cbar.set_label("Field Strength")

plt.xlim(-2.1, 2.1)
plt.ylim(-2.1, 2.1)
plt.savefig("../figs/field_map.png")
plt.show()
