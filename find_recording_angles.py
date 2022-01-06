import matplotlib
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class RecordingAngles:

    def __init__(self, wavelength, input_air, output_air, n_environment, n_medium1, n_medium2, output_grating) -> None:
        
        # Define wavelength
        self.wavelength = wavelength

        # Define input angle in air. Convert to radians
        self.input_air =  input_air*np.pi/180

        # Define output angle in air
        self.output_air = output_air*np.pi/180

        # Define environment refractive index (e.g. for air this equals 1)
        self.n_environment = n_environment

        # Define environment refractive index (e.g. for air this equals 1)
        self.n_medium1 = n_medium1

        # Define refractive index for material containing the grating pattern 
        self.n_medium2 = n_medium2

        # Define grating input angle. Use Snell's Law
        self.grating_input = np.arcsin((self.n_environment/self.n_medium1)*np.sin(self.input_air))

        # Define grating output beam angle
        self.grating_output = output_grating*np.pi/180

    def slant_angle(self):
        return (self.grating_input+self.grating_output)/2

    def bragg_angle(self):
        return (self.grating_input-self.grating_output)/2

    def period(self):
        return np.abs(self.wavelength/2*self.n_medium2*np.sin(self.bragg_angle()))

    def spatial_frequency(self):
        return 1/self.period()

    def half_interbeam_angle(self):
        return np.arcsin(self.wavelength/(self.n_medium1*2*self.period()))


setup1 = RecordingAngles(623.8, -55, 45, 1, 1.5, 1.52, 45)

print("Input angle in air: ", setup1.grating_input*180/np.pi)
print("Grating input angle:", setup1.grating_input*180/np.pi)
print("Grating output angle:", setup1.grating_output*180/np.pi)
print("Slant angle:", setup1.slant_angle()*180/np.pi)
print("Theta_r:", setup1.half_interbeam_angle()*180/np.pi)
print("Slant angle + theta_r:", setup1.slant_angle()*180/np.pi + setup1.half_interbeam_angle()*180/np.pi)
print("Slant angle - theta_r:", setup1.slant_angle()*180/np.pi - setup1.half_interbeam_angle()*180/np.pi)
print("Bragg angle:", setup1.bragg_angle()*180/np.pi)
print("Period:", setup1.period(), "nm")
print("Spatial frequency:", setup1.spatial_frequency())
print(f"It's np.isnan  : {np.isnan(setup1.half_interbeam_angle())}")
print(setup1.half_interbeam_angle())

