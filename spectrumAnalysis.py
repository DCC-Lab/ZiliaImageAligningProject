import pandas as pd
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
from scipy.optimize import nnls

# global variables for cropping wavelength
lowerLimit = 510
upperLimit = 590

"""
Relative paths of test spectras
Dark ref came from E:\Background\20210316-102946-bresil-dark-2
Spectrum came from E:\Baseline3\Bresil 1511184\20210316-095955-bresil-od-onh-rlp2
"""
# These 3 will always be the same for every test
whiteRefName = r"./tests/TestSpectrums/int75_WHITEREFERENCE.csv"
refNameNothinInfront = r"./tests/TestSpectrums/int75_LEDON_nothingInFront.csv"
componentsSpectra = r'./tests/TestSpectrums/_components_spectra.csv'


class Spectrum:
    data = np.array([])
    wavelength = np.array([])

def loadComponentsSpectra(componentsSpectra):
    '''load components spectrums for the analysis'''
    spectrumComponents = pd.read_csv(componentsSpectra)
    npComponents = spectrumComponents.to_numpy()
    wavelengths = npComponents[:,0]
    oxyhemoglobin = npComponents[:,1]
    deoxyhemoglobin = npComponents[:,2]
    methemoglobin = npComponents[:,3]
    carboxyhemoglobin = npComponents[:,4]
    eumelanin = npComponents[:,5]
    yc1a = npComponents[:,6]
    yc2a = npComponents[:,7]

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
    Spec.data = Spec.data/np.std(Spec.data)
    return Spec

def loadWhiteRef(refNameNothinInfront, whiteRefName,
                 skipRowsNothing=24, skipRowsWhite=24, wavelengthColumn=1,
                 firstSpecColumn=4):
    # returns cropped (between 500 to 600) white reference and the wavelength"
    refNothingInfront = pd.read_csv(refNameNothinInfront, sep=',', skiprows=skipRowsNothing).to_numpy()
    refWhite = pd.read_csv(whiteRefName, sep=',', skiprows=skipRowsWhite).to_numpy()
    refSpectrum = Spectrum()
    refSpectrum.wavelength = refWhite[:,wavelengthColumn]
    refSpectrum.data = np.mean(refWhite[:,firstSpecColumn:],axis=1)-np.mean(refNothingInfront[:,firstSpecColumn:],axis=1)
    croppedRef = cropFunction(refSpectrum)
    refCroppedNormalized = normalizeRef(croppedRef)
    return refCroppedNormalized

def loadDarkRef(darkRefPath, skipRows=4, wavelengthColumn=0, firstSpecColumn=3):
    ''' returns cropped (between 500 to 600) dark reference and the wavelength'''
    filetypes = [("csv files", "*.csv")]
    # csv_file_path = askopenfilename(title="select the dark reference .csv file",filetypes=filetypes)
    csv_file_path = darkRefPath
    darkRef = pd.read_csv(csv_file_path, sep=',', skiprows=skipRows).to_numpy()
    darkRefSpec = Spectrum()
    darkRefSpec.data = np.mean(darkRef[:,firstSpecColumn:],axis=1)
    darkRefSpec.wavelength = darkRef[:,wavelengthColumn]
    croppedDarkRef = cropFunction(darkRefSpec)
    return croppedDarkRef

def loadSpectrum(spectrumPath, skipRows=4, wavelengthColumn=0, firstSpecColumn=3):
    ''' returns dark reference and the wavelength'''
    filetypes = [("csv files", "*.csv")]
    # csv_file_path = askopenfilename(title="select the spectrum .csv file", filetypes=filetypes)
    csv_file_path = spectrumPath
    spectrumData = pd.read_csv(csv_file_path, sep=',', skiprows=skipRows).to_numpy()
    spec = Spectrum()
    spec.data = spectrumData[:, firstSpecColumn:]
    spec.wavelength = spectrumData[:, wavelengthColumn]
    croppedSpectrum = cropFunction(spec)
    return croppedSpectrum

def normalizeSpectrum(spec, darkRef):
    """returns the normalized spectrum for the data"""
    dRefTile = np.tile(darkRef.data, (spec.data.shape[1], 1))
    spectrumData = spec.data-dRefTile.T
    STDspectrum = np.std(spectrumData,axis=1)
    spectrumDataNormalized = Spectrum()
    spectrumDataNormalized.data = spectrumData/STDspectrum[:,None]
    spectrumDataNormalized.wavelength = spec.wavelength
    return spectrumDataNormalized

def find_nearest(array, value):
    """find the nearest value to a value in an array and returns the index"""
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def absorbanceSpectrum(refSpec, normalizedSpec):
    """calculate the absorbance spectrum using white reference and normalized spectrum"""
    modifiedData = np.zeros(normalizedSpec.data.shape)
    for i in range(normalizedSpec.wavelength.shape[0]):
        modifiedData[i,:] = refSpec.data[find_nearest(refSpec.wavelength, normalizedSpec.wavelength[i])]
    modifiedSpec = Spectrum()
    normalizedSpec.data[normalizedSpec.data==0] = 0.0001
    modifiedSpec.data = np.log(np.divide(modifiedData, normalizedSpec.data, out=None, where=True, casting= 'same_kind',
                                order = 'K', dtype = None))
    modifiedSpec.wavelength = normalizedSpec.wavelength
    return modifiedSpec



def scattering(spec, bValue=1.5):
    """calculate the scattering spectrum"""
    return (spec.wavelength / 500) ** (-1 * bValue)

def reflection(spec):
    """calculate the reflection spectrum"""
    return np.squeeze(-np.log(spec.wavelength.reshape(-1, 1)))



def cropComponents(absorbanceSpectrum, componentsSpectra):
    """crop the components regarding the upper limit and lower limit wavelengths"""
    Components = loadComponentsSpectra(componentsSpectra)
    # absorbance, spectrumWavelength = absorbanceSpectrum()
    oxyhemoglobin = np.zeros(absorbanceSpectrum.wavelength.shape)
    deoxyhemoglobin = np.zeros(absorbanceSpectrum.wavelength.shape)
    melanin = np.zeros(absorbanceSpectrum.wavelength.shape)
    scat = scattering(absorbanceSpectrum)
    ref = reflection(absorbanceSpectrum)
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

def getCoef(absorbance, variables):
    """apply nnls and get coefs"""
    allCoef = np.zeros([absorbance.data.shape[1],variables.shape[0]])
    for i in range(absorbance.data.shape[1]):
        coef = nnls(variables.T,absorbance.data[:,i],maxiter=2000 )

        allCoef[i,:]=coef[0]
    print('all coef shape : ',allCoef.shape)
    print('all coefs :' , allCoef)
    return allCoef

def mainAnalysis(darkRefPath, spectrumPath, componentsSpectra=componentsSpectra,
                whiteRefName=whiteRefName, refNameNothinInfront=refNameNothinInfront):
    """load data, do all the analysis, get coefs as concentration"""
    whiteRef = loadWhiteRef(refNameNothinInfront, whiteRefName)
    darkRef = loadDarkRef(darkRefPath)
    spectrums = loadSpectrum(spectrumPath)
    normalizedSpectrum = normalizeSpectrum(spectrums, darkRef)
    absorbance = absorbanceSpectrum(whiteRef, normalizedSpectrum)
    croppedComponent = cropComponents(absorbance, componentsSpectra)
    features = componentsToArray(croppedComponent)
    # print('features shape :', features.shape)
    # coef = getCoef(absorbance,features)
    # concentration = 100 * coef[:,1] /(coef[:,1]+coef[:,2])
    # concentration[np.isnan(concentration)] = 0

    return features


# darkRefPath = r"./tests/TestSpectrums/bresilODrlp2/background.csv"
# spectrumPath = r"./tests/TestSpectrums/bresilODrlp2/spectrum.csv"

# mainAnalysis(darkRefPath, spectrumPath)


#### This is for test

# def testAnalysis ():
#     """load data, do all the analysis, get coefs as concentration"""
#     whiteRef=loadWhiteRef()
#     darkRef=loadDarkRef()
#     spectrums=loadSpectrum()
#     normalizedSpectrum=normalizeSpectrum(spectrums,darkRef)
#     absorbance=absorbanceSpectrum(whiteRef,normalizedSpectrum)
#     croppedComponent=cropComponents(absorbance)
#
#     #test spectrum with oxyhemoglobin
#     testSpec=Spectrum()
#     testSpec.data=(10+2*croppedComponent['oxyhemoglobin']+3*croppedComponent['deoxyhemoglobin']+
#                    croppedComponent['melanin']+4*croppedComponent['scattering']+
#                    croppedComponent['reflection']).reshape(-1,1)
#     testSpec.wavelength=absorbance.wavelength
#
#     features=componentsToArray(croppedComponent)
#     coef=getCoef(testSpec,features)
#     concentration = 100 * coef[:,1] /(coef[:,1]+coef[:,2])
#     concentration[np.isnan(concentration)]=0
#     print(np.mean(concentration))
#     print(np.std(concentration))
#     print(concentration)
#     print(concentration.shape)
#     return concentration
#
# testAnalysis()

####### blood sample test

# def bloodTest ():
#     """load data, do all the analysis, get coefs as concentration"""
#     whiteRef=loadWhiteRef(refNameNothinInfront='/Users/elahe/Documents/Bloodsamples/int75_LEDON_nothingInFront.csv',
#                           whiteRefName='/Users/elahe/Documents/Bloodsamples/int75_WHITEREFERENCE.csv')
#     darkRef=loadDarkRef(skipRows=24,wavelengthColumn=1,firstSpecColumn=4)
#     darkRef.data[np.isnan(darkRef.data)] = 0
#     spectrums=loadSpectrum(skipRows=24,wavelengthColumn=1,firstSpecColumn=4)
#     spectrums.data[np.isnan(spectrums.data)] = 0
#     print(spectrums.data.shape)
#     normalizedSpectrum=normalizeSpectrum(spectrums,darkRef)
#     normalizedSpectrum.data[np.isnan(normalizedSpectrum.data)] = 0
#     absorbance=absorbanceSpectrum(whiteRef,normalizedSpectrum)
#     absorbance.data[np.isnan(absorbance.data)] = 0
#
#
#     croppedComponent=cropComponents(absorbance)
#     features=componentsToArray(croppedComponent)
#
#
#     coef=getCoef(absorbance,features)
#     concentration = 100 * coef[:,1] /(coef[:,1]+coef[:,2])
#     concentration[np.isnan(concentration)]=0
#     print(np.mean(concentration))
#     print(np.std(concentration))
#     print(concentration)
#     print(concentration.shape)
#     return concentration
#
# bloodTest()
