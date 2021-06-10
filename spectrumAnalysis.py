import pandas as pd
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
from scipy.optimize import nnls

# global variables for cropping wavelength
lowerLimit=510
upperLimit=590

class Spectrum:
    data=np.array([])
    wavelength=np.array([])

def loadComponentesSpectra():
    '''load components spectrums for the analysis'''
    spectrumComponents = pd.read_csv (r'_components_spectra.csv')
    npComponents=spectrumComponents.to_numpy()
    wavelengths=npComponents[:,0]
    oxyhemoglobin=npComponents[:,1]
    deoxyhemoglobin=npComponents[:,2]
    methemoglobin=npComponents[:,3]
    carboxyhemoglobin=npComponents[:,4]
    eumelanin=npComponents[:,5]
    yc1a=npComponents[:,6]
    yc2a=npComponents[:,7]

    components_spectra = {
            "wavelengths": wavelengths,
            "oxyhemoglobin": oxyhemoglobin,
            "deoxyhemoglobin": deoxyhemoglobin,
            "methemoglobi": methemoglobin,
            "carboxyhemoglobin": carboxyhemoglobin,
            "eumelanin": eumelanin,
            "yc1a": yc1a,
            "yc2a": yc2a
        }
    return components_spectra

def cropFunction(Spec):
    """crop the spectrum between lower limit and upper limit"""
    croppedSpectrum = Spectrum()
    croppedSpectrum.wavelength = Spec.wavelength[
        np.where(np.logical_and(lowerLimit <= Spec.wavelength, Spec.wavelength <= upperLimit))]
    croppedSpectrum.data = Spec.data[
        np.where(np.logical_and(lowerLimit <= Spec.wavelength, Spec.wavelength <= upperLimit))]
    return croppedSpectrum

def normalizeRef(Spec):
    """divide the spectrum by its standard deviation"""
    Spec.data=Spec.data/np.std(Spec.data)
    return Spec

def loadWhiteRef(referenceNameNothinInfront='int75_LEDON_nothingInFront.csv',
                 whiteReferenceName = 'int75_WHITEREFERENCE.csv',
                 skipRowsNothing=23, skipRowsWhite=23):
    ''' returns cropped (between 500 to 600) white reference and the wavelength'''
    refNothingInfront = pd.read_csv (referenceNameNothinInfront,sep=',',skiprows=skipRowsNothing).to_numpy()
    refWhite = pd.read_csv(whiteReferenceName,sep=',',skiprows=skipRowsWhite).to_numpy()
    refSpectrum = Spectrum()
    refSpectrum.wavelength = refWhite[:,1]
    refSpectrum.data = np.mean(refWhite[:,4:],axis=1)-np.mean(refNothingInfront[:,4:],axis=1)
    croppedRef=cropFunction(refSpectrum)
    refCroppedNormalized=normalizeRef(croppedRef)
    return refCroppedNormalized

def loadDarkRef(skipRows=4):
    ''' returns cropped (between 500 to 600) dark reference and the wavelength'''
    filetypes = [("csv files", "*.csv")]
    csv_file_path = askopenfilename(title="select the dark reference .csv file",filetypes=filetypes)
    darkRef = pd.read_csv(csv_file_path, sep=',', skiprows=skipRows).to_numpy()
    darkRefSpec=Spectrum()
    darkRefSpec.data = np.mean(darkRef[:,3:],axis=1)
    darkRefSpec.wavelength = darkRef[:,0]
    croppedDarkRef=cropFunction(darkRefSpec)
    return croppedDarkRef

def loadSpectrum(skipRows=4):
    ''' returns dark reference and the wavelength'''
    filetypes = [("csv files", "*.csv")]
    csv_file_path = askopenfilename(title="select the spectrum .csv file", filetypes=filetypes)
    spectrumData = pd.read_csv(csv_file_path, sep=',', skiprows=skipRows).to_numpy()
    spec = Spectrum()
    spec.data = spectrumData[:, 3:]
    spec.wavelength = spectrumData[:, 0]
    croppedSpectrum = cropFunction(spec)
    return croppedSpectrum

def normalizeSpectrum(spec,darkRef):
    """returns the normalized spectrum for the data"""
    dRefTile = np.tile(darkRef.data, (spec.data.shape[1], 1))
    spectrumData=spec.data-dRefTile.T
    STDspectrum=np.std(spectrumData,axis=1)
    spectrumDataNormalized = Spectrum()
    spectrumDataNormalized.data = spectrumData/STDspectrum[:,None]
    spectrumDataNormalized.wavelength = spec.wavelength
    return spectrumDataNormalized

def find_nearest(array, value):
    """find the nearest value to a value in an array and returns the index"""
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def absorbanceSpectrum(refSpec,normalizedSpec):
    """calculate the absorbance spectrum using white reference and normalized spectrum"""
    modifiedData = np.zeros(normalizedSpec.data.shape)
    for i in range(normalizedSpec.wavelength.shape[0]):
        modifiedData[i,:] = refSpec.data[find_nearest(refSpec.wavelength, normalizedSpec.wavelength[i])]
    modifiedSpec=Spectrum()
    normalizedSpec.data[normalizedSpec.data==0]=0.0001
    modifiedSpec.data=np.log(np.divide(modifiedData, normalizedSpec.data, out=None, where=True, casting= 'same_kind',
                                order = 'K', dtype = None))
    modifiedSpec.wavelength = normalizedSpec.wavelength
    return modifiedSpec



def scattering(spec,bValue=1.5):
    """calculate the scattering spectrum"""
    return (spec.wavelength / 500) ** (-1 * bValue)

def reflection(spec):
    """calculate the reflection spectrum"""
    return np.squeeze(-np.log(spec.wavelength.reshape(-1, 1)))



def cropComponents(absorbanceSpectrum):
    """crop the components regarding the upper limit and lower limit wavelengths"""
    Components = loadComponentesSpectra()
    # absorbance, spectrumWavelength = absorbanceSpectrum()
    oxyhemoglobin = np.zeros(absorbanceSpectrum.wavelength.shape)
    deoxyhemoglobin = np.zeros(absorbanceSpectrum.wavelength.shape)
    melanin = np.zeros(absorbanceSpectrum.wavelength.shape)
    scat=scattering(absorbanceSpectrum)
    ref=reflection(absorbanceSpectrum)
    for i in range(absorbanceSpectrum.wavelength.shape[0]):
        oxyhemoglobin[i] = Components["oxyhemoglobin"][find_nearest(Components["wavelengths"],
                                                                    absorbanceSpectrum.wavelength[i])]
        deoxyhemoglobin[i] = Components["deoxyhemoglobin"][find_nearest(Components["wavelengths"],
                                                                      absorbanceSpectrum.wavelength[i])]
        melanin[i] = Components["eumelanin"][find_nearest(Components["wavelengths"],
                                                          absorbanceSpectrum.wavelength[i])]
    componentsCrop = {
        "scattering": scat,
        "reflection": ref,
        "oxyhemoglobin": oxyhemoglobin,
        "deoxyhemoglobin": deoxyhemoglobin,
        "melanin": melanin}
    return componentsCrop

def componentsToArray(components):
    """make an n*m array of the components to use as input of the nnls"""
    variables = np.ones(components["oxyhemoglobin"].shape)
    variables = np.vstack([variables, components["oxyhemoglobin"]])
    variables = np.vstack([variables, components["deoxyhemoglobin"]])
    variables = np.vstack([variables, components["melanin"]])
    variables = np.vstack([variables, components["scattering"]])
    variables = np.vstack([variables, components["reflection"]])

    return variables

def getCoef(absorbance,variables):
    """apply nnls and get coefs"""
    allCoef=np.zeros([absorbance.data.shape[1],variables.shape[0]])
    for i in range(absorbance.data.shape[1]):
        coef=nnls(variables.T,absorbance.data[:,i],maxiter=2000 )

        allCoef[i,:]=coef[0]
    return allCoef

def mainAnalysis ():
    """load data, do all the analysis, get coefs as concentration"""
    whiteRef=loadWhiteRef()
    darkRef=loadDarkRef()
    spectrums=loadSpectrum()
    normalizedSpectrum=normalizeSpectrum(spectrums,darkRef)
    absorbance=absorbanceSpectrum(whiteRef,normalizedSpectrum)
    croppedComponent=cropComponents(absorbance)
    features=componentsToArray(croppedComponent)
    concentration=getCoef(absorbance,features)
    return concentration