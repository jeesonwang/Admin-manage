from numpy import *

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [list(map(float,line)) for line in stringArr]
    return mat(datArr)

def pca(dataMat, topNfeat=9999999):
    meanVals = mean(dataMat, axis=0)
    meanRemoved = dataMat - meanVals #去除平均值
    covMat = cov(meanRemoved, rowvar=0)
    eigVals,eigVects = linalg.eig(mat(covMat))
    eigValInd = argsort(eigVals)            #排序，从大到小排序
    eigValInd = eigValInd[:-(topNfeat+1):-1]  #去除不需要的维度
    redEigVects = eigVects[:,eigValInd]       #特征向量进行排序，从大到小排序
    lowDDataMat = meanRemoved * redEigVects   #把数据转化成新的维度
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat, reconMat

#将NaN替换成平均值
def replaceNanWithMean(): 
    datMat = loadDataSet('secom.data', ' ')
    numFeat = shape(datMat)[1]
    for i in range(numFeat):
        meanVal = mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i]) #values that are not NaN (a number)
        datMat[nonzero(isnan(datMat[:,i].A))[0],i] = meanVal  #set NaN values to mean
    return datMat

daMat = replaceNanWithMean()
lowDDataMat, reconMat = pca(daMat)
print(shape(daMat))
print(shape(lowDDataMat))
