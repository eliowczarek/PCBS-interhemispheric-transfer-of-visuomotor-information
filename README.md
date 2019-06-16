Interhemispheric Transfer of Visuomotor Information
===================================================

The aim of this project is to measur thanks to a unimanual reaction time (RT) paradigm and lateralized visual stimuli an estimatation of interhemispheric transfer time in normal right-handed subjects. Poffenberger in 1912 was the first to study thanks to a real simple task to measure this time transfer between the two emispheres.
Moreover, Marzi et al. in 1991 shown other results. Firstly there is a difference in the measur of reaction time (RT) when a task is performed by only one hemisphere compared to the both (one visual stimuli treated by one hemisphere and the movement is performed thanks to the other). Secondly, they shown a difference of accuracy between the two hemisphere (one performed the tasks faster).

The experiment consist of the presentation of a dot in one hemi-field per trial (right or left), the participant has to press with one hand the key indicating the side of the dot on the screen.
Before each block there is some instructions, indicating which hand the participants has to use and which eyes he has to close. They had to close one eye in order to respect some of the paper presented in Marzi et al. (1991).

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Interhemispheric Transfer of Visuomotor Information](#interhemisphericT-transfert-of-visuomotor-information)
    - [Experiment](#experiment)
      - [Importation and experimental constant](#importation-and-experimental-constant)
      - [Preparation of the stimuli](#preparation-of-the-experiment)
      - [Instructions](#instructions)
      - [Setting and end of the experiment](#setting-and-end-of-the-experiment)
      - [Training](#training)
      - [Main Experiment](#main-experiment)
    - [Analysis](#analysis)
      - [Data reorganisation](#data-reorganisation)
      - [Mean and standard deviation](#mean-and-standard-deviasion)
      - [Execusion](#execusion)
    - [CONCLUSION](#conclusion)

<!-- markdown-toc end -->

## Experiment

### Importation and experimental constant

We firstly import what we need to run our script (basic python importation), be sure that we are in the right file, and hardcode the number of blocks and trials for the main experiment and the training.

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

### Preparation of the stimuli

There is 3 different functions for the 3 different stimuli : Fixation Cross, stimulationRight on the right and stimulationLeft on the left.

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

### Instructions

You can call the function "fcanvas" to put some instruction on one screen between or during a trial

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

Then we have the instructions

    def instructions():
    #Instructions
    fcanvas(["In this task you'll have to look at a fixation cross during 1 second",
            "After 1 second a dot will appear on the right or on the left",
            "Your task will be to keep fixating the fixation cross and answer right or left with the key <- and -> as fast as possible",
            "Next screen is an example of a fixation cross"])
            
Here are example of fixation cross and stimuli, they stay 2 seconds on the screen
            
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





