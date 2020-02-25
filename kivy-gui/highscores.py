import math, time, random, numpy, os

import pygame
from pygame.locals import *




samplePlaceholder = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]



class Scoreboard:
    def __init__(self, amount, scorerange):

        self.top = amount
        self.scorepath = "./highscores.txt" #Where the scores file is located.
        self.low, self.high = scorerange

        try:
            f = open(self.scorepath,"r")
            f.close()
        except:
            self.createNew()

        #autopopulate if no scores found
        with open(self.scorepath) as f:
            first = f.read(1)
            if not first:
                self.genScores()

    def createNew(self):
        f = open(self.scorepath,"a")
        self.genScores()
        self.orderScores()
        f.close()

    def addEntry(self,name,score):
        f=open(self.scorepath,"a")
        f.write("{}/{}/\n".format(name, score))

    def getTop(self,number):
        names = []
        scores = []

        f=open(self.scorepath,"r")
        lines = f.readlines()
        read = lines[0:number]

        for x in read:
            name = x.split("/")[0]
            score = x.split("/")[1]
            names.append(name)
            scores.append(score)

        return names,scores

    def getEntry(self, number):
        f=open(self.scorepath,"r")

        lines = f.readlines()
        read = lines[number-1]

        name = read.split("/")[0]
        score = read.split("/")[1]

        return name,score

    def deleteEntry(self, number):
        with open(self.scorepath,"r") as f:
            lines = f.readlines()

        lines.pop(number-1)

        with open(self.scorepath, "w") as f:
            for line in lines:
                f.write(line)

    def genScores(self):
        random.seed()
        for x in range(0,self.top):
            name = ""
            for x in range(0,3):
                name += (random.choice(samplePlaceholder))
            score = random.randint(self.low, self.high)
            self.addEntry(name,score)

    def orderScores(self):
        scores = []
        with open(self.scorepath,"r") as f:
            lines = f.readlines()

        for x in lines:
            name = x.split("/")[0]
            score = x.split("/")[1]
            scores.append([name,int(float(score))])

        sort = sorted(scores, key=lambda x: x[1])

        parsed = []
        for arr in sort:
            par = "/".join([arr[0],str(arr[1]),"\n"])
            parsed.append(par)

        with open(self.scorepath, "w") as f:
            index = 0
            lineCount = 0
            for line in lines:
                f.write(parsed[index])
                lineCount += 1
                if lineCount >= self.top:
                    break
                index+=1

    def checkScores(self,score):
        check = False
        self.orderScores()
        name,scoir = self.getEntry(self.top)
        if score < int(scoir): #less score is better
            check = True
        return check

        
    def getTotal(self):
        total = 0
        with open(self.scorepath,"r") as f:
            lines = f.readlines()
        for item in lines:
            total += 1
        return total

    def getRanking(self, score):
        scores = []
        self.orderScores()

        rank = 1

        with open(self.scorepath,"r") as f:
            lines = f.readlines()

        for x in lines:
            scoir = int(x.split("/")[1])
            if scoir < score:
                rank += 1
            else:
                break
        return rank

    def secToDisp(self, secs): #convert raw seconds into minutes:seconds. Try to keep it below one hour.
        mins = 0
        sec = secs
        while sec >= 60:
            mins += 1
            sec -= 60
        return "{}:{:02d}".format(mins,sec)

class Stopwatch:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.startTime = 0

    def startTimer(self):
        self.startTime = time.time()

    def updateTimer(self):
        seconds = time.time()-self.startTime
        minutes = 0
        while seconds >=60:
            minutes += 1
            seconds -= 60
            seconds += 1

        return (minutes, seconds)


    def stopTimer(self):
        print("Time Elasped: %d seconds" %(time.time()-self.startTime))
        return time.time()-self.startTime
