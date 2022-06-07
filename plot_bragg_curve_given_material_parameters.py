from cmath import sin
import numpy as np 
import matplotlib.pyplot as plt

# Set the default text font size
plt.rc('font', size=18)
# Set the axes title font size
plt.rc('axes', titlesize=22)
# Set the axes labels font size
plt.rc('axes', labelsize=22)
# Set the font size for x tick labels
plt.rc('xtick', labelsize=18)
# Set the font size for y tick labels
plt.rc('ytick', labelsize=18)
# Set the legend font size
plt.rc('legend', fontsize=18)
# Set the font size of the figure title
plt.rc('figure', titlesize=24)

# Define wavelength of recording beam
record_wavelength = 532

# Define wavelength of probe beam
probe_wavelength = 633

# Define recording beam angles
beam1_angle = 30
beam2_angle = -30

# Define refractive index of film
n_film = 1.5

# Correct for material refractive index, for unslanted grating this is equivalent to the Bragg angle at the recording wavelength
# Angles in rads
beam1_angle_medium = np.arcsin((np.sin(np.deg2rad(beam1_angle)))/n_film) 
beam2_angle_medium = np.arcsin((np.sin(np.deg2rad(beam2_angle)))/n_film) 

# Find grating period
period = record_wavelength/(2*n_film*np.sin(beam1_angle_medium))

print(period)
print(2*n_film*np.sin(beam1_angle_medium))

# Find bragg angle (in material) for probe beam (633nm)
#bragg_probe = np.arcsin((probe_wavelength)/(2*n_film*period))
bragg_probe = np.deg2rad(16.64)
print(np.rad2deg(bragg_probe))

# Define film thickness (um)
thickness = 70

# range of bragg deviations in medium (rads)
bragg_deviation = np.linspace(-beam1_angle_medium/2, beam1_angle_medium/2, 10000)

# range of bragg deviations in air (degress)
bragg_deviation_in_air = np.linspace(-beam1_angle/2, beam1_angle/2, 10000)

def off_bragg():
    return (bragg_deviation*2*np.pi*n_film*thickness*np.sin(bragg_probe))/(probe_wavelength*0.001)
    
off_braggs = off_bragg()

"""def delta_n():
# delta n for v = pi/2
    return (probe_wavelength*0.001*np.cos((bragg_probe)))/(2*thickness)"""
delta_n = 0.002
v = (np.pi*delta_n*thickness)/(probe_wavelength*0.001*np.cos(bragg_probe))
v = 1.57

def diffraction_efficiency(bragg_deviation):
    E = (bragg_deviation*2*np.pi*n_film*thickness*np.sin(bragg_probe))/(probe_wavelength*0.001)
    #de= (np.sin(np.sqrt((np.pi/2)**2 + off_braggs**2))**2)/(1+(off_braggs**2/(np.pi/2)**2))
    #return np.sin(v**2 + E**2)
    de= np.sin(np.sqrt((v)**2 + E**2))**2/(1+(E**2/(v)**2))
    return de
        
E = off_braggs

DE = diffraction_efficiency(bragg_deviation)



plt.plot(bragg_deviation_in_air, DE)
#plt.title(r'Thickness = 10 $\mu$m , n = 1.5, $\Delta n = 0.0291$ ')
plt.ylabel(r'DE  (%)')
plt.xlabel(r'$\Delta \theta_{air}$ ($\circ$)')
plt.show()
#print(off_braggs)
#print("RIM: {0:.3g}".format(delta_n()))
print(bragg_probe)
print('Period: {0:.3g}'.format(period))
print('SF: {0:.3g}'.format(1000000/period))
print(r'$\Delta \theta_{air}$', np.rad2deg((period*0.001)/thickness))
#print(bragg_deviation)
print('Off bragg', E)