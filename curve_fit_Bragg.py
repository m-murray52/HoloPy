import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline
import argparse 

# load video and select frame averaging method
parser = argparse.ArgumentParser(description='Code for plotting measured Bragg Curve Data and plottng best fit')
parser.add_argument("--file", type=str, required= True, help='path to CSV file')
args = parser.parse_args()

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


class Grating:

    def __init__(self, spatial_frequency, wavelength_air, RIM, n_film, n_substrate, film_thickness) -> None:
        # use microns for distance unit
        # from given parameters work out parameters for plotting DE
        # bragg angle
        self.spatial_frequency = spatial_frequency
        self.wavelength_air = wavelength_air
        self.RIM = RIM
        self.n_film = n_film
        self.film_thickness = film_thickness
        self.bragg_angle = np.arcsin((spatial_frequency*wavelength_air)/(2*n_film))
        self.phase_par = (np.pi*RIM*film_thickness)/(wavelength_air*np.cos(self.bragg_angle))



def main():
    
    file = args.file
#file ='/home/michael/Documents/PhD_docs/16Feb22_VerdiLab/Bragg_CSV/MM16Feb_S5_R1_bgB.csv'
#file = '/home/michael/Documents/PhD_docs/23Feb_Verdi/Bragg_CSV/S3A_bragg_03_100.csv'
# Load experimental data
    df = pd.read_csv(file)
    angles = df.Angle
    diff_efficiencies = list((np.max(df.DE) - df.DE)*0.01)
    max_DE = max(diff_efficiencies)
    print(type(max_DE))
    index_maxDE = diff_efficiencies.index(max_DE)

    max_DE_angle = angles[index_maxDE]

    angles = [angle-max_DE_angle for angle in angles]


    grating1 = Grating(0.8, 0.532, 0.002, 1.5, 0, 50) 

    n_film =grating1.n_film
    wavelength_air = grating1.wavelength_air
    bragg_angle = grating1.bragg_angle
    thickness = grating1.film_thickness

    def diffraction_efficiency(bragg_deviation, RIM, thickness):
        # Convert angles to rads
    #bragg_deviation = np.deg2rad(bragg_deviation)
    # find deviation in film
        bragg_deviation = np.arcsin((np.sin(np.deg2rad(bragg_deviation)))/n_film)
        E = (bragg_deviation*2*np.pi*n_film*thickness*np.sin(bragg_angle))/(wavelength_air)
        v = (np.pi*RIM*thickness)/(wavelength_air*np.cos(bragg_angle))

        #de= (np.sin(np.sqrt((np.pi/2)**2 + off_braggs**2))**2)/(1+(off_braggs**2/(np.pi/2)**2))
        #return np.sin(v**2 + E**2)
        de= np.sin(np.sqrt((v)**2 + E**2))**2/(1+(E**2/(v)**2))
        return de

    def theoretical_diffraction_efficiency(bragg_deviation, v):
        # Convert angles to rads
        # Convert to angle in film
        bragg_deviation = np.arcsin((np.sin(np.deg2rad(bragg_deviation)))/n_film)
        E = (bragg_deviation*2*np.pi*n_film*thickness*np.sin(bragg_angle))/(wavelength_air)
        #v = (np.pi*RIM*thickness)/(wavelength_air*np.cos(bragg_angle))
        #de= (np.sin(np.sqrt((np.pi/2)**2 + off_braggs**2))**2)/(1+(off_braggs**2/(np.pi/2)**2))
        #return np.sin(v**2 + E**2)
        de= np.sin(np.sqrt((v)**2 + E**2))**2/(1+(E**2/(v)**2))
        return de

    plt.scatter(angles, diff_efficiencies, s= 20, label='measured data')
    popt, pcov = curve_fit(diffraction_efficiency, angles, diff_efficiencies, bounds=(0.000, [0.006, 55]))
    popt


    v = (np.pi*popt*thickness)/(wavelength_air*np.cos(bragg_angle))  
    RIM = float(popt[0])
    bestfit_thickness = float(popt[1])

    plt.plot(angles, diffraction_efficiency(angles, *popt), 'r-', label='Best-fit, RIM = {0:.3g},'.format(RIM) + ' T = {0:.3g}'.format(bestfit_thickness) + r'$\mu m$')
    # , RIM = {0:.3g}'.format(RIM)
    DE_max = np.max(diff_efficiencies)

    # Analytically derived phase parameter
    v = np.arcsin(np.sqrt(DE_max))
    #v = np.pi/2
    RIM = float((v*wavelength_air*np.cos(bragg_angle))/(np.pi*thickness))
    DE = [theoretical_diffraction_efficiency(angle, v) for angle in angles]
    print(len(angles))
    print(len(DE))


    # Plot DE vs delta_theta
    plt.plot(angles, DE, 'g-', label='Analytical, RIM = {0:.3g},'.format(RIM) + ' T = {0:.3g}'.format(thickness) + r'$\mu m$')
 
#angles = np.arange(0,len(angles),1)
#DE = np.arange(0,len(DE),1)
    spline = UnivariateSpline(angles, DE-np.max(DE)/2, s=0)
    r1, r2 = spline.roots() # find the roots
    plt.hlines(np.max(DE)/2, r1, r2, alpha = 0.75)

    plt.title(r'DE vs $\Delta \theta$, Thickness $= 50 \mu m$')
    plt.xlabel(r'$\Delta \theta_{air} (\circ)$')
    plt.ylabel('DE (au)')

    plt.legend(loc='upper right')
    plt.show()
    print(r2 - r1)


    v = (np.pi*popt*thickness)/(wavelength_air*np.cos(bragg_angle))  
    print('Phase parameter', v)
    print('Bragg angle', bragg_angle)
    print('Wavelength air', wavelength_air)
    print('Thickness', thickness)
    RIM = (v*wavelength_air*np.cos(bragg_angle))/(np.pi*thickness)
    print('RIM', RIM)
    print('Delta theta', grating1.spatial_frequency*thickness)



if __name__ == '__main__':
    print(__doc__)
    main()

"""# Define recording beam angles
beam1_angle = 30
beam2_angle = -30

# Correct for material refractive index, for unslanted grating this is equivalent to the Bragg angle at the recording wavelength
# Angles in rads
beam1_angle_medium = np.arcsin((np.sin(np.deg2rad(beam1_angle)))/grating1.n_film) 
beam2_angle_medium = np.arcsin((np.sin(np.deg2rad(beam2_angle)))/grating1.n_film) 

# range of bragg deviations in rads
bragg_deviation = np.linspace(-beam1_angle_medium/2, beam1_angle_medium/2, 10000)

# range of bragg deviations in air (degress)
bragg_deviation_in_air = np.linspace(-beam1_angle/2, beam1_angle/2, 10000)"""