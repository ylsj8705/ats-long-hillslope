from numpy import loadtxt
import numpy as np
import matplotlib.pyplot as plt
import h5py
import glob

# Set up which data to read in
locations='no_pf','disc_pf','pf'
obs='mass_flux','mass_flux_moss','surface_mass_flux_east','evaporative_flux'
simulations='/north/ob*','/south/ob*'
sim1_data={}
sim1_names=[]
temp_data=[]

# read in data
for i in range(len(locations)):
    for j in range(len(simulations)):
        for k in range(len(obs)):
            temp_names=sorted(glob.glob(locations[i]+simulations[j]+'/'+obs[k]+'.dat'))
            var_names=sorted([locations[i]+'-'+simulations[j][1:6]+'-'+obs[k]])
#            print temp_names
#            print var_names
            temp_data=loadtxt(temp_names[0],comments='#',usecols=(1),unpack=False)
            sim1_data[var_names[0]]=temp_data
times=loadtxt(temp_names[0],comments='#',usecols=(0),unpack=False)
time=np.array(times)*(1.0/(1*86400))

#no_pf_total_mass=sim1_data['no_pf-north-mass_flux']+sim1_data['no_pf-north-surface_mass_flux_east']
#pf_total_mass=sim1_data['pf-north-mass_flux']+sim1_data['pf-north-surface_mass_flux_east']
#disc_pf_total_mass=sim1_data['disc_pf-north-mass_flux']+sim1_data['disc_pf-north-surface_mass_flux_east']

# Read input forcing data
force_dat = h5py.File('../hillslope_obs_daily.h5','r')

# water density...
h2o_mol = 18.0 # water molar mass
h2o_density = 1000000.0 # water grams per m3
moles_m3 = h2o_density/h2o_mol # Moles per m3

surface_area=1000.0 #domain surface area 1000m2
fm3s=86400.00/(surface_area*moles_m3)

# time period, x-axis in plots
day1=-366
dayend=-1
x_ax=range(abs(day1-dayend))

# Extract rain input data from input File
rain=86400.*(force_dat['Pr'][day1:dayend])
snow=86400.*(force_dat['Ps'][day1:dayend])

# Some stats of output data for mass balance
print 'PRECIPITATION'
print 'Total rain: ', sum(rain)
print 'Total snow: ', sum(snow)
print 'Total precip: ', sum(rain)+sum(snow)
print 'GROUNDWATER'
print 'Total gw flux pf north: ', sum(sim1_data['pf-north-mass_flux'][day1:dayend])*86400/(surface_area*moles_m3)
print 'Total gw flux pf south: ', sum(sim1_data['pf-south-mass_flux'][day1:dayend])*86400/(surface_area*moles_m3)
print 'Total gw flux disc. pf north: ', sum(sim1_data['disc_pf-north-mass_flux'][day1:dayend])*86400/(surface_area*moles_m3)
print 'Total gw flux disc. pf south: ', sum(sim1_data['disc_pf-south-mass_flux'][day1:dayend])*86400/(surface_area*moles_m3)
print 'Total gw flux no pf north: ', sum(sim1_data['no_pf-north-mass_flux'][day1:dayend])*86400/(surface_area*moles_m3)
print 'Total gw flux no pf south: ', sum(sim1_data['no_pf-south-mass_flux'][day1:dayend])*86400/(surface_area*moles_m3)
print 'min / max gw flux pf north: ', min(sim1_data['pf-north-mass_flux'][day1:dayend]),' / ',max(sim1_data['pf-north-mass_flux'][day1:dayend])
print 'min / max gw flux pf south: ', min(sim1_data['pf-south-mass_flux'][day1:dayend]),' / ',max(sim1_data['pf-south-mass_flux'][day1:dayend])
print 'min / max gw flux disc. pf north: ', min(sim1_data['disc_pf-north-mass_flux'][day1:dayend]),' / ',max(sim1_data['disc_pf-north-mass_flux'][day1:dayend])
print 'min / max gw flux disc. pf south: ', min(sim1_data['disc_pf-south-mass_flux'][day1:dayend]),' / ',max(sim1_data['disc_pf-south-mass_flux'][day1:dayend])
print 'min / max gw flux no pf north: ', min(sim1_data['no_pf-north-mass_flux'][day1:dayend]),' / ',max(sim1_data['no_pf-north-mass_flux'][day1:dayend])
print 'min / max gw flux no pf south: ', min(sim1_data['no_pf-south-mass_flux'][day1:dayend]),' / ',max(sim1_data['no_pf-south-mass_flux'][day1:dayend])
print 'SURFACE WATER'
print 'Total sw flux pf north: ', sum(sim1_data['pf-north-surface_mass_flux_east'][day1:dayend])*86400/(surface_area*moles_m3)
print 'Total sw flux pf south: ', sum(sim1_data['pf-south-surface_mass_flux_east'][day1:dayend])*86400/(surface_area*moles_m3)
print 'Total sw flux disc. pf north: ', sum(sim1_data['disc_pf-north-surface_mass_flux_east'][day1:dayend])*86400/(surface_area*moles_m3)
print 'Total sw flux disc. pf south: ', sum(sim1_data['disc_pf-south-surface_mass_flux_east'][day1:dayend])*86400/(surface_area*moles_m3)
print 'Total sw flux no pf north: ', sum(sim1_data['no_pf-north-surface_mass_flux_east'][day1:dayend])*86400/(surface_area*moles_m3)
print 'Total sw flux no pf south: ', sum(sim1_data['no_pf-south-surface_mass_flux_east'][day1:dayend])*86400/(surface_area*moles_m3)
print 'EVAPORATION'
# Evaporation is given in m3/s as I take out m/s data as extensive integral. Convert to m/d

print 'Total evaporative flux pf north: ', sum(sim1_data['pf-north-evaporative_flux'][day1:dayend])*86400/surface_area
print 'Total evaporative flux pf south: ', sum(sim1_data['pf-south-evaporative_flux'][day1:dayend])*86400/surface_area
print 'Total evaporative flux disc. pf north: ', sum(sim1_data['disc_pf-north-evaporative_flux'][day1:dayend])*86400/surface_area
print 'Total evaporative flux disc. pf south: ', sum(sim1_data['disc_pf-south-evaporative_flux'][day1:dayend])*86400/surface_area
print 'Total evaporative flux no pf north: ', sum(sim1_data['no_pf-north-evaporative_flux'][day1:dayend])*86400/surface_area
print 'Total evaporative flux no pf south: ', sum(sim1_data['no_pf-south-evaporative_flux'][day1:dayend])*86400/surface_area


# Plot groundwater flux
(figur, main_axis) = plt.subplots()
main_axis.plot(x_ax,(fm3s*(sim1_data['pf-north-mass_flux'][day1:dayend])),'b',x_ax,fm3s*(sim1_data['disc_pf-north-mass_flux'][day1:dayend]),'g',x_ax,fm3s*(sim1_data['no_pf-north-mass_flux'][day1:dayend]),'r')
main_axis.set_ylabel('GW flux (m/d)', color='red')
main_axis.tick_params(axis='y', labelcolor='red')
main_axis.legend(['Permafrost', 'Some permafrost', 'No permafrost'])
# Create right axis.
right_axis = main_axis.twinx()  # Instantiate a second axes that shares the same x-axis
right_axis.bar(x_ax, rain, color='blue')
right_axis.set_ylabel('Rain (m/d)', color='blue')
right_axis.tick_params(axis='y', labelcolor='blue')
right_axis.set_ylim(right_axis.get_ylim()[::-1])
plt.show()


# Plot subsurface and surface flux summed
plt.figure(4)
plt.plot(x_ax,(fm3s*(sim1_data['pf-north-mass_flux'][day1:dayend])+(fm3s*(sim1_data['pf-north-surface_mass_flux_east'][day1:dayend]))),'b',x_ax,fm3s*(sim1_data['disc_pf-north-mass_flux'][day1:dayend])+(fm3s*(sim1_data['disc_pf-north-surface_mass_flux_east'][day1:dayend])),'g',x_ax,fm3s*(sim1_data['no_pf-north-mass_flux'][day1:dayend])+fm3s*(sim1_data['no_pf-north-surface_mass_flux_east'][day1:dayend]),'r')
plt.title('GW+SW flux')
plt.legend(['Permafrost', 'Some permafrost', 'No permafrost'])
plt.show()
