# Script of the experiment

import expyriment
import expyriment.design.extras
import random
import os

os.chdir("/Users/work/Desktop/Projet_AE/")

#Hardcoding of the constants of the experiment
NumberOfBlock         = 4;
NumberOfTrial         = 100;
FirstTrial            = 1;
NumberOfBlockTraining = 1;
NumberOfTrialTraining = 10;
FirstTrialTraining    = 1;

exp = expyriment.design.Experiment(name="Experiment AE")
expyriment.control.initialize(exp)

#3 different functions for the 3 different stimuli : Fixation Cross, stimulationRight on the right
#and stimulationLeft on the left.
def FixationCross():
    stim    = expyriment.stimuli.FixCross(size=(60,60))
    stim.present()
def stimulationRight():
    canvas  = expyriment.stimuli.Canvas(size=(1500,1500))
    stim1   = expyriment.stimuli.FixCross(size=(60,60))
    stim1.plot(canvas)
    stim2   = expyriment.stimuli.Circle(40, position=(500,0))
    stim2.plot(canvas)
    canvas.present()
def stimulationLeft():
    canvas  = expyriment.stimuli.Canvas(size=(1500,1500))
    stim1   = expyriment.stimuli.FixCross(size=(60,60))
    stim1.plot(canvas)
    stim2   = expyriment.stimuli.Circle(40, position=(-500,0))
    stim2.plot(canvas)
    canvas.present()

#You can call the function "fcanvas" to put some instruction between or during a trial
def fcanvas(contents):
    spacing = 100
    pos = len(contents) * spacing / 2
    canvas  = expyriment.stimuli.Canvas(size=(1500,1500))
    for i in range(0,len(contents)):
        line = expyriment.stimuli.TextLine(text=contents[i], position=(0,pos))
        line.plot(canvas)
        pos = pos - spacing
    line = expyriment.stimuli.TextLine(text="<press space to continue>", position=(0,pos))
    line.plot(canvas)
    canvas.present()
    _, _ = exp.keyboard.wait([expyriment.misc.constants.K_SPACE])

def settings():
    expyriment.io.defaults.outputfile_time_stamp = False
    #To have the variable names of what is logged in there
    expyriment.control.start()
    #To have the variable names of what is logged in there
    exp.data_variable_names = ["Block", "Trial", "Key", "RT"]

def instructions():
    #Instructions
    fcanvas(["In this task you'll have to look at a fixation cross during 1 second",
            "After 1 second a dot will appear on the right or on the left",
            "Your task will be to keep fixating the fixation cross and answer right or left with the key <- and -> as fast as possible",
            "Next screen is an example of a fixation cross"])
    #Example of a fixation cross
    stim    = expyriment.stimuli.FixCross(size=(60,60))
    stim.present()
    exp.clock.wait(2000)
    #Example of a right dot stimulation
    fcanvas(["Next screen is an example of a right dot stimulation"])
    stimulationRight()
    exp.clock.wait(2000)
    #Example of a left dot stimulation
    fcanvas(["Next screen is an example of a left dot stimulation"])
    stimulationLeft()
    exp.clock.wait(2000)

#Task
#The Experiment begin with a training
def training():
    for BlockTraining in range(1, NumberOfBlockTraining+1):
        block = expyriment.design.Block(name = 1) #FirstBlock
        trial = expyriment.design.Trial()
        OrderOfTheTrials = random.sample(range(1,11), 10); #pic a random number between 1 and 10 allow to randomize the side of the stimulus across trials
        fcanvas(["The experiment will begin with a training block"])
        TextReady = expyriment.stimuli.TextLine(text="Ready ?")
        TextReady.present()
        exp.clock.wait(1000)
        for FirstTrialTraining in range(1,NumberOfTrialTraining+1) :
            FixationCross()
            exp.clock.wait(1000)
            if OrderOfTheTrials[FirstTrialTraining-1] > 5:
                stimulationRight()
                key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT, expyriment.misc.constants.K_RIGHT])
            else:
                stimulationLeft()
                key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT, expyriment.misc.constants.K_RIGHT])
            FirstTrialTraining += 1;
        fcanvas(["Congratulation !",
                "This is the end of the training block",
                "Are you ready to begin?"])

#After the training the experiment can begin
def experiment():
    TextReady = expyriment.stimuli.TextLine(text="Ready ?")
    TextReady.present()
    exp.clock.wait(1000)
    f = open("data/" + exp.data.filename[0:-4] + "_OrderOfTheTrials.txt","w+")
    #There is 4 Blocks For each condition, 4 differents instructions for the differents conditions
    for Block in range(1, NumberOfBlock+1):
        eye = "left" if Block % 2 == 0 else "right"
        hand = "left" if (Block % 4 == 0 or Block % 4 == 1) else "right"
        fcanvas(["Please close the " + eye + " eye and answer with the " + hand + " hand during this block"])
        f.write("eye " + eye + " hand " + hand + "\n")
        block = expyriment.design.Block(name = Block)
        trial = expyriment.design.Trial()
        OrderOfTheTrials = random.sample(range(1,NumberOfTrial+1), NumberOfTrial);
        for FirstTrial in range(1,NumberOfTrial+1) :
            FixationCross()
            exp.clock.wait(1000)
            if OrderOfTheTrials[FirstTrial-1] >= NumberOfTrial/2:
                stimulationRight()
                key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT, expyriment.misc.constants.K_RIGHT])
                exp.data.add([block.name, trial.id, key, rt])
                f.write("right" + "\n")
            else:
                stimulationLeft()
                key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT, expyriment.misc.constants.K_RIGHT])
                exp.data.add([block.name, trial.id, key, rt])
                f.write("left" + "\n")
            FirstTrial += 1;
        fcanvas(["End of the block " + str(Block)])
    fcanvas(["Congrats!","You finished the experiment"])
    f.close()

def close():
    expyriment.control.end()

#we call each function separately, that allow us to sequanciate the code and easier localize potentials problems
def mainExperiment():
    settings()
    instructions()
    training()
    experiment()
    close()

if __name__ == "__main__":
    mainExperiment()

#Script of the analisis
#we call each function separately, that allow us to sequanciate the code and easier localize potentials problems

import os
import numpy as np

os.chdir("/Users/work/Desktop/Projet_AE/")

def analyse(resultsFilepath, instructionsFilepath):
    try:
        with open(resultsFilepath) as resultsFp:
            with open(instructionsFilepath) as instructionsFp:
                readingResults = False
                organizedResults = []
                for _, result in enumerate(resultsFp):
                    if (readingResults):
                        instruction = instructionsFp.readline().rstrip()
                        result = result.rstrip().split(',')
                        if (instruction.startswith("eye")): #new block
                            organizedResults.append([instruction, ["left"], ["right"]])
                            instruction = instructionsFp.readline().rstrip()

                        #organize result
                        if (instruction == "left" and result[3] == "276"):#if the stimulus is on the left and the participant pressed the left arrow
                            organizedResults[-1][1].append(int(result[4]))#last block, list "left": add the reaction time at the end
                        elif (instruction == "right" and result[3] == "275"):#if the stimulus is on the right and the participant pressed the right arrow
                            organizedResults[-1][2].append(int(result[4]))#last block, list "right": add the reaction time at the end
                    elif (result.startswith("subject_id")):
                        readingResults = True
            return organizedResults
    finally:
        resultsFp.close()
        instructionsFp.close()

def sortByIntraOrInterHemisphere(organizedResults):
    intra = []
    inter = []
    for block in organizedResults:
        if (block[0].split()[3] == "left"):#left hand
            intra += block[1][1:]#left stimulus (exclude first element saying "left")
            inter += block[2][1:]#right stimulus (exclude first element saying "right")
        else:#right hand
            inter += block[1][1:]#left stimulus (exclude first element saying "left")
            intra += block[2][1:]#right stimulus (exclude first element saying "right")
    return inter, intra

#comput mean and standard deviation
def analysedata(data):
    print(np.mean(data))
    print(np.std(data, 0))

if __name__ == "__main__":
    NbParticipants = 2
    allInter = []
    allIntra = []

    for i in range(1, NbParticipants+1):
        numParticipant = "0" + str(i) if i < 10 else str(i)
        organizedResults = analyse('data/ProjetAE_' + numParticipant + '.xpd', 'data/ProjetAE_' + numParticipant + '_OrderOfTheTrials.txt')
        inter, intra = sortByIntraOrInterHemisphere(organizedResults)
        allInter += inter
        allIntra += intra
        print(inter)
        print(intra)
    analysedata(allInter)
    analysedata(allIntra)
