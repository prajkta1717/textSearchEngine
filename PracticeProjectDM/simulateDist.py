import sys
import math
import random as randNumGen

def sampleMean(samples):
    return (float(sum(samples)) / float(len(samples)))

def sampleVariance(mean, samples):
    sum = 0.0
    for sample in samples:
        sum = sum + float((sample - mean) * (sample - mean))

    if len(samples) == 1:
        return sum
    return sum / float(len(samples) - 1)

def calculateCumulativeDistFunction(p):
    result = []
    for i in range(len(p)):
        result.append(sum(p[0:i + 1]))
    return result

def bernoulliDistribution(value, argumentNumber):
    result = []
    allValues = []
    if (len(argumentNumber)!=1):
        sys.exit('Please Enter correct number of arguments ber')
    probability = float(argumentNumber[0])
    if ((probability > 1.0) or (probability < 0.0)):
        sys.exit('probability value is not correct: '+ str(probability))
    for i in range(value):
        if (randNumGen.random() <= probability):
            result.append(1)
        else:
            result.append(0)
    populationMean = probability
    populationVariance = probability * (1 - probability)
    allValues.append(result)
    allValues.append(populationMean)
    allValues.append(populationVariance)
    return allValues


def binomialDistribution(noOfvalues, argumentNumber):
    if(len(argumentNumber)!=2):
        sys.exit('Please Enter correct number of arguments bin')

    probability = float(argumentNumber[1])
    if ((probability < 0.0) or (probability > 1.0)):
        sys.exit('probability value is incorrect for binomial Distribution: ')

    result = []
    numberOfTrials = int(argumentNumber[0])
    for i in range(noOfvalues):
        temp = 0
        for j in range(numberOfTrials):
            if randNumGen.random()<=probability:
                temp = temp + 1
        result.append(temp)
    populationMean = numberOfTrials * probability
    populationVariance = numberOfTrials * probability * (1 - probability)

    allValues = []
    allValues.append(result)
    allValues.append(populationMean)
    allValues.append(populationVariance)
    return allValues


def geometricDistribution(numberOfValues, arguments):
    if (len(arguments) != 1):
        sys.exit('Please Enter correct number of arguments geo')
    probability = float(arguments[0])
    if ((probability > 1.0) or (probability < 0.0)):
        sys.exit('probability value is not correct: ')

    result = []
    for i in range(numberOfValues):
        temp = 1
        while randNumGen.random() > probability:
            temp = temp + 1
        result.append(temp)
    populationMean = 1 / probability
    populationVariance = (1 - probability) / (probability * probability)

    allValues = []
    allValues.append(result)
    allValues.append(populationMean)
    allValues.append(populationVariance)
    return allValues


def negBinomialDistribution(value, argumentNumber):
    result = []
    if (len(argumentNumber) != 2):
        sys.exit('Please Enter correct number of arguments neg')
    j=int(argumentNumber[0])
    probability = float(argumentNumber[1])

    populationMean = j / probability
    populationVariance = (j * (1 - probability)) / (probability * probability)

    for i in range(value):
        result.append(sum(geometricDistribution(j, [probability])[0]))

    allValues = []
    allValues.append(result)
    allValues.append(populationMean)
    allValues.append(populationVariance)
    return allValues

def exponentialDistribution(argumentNumber, value):
    if(len(argumentNumber)!=1):
        sys.exit('Entered number of arguments is not correct ')
    lam = float(argumentNumber[0])
    result = []
    for i in range(value):
        result.append((0-(1/lam))*math.log(1 - randNumGen.random()))

    populationMean = 1 / lam
    populationVariance = 1 / lam ** 2

    allValues = []
    allValues.append(result)
    allValues.append(populationMean)
    allValues.append(populationVariance)
    return allValues


def poissonDistribution(value, argumentNumber):
    if(len(argumentNumber)!=1):
        sys.exit('Please Enter correct number of arguments poi')
    lam = float(argumentNumber[0])
    result = []
    for i in range(value):
        x = 0
        randNum=randNumGen.random()
        while randNum >= math.exp((0.0 - lam)):
            x = x + 1
            randNum = randNum * randNumGen.random()
        result.append(x)

    populationMean = lam
    populationVariance = lam

    allValues = []
    allValues.append(result)
    allValues.append(populationMean)
    allValues.append(populationVariance)
    return allValues

def arbDiscreteDistribution(values, argumentNumbers):

    floatValues = []
    for argNum in argumentNumbers:
        floatValues.append(float(argNum))
    F = calculateCumulativeDistFunction(floatValues)
    if (F[(len(F) - 1)] != 1):
        sys.exit('Total probability should be 1')
    result = []
    for value in range(values):
        randNum = randNumGen.random()
        temp = 0
        while F[temp] <= randNum:
            temp = temp + 1
        result.append(temp)

    populationMean = sum(floatValues)/len(floatValues)
    populationVariance = sampleVariance(populationMean, floatValues)

    allValues = []
    allValues.append(result)
    allValues.append(populationMean)
    allValues.append(populationVariance)
    return allValues


def uniformDistribution(values, argumentNumber):
    if (len(argumentNumber)!=2):
        sys.exit('Entered number of arguments is not correct')

    firstArg = float(argumentNumber[0])
    secondArg = float(argumentNumber[1])
    result = []

    if (firstArg > secondArg):
        temp = firstArg;
        firstArg = secondArg;
        secondArg = temp;
    for value in range(values):
        result.append(firstArg + ((secondArg - firstArg) * randNumGen.random()))

    populationMean = float(firstArg + secondArg) / 2
    populationVariance = float(((secondArg - firstArg) ** 2) / 12)
    allValues = []
    allValues.append(result)
    allValues.append(populationMean)
    allValues.append(populationVariance)
    return allValues

def gammaDistribution(value, argumentNumber):
    if (len(argumentNumber)!=2):
        sys.exit('Incorrect number of arguments')

    number=int(argumentNumber[0])
    lam = float(argumentNumber[1])
    result = []
    for i in range(value):
        result.append(sum(exponentialDistribution([lam], number)[0]))

    populationMean = number / lam
    populationVariance = number / lam ** 2

    allValues = []
    allValues.append(result)
    allValues.append(populationMean)
    allValues.append(populationVariance)
    return allValues


def normalDistribution(value, argumentNumber):
    if (len(argumentNumber) != 2):
        sys.exit('Number of arguments is not correct')
    halfValue= int(math.ceil(float(value) / 2))
    mu = float(argumentNumber[0])
    sigma= float(argumentNumber[1])
    result=[]

    for i in range(halfValue):
        rand1=randNumGen.random()
        rand2=randNumGen.random()

        z1=math.sqrt((0 - 2)*math.log(rand1)) * math.cos(2*(math.pi)*(rand2))
        result.append(mu+ z1 * sigma)
        z2=math.sqrt((0 - 2)*math.log(rand1)) * math.cos(2*(math.pi)*(rand2))
        result.append(mu + z2 * sigma)

        populationMean = mu
        populationVariance = sigma ** 2

        allValues = []
        allValues.append(result)
        allValues.append(populationMean)
        allValues.append(populationVariance)
        return allValues

    if (value % 2 != 0):
        result =result[0:len(result) - 1]

    return  result

def calculateDistributionValues(inputValues):
    try:

        numberOfValues = int(inputValues[1])
        inputLen = len(inputValues)
        arguments = inputValues[3: inputLen]

        randNumGen.seed(5)

        if (inputValues[2].upper()=='BINOMIAL'):
            allResultValues = binomialDistribution(numberOfValues, arguments)
            result = allResultValues[0]
            populationMean = allResultValues[1]
            populationVariance = allResultValues[2]

        elif (inputValues[2].upper()=='BERNOULLI'):
            allResultValues = bernoulliDistribution(numberOfValues, arguments)
            result = allResultValues[0]
            populationMean = allResultValues[1]
            populationVariance = allResultValues[2]
        elif (inputValues[2].upper()=='GEOMETRIC'):
            allResultValues = geometricDistribution(numberOfValues, arguments)
            result = allResultValues[0]
            populationMean = allResultValues[1]
            populationVariance = allResultValues[2]
        elif (inputValues[2].upper()=='POISSON'):
            allResultValues = poissonDistribution(numberOfValues, arguments)
            result = allResultValues[0]
            populationMean = allResultValues[1]
            populationVariance = allResultValues[2]
        elif (inputValues[2].upper()=='NEG-BINOMIAL'):
            print("hello")
            allResultValues = negBinomialDistribution(numberOfValues, arguments)
            result = allResultValues[0]
            populationMean = allResultValues[1]
            populationVariance = allResultValues[2]
        elif (inputValues[2].upper()=='NORMAL'):
            allResultValues = normalDistribution(numberOfValues, arguments)
            result = allResultValues[0]
            populationMean = allResultValues[1]
            populationVariance = allResultValues[2]
        elif (inputValues[2].upper()=='UNIFORM'):
            allResultValues = uniformDistribution(numberOfValues, arguments)
            result = allResultValues[0]
            populationMean = allResultValues[1]
            populationVariance = allResultValues[2]
        elif (inputValues[2].upper()=='GAMMA'):
            allResultValues = gammaDistribution(numberOfValues, arguments)
            result = allResultValues[0]
            populationMean = allResultValues[1]
            populationVariance = allResultValues[2]
        elif (inputValues[2].upper()=='EXPONENTIAL'):
            allResultValues = exponentialDistribution(arguments, numberOfValues)
            result = allResultValues[0]
            populationMean = allResultValues[1]
            populationVariance = allResultValues[2]
        elif (inputValues[2].upper()=='ARB-DISCRETE'):
            allResultValues = arbDiscreteDistribution(numberOfValues, arguments)
            result = allResultValues[0]
            populationMean = allResultValues[1]
            populationVariance = allResultValues[2]
        else:
            sys.exit('Above Distribution is not present')
        print('Values are: ' + str(result))

        meanValue = sampleMean(result)
        print('Sample Mean is: '+str(meanValue))

        print('Sample Variance is: '+str(sampleVariance(meanValue, result)))
        print('Population Mean is: ' + str(populationMean))
        print('Population Variance is: ' + str(populationVariance))

    except ValueError:
        print('Number format Error')


if __name__ == '__main__':
    calculateDistributionValues(sys.argv)