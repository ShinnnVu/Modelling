import numpy as np
from scipy.stats import gamma
from scipy.stats import uniform
import decimal
import matplotlib.pyplot as plt
#With lambda
sizeOfSample = int(input("Type the sample number: "))
listBeta = []
listGamma = []
beta0 = gamma.pdf(0.5, 1)
gamma0  = gamma.pdf(0.2, 1)
listBeta.append(beta0)
listGamma.append(gamma0)
print("Base beta is", listBeta[0])
print("Base gamma is", listGamma[0])

while ((len(listBeta) < sizeOfSample) and (len(listGamma) < sizeOfSample)):
    betaVar = listBeta[-1]
    gammaVar = listGamma[-1]
    # Normal distribution with sigma = (0.034)
    betaS = np.random.normal(betaVar, 0.034) 
    gammaS = np.random.normal(gammaVar, 0.034)
    # print("Beta star is", betaS)
    # print("Gamma star is", gammaS)
    betaS = gamma.pdf(betaS, 1)
    gammaS  = gamma.pdf(gammaS, 1)
    r = min(1, (betaS * gammaS) / (betaVar * gammaVar)) 
    q = np.random.uniform(0,1)  # Uniform distribution (continuous) U(0,1)
    # print("q is", q)

    if (q < r):
        listBeta.append(betaS)
        listGamma.append(gammaS)
    else:
        listBeta.append(listBeta[-1])
        listGamma.append(listGamma[-1])

n = np.linspace(0, sizeOfSample, sizeOfSample)
logBetaRange = [np.log(x) for x in listBeta]       # To plot 
logGammaRange = [np.log(x) for x in listGamma]
fig, axs = plt.subplots(2)
fig.suptitle('Plot of Beta and Gamma with log value')
axs[0].plot(n, logBetaRange, 'b', alpha=0.5, lw=2, label='Beta')
axs[1].plot(n, logGammaRange, 'r', alpha=0.5, lw=2, label='Gamma')
#title.set_text('Beta and Gamma with ' + str(sizeOfSample) +  ' samples')
axs[0].set_xlabel('Iteration')
axs[1].set_xlabel('Iteration')
axs[0].set_ylabel('Logarithm beta value')
axs[1].set_ylabel('Logarithm gamma value')
print("Mathematical Modeling is my favorite subject")
plt.show()