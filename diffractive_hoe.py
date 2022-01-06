'''
A simple script used to interactively visualise plots used to model diffractive optical elements. So far only a simple diffractive lens of diameter 14 mm has been modeled here. 
User can alter the code to correspond to other lens sizes. The lenses are assumed to be thin lenses. 
User can use sliders to vary other optical lens parameters.


Usage:
  diffractive.py [--input_angle=<input_angle>] 

  Click on the image to set seed point

'''

import matplotlib
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

import argparse


parser = argparse.ArgumentParser(description='Tool for modelling holographic diffractive optical elements (DOEs)')
parser.add_argument('--input_angle', type=float, required= False, help='Input angle of beam')

args = parser.parse_args()


class DiffractiveLens:
    # a class object that contains the parameters that define a specific holographic diffractive lens
    def __init__(self, diameter, focal_length, refractive_index, input_angle, wavelength) -> None:
        self.diameter = diameter
        self.focal_length = focal_length
        self.refractive_index = refractive_index
        self.input_angle = input_angle*(np.pi/180)
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


diffractive_lens1 = DiffractiveLens(14000, 50000, 1.5, 0, 0.532)
print(diffractive_lens1.bragg_angle())
print(diffractive_lens1.min_fringe_spacing())




# Function to plot fringe spacing

def fringe_spacing(wavelength, refractive_index, radius, focus, input_angle):
    return np.abs(wavelength/(2*refractive_index*np.sin((np.arctan(radius/focus)- input_angle)/2)))

def slant_angle(radius, focus, input_angle):
    output_angle = np.arctan(radius/focus)
    return (output_angle - input_angle)/2

r = np.linspace(-7000, 7000, 700)



# Create the figure and the line that we will manipulate
fig, ax = plt.subplots(nrows = 3, ncols= 1, sharex= True, sharey=False, gridspec_kw={'height_ratios':[0.5,0.5, 0.5]})
plt.subplot(311)
line1, = plt.plot(r, fringe_spacing(diffractive_lens1.wavelength, diffractive_lens1.refractive_index, r, diffractive_lens1.focal_length, diffractive_lens1.input_angle), lw=2)
ax[0].set_xlabel('r (um)')
ax[0].set_ylabel('d (um)')

plt.subplot(312)
line2, = plt.plot(r, 1/(fringe_spacing(diffractive_lens1.wavelength, diffractive_lens1.refractive_index, r, diffractive_lens1.focal_length, diffractive_lens1.input_angle)), lw=2)
ax[1].set_xlabel('r (um)')
ax[1].set_ylabel('1/d (1/um)')
#plt.ylim(0, 100)


plt.subplot(313)
line3, = plt.plot(r, (slant_angle(r, diffractive_lens1.focal_length, diffractive_lens1.input_angle))*(180/np.pi), lw=2)
ax[2].set_xlabel('r (um)')
ax[2].set_ylabel('Slant (degrees)')

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.33)

# Make a horizontal slider to control the frequency.
axangle = plt.axes([0.25, 0.05, 0.65, 0.03])
angle_slider = Slider(
    ax=axangle,
    label='Angle',
    valmin=-(np.pi)/2,
    valmax=(np.pi)/2,
    valinit=diffractive_lens1.input_angle,
)

# Make a horizontal slider to control the frequency.
axfocus = plt.axes([0.25, 0.1, 0.65, 0.03])
focus_slider = Slider(
    ax=axfocus,
    label='Focal Length',
    valmin=0,
    valmax=250000,
    valinit=diffractive_lens1.focal_length,
)

axwavelength = plt.axes([0.25, 0.15, 0.65, 0.03])
wavelength_slider = Slider(
    ax=axwavelength,
    label='Wavelength',
    valmin=0.380,
    valmax=0.750,
    valinit=diffractive_lens1.wavelength,
)

axrefractive_index = plt.axes([0.25, 0.20, 0.65, 0.03])
refractive_index_slider = Slider(
    ax=axrefractive_index,
    label='n',
    valmin=1,
    valmax=5,
    valinit=diffractive_lens1.refractive_index,
)
# The function to be called anytime a slider's value changes
def update(val):
    line1.set_ydata(fringe_spacing(wavelength_slider.val, refractive_index_slider.val, r, focus_slider.val, input_angle=angle_slider.val))
    line2.set_ydata(1/(fringe_spacing(wavelength_slider.val, refractive_index_slider.val, r, focus_slider.val, input_angle=angle_slider.val)))
    line3.set_ydata(slant_angle(r, focus_slider.val, angle_slider.val)*(180/np.pi))
    fig.canvas.draw_idle()


# register the update function with each slider
angle_slider.on_changed(update)
focus_slider.on_changed(update)
wavelength_slider.on_changed(update)
refractive_index_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    angle_slider.reset()
    focus_slider.reset()
    wavelength_slider.reset()
    refractive_index_slider.reset()
button.on_clicked(reset)


plt.show()

# Function to plot spatial frequencies
def plot_spatial_frequency(wavelength, refractive_index, radius, focus, input_angle, r):
    return plot(sp.Abs(2*refractive_index*sp.sin((sp.atan(r/focus)- input_angle)/2)/wavelength), (r, -radius, radius), xscale='linear', yscale='linear', show=True)



#spatial_frequency_plot = plot_spatial_frequency(diffractive_lens1.wavelength, diffractive_lens1.refractive_index, diffractive_lens1.radius(), diffractive_lens1.focal_length, diffractive_lens1.input_angle, r)
#spatial_frequency_plot

# Function to calculate 
def slant_angle(radius, focus, input_angle):
    output_angle = np.atan(radius/focus)
    return (output_angle - input_angle)/2

#slant_angle_plot = plot(slant_angle(r, diffractive_lens1.focal_length, diffractive_lens1.input_angle), (r, -diffractive_lens1.radius(), diffractive_lens1.radius()))
#slant_angle_plot

