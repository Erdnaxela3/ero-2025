# ERO 2025 - ShrekGang

## Name
ERO 2025 - ShrekGang

## Description

## Installation
First of all, your pc should have at least python v3.10.9 to have a stable run of the program : https://www.python.org/downloads/

After that, you need to install all the necessary libraries :

    pip install -r requirement.txt

Now, you should have all the requirements to run the program

## Getting started

To run Outremont as an example on the GUI, type this command at the root of the project:

    make

Plowing:
- Click on the 'Outremont' button to load the area
- Type any number of vehicles under 'Vehicle number for plowing'
- Click on 'Plow Area' at the bottom
- Enjoy the animation
- 'plow_report.json' has been generated, enjoy the different information provided

Drone:
- Click on 'Drone Recon'
- Enjoy the animation
- 'drone_report.json' has been generated, enjoy the different information provided

## How to use the GUI

Follow the steps for a good use of the interface :

    1. Load a graph - Click on one of the predefined area or type a custom one and click on 'load custom'
    2. Type the number of the vehicle you want to use (if your choice is different from 1)
    3. Select the type of the vehicle (if your choice is different from T1)
    4. Click on the desired mode : Drone Recon or Plow Area
    5. Enjoy the animation

Now you can see that, the program is running. It will generate a report called *drone_report.js* or *plow_report* according to the choosen mode and *.p pickle file to save the solutions (and avoid reruns)
These reports contains many informations on the desired operation (cost & time details, path followed by each vehicle, cost & time per vehicle details and much more)

*WARNING: You cannot change the mode or load an other area if the current area is processing - You have to quit the interface with the button QUIT (it will take some time to close) or shut down manually*

If you see the animation skipping roads, it's normal because the path visits this road more than once, it will be colored on its last visit

## User Stories

For a case study in a pre-defined location with specific parameters, follow this steps :

    1. Go to the repository of the desired case study 
       For example :
        cd src/outremont/
        cd src/le-plateau-mont-royal/
        cd src/rivière-des-prairies-pointe-aux-trembles/
        cd src/saint-léonard/
        cd src/verdun/
    2. Follow the instruction in the according section for your desired result:
        - What path should my N vehicles take?
        - Should I upgrade my fleet to T2 vehicles?
        - How many vehicles should i buy?

# What path should my N vehicles take?

You have N=40 T1 vehicles for example. What path should they take each?

    python3 outremont_plow.py --report 40 T1

For T2 vehicles

    python3 outremont_plow.py --report 40 T2

If you already ran the command you can speed it by adding the --load option. (It uses the pickle file with the solutions saved)

    python3 outremont_plow.py --report 20 T1 --load

The command generated a report in JSON format. The report contains the path that each vehicle should take, from start to finish.

# Should I upgrade my fleet to T2 vehicles? / keep T1 / downgrade to T1

You have N=40 T1 vehicles for example. My time constraint is 3 hours and budget is 10000$ Should i upgrade them to T2?
If not specified, default time will be 2 hours and budget 1000$.

    python3 outremont_plow.py --upgrade 40 --time 3 --budget 10000

A message will be printed suggesting upgrading or not. Two reports will also be generated so you can compare the two options.
You can use the same --load option to speed up the process if the *.p files have been generated.

# How many vehicles should i buy?

For example, you have a budget of 10000$, a time constraint of 3 hours, you are willing to buy up to 30 vehicles.
If not specified, default time will be 2 hours, default budget 1000$, default number of vehicle 20.

    python3 outremont_plow.py --optimal --time 3 --budget 10000 --vehicle 30

A chart will pop up and will show you the best option for this case. You could also find the result in .png format.
You can use the same --load option to speed up the process if the *.p files have been generated.

*WARNING*: Be careful about the parameters, the more vehicles you ask, the longer it takes

## Authors and acknowledgment
Paul GUAN <paul.guan@epita.fr>

Lalariniaina Prisca RAMANANTIANINA <lalariniaina-prisca.ramanantoanina@epita.fr>

Alexandre WENG <alexandre.weng@epita.fr>

William YE <william.ye@epita.fr>

## License
PRIVATE FOR EPITA - Don't cheat 

## Project status
ONGOING ...