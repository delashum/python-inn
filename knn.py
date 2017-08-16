#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import random
import math
import operator


def loadDataset(
    filename,
    split,
    trainingSet=[],
    testSet=[],
    ):

    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset) - 1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])


def distance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow(instance1[x] - instance2[x], 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = distance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x][length], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = {}

    for x in range(k):
        dist = distances[x][0]
        if dist not in neighbors:
            neighbors[dist] = 0
        neighbors[dist] += 1
    return neighbors


def getMajority(neighbors):
    mostval = 0
    for key in neighbors:
        if neighbors[key] > mostval:
            mostkey = key
            mostval = neighbors[key]
    return key


def classify(data, training):
    neighbors = getNeighbors(training, data, 3)
    return getMajority(neighbors)


def validateKNN(training, test):
    correct = 0
    for i in range(len(test)):
        if classify(test[i], training) == test[i][len(test[i]) - 1]:
            correct += 1
    return correct / float(len(test))


trainingSet = []
testSet = []
loadDataset('iris.data', 0.66, trainingSet, testSet)

correct = validateKNN(trainingSet, testSet)
print str(correct * 100) + '% correct!'
