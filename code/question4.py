import numpy as np
import pandas as pd
from scipy.special import gamma
from scipy.stats import gamma as sGamma
import matplotlib.pyplot as plt
import decimal
import requests
import io
import math
START_DATE = '1/22/20'
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
contentFile = requests.get(url).content
df = pd.read_csv(io.StringIO(contentFile.decode('utf-8')))
dailyTime = df.columns[4:]

def loadData(type, country):
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'
    contentFile = requests.get(url + str(type) + '_global.csv').content
    df = pd.read_csv(io.StringIO(contentFile.decode('utf-8')))
    country_df = df[df['Country/Region'] == country]
    return country_df.loc[START_DATE:]

def dailyData(data, time):
    sumValue = 0
    for x in data[time]:
        sumValue += x
    return sumValue

def processData(country, b, g):
    i = 0
    piX = 1
    dataI = loadData('confirmed', country)
    dataR = loadData('recovered', country)
    while (i < len(dailyTime)):
        dailyI = dailyData(dataI, dailyTime[i])
        dailyR = dailyData(dataR, dailyTime[i])
        X = dailyI + dailyR
        piX *= (g**b * (X)**(b - 1) * math.exp((-1) * g * X)) / gamma(b)
        print("Date: ",dailyTime[i],"->R0: ", piX)
        i += 1
    return piX

def main():
    sizeOfSample = int(input("Type the sample number: "))
    listBeta = []
    listGamma = []
    # Can choose a different value for beta0 and gamma0
    beta0 = sGamma.pdf(0.5, 1)
    gamma0  = sGamma.pdf(0.2, 1)
    listBeta.append(beta0)
    listGamma.append(gamma0)
    print("Base beta is", listBeta[0])
    print("Base gamma is", listGamma[0])

    while ((len(listBeta) < sizeOfSample) and (len(listGamma) < sizeOfSample)):
        betaVar = listBeta[-1]
        gammaVar = listGamma[-1]
        # Normal distribution with sigma = (x* 0.34)^2
        betaS = np.random.normal(betaVar, decimal.Decimal(betaVar * 0.34) ** 2)       # Use decimal when overflow
        gammaS = np.random.normal(gammaVar, decimal.Decimal(gammaVar * 0.34) ** 2)
        # print("Beta star is", betaS)
        # print("Gamma star is", gammaS)
        betaS = sGamma.pdf(betaS, 1)
        gammaS  = sGamma.pdf(gammaS, 1)
        r = min(1, (betaS * gammaS) / (betaVar * gammaVar)) 
        q = np.random.uniform(0,1)  # Uniform distribution (continuous) U(0,1)
        # print("q is", q)

        if (q < r):
            listBeta.append(betaS)
            listGamma.append(gammaS)
        else:
            listBeta.append(listBeta[-1])
            listGamma.append(listGamma[-1])

    i = 0
    ERo = 0
    country = 'China'
    while (i < sizeOfSample):
        ERo += processData(country, listBeta[i], listGamma[i]) * (listBeta[i] / listGamma[i])
        i += 1
    print('R = ',ERo)

if __name__== "__main__":
    main()