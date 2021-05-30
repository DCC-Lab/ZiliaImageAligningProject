import pandas as pd
import numpy as np


def loadComponentesSpectra():
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
    RefNothingInfront = pd.read_csv ('int75_LEDON_nothingInFront.csv',sep=',',skiprows=23).to_numpy()
    RefWhite = pd.read_csv ('int75_WHITEREFERENCE.csv',sep=',',skiprows=23).to_numpy()
    wavelengthRef=RefWhite[:,1]
    print(np.mean(RefWhite[4:],axis=1)-np.mean(RefNothingInfront[4:],axis=1))
    return np.mean(RefWhite[4:],axis=1)-np.mean(RefNothingInfront[4:],axis=1),wavelengthRef




