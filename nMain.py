from tkinter import *
import psutil
import os
import time
from datetime import datetime
import sys
import threading
from tktooltip import ToolTip


from nGenAlgos import binaryTree, dfg, recursiveDivision, kruskals, growingTree
from nSolAlgos import tremaux, bfs, threadedbfs, aStar, dijkstras, dead_end_filling


# Maximise maximum recursions per function for Recursive Division
sys.setrecursionlimit(1000000000)


# Define the main "frame" as a Tkinter window
frame = Tk()
# Set canvas to take up whole frame, of size 1200x750
canvas = Canvas(width=1200, height=750, highlightthickness=0)
frame.geometry("1200x750")


# List of all generation/solving algorithms
gens = ["Binary Tree", "Depth-First Growth", "Recursive Division", "Kruskal's Algorithm", "Growing Tree"]
sols = ["Trémaux Algorithm", "Breadth-First Search", "Multithreaded BFS", "A Star", "Dijkstra's Algorithm", "Dead-End Filling"]


# Is the "previous runs" menu on the main menu expanded?
runExpanded = False
# Starting generation algorithm for cyclical selection of generation algorithms in "previous runs" menu
currentGen = "Depth-First Growth"


def runExpand():
    global runExpanded


    def changeAlgo(shift):
        global currentGen
        # Move to next index in array
        if shift == "forward":
            # If currentGen is already at end of list, cycle back to front
            if gens.index(currentGen) != len(gens)-1:
                genAlgoQuery = gens[gens.index(currentGen)+1]
            else:
                genAlgoQuery = gens[0]
        # Move to previous index in array
        else:
            # If currentGen is already at front of list, cycle back to end
            if gens.index(currentGen) != 0:
                genAlgoQuery = gens[gens.index(currentGen)-1]
            else:
                genAlgoQuery = gens[-1]
        # Update generation algorithm title
        algoTitle["text"] = genAlgoQuery
        currentGen = genAlgoQuery
        # Get runs with the same generation algorithm
        sameCombos = [tempRun for tempRun in runs if tempRun.gen == genAlgoQuery]
        # Get list of all solving algorithms from algorithms of the same generation algorithm. Remove duplicates to get a unique list
        uniqueRuns = len(list(dict.fromkeys([run.sol for run in sameCombos])))
        # If every solving algorithmm has been run on this generation algorithm, change colors of algorithm title
        if uniqueRuns == 6:
            algoTitle["fg"] = "white"
            algoTitle["bg"] = "#014d4e"
        else:
            algoTitle["bg"] = "white"
            algoTitle["fg"] = "#014d4e"
        # If there are any recordings for this run, get the average runtime
        if len(sameCombos) > 0:
            avgRuntime = sum([run.tim for run in sameCombos]) / len(sameCombos)
        else:
            # Otherwise, set the average runtime to 0
            avgRuntime = 0
                                                                                 
        runDescription["text"] = f"Total Runs - {len(sameCombos)}\n" + f"Unique Runs - {uniqueRuns}/6\n" + f"Average Runtime/Cell - {'{:.4f}'.format(avgRuntime)} µs"
        # Declare times, cpus and mems as dictionaries that map a key (the run object) to a value (its time/average CPU usage/average memory usage) to retreive run object from performance metrics
        times, cpus, mems = {}, {}, {}
        for tempRun in sameCombos:
            times[tempRun] = tempRun.tim
            cpus[tempRun] = tempRun.acu
            mems[tempRun] = tempRun.ame
        # Sort dictionaries by values
        sortedTimes = {k: v for k, v in sorted(times.items(), key=lambda item: item[1])}
        sortedCPUs = {k: v for k, v in sorted(cpus.items(), key=lambda item: item[1])}
        sortedMems = {k: v for k, v in sorted(mems.items(), key=lambda item: item[1])}
        # If there are no runs, fill with N/As
        if len(sameCombos) == 0:
            timeDescription["text"] = f"Time\n\n1. N/A\n2. N/A\n3. N/A"
            computeDescription["text"] = f"CPU Usage\n\n1. N/A\n2. N/A\n3. N/A"
            memoryDescription["text"] = f"Memory Usage\n\n1. N/A\n2. N/A\n3. N/A"
        # If there is one run, list the most efficient algorithm for each category with the number of runs it occupied, fill the rest with N/As
        if len(sameCombos) == 1:
            timeDescription["text"] = f"Time\n\n1. {(list(sortedTimes.keys())[0]).sol} - {(list(sortedTimes.keys())[0]).run} runs\n2. N/A\n3. N/A"
            computeDescription["text"] = f"CPU Usage\n\n1. {(list(sortedCPUs.keys())[0]).sol} - {(list(sortedCPUs.keys())[0]).run} runs\n2. N/A\n3. N/A"
            memoryDescription["text"] = f"Memory Usage\n\n1. {(list(sortedMems.keys())[0]).sol} - {(list(sortedMems.keys())[0]).run} runs\n2. N/A\n3. N/A"
        elif len(sameCombos) == 2:
            timeDescription["text"] = f"Time\n\n1. {(list(sortedTimes.keys())[0]).sol} - {(list(sortedTimes.keys())[0]).run} runs\n2. {(list(sortedTimes.keys())[1]).sol} - {(list(sortedTimes.keys())[1]).run} runs\n3. N/A"
            computeDescription["text"] = f"CPU Usage\n\n1. {(list(sortedCPUs.keys())[0]).sol} - {(list(sortedCPUs.keys())[0]).run} runs\n2. {(list(sortedCPUs.keys())[1]).sol} - {(list(sortedCPUs.keys())[1]).run} runs\n3. N/A"
            memoryDescription["text"] = f"Memory Usage\n\n1. {(list(sortedMems.keys())[0]).sol} - {(list(sortedMems.keys())[0]).run} runs\n2. {(list(sortedMems.keys())[1]).sol} - {(list(sortedMems.keys())[1]).run} runs\n3. N/A"
        if len(sameCombos) >= 3:
            timeDescription["text"] = f"Time\n\n1. {(list(sortedTimes.keys())[0]).sol} - {(list(sortedTimes.keys())[0]).run} runs\n2. {(list(sortedTimes.keys())[1]).sol} - {(list(sortedTimes.keys())[1]).run} runs\n3. {(list(sortedTimes.keys())[2]).sol} - {(list(sortedTimes.keys())[2]).run}"
            computeDescription["text"] = f"CPU Usage\n\n1. {(list(sortedCPUs.keys())[0]).sol} - {(list(sortedCPUs.keys())[0]).run} runs\n2. {(list(sortedCPUs.keys())[1]).sol} - {(list(sortedCPUs.keys())[1]).run} runs\n3. {(list(sortedCPUs.keys())[2]).sol} - {(list(sortedCPUs.keys())[2]).run}"
            memoryDescription["text"] = f"Memory Usage\n\n1. {(list(sortedMems.keys())[0]).sol} - {(list(sortedMems.keys())[0]).run} runs\n2. {(list(sortedMems.keys())[1]).sol} - {(list(sortedMems.keys())[1]).run} runs\n3. {(list(sortedMems.keys())[2]).sol} - {(list(sortedMems.keys())[2]).run}"
       
    # If the previous runs bar is not expanded, expand, otherwise, close the previous runs bar
    if not runExpanded:
        # Destroy all items in mainOptions (the left side of the main menu), such that the run sidebar is still visible on the right
        for x in mainOptions:
            x.destroy()
        third_frame = Frame(canvas)
        canvas.create_window((0,0), window=third_frame, anchor="nw")
        algoTitle = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 24), width=25, pady=57, justify="center", text="Recursive Division")
        algoTitle.grid(row=0, column=0, rowspan=2, columnspan=2)
        upOption = Button(third_frame, bg="#014d4e", borderwidth=0.5, activebackground="white", activeforeground="#014d4e", relief="groove", fg="white", text="▲", command=lambda: changeAlgo("forward"), font=("Calibri", 28), width=10)
        upOption.grid(row=0, column=2)
        downOption = Button(third_frame, bg="#014d4e", borderwidth=0.5, activebackground="white", activeforeground="#014d4e", relief="groove", fg="white", text="▼", command=lambda: changeAlgo("backward"), font=("Calibri", 28), width=10)
        downOption.grid(row=1, column=2)
        # Default vaues for runDescription, changed with changeAlgo()
        runDescription = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 18), width=50, pady=40, justify="center", text=
        """Total Runs - 0
Unique Runs - 0/6
Average Runtime/Cell - 0.0000 µs""")
        runDescription.grid(row=2, column=0, columnspan=3, sticky="w")
        timeDescription = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 18), wraplength=150, padx=4, height=16, justify="center", text=
        """Time
   
1. N/A
2. N/A
3. N/A""")
        timeDescription.grid(row=3, column=0, sticky="nesw")
        computeDescription = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 18), wraplength=150, padx=4, height=16, justify="center", text=
        """CPU Usage


1. N/A
2. N/A
3. N/A""")
        computeDescription.grid(row=3, column=1, sticky="nesw")
        memoryDescription = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 18), wraplength=150, padx=4, height=16, justify="center", text=
        """Memory Usage
   
1. N/A
2. N/A
3. N/A""")
        memoryDescription.grid(row=3, column=2, sticky="nesw")
        changeAlgo("forward")
       
        # Toggle runExpanded
        runExpanded = True
    else:
        # Toggle runExpanded and open the main menu
        runExpanded = False
        mainMenuCmd()


def specificRunExpand():
    for x in mainOptions:
        x.destroy()


    # Get position of cursor relative to frame position
    yPos = frame.winfo_pointery()-frame.winfo_rooty()
    # 93.75 = 750/8 for the 8 rows in the run sidebar
    # E.g. If cursor occupies y position between 93.75 and 93.75x2 at time of clicking, the most recent run has been clicked, as the space between 0 and 93.75 is occupied by the previous runs title
    run = runs[len(runs)-1-int((yPos//93.75)-1)]


    third_frame = Frame(canvas)
    canvas.create_window((0,0), window=third_frame, anchor="nw")
    runCount = Label(third_frame, bd=0, bg="#014d4e", borderwidth=0.5, relief="groove", fg="white", font=("Calibri", 20), width=14, height=4, pady=11, justify="center", text="Run #" + str(run.rpo) + "\n" + str(run.gen).replace(' ', '\n') + " #" + str(run.ott))
    runCount.grid(row=0, column=0)
    algoTitle = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 22), width=26, height=4, pady=5, justify="center", text=str(run.gen) + "\n+ " + str(run.sol))
    algoTitle.grid(row=0, column=1, columnspan=2)
    # E.g. Time of Run - (timestamp)
    # Runs of this combo - (# simulations where this generation algorithm has run with this solving algorithm)
    # Grid size - (gridCols x gridRows for this series of simulations)
    # CPU/Memory sampling interval - (CPU/Memory sampling interval for this series of simulations) seconds
    runDescription = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 18), width=50, pady=40, justify="center", text=
    f"Time of Run – {run.abt}\nRuns of this combo – 1\nGrid size – {run.cols}x{run.rows}\nCPU/Memory sampling interval – {run.cms} seconds")
    runDescription.grid(row=1, column=0, columnspan=3, sticky="w")


    # Table is initiated, with attributes of run object, formatted to 2 decimal places, displayed in 2nd column of table
    data = [["", "Overall Solving"],
    ["Overall Runtime", f"{'{:.2f}'.format(run.ort)} seconds"],
    ["Average Runtime", f"{'{:.2f}'.format(run.tim)} μs"],
    ["Peak Memory Usage", f"{'{:.2f}'.format(run.pme)} MB"],
    ["Average Memory Usage", f"{'{:.2f}'.format(run.ame)} MB"],
    ["Peak CPU Usage", f"{'{:.2f}'.format(run.pcu)}%"],
    ["Average CPU Usage", f"{'{:.2f}'.format(run.acu)} %"]]
    for rowCnt, row in enumerate(data):
        # Category
        cat = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 14, "bold"), width=30, pady=16, justify="center", text=row[0])
        cat.grid(row=rowCnt+2, column=0, columnspan=2, sticky="w")
        # Entry
        entry = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 14), width=30, pady=16, justify="center", text=row[1])
        entry.grid(row=rowCnt+2, column=1, columnspan=2, sticky="e")


# Dictionary mapping a key (tuple contain generation and solving algorithm) to a value (# of simulations using this combo). Default values are 0
combos = {}
for gen in gens:
    for sol in sols:
        combos[(gen, sol)] = 0


def runEnd():
    global combos
    # Incrementing the entry in the dictionary by the number of simulations in this series
    combos[(genAlgo, solAlgo)] += simulations


    # Reset canvas, destroy the run sidebar (right side of main menu)
    canvas.delete("all")
    canvas.configure(width=1200, height=750)
    for x in runSideBar:
        x.destroy()


    third_frame = Frame(canvas)
    canvas.create_window((0,0), window=third_frame, anchor="nw")
    runCount = Label(third_frame, bd=0, bg="#014d4e", borderwidth=0.5, relief="groove", fg="white", font=("Calibri", 20), width=15, height=4, pady=11, justify="center", text=f"Run #" + str(len(runs)) + "\n" + str(genAlgo).replace(' ', '\n') + " #" + str(len([1 for run in runs if run.gen == genAlgo])))
    runCount.grid(row=0, column=0)
    algoTitle = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 22), width=26, height=4, pady=5, justify="center", text=str(genAlgo) + "\n+ " + str(solAlgo))
    algoTitle.grid(row=0, column=1, columnspan=2)
    runDescription = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 18), width=51, pady=40, justify="center", text=
    f"Time of Run – {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}\nRuns of this combo – {combos[(genAlgo, solAlgo)]}\nGrid size – {gridCols}x{gridRows}\nCPU/Memory sampling interval – {sampleRate} seconds")
    runDescription.grid(row=1, column=0, columnspan=3, sticky="w")
   
    # Table is initialised as before, but with calclation of global variables instead of reading object attributes
    data = [["", "Overall Solving"],
    ["Overall Runtime", f"{'{:.2f}'.format(sum(runTimes))} seconds"],
    ["Average Runtime Per Cell", f"{'{:.2f}'.format((1000000*sum(runTimes))/(len(runTimes)*(gridCols*gridRows)))} µs"],
    ["Peak Memory Usage", f"{'{:.2f}'.format(max(memReadings))} MB"],
    ["Average Memory Usage", f"{'{:.2f}'.format(sum(memReadings)/len(memReadings))} MB"],
    ["Peak CPU Usage", f"{'{:.2f}'.format(max(cpuReadings))}%"],
    ["Average CPU Usage", f"{'{:.2f}'.format(sum(cpuReadings)/len(cpuReadings))} %"]]
    for rowCnt, row in enumerate(data):
        cat = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 14, "bold"), width=31, pady=16, justify="center", text=row[0])
        cat.grid(row=rowCnt+2, column=0, columnspan=2, sticky="w")
        entry = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 14), width=31, pady=16, justify="center", text=row[1])
        entry.grid(row=rowCnt+2, column=1, columnspan=2, sticky="e")
   
    rerunButton = Button(third_frame, bd=0, bg="#014d4e", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", fg="white", font=("Calibri", 32), width=27, height=5, pady=27, justify="center", text=f"Re-Run Configuration", command=runProgram)
    rerunButton.grid(row=0, rowspan=2, column=4, columnspan=5, sticky="nw")
    reconfigButton = Button(third_frame, bd=0, bg="#014d4e", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", fg="white", font=("Calibri", 32), width=27, height=5, pady=50, justify="center", text=f"Re-Config", command=config)
    reconfigButton.grid(row=2, rowspan=8, column=4, columnspan=5, sticky="nw")


def settingsExpand():
    def confirmSettings():
        global sampleRate
        sample = sampleEntry.get()
        try: # Checking if entry is float
            sample = float(sample)
            if sample <= 0:
                seterrorLabel["text"] = "Sample rate is not a positive number"
                return
            if sample < 0.001:
                seterrorLabel["text"] = "Sample rate too high, please re-enter"
                return
            elif sample > 10:
                seterrorLabel["text"] = "Sample rate too low, please re-enter"
                return
        except:
            seterrorLabel["text"] = "Sample is not an integer"
            return
        # If not caught by any error, go back to main menu
        sampleRate = sample
        mainMenuCmd()
    # Destroy each main option (left side of main menu)
    for x in mainOptions:
        x.destroy()


    third_frame = Frame(canvas)
    canvas.create_window((0,0), window=third_frame, anchor="nw")
    settingsTitle = Label(third_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 36), width=25, pady=45, justify="center", text="Settings")
    settingsTitle.grid(row=0, column=0, columnspan=3)
    returnToMenuButton = Button(third_frame, bd=0, bg="#014d4e", fg="white", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", font=("Calibri", 20), width=3, pady=9, justify="center", text="X", command=mainMenuCmd)
    returnToMenuButton.grid(row=0, column=0, sticky="nw")
    sampleLabel = Label(third_frame, bd=0, bg="#014d4e", fg="white", font=("Calibri", 22), width=40, pady=40, justify="center", text="Memory/CPU Sampling Rate\n(seconds/sample)")
    sampleLabel.grid(row=3, column=0, columnspan=3)
    sampleEntry = Entry(third_frame, width=39, fg="#014d4e", font=("Calibri", 22), justify="center", bd=0)
    sampleEntry.grid(row=4, column=0, columnspan=3, ipady=30, ipadx=10)
    if sampleEntry.get() == "":
        sampleEntry.insert(END, 0.1)
    confirmButton = Button(third_frame, bg="#014d4e", activebackground="white", activeforeground="#014d4e", relief="groove", fg="white", text="Confirm", font=("Calibri", 26), width=33, height=4, command=confirmSettings)
    confirmButton.grid(row=5, column=0, columnspan=3)
    seterrorLabel = Label(third_frame, bg="#014d4e", activebackground="white", activeforeground="#014d4e", relief="groove", fg="white", text="", font=("Calibri", 26), width=33, height=3, pady=10, padx=3)
    seterrorLabel.grid(row=6, column=0, columnspan=3)


# Generation and Solving algorithm set to None as default, to be checked in lpc() whether any generation/solving algorithm has been inputted by the user
genAlgo, solAlgo = None, None
# Render mode set to False by default
renderMode = False
def config():
    # Reset canvas
    canvas.delete("all")
    canvas.configure(width=1200, height=750)
    third_frame = Frame(canvas)


    # Nested function for creating buttons and running validity checks and updating global variables once a button is pressed
    def createButton(text="", algoType="", run=""):
        def runCmd(tempRun, tempAlgoType):
            global gridCols, gridRows, simulations, genAlgo, solAlgo
            gcol, grow = gridSizeCEntry.get(), gridSizeREntry.get()
            numsim = simulationPassesEntry.get()
            # If start button has been pressed, perform validity checks on entries
            if tempAlgoType == "start":
                if gcol.isdigit() and grow.isdigit(): # Checking if entries are whole integers
                    gcol, grow = int(gcol), int(grow)
                    if gcol >= 3 and grow >= 3 and gcol <= 500 and grow <= 500: # Checking if entries are on edges of maze
                        gridCols, gridRows = gcol, grow
                    else:
                        errorLabel["text"] = "Invalid range for col/row entry"
                        return
                else:
                    errorLabel["text"] = "Col/row not int"
                    return
                if numsim.isdigit():
                    numsim = int(numsim)
                    if numsim >= 1 and numsim <= 100:
                        simulations = numsim
                    else:
                        errorLabel["text"] = "Invalid range for simulations entry"
                        return
                else:
                    errorLabel["text"] = "Simulation not int"
                    return
               
                if genAlgo == None: # Have algorithms been selected?
                    errorLabel["text"] = "Please select generation algorithm"
                    return
                if solAlgo == None:                    
                    errorLabel["text"] = "Please select solving algorithm"
                    return
                # If all validity checks passed, run program with parameters
                runProgram()


            else: # If button has been pressed to specify an algorithm
                if tempAlgoType == "gen":
                    genAlgo = tempRun
                else:
                    if solAlgo == "Multithreaded BFS" and tempRun == "Breadth-First Search":
                        # Toggling color of BFS button if clicking on BFS button after it has turned to Multithreaded BFS
                        threadedBFSButton["fg"] = "#014d4e"
                        threadedBFSButton["bg"] = "white"
                        BFSButton["bg"] = "#014d4e"
                        BFSButton["fg"] = "white"
                        BFSButton["pady"] = 35
                        BFSButton["text"] = "BFS"
                    solAlgo = tempRun
        # Creation of button, all nested functions called through the pressing of the button
        return Button(third_frame, bd=0, bg="#014d4e", fg="white", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", font=("Calibri", 20), width=21, pady=35, justify="center", text=text, command=lambda: runCmd(run, algoType))
    def setRenderMode(toggle):
        # Toggle render mode
        global renderMode
        renderMode = toggle
    def bfsE():
        # os.cpu_count() returns the # logical processors (threads) available on the system
        systemThreads = os.cpu_count()
        # Declare an empty list to contain the Multithreaded BFS expand widgets for later deletion
        threadExpand = []
        def confirmBFSE():
            global threads, solAlgo
            tempThreads = threadsEntry.get()
            if tempThreads.isdigit():
                tempThreads = int(tempThreads)
                if tempThreads == 0:
                    threadErrorLabel["text"] = "Thread count cannot be 0"
                    return
                elif tempThreads > systemThreads:
                    threadErrorLabel["text"] = "More threads specified than available"
                    return
            else:
                threadErrorLabel["text"] = "Threads not positive integer"
                return
            # If all vailidity checks passed, set threads to the threads specified by user
            threads = tempThreads
            # Destroy all widgets in the Multithreaded BFS expansion
            for x in threadExpand:
                x.destroy()
            # Change the color of the BFS button, and set solving algorithm to Multithreaded BFS
            threadedBFSButton["bg"] = "#014d4e"
            threadedBFSButton["fg"] = "white"
            BFSButton["fg"] = "#014d4e"
            BFSButton["bg"] = "white"
            BFSButton["pady"] = 18
            BFSButton["text"] = "Multithreaded\nBFS"
            solAlgo = "Multithreaded BFS"
            


        threadsLabel = Label(third_frame, bd=0, bg="#014d4e", fg="white", borderwidth=0.5, relief="groove", font=("Calibri", 18, "bold"), width=19, padx=6, pady=3, height=4, justify="center", text=f"Enter # Threads Usable")
        threadsLabel.grid(row=2, column=4)
        threadsEntry = Entry(third_frame, bd=0, bg="#014d4e", fg="white", borderwidth=0.5, relief="groove", font=("Calibri", 18, "bold"), width=19, justify="center", text=f"Enter # Threads Usable")
        threadsEntry.grid(row=2, column=5, ipady=16, columnspan=3, sticky="nw")
        ToolTip(threadsLabel, msg=f"Enter a value between 0-{systemThreads} (total # of threads on system)\nThis quantity of threads will be designated to BFS")
        if threadsEntry.get() == "":
            threadsEntry.insert(END, systemThreads)
        threadErrorLabel = Label(third_frame, bd=0, bg="#014d4e", fg="white", borderwidth=0.5, relief="groove", font=("Calibri", 10, "bold"), width=31, padx=7, justify="center", text="")
        threadErrorLabel.grid(row=2, column=5, ipady=23, columnspan=3, sticky="sw")
        threadConfirmButton = Button(third_frame, bd=0, bg="#014d4e", fg="white", borderwidth=0.5, relief="groove", font=("Calibri", 18, "bold"), width=7, height=3, pady=9, padx=7, justify="center", text="Confirm", command=confirmBFSE)
        threadConfirmButton.grid(row=2, column=7, columnspan=1, sticky="e")
        threadExpand = [threadsLabel, threadsEntry, threadErrorLabel, threadConfirmButton]
   
    canvas.create_window((0,0), window=third_frame, anchor="nw")
    title = Label(third_frame, bd=0, bg="white", fg="#014d4e", borderwidth=0.5, relief="groove", font=("Calibri", 18), width=50, pady=20, justify="center", text=f"Config + Start")
    title.grid(row=0, column=0, columnspan=4)
    returnToMenuButton = Button(third_frame, bd=0, bg="#014d4e", fg="white", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", font=("Calibri", 20), width=3, pady=9, justify="center", text="X", command=mainMenuCmd)
    returnToMenuButton.grid(row=0, column=0, sticky="w")
    generationLabel = Label(third_frame, bd=0, bg="#014d4e", fg="white", borderwidth=0.5, relief="groove", font=("Calibri", 18, "bold"), width=23, pady=20, justify="center", text=f"Choose Generation Algo")
    generationLabel.grid(row=1, column=0, columnspan=2)
    solvingLabel = Label(third_frame, bd=0, bg="#014d4e", fg="white", borderwidth=0.5, relief="groove", font=("Calibri", 18, "bold"), width=23, pady=20, justify="center", text=f"Choose Solving Algo")
    solvingLabel.grid(row=1, column=2, columnspan=2)


    # Buttons to specify generation algorithms
    createButton("Growing Tree", algoType="gen", run="Growing Tree").grid(row=2, column=0, columnspan=2)
    createButton("Recursive Division", algoType="gen", run="Recursive Division").grid(row=3, column=0, columnspan=2)
    createButton("Binary Tree", algoType="gen", run="Binary Tree").grid(row=4, column=0, columnspan=2)
    createButton("Kruskal's Algorithm", algoType="gen", run="Kruskal's Algorithm").grid(row=5, column=0, columnspan=2)
    createButton("Depth-First Growth (DFG)", algoType="gen", run="Depth-First Growth").grid(row=6, column=0, columnspan=2)


    # Buttons to specify solution algorithms
    BFSButton = createButton("BFS", algoType="sol", run="Breadth-First Search")
    BFSButton.grid(row=2, column=2, columnspan=2)
    # Expand arrow causes bfsE to trigger, expanding the Multithreaded BFS menu
    threadedBFSButton = Button(third_frame, bd=0, bg="white", fg="#014d4e", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, font=("Calibri", 26), relief="groove", text="▶", pady=27, command=bfsE)
    threadedBFSButton.grid(row=2, column=3, sticky="e")
    ToolTip(threadedBFSButton, msg="Configure + Select\nMultithreaded BFS")
    createButton("A*", algoType="sol", run="A Star").grid(row=3, column=2, columnspan=2)
    createButton("Dead-End Filling", algoType="sol", run="Dead-End Filling").grid(row=4, column=2, columnspan=2)
    createButton("Trémaux Algorithm", algoType="sol", run="Trémaux Algorithm").grid(row=5, column=2, columnspan=2)
    createButton("Dijkstra's Algorithm", algoType="sol", run="Dijkstra's Algorithm").grid(row=6, column=2, columnspan=2)
    
    # Specifying grid dimensions
    gridSizeLabel = Label(third_frame, bd=0, bg="#014d4e", fg="white", borderwidth=0.5, relief="groove", font=("Calibri", 18, "bold"), width=46, pady=20, justify="center", text=f"Enter Grid Dimensions (Columns x Rows)")
    gridSizeLabel.grid(row=0, column=4, columnspan=4)
    ToolTip(gridSizeLabel, msg="Enter a value between 20-500\nNote: Values >=200 may crash program")
    gridSizeCEntry = Entry(third_frame, width=16, fg="#014d4e", font=("Calibri", 22), justify="center", bd=0.1)
    gridSizeCEntry.grid(row=1, column=4, columnspan=2, sticky="w", ipady=15, ipadx=10)
    if gridSizeCEntry.get() == "":
        gridSizeCEntry.insert(END, 50)
    xLabel = Label(third_frame, bd=0, bg="white", fg="#014d4e", font=("Calibri", 29), width=4, pady=10, justify="center", text="x")
    xLabel.grid(row=1, column=6)
    gridSizeREntry = Entry(third_frame, width=16, fg="#014d4e", font=("Calibri", 22), justify="center", bd=0.1)
    gridSizeREntry.grid(row=1, column=7, columnspan=2, sticky="e", ipady=15, ipadx=11)
    if gridSizeREntry.get() == "":
        gridSizeREntry.insert(END, 50)


    # Specifying whether render mode is enabled, set to disabled by default
    renderLabel = Label(third_frame, bd=0, bg="#014d4e", fg="white", borderwidth=0.5, relief="groove", font=("Calibri", 18, "bold"), width=46, pady=46, justify="center", text=f"Live Render Algos?")
    renderLabel.grid(row=2, column=4, columnspan=7, sticky="w")
    renderButton = Button(third_frame, bd=0, bg="#014d4e", fg="white", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", font=("Calibri", 20), width=21, pady=35, padx=5, justify="center", text="Render", command=lambda: setRenderMode(True))
    renderButton.grid(row=3, column=4, sticky="w", columnspan=3)
    ToolTip(renderButton, msg="Each wall break/spawn in the generation phase\nAnd tracer position updates in the solving phase\nWill be rendered as lines and shaded cells as the algorithm processes it\nNote: Comes with a significant time penalty, results are not recorded")
    noRenderButton = Button(third_frame, bd=0, bg="#014d4e", fg="white", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", font=("Calibri", 20), width=20, pady=35, padx=5, justify="center", text="Don't Render", command=lambda: setRenderMode(False))
    noRenderButton.grid(row=3, column=6, sticky="e", columnspan=2)
    ToolTip(noRenderButton, msg="Generation/solving is instantaneous, showing all\nwalls/the located path once the algorithms have completed\nSimulation pauses for 0.5 seconds after solving each maze to display the path")


    # Specifying # of simulation passes
    simulationPassesLabel = Label(third_frame, bd=0, bg="#014d4e", fg="white", borderwidth=0.5, relief="groove", font=("Calibri", 18, "bold"), width=46, pady=46, justify="center", text=f"Enter # Simulation Passes")
    simulationPassesLabel.grid(row=4, column=4, columnspan=7, sticky="w")
    ToolTip(simulationPassesLabel, msg="# of consecutive runs of this combo. A higher sample may provide more reliable readings")
    simulationPassesEntry = Entry(third_frame, width=38, fg="#014d4e", font=("Calibri", 22), justify="center", bd=0.1)
    simulationPassesEntry.grid(row=5, column=4, sticky="w", columnspan=7, ipady=43, ipadx=11)
    if simulationPassesEntry.get() == "":
        simulationPassesEntry.insert(END, 10)


    # An empty label to old error messages, and the start button to trigger validity checks and progress to runProgram()
    errorLabel = Label(third_frame, bd=0, bg="#014d4e", fg="white", borderwidth=0.5, relief="groove", font=("Calibri", 14), width=31, pady=50, justify="center", text="")
    errorLabel.grid(row=6, column=4, columnspan=3, sticky="w")
    createButton("Start", algoType="start").grid(row=6, column=6, columnspan=3, sticky="e")


def lpc():
    # If the program has never been configured, run default settings
    if genAlgo == None:
        global gridCols, gridRows, simulations, renderMode
        gridCols, gridRows = 50, 50
        simulations = 10
        renderMode = False


    runProgram()


# Must be declared globally to be deleted by other functions
mainOptions = []
runbar = []
my_scrollbar, second_frame = None, None


# Must be decalred globally to be accessed by runProgram()
runs = []


def mainMenuCmd():
    canvas.delete("all")
    second_frame = Frame(canvas)
    canvas.create_window((0,0), window=second_frame, anchor="nw")
    # Contents of sidebar, stored in array runbar
    runRecord = Label(second_frame, bd=0, bg="#014d4e", borderwidth=0.5, relief="groove", fg="white", font=("Calibri", 18), width=50, pady=30, justify="center", text=f"Previous Runs - {len(runs)} Recorded")
    runRecord.grid(row=0, column=1, sticky="ne")
    runExpandButton = Button(second_frame, command=runExpand, bg="#014d4e", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", fg="white", text="◀", font=("Calibri", 26), pady=10)
    runExpandButton.grid(row=0, column=1, sticky="nw")
    # Append all to runbar for later deletion
    runbar.extend([runRecord, runExpandButton])


    # Iterate through reversed list so most recent runs appear on top
    for runCnt, run in enumerate(runs[::-1]):
        # Get runs of the same generation algorithm
        sameCombos = [tempRun for tempRun in runs if tempRun.gen == run.gen]
        # If there are any runs with the same generation algorithm, get position of run in list sorted in ascending order, divide by the total number of runs of the same generation algorithm and multiply by 100% to recieve percentile
        if len(sameCombos) > 0:
            timPercentile = ((sorted([tempRun.tim for tempRun in sameCombos]).index(run.tim) + 1) * 100) / len(sameCombos)
            cpuPercentile = ((sorted([tempRun.acu for tempRun in sameCombos]).index(run.acu) + 1) * 100) / len(sameCombos)
            memPercentile = ((sorted([tempRun.ame for tempRun in sameCombos]).index(run.ame) + 1) * 100) / len(sameCombos)
        else:
            # If there are no runs with the same generation algorithm, set all to 100
            timPercentile, cpuPercentile, memPercentile = 100, 100, 100
        # Formatting raw performance data to 4 decimal places, percentiles to 2 decimal places
        description = Label(second_frame, bd=0, bg="#014d4e", borderwidth=0.5, relief="groove", fg="white", font=("Calibri", 11), width=55, pady=1, justify="center", text=
        f"{run.gen} + {run.sol}\n" + 
        f"-  μs/Cell - {'{:.4f}'.format(run.tim)}, {'{:.2f}'.format(timPercentile)}% percentile\n" +
        f"-  Avg CPU - {'{:.4f}'.format(run.acu)}, {'{:.2f}'.format(cpuPercentile)}% percentile\n" +
        f"-  Avg Mem - {'{:.4f}'.format(run.ame)}, {'{:.2f}'.format(memPercentile)}% percentile\n")
        description.grid(row=1+runCnt, column=1, sticky="nw")


        # No argument is passed through specificRunExpand as mouse position obtained to determine selection
        expand = Button(second_frame, command=specificRunExpand, bg="#014d4e", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", fg="white", text="◀", font=("Calibri", 26), pady=12)
        expand.grid(row=1+runCnt, column=1, sticky="nw")
        runData = Label(second_frame, bd=0, bg="#014d4e", relief="groove", fg="white", font=("Calibri", 18), borderwidth=0.5, pady=17, padx=15, justify="center", text=f"Run #{run.run}\n{run.gen} #{run.ott}")
        runData.grid(row=1+runCnt, column=1, sticky="ne")
        # Append all to runbar for later deletion
        runbar.extend([description, expand, runData])
    # Main options, i.e. 3 buttons on main menu
    title = Label(second_frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 26), width=33, pady=50, padx=3, justify="center", text=f"Maze Generation and\nSolving Algorithm Compatibilities")
    title.grid(column=0, row=0, rowspan=2)
    lpcButton = Button(second_frame, bd=0, command=lpc, bg="#014d4e", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", fg="white", font=("Calibri", 32), width=27, pady=50, justify="center", text=f"Load Previous Config + Start")
    lpcButton.grid(column=0, row=2, rowspan=2)
    configButton = Button(second_frame, bd=0, command=config, bg="#014d4e", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", fg="white", font=("Calibri", 32), width=27, pady=50, justify="center", text=f"Config + Start")
    configButton.grid(column=0, row=4, rowspan=2)
    settingsButton = Button(second_frame, bd=0, command=settingsExpand, bg="#014d4e", activebackground="white", activeforeground="#014d4e", borderwidth=0.5, relief="groove", fg="white", font=("Calibri", 32), width=27, pady=50, justify="center", text=f"Settings")
    settingsButton.grid(column=0, row=6, rowspan=2)
    mainOptions = [title, lpcButton, configButton, settingsButton]
mainMenuCmd()


####################################################################################################################


defaultWall = True
class Cell:
    # Constructor takes column and row as necessary parameters
    def __init__(self, col, row):
        # Walls set to non-existent if not explicitly defined
        self.col, self.row = col, row
        self.rWall, self.dWall = defaultWall, defaultWall
        # When state = 0, cell is unvisited
        # = 1, cell is visited
        self.state = 0
        # Dijkstra's
        self.parent = None
        # A*
        # Distance from root and fScore set to large number by default to take lower priority than visited cells when backtracking in A*
        self.distanceFromRoot = 999999
        self.fScore = 999999
        # Trémaux
        # Number of marks in direction given by key
        self.marks = {(0,-1) : 0, (0,1) : 0, (-1,0) : 0, (1,0) : 0}
        # If cell is intersection (has more than 1 neighbour) and has been visited, turns to True
        self.intersectionV = False


    def connect(self, parentCell):
        # Link subtree onto node on main tree
        self.parent = parentCell
        parentCell.children.append(self)


    def connected(self, opCell):
        return self.parent == opCell or opCell.parent == self


    def render(self):
        # If the rightWall/downWall is present, add line object in given direction to wallGrid
        if self.rWall:
            wallGrid[self.col][self.row][0] = canvas.create_line((self.col+1)*cellS, self.row*cellS, (self.col+1)*cellS, (self.row+1)*cellS)
        if self.dWall:
            wallGrid[self.col][self.row][1] = canvas.create_line(self.col*cellS, (self.row+1)*cellS, (self.col+1)*cellS, (self.row+1)*cellS)


    def updateWall(self, wall, state):
        if wall == "u":
            # Set the downWall of the cell above to False
            grid[self.col][self.row-1].dWall = state
            if state == False:
                # Delete wall from wallGrid such that it is not rendered on the next pass
                canvas.delete(wallGrid[self.col][self.row-1][1])
        elif wall == "l":
            grid[self.col-1][self.row].rWall = state
            # Set the rightWall of the cell to the left to False
            if state == False:
                canvas.delete(wallGrid[self.col-1][self.row][0])
        elif wall == "r":
            self.rWall = state
            if state == False:
                canvas.delete(wallGrid[self.col][self.row][0])
        elif wall == "d":
            self.dWall = state
            if state == False:
                canvas.delete(wallGrid[self.col][self.row][1])


    # Draw a rectangle of color "fill" to shade in the specified cell, leaving "offset" pixel distance with the walls of the cells
    def shade(self, fill, offset=1):
        shadeGrid.append(canvas.create_rectangle(self.col*cellS+offset, self.row*cellS+offset, (self.col+1)*cellS-offset, (self.row+1)*cellS-offset, fill=fill, outline=""))


    def getNeighbours(self, dire=False, walls=False, visit=True):
        dirs, neighbours = [], []
        if visit == False:
            if walls == True:
                # If neighbour is in bounds of grid AND if neighbour is not separated by wall
                if self.row > 0 and grid[self.col][self.row-1].dWall == False:
                    dirs.append("u")
                    neighbours.append(grid[self.col][self.row-1])
                if self.row < gridRows-1 and self.dWall == False:
                    dirs.append("d")
                    neighbours.append(grid[self.col][self.row+1])
                if self.col > 0 and grid[self.col-1][self.row].rWall == False:
                    dirs.append("l")
                    neighbours.append(grid[self.col-1][self.row])
                if self.col < gridCols-1 and self.rWall == False:
                    dirs.append("r")
                    neighbours.append(grid[self.col+1][self.row])
            else:
                # If neighbour is in bounds of grid (adjacency check)
                if self.row > 0:
                    dirs.append("u")
                    neighbours.append(grid[self.col][self.row-1])
                if self.row < gridRows-1:
                    dirs.append("d")
                    neighbours.append(grid[self.col][self.row+1])
                if self.col > 0:
                    dirs.append("l")
                    neighbours.append(grid[self.col-1][self.row])
                if self.col < gridCols-1:
                    dirs.append("r")
                    neighbours.append(grid[self.col+1][self.row])
        else:
            # If neighbour is in bounds of grid AND if neighbour is not visited
            if walls == False:
                if self.row > 0 and grid[self.col][self.row-1].state == 0:
                    dirs.append("u")
                    neighbours.append(grid[self.col][self.row-1])
                if self.row < gridRows-1 and grid[self.col][self.row+1].state == 0:
                    dirs.append("d")
                    neighbours.append(grid[self.col][self.row+1])
                if self.col > 0 and grid[self.col-1][self.row].state == 0:
                    dirs.append("l")
                    neighbours.append(grid[self.col-1][self.row])
                if self.col < gridCols-1 and grid[self.col+1][self.row].state == 0:
                    dirs.append("r")
                    neighbours.append(grid[self.col+1][self.row])
            # If neighbour is in bounds of grid AND if neighbour is not separated by wall AND if neighbour is not visited
            else:
                if self.row > 0 and grid[self.col][self.row-1].dWall == False and grid[self.col][self.row-1].state == 0:
                    dirs.append("u")
                    neighbours.append(grid[self.col][self.row-1])
                if self.row < gridRows-1 and self.dWall == False and grid[self.col][self.row+1].state == 0:
                    dirs.append("d")
                    neighbours.append(grid[self.col][self.row+1])
                if self.col > 0 and grid[self.col-1][self.row].rWall == False and grid[self.col-1][self.row].state == 0:
                    dirs.append("l")
                    neighbours.append(grid[self.col-1][self.row])
                if self.col < gridCols-1 and self.rWall == False and grid[self.col+1][self.row].state == 0:
                    dirs.append("r")
                    neighbours.append(grid[self.col+1][self.row])
       
        if dire == True:
            # If directions want to be printed, output will take the form
            # [["r", "l"], [<Cell>, <Cell>]]
            # Where calling getNeighbours()[0] will return list of directions, [1] will return list of valid cells
            return dirs, neighbours
        else:
            # Otherwise only list of cells is returned
            return neighbours
    
    # Dunder method to check if other distanceFromRoot is greater than self distanceFromRoot
    def __lt__(self, other):
        return self.distanceFromRoot < other.distanceFromRoot


#########################################################


# runSideBar, wallGrid, and shadeGrid can be destroyed by other functions, grid is used across the program
runSideBar = []
grid, wallGrid, shadeGrid = [], [], []
# Declaring variables to be adjusted by config menu
cellS = 0
sampleRate = 0.1
threads = 0
ofEachGen = {}
totalRunCnt = 1


# Create a dictionary in which a key (each generation algorithm) is assigned to a value (the number of times this generation algorithm has been run)
for genAlgo in gens:
    ofEachGen[genAlgo] = 0


def runProgram():
    global runSideBar, grid, wallGrid, shadeGrid, cellS, defaultWall
    global runTimes, memReadings, cpuReadings
    global runs, totalRunCnt


    # Declare an empty 2D array with Cell objects with the col and row attributes pre-assigned
    grid = [[Cell(col, row) for row in range(gridRows)] for col in range(gridCols)]
    # Declare an empty wall grid that is parallel with the grid 2D array, used for holding each line drawn by Tkinter in the maze (to signify the presence of a wall)
    # This allows walls to be removed from the canvas in case of a wall break
    wallGrid = [[[None, None] for row in range(gridRows)] for col in range(gridCols)]
    # Width/height of a cell in pixels
    cellS = 750/max([gridCols, gridRows])
    # Some algorithms may take alternate start/target cells, but this is tandardised to the top-left and bottom-right of the grid to ensure same parameters for investigation
    startCell, targetCell = grid[0][0], grid[-1][-1]


    # Start stopwatch for series of runs total runtime
    totalStartTime = time.time()


    # Canvas is reset
    canvas.config(width=750, height=750)
    canvas.delete("all")


    title = Label(frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 26), width=35, pady=50, justify="center", text="")
    title.pack(side=TOP, anchor=NE)
    blurb = Label(frame, bd=0, bg="white", borderwidth=0.5, relief="groove", fg="#014d4e", font=("Calibri", 16), pady=50, text="")
    blurb.pack(side=TOP, anchor=NE, expand=1, fill=BOTH)
    runSideBar = [title, blurb]


    # Set all data to be unrecorded by default
    runTimes = []
    memReadings, cpuReadings = [], []
   
    # Thread to retreive memory and cpu readings, update the blurb, append the readings to arrays and pause for the sample rate specified
    def updateReadings():
        while True:
            # Try except used here to break from function when algorithm is over (i.e. When the blub label is destroyed, as the program has moved onto the next stage)
            try:
                memory_usage = round((psutil.virtual_memory().used - baselineMemory)/1000000, 2)
                cpu_usage = psutil.cpu_percent() - baselineCPU
                blurb["text"] = f"Time Elapsed (seconds): {'{:.2f}'.format(time.time()-totalStartTime)}\nMemory Usage (MB): {memory_usage}\nCPU Usage (%): {'{:.2f}'.format(cpu_usage)}"
                memReadings.append(memory_usage)
                cpuReadings.append(cpu_usage)
                time.sleep(sampleRate)
            except:
                break


    # psutil.virtual_memory().used returns memory currently used by all processes on the computer, not just the relavant Python process
    baselineMemory = psutil.virtual_memory().used
    # psutil.cpu_percent() returns CPU Usage currently used by all processes on the computer, not just the relavant Python process
    # This will be taken away from CPU and memory readings as a baseline, such that there is minimal performance impact from other processes
    baselineCPU = psutil.cpu_percent()
    # Start the continuous recording thread
    threading.Thread(target=updateReadings).start()
    for simulation in range(simulations):
        if genAlgo == "Recursive Division":
            # If generation algorithm is recursive division, no walls present on grid by default
            defaultWall = False
        else:
            # Other generation algorithms break walls, so all walls present if any other gen algo
            defaultWall = True
        for col in range(gridCols):
            for row in range(gridRows):
                # Set each cell in grid to default values
                grid[col][row].__init__(col, row)


        # Reset canvas
        canvas.delete("all")


        # Update title to show generating
        title["text"] = f"Generating...\n{genAlgo}"


        match genAlgo:
            # Take parameters in form of render (whether renderMode is on or off), frame, canvas, grid
            # Binary Tree requires directional biases
            case "Binary Tree":
                binaryTree(renderMode, frame, canvas, grid, ["d","r"])
            case "Kruskal's Algorithm":
                kruskals(renderMode, frame, canvas, grid)
            case "Depth-First Growth":
                # DFG requires start cell
                dfg(renderMode, frame, canvas, grid, grid[0][0])
            case "Recursive Division":
                # Recursive Division requires coordinates of first subfield, and orientation
                recursiveDivision(renderMode, frame, canvas, grid, 0, 0, gridCols-1, gridRows-1, 0)
            case "Growing Tree":
                # Growing Tree requires start cell
                growingTree(renderMode, frame, canvas, grid[0][0])


        # Render all wall updates, set each cell to unvisited
        for col in grid:
            for cell in col:
                cell.render()
                cell.state = 0
        # Delete all shade rectangles to shade again if using render mode
        for x in shadeGrid:
            canvas.delete(x)


        # Update title to show solving
        title["text"] = f"Solving...\n{solAlgo}"


        # Start stopwatch for this combo of generation/solving
        startTime = time.time()
        match solAlgo:
            # Take parameters in form of render, frame, canvas, grid, cell, targetCell
            case "A Star":
                # A Star uses tuple positions to define its start and target cells
                aStar(renderMode, frame, canvas, grid, (targetCell.col, targetCell.row), (startCell.col, startCell.row))
            case "Dijkstra's Algorithm":
                dijkstras(renderMode, frame, canvas, grid, grid[0][0], targetCell)
            case "Trémaux Algorithm":
                Trémaux(renderMode, frame, canvas, grid, grid[0][0], targetCell)
            case "Breadth-First Search":
                bfs(renderMode, frame, canvas, grid, grid[0][0], targetCell)
            case "Multithreaded BFS":
                # Multithreaded BFS takes input of threadCount designated
                threadedbfs(renderMode, frame, canvas, grid, grid[0][0], targetCell, threadCount=threads)
            case "Dead-End Filling":
                dead_end_filling(renderMode, frame, canvas, grid, grid[0][0], targetCell)
        runTime = time.time()-startTime
        runTimes.append(runTime)


        # Pause for 0.5 seconds if renderMode is enabled, otherwise path is never shown
        if renderMode:
            time.sleep(0.5)
       
        frame.update()
        canvas.pack()


    # Sequential position of simulations (e.g. 1-10, group this series of runs as the 1st to 10th simulation the program has run since boot)
    numRun = f"{totalRunCnt}-{totalRunCnt+simulations-1}"


    # Declaration of Run class to store all details of a run in the same object
    class Run():
        def __init__(self, gen, sol, tim, run, pme, ame, pcu, acu, ort, abt, cols, rows, cms, ott, rpo):
            # gen = Generation Algorithm
            # sol = Solving Algorithm
            self.gen, self.sol = gen, sol
            # tim = Average time to process one cell during solving (in µs)
            # run = Sequential position of run(s) from all recorded runs
            self.tim, self.run = tim, run
            # pme = Peak memory usage during solving from samples
            # ame = Average memory usage during solving from samples
            self.pme, self.ame = pme, ame
            # pcu = Peak CPU usage (across all threads) during solving from samples
            # acu = Average CPU usage (across all threads) during solving from samples
            self.pcu, self.acu = pcu, acu
            # ort = Overall runtime, total runtime of all simulation passes (in seconds)
            # abt = Timestamp of series of runs (recorded at time of finishing)
            self.ort, self.abt = ort, abt
            # cols = gridCols value in this set of runs
            # rows = gridRows value in this set of runs
            self.cols, self.rows = cols, rows
            # cms = CPU/Memory sampling rate in this set of runs (in seconds/sample)
            # ott = Runs of this type, using the same generation algorithm
            self.cms, self.ott = cms, ott
            # rpo = Sequential position of series of runs from all recorded series of runs
            self.rpo = rpo


    # Only stores recordings if renderMode is disabled
    if renderMode == False:
        # Increases total simulations program has performed by the number of simulations in this series of simulations
        totalRunCnt += simulations
        # Stores average time to process one cell by finding average of runTimes divided by the number of cells in the grid, multiplied by 1000000 to convert seconds -> microseconds
        avgTime = (1000000*sum(runTimes))/(len(runTimes)*(gridCols*gridRows))
        avgCPU = sum(cpuReadings)/len(cpuReadings)
        avgMem = sum(runTimes)/len(runTimes)
        # Number of series including this generation algorithm is increased by 1
        ofEachGen[genAlgo] += 1
        runs.append(Run(gen=genAlgo, sol=solAlgo,
                        tim=avgTime, run=numRun,
                        pme=max(memReadings), ame=avgMem,
                        pcu=max(cpuReadings), acu=avgCPU,
                        # abt uses datetime module to store current date in dd/mm/yy, hh:mm:ss form
                        ort=sum(runTimes), abt=datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
                        cols=gridCols, rows=gridRows,
                        # ott gets simulations with this generation algorithm
                        cms=sampleRate, ott=ofEachGen[genAlgo],
                        rpo=len(runs)+1))
   
    runEnd()
    frame.mainloop()


frame.resizable(False,False)
canvas.pack(side=LEFT)
frame.mainloop()
