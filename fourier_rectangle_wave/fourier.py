import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np 

number_of_harmonics = 10

amplitude = 5
time_limits = np.array([0, 5])
time_period = 1
duty_ratio = 0.3

stepsize = 1e-3

t = np.arange(0, 5, stepsize)

fig, ax = plt.subplots(2, 1, figsize=(8,6))

def input_voltage(time, T = time_period, alpha = duty_ratio, A = amplitude):
    if (time % T) <= (alpha * T):
        return A
    else :
        return 0

response = [input_voltage(x) for x in t]
ax[1].plot(t, response, color="orange", label="original signal")

def get_fourier_response(A = amplitude, N = number_of_harmonics):
    fourier_response = list()
    for x in t:
        v_in_t = A * duty_ratio
        for k in range(1, N + 1):
            v_in_t += ((A * np.sin(2 * np.pi * k * duty_ratio))/(np.pi * k))*np.cos((2 * np.pi * k * x)/time_period) - (A/(np.pi * k))*(np.cos(2 * np.pi * k * duty_ratio) - 1) * np.sin((2 * np.pi * k * x)/time_period) 

        fourier_response.append(v_in_t)

ax[0].plot(t, fourier_response, color="blue", label="fourier approx")
ax[0].legend(loc='best')
ax[1].legend(loc='best')
plt.tight_layout()
plt.show()
