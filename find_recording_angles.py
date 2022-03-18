import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


class RecordingAngles:

    def __init__(self, diff_wavelength, record_wavelength, input_air, output_air, n_environment, n_medium1, n_medium2, output_grating) -> None:
        
        # Define diffraction wavelength
        self.diff_wavelength = diff_wavelength

        # Define recording wavelength
        self.record_wavelength = record_wavelength

        # Define input angle in air for probe. Convert to radians
        self.input_air =  input_air*np.pi/180

        # Define output angle in air for probe beam
        self.output_air = output_air*np.pi/180

        # Define environment refractive index (e.g. for air this equals 1)
        self.n_environment = n_environment

        # Define environment refractive index (e.g. for air this equals 1)
        self.n_medium1 = n_medium1

        # Define refractive index for material containing the grating pattern 
        self.n_medium2 = n_medium2

        # Define grating input angle for probe beam. Use Snell's Law
        self.grating_input = np.arcsin((self.n_environment/self.n_medium2)*np.sin(self.input_air))

        # Define grating output beam angle in rads
        self.grating_output = output_grating*np.pi/180

        self.slant = (self.grating_input+self.grating_output)/2
         
        # Theta_r or, equivalently, the bragg angle required inside the material
        self.theta_r = self.slant - self.grating_input
        self.bragg = self.theta_r 
        
    def slant_angle(self):
        # Calculate slant
        return (self.grating_input+self.grating_output)/2

    #def bragg_angle(self):
        # radians
        #return (self.grating_input-self.grating_output)/2
    #    return np.arcsin(self.diff_wavelength/(2*self.period()))
    
    #def probe_bragg(self):

    # calculate the period reqired
    def period(self):
        # Period required depends on probe wavelength
        #return np.abs(self.diff_wavelength/(2*self.n_medium2*np.sin(self.bragg_angle())))
        return np.abs(self.diff_wavelength/(2*self.n_medium2*np.sin(self.theta_r)))

    def spatial_frequency(self):
        return (1/self.period())*1000000

    #def min_replay_wavelength(self):
    #    return self.n_medium1*2*self.period()

    def half_interbeam_angle(self):
        #if self.record_wavelength >= self.min_replay_wavelength():
        # Depends on record wavelength
        angle = np.arcsin(self.record_wavelength/(self.n_medium2*2*self.period()))
        if np.isnan(angle) == True:
            return 0
        else:
            return angle

        #else:
        #    return 0

    def theta1(self):
        
        theta = np.rad2deg(self.slant_angle() + self.half_interbeam_angle())
        
        if np.isnan(theta)== False:
            return theta
        
        else:
            # set to 0 if nan value, purely for plotting purposes
            return 0

    def theta2(self):
        theta = np.rad2deg(self.slant_angle() - self.half_interbeam_angle())
        
        if np.isnan(theta)== False:
            return theta
        
        else:
            return 0
        
    def theta1_in_air(self):
        # For recording beam
        theta1_in_air = np.arcsin((self.n_medium2/self.n_environment)*(np.deg2rad(np.sin(self.theta1()))))
        return np.rad2deg(theta1_in_air)

    def theta2_in_air(self):
        #Stheta2_in_air = 2*self.slant_angle() - self.theta1_in_air()
        theta2_in_air = np.arcsin((self.n_medium2/self.n_environment)*(np.deg2rad(np.sin(self.theta2()))))
        return np.rad2deg(theta2_in_air)


def phase_param(T, n, bragg, wavelength):
    return (np.pi*n*T/(wavelength*np.cos(bragg)))

def off_bragg(delta_theta, n, T, bragg, wavelength):
    return (delta_theta*2*np.pi*n*T*np.sin(bragg))/wavelength

def thickness(wavelength, n1, bragg, v = np.pi/2):
    return v*wavelength*np.cos(bragg)/(np.pi*n1)


def diffraction_efficiency(v, E):
    de= np.sin(np.sqrt(v**2 + E**2))**2/(1+(E**2/v**2))
    #return np.sin(v**2 + E**2)
    if np.isnan(de)== False:
        return de
        
    else:
        return 0
        
def angular_selectivity(T, period):
    # returns angular selectivity in radians
    #delta_theta = (E*wavelength)/(2*np.pi*n*T*np.sin(np.abs(bragg)))
    return (period)/T

setup1 = RecordingAngles(633, 532, 30, 30, 1, 1, 1.5, 0)

#T = thickness(setup1.diff_wavelength, 0.06, setup1.bragg)
# Thickness affects DE and angular selectivity

# Thickness in nm
T = 70000

# Find angular selectivity in radians
delta_theta = angular_selectivity(T, setup1.period())


# Plot theta 1 and theta2 vs wavelength
replay_lamda = np.linspace(511, 1000, 489)

# Periods
half_angle = []
half_angle = [setup1.half_interbeam_angle() for replay_lamda in replay_lamda] 

# Theta1
theta1 = []
theta1 = [setup1.theta1() for replay_lamda in replay_lamda]
theta1 = [theta for theta in theta1 if theta != None]


# Theta2
theta2 = []
theta2 = [setup1.theta2() for replay_lamda in replay_lamda]
theta2 = [theta for theta in theta2 if theta != None]
#print(theta2)

#plt.plot(replay_lamda, theta1, 'tab:blue')

#plt.plot(replay_lamda, theta2, 'tab:orange')
#plt.show()

#print(half_angle)

fig, ax = plt.subplots()
ax.plot(replay_lamda, theta1, 'tab:blue')
ax.plot(replay_lamda, theta2, 'tab:orange')
#ax.set_aspect('equal')
ax.grid(False, which='both')

ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
plt.show()



# Produce graph of DE vs E

# Define range of E
# Plot theta 1 and theta2 vs wavelength
range_theta = np.linspace(-2*delta_theta, 2*delta_theta, 10000)


#E = [off_bragg(theta, setup1.n_environment, T, setup1.bragg_angle(), setup1.diff_wavelength) for theta in range_theta]
E = np.linspace(0, 3, 100)
DE = [diffraction_efficiency(v=np.pi/2, E= E) for E in E]



fig, ax = plt.subplots()
ax.plot(E, DE, 'tab:blue')

#ax.set_aspect('equal')
ax.grid(False, which='both')

ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
ax.set_xlabel('Off-bragg')
plt.show()
#print(E)
#print(diffraction_efficiency(v=np.pi/2, E= 0))
#print(DE)
E = []
E = [off_bragg(theta, setup1.n_medium1, T, setup1.bragg, setup1.diff_wavelength) for theta in range_theta]
DE = [diffraction_efficiency(v=np.pi/2, E= E) for E in E]
fig, ax = plt.subplots()

range_degrees = [np.rad2deg(theta) for theta in range_theta]
ax.plot(range_degrees, DE, 'tab:blue')

#ax.set_aspect('equal')
ax.grid(False, which='both')

ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
ax.set_xlabel('Delta Theta (degrees)')
plt.show()


print("Grating period: {0:.3g}".format(setup1.period())+ "nm")
print("Spatial frequency: {0:.3g}".format(setup1.spatial_frequency())+ "l/mm")
print("Slant angle: {0:.3g}".format(np.rad2deg(setup1.slant_angle()))+ 'degrees')
print("Record angle 1 (in air): {0:.3g}".format(setup1.theta1_in_air())+ "degrees")
print("Record angle 2 (in air): {0:.3g}".format((setup1.theta2_in_air()))+ "degrees")
print("Inter beam angle (in air): {0:.3g}".format(np.abs(np.rad2deg(setup1.theta2_in_air()-setup1.theta1_in_air()))))
print("Film thickness: {0:.3g}".format(T*0.001)+ "um")
#print(delta_theta*180/np.pi)
#print(diffraction_efficiency(v=np.pi/2, E= 0))


"""print(1/setup1.period())
print(setup1.bragg_angle()*180/np.pi)
print("Bragg angle: {0:.3g}".format(setup1.bragg_angle()*180/np.pi)+ "degrees")
print("Angular Selectivity: {0:.3g}".format(np.rad2deg(delta_theta))+ "degrees")"""


"""print("Input angle in air: ", setup1.grating_input*180/np.pi)
print("Grating input angle:", setup1.grating_input*180/np.pi)
print("Grating output angle:", setup1.grating_output*180/np.pi)
print("Slant angle:", setup1.slant_angle()*180/np.pi)
print("Theta_r:", setup1.half_interbeam_angle()*180/np.pi)
# Recording beam angles in glass
print("Slant angle + theta_r:", setup1.slant_angle()*180/np.pi + setup1.half_interbeam_angle()*180/np.pi)
print("Slant angle - theta_r:", setup1.slant_angle()*180/np.pi - setup1.half_interbeam_angle()*180/np.pi)
print("Bragg angle:", setup1.bragg_angle()*180/np.pi)
print("Period:", setup1.period(), "nm")
print("Spatial frequency:", setup1.spatial_frequency()*1000, "um^-1")
print(f"It's np.isnan  : {np.isnan(setup1.half_interbeam_angle())}")
print(2*setup1.half_interbeam_angle()*180/np.pi)"""
