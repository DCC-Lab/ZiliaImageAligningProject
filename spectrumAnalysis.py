import pandas as pd
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename

# global variables for cropping wavelength
lowerLimit=510
upperLimit=590

class spectrum:
    data=np.array([])
    wavelength=np.array([])
# spectrum = {
#     "data": np.array([]),
#     "wavelength": np.array([])
# }

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
    croppedSpectrum = spectrum()
    croppedSpectrum.wavelength = Spec.wavelength[
        np.where(np.logical_and(lowerLimit <= Spec.wavelength, Spec.wavelength <= upperLimit))]
    croppedSpectrum.data = Spec.data[
        np.where(np.logical_and(lowerLimit <= Spec.wavelength, Spec.wavelength <= upperLimit))]
    return croppedSpectrum

def normalizedSpectrum(Spec):
    Spec.data=Spec.data/np.std(Spec.data)
    return Spec

def loadWhiteRef(referenceNameNothinInfront='int75_LEDON_nothingInFront.csv',
                 whiteReferenceName = 'int75_WHITEREFERENCE.csv',
                 skipRowsNothing=23, skipRowsWhite=23):
    ''' returns cropped (between 500 to 600) white reference and the wavelength'''
    RefNothingInfront = pd.read_csv (referenceNameNothinInfront,sep=',',skiprows=skipRowsNothing).to_numpy()
    RefWhite = pd.read_csv(whiteReferenceName,sep=',',skiprows=skipRowsWhite).to_numpy()
    refSpectrum = spectrum()
    refSpectrum.wavelength = RefWhite[:,1]
    refSpectrum.data = np.mean(RefWhite[:,4:],axis=1)-np.mean(RefNothingInfront[:,4:],axis=1)
    croppedRef=cropFunction(refSpectrum)
    RefCroppedNormalized=normalizedSpectrum(croppedRef)
    return RefCroppedNormalized


def loadDarkRef(skipRows=4):
    ''' returns cropped (between 500 to 600) dark reference and the wavelength'''
    filetypes = [("csv files", "*.csv")]
    csv_file_path = askopenfilename(title="select the dark reference .csv file",filetypes=filetypes)
    darkRef = pd.read_csv(csv_file_path, sep=',', skiprows=skipRows).to_numpy()
    darkRefSpec=spectrum()
    darkRefSpec.data = np.mean(darkRef[:,3:],axis=1)
    darkRefSpec.wavelength = darkRef[:,0]
    croppedDarkRef=cropFunction(darkRefSpec)
    return croppedDarkRef

a=loadWhiteRef()
b=loadDarkRef()
print(b.wavelength.shape)
print(b.data.shape)


def loadSpectrum():
    ''' returns dark reference and the wavelength'''
    filetypes = [("csv files", "*.csv")]
    csv_file_path = askopenfilename(title="select the spectrum .csv file", filetypes=filetypes)
    spectrumData = pd.read_csv(csv_file_path, sep=',', skiprows=4).to_numpy()
    spectrum=spectrumData[:, 3:]
    specWavelength=spectrumData[:, 0]
    wavelengthCropped = specWavelength[np.where(np.logical_and(lowerLimit <= specWavelength, specWavelength <= upperLimit))]
    specCropped = spectrum[np.where(np.logical_and(lowerLimit <= specWavelength, specWavelength <= upperLimit))]
    return specCropped,wavelengthCropped

def normalizeSpec():
    """returns the normalized spectrum for the data"""
    dRef, dRefWavelength = loadDarkRef()
    spectrum, specWavelength = loadSpectrum()
    dRefTile = np.tile(dRef, (spectrum.shape[1], 1))
    SpectrumData=spectrum-dRefTile.T
    STDspectrum=np.std(SpectrumData,axis=1)
    SpectrumDataNormalized=SpectrumData.T/STDspectrum
    return SpectrumDataNormalized , specWavelength

def find_nearest(array, value):
    """find the nearest value to a value in an array and returns the index"""
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def absorbanceSpectrum():
    """calculate the absorbance spectrum using white reference and normalized spectrum"""
    ref, refWavelength = loadWhiteRef()
    spectrum, spectrumWavelength = normalizeSpec()
    refModified = np.zeros(spectrum.shape)
    for i in range(spectrumWavelength.shape[0]):
        refModified[:, i] = ref[find_nearest(refWavelength, spectrumWavelength[i])]
    return np.log(refModified / spectrum),spectrumWavelength


def cropComponents():
    """crop the components regarding the upper limit and lower limit wavelengths"""
    Components = loadComponentesSpectra()
    absorbance, spectrumWavelength = absorbanceSpectrum()
    oxyhemoglobin = np.zeros(spectrumWavelength.shape)
    deoxyhemoglobin = np.zeros(spectrumWavelength.shape)
    melanin = np.zeros(spectrumWavelength.shape)
    for i in range(spectrumWavelength.shape[0]):
        oxyhemoglobin[i] = Components["oxyhemoglobin"][find_nearest(Components["wavelengths"], spectrumWavelength[i])]
        deoxyhemoglobin[i] = Components["oxyhemoglobin"][find_nearest(Components["wavelengths"], spectrumWavelength[i])]
        melanin[i] = Components["eumelanin"][find_nearest(Components["wavelengths"], spectrumWavelength[i])]
    componentsCrop = {
        "oxyhemoglobin": oxyhemoglobin,
        "deoxyhemoglobin": deoxyhemoglobin,
        "melanin": melanin}
    return componentsCrop

def componentsToArray(components):
    variables = np.ones(componentsCrop["oxyhemoglobin"].shape)
    variables = np.vstack([variables, componentsCrop["oxyhemoglobin"]])
    variables = np.vstack([variables, componentsCrop["deoxyhemoglobin"]])
    variables = np.vstack([variables, componentsCrop["melanin"]])
    return variables

def getCoef(absorbance,variables):
    for i in range(absorbance.shape[0]):
        coef=np.linalg.lstsq(variables,absorbance[i,:])
        print(coef)
    return

# componentsCrop=cropComponents()
# variables=componentsToArray(componentsCrop)
# absorbance,wavelength=absorbanceSpectrum()
# getCoef(absorbance,variables)


# componentsWCropped=Components['wavelength'][np.where(np.logical_and(500<= wavelengthDark, wavelengthDark <= 600))]
#
#
# darkRefCropped = dRef[np.where(np.logical_and(500<= wavelengthDark, wavelengthDark <= 600))]

# components_spectra = {
#             "wavelengths": wavelengths,
#             "oxyhemoglobin": oxyhemoglobin,
#             "deoxyhemoglobin": deoxyhemoglobin,
#             "methemoglobi": methemoglobin,
#             "carboxyhemoglobin": carboxyhemoglobin,
#             "eumelanin": eumelanin,
#             "yc1a": yc1a,
#             "yc2a": yc2a


# components=loadComponentesSpectra()
# wRef, wRefWavelength=loadWhiteRef()
# # print(wRef)
# a,w=normalizeSpec()
# print(a.shape)
# print(a)
# print(w.shape)

