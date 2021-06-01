import pandas as pd
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename


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

def loadWhiteRef():
    ''' returns cropped (between 500 to 600) white reference and the wavelength'''
    RefNothingInfront = pd.read_csv ('int75_LEDON_nothingInFront.csv',sep=',',skiprows=23).to_numpy()
    RefWhite = pd.read_csv ('int75_WHITEREFERENCE.csv',sep=',',skiprows=23).to_numpy()
    wavelengthRef=RefWhite[:,1]
    wRef=np.mean(RefWhite[:,4:],axis=1)-np.mean(RefNothingInfront[:,4:],axis=1)
    wavelengthCropped=wavelengthRef[np.where(np.logical_and(500<= wavelengthRef, wavelengthRef <= 600))]
    RefCropped = wRef[np.where(np.logical_and(500 <= wavelengthRef, wavelengthRef <= 600))]
    RefCroppedNormalized=RefCropped/np.std(RefCropped)
    return RefCroppedNormalized,wavelengthCropped

def loadDarkRef():
    ''' returns cropped (between 500 to 600) dark reference and the wavelength'''
    filetypes = [("csv files", "*.csv")]
    csv_file_path = askopenfilename(title="select the dark reference .csv file",filetypes=filetypes)
    darkRef = pd.read_csv(csv_file_path, sep=',', skiprows=4).to_numpy()
    dRef = np.mean(darkRef[:,3:],axis=1)
    wavelengthDark = darkRef[:,0]
    wavelengthCropped=wavelengthDark[np.where(np.logical_and(500<= wavelengthDark, wavelengthDark <= 600))]
    darkRefCropped = dRef[np.where(np.logical_and(500<= wavelengthDark, wavelengthDark <= 600))]
    return darkRefCropped,wavelengthCropped

def loadSpectrum():
    ''' returns dark reference and the wavelength'''
    filetypes = [("csv files", "*.csv")]
    csv_file_path = askopenfilename(title="select the spectrum .csv file", filetypes=filetypes)
    spectrumData = pd.read_csv(csv_file_path, sep=',', skiprows=4).to_numpy()
    spectrum=spectrumData[:, 3:]
    specWavelength=spectrumData[:, 0]
    wavelengthCropped = specWavelength[np.where(np.logical_and(500 <= specWavelength, specWavelength <= 600))]
    specCropped = spectrum[np.where(np.logical_and(500 <= specWavelength, specWavelength <= 600))]
    return specCropped,wavelengthCropped

def normalizeSpec():
    dRef, dRefWavelength = loadDarkRef()
    spectrum, specWavelength = loadSpectrum()
    dRefTile = np.tile(dRef, (spectrum.shape[1], 1))
    SpectrumData=spectrum-dRefTile.T
    STDspectrum=np.std(SpectrumData,axis=1)
    SpectrumDataNormalized=SpectrumData.T/STDspectrum
    return SpectrumDataNormalized , specWavelength

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def absorbanceSpectrum():
    ref, refWavelength = loadWhiteRef()
    spectrum, spectrumWavelength = normalizeSpec()
    refModified = np.zeros(spectrum.shape)
    print(ref.shape)
    for i in range(spectrumWavelength.shape[0]):
        refModified[:, i] = ref[find_nearest(refWavelength, spectrumWavelength[i])]
    return np.log(refModified / spectrum)


def componentsCoef():




# components=loadComponentesSpectra()
# wRef, wRefWavelength=loadWhiteRef()
# # print(wRef)
# a,w=normalizeSpec()
# print(a.shape)
# print(a)
# print(w.shape)

