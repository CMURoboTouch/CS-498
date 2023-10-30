import numpy as np

def uniform_weighting(z,
                  zmin = 0,
                  zmax = 1):
  mask = np.logical_and(z<=zmax, z>=zmin)
  return (mask)*1.0

def tent_weighting(z,
                  zmin = 0,
                  zmax = 1):
  mask = np.logical_and(z<=zmax, z>=zmin)
  return (np.minimum(z, 1-z))*mask

def gaussian_weighting(z,
                  zmin = 0,
                  zmax = 1):
  mask = np.logical_and(z<=zmax, z>=zmin)
  return (np.exp(-4*(z-0.5)*(z-0.5)/(0.5*0.5)))*mask

def photon_weighting(z, tk=1,
                  zmin = 0,
                  zmax = 1):
  mask = np.logical_and(z<=zmax, z>=zmin)
  return tk*mask

def optimal(z, g, sig2, tk=1,
                  zmin = 0,
                  zmax = 1):
  mask = np.logical_and(z<=zmax, z>=zmin)

  return ((tk*tk)/(g*z+ sig2))*mask
