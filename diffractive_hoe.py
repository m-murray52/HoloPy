import matplotlib
import numpy as np 
import sympy as sp 
from sympy import symbols
from sympy.plotting import plot



class DiffractiveLens:
    # a class object that contains the parameters that define a specific holographic diffractive lens
    def __init__(self, diameter, focal_length, refractive_index, input_angle, wavelength) -> None:
        self.diameter = diameter
        self.focal_length = focal_length
        self.refractive_index = refractive_index
        self.input_angle = input_angle
        self.wavelength = wavelength

    def max_output_angle(self) -> float:
        theta2 = np.arctan(0.5*self.diameter/self.focal_length)
        return theta2

    def bragg_angle(self):
        theta_bragg = (self.max_output_angle() - self.input_angle)/2
        return theta_bragg

    def min_fringe_spacing(self):
        fringe = self.wavelength/(2*self.refractive_index*np.sin(self.bragg_angle()))
        return fringe

    def radius(self) -> float:
        return self.diameter/2


diffractive_lens1 = DiffractiveLens(14000, 50000, 1, 0, 0.532)
print(diffractive_lens1.bragg_angle())
print(diffractive_lens1.min_fringe_spacing())

# Plot fring spacing vs r

r = symbols('r')


# Function to plot fringe spacing

def plot_fringes(wavelength, refractive_index, radius, focus, input_angle, r):
    return plot(wavelength/(2*refractive_index*sp.sin((sp.atan(r/focus)- input_angle)/2)), (r, -radius, radius), ylim = (-1000, 1000), xscale='linear', yscale='linear', show=True)

#fringe_plot = plot_fringes(diffractive_lens1.wavelength, diffractive_lens1.refractive_index, diffractive_lens1.radius(), diffractive_lens1.focal_length, diffractive_lens1.input_angle, r)
#fringe_plot




def plot_spatial_frequency(wavelength, refractive_index, radius, focus, input_angle, r):
    return plot(sp.Abs(2*refractive_index*sp.sin((sp.atan(r/focus)- input_angle)/2)/wavelength), (r, -radius, radius), xscale='linear', yscale='linear', show=True)



spatial_frequency_plot = plot_spatial_frequency(diffractive_lens1.wavelength, diffractive_lens1.refractive_index, diffractive_lens1.radius(), diffractive_lens1.focal_length, diffractive_lens1.input_angle, r)
spatial_frequency_plot