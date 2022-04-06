from cProfile import label
import numpy as np
from scipy.interpolate import UnivariateSpline
import pandas as pd
import glob

files = glob.glob('/home/michael/Documents/PhD_docs/23Feb_Verdi/Bragg_CSV/*.csv')

print(files)
# Create class object to replicate lines 6-12 
class CurveData:
    def __init__(self, file) -> None:
        self.df = pd.read_csv(file)
        self.angles = self.df.Angle
        print(self.df.DE)
        self.diff_efficiencies = np.max(self.df.DE) - self.df.DE
        self.spline = UnivariateSpline(self.angles, self.diff_efficiencies-np.max(self.diff_efficiencies)/2, s=0)
        self.r1, self.r2 = self.spline.roots() # find the roots
        self.power = self.df['Power'][0]

curves = [CurveData(file) for file in files]
fwhms = []


import pylab as plt


for curve in curves:
    #sc = plt.scatter(curve.angles, curve.diff_efficiencies, s= 15, alpha = 0.75, label= curve.power)
    sc = plt.plot(curve.angles, curve.diff_efficiencies, label= curve.power)
    #col = sc.get_facecolors()[1].tolist()
    plt.hlines(np.max(curve.diff_efficiencies)/2, curve.r1, curve.r2, alpha = 0.75)

    # append line width to list
    fwhms.append(np.abs(curve.r1 - curve.r2))

    #plt.axvspan(curve.r1, curve.r2, facecolor='g', alpha=0.5)

plt.title(r'Diffraction Efficiency vs $\Delta \theta$, Thickness $= 100 \mu m$')
plt.ylabel(r'Diffraction Efficieny (%)')
plt.xlabel(r'$\Delta \theta$ ($\circ$)')

plt.legend()
plt.show()

labels = [curve.power for curve in curves]


x = np.arange(len(labels))  # the label locations
width = 0.35 

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, fwhms, width)
#rects2 = ax.bar(x + width/2, women_means, width, label='Women')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel(r'FWHM ($\circ$)')
ax.set_title('Profile width vs angle')
ax.set_xticks(x, labels)
#ax.legend()

#ax.bar_label(rects1, padding=3)
#ax.bar_label(rects2, padding=3)

fig.tight_layout()

#plt.show()

#plt.legend()
plt.show()

#print(diff_efficiencies)
#print(curve1.r1, curve1.r2)
print(type(curves[1].power))
