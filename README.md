# ERO 2025 - ShrekGang

## Name
ERO 2025 - ShrekGang

## Description

## Installation
First of all, your pc should have at least python v3.10.9 to have a stable run of the program : https://www.python.org/downloads/

After that, you need to install all the necessary libraries :

    pip install -r requirement.txt

Now, you should have all the requirements to run the program

*WARNING: The better the computer resources you have, the faster the program is*


## How to begin

To run the program, type this command in the root of the project:

    make

It will display an interface with the differents areas that you can load or directly type the name of the town you want to load

You can choose :
    
- the number of the vehicle you want to plow the area (default : 1)
- the type of the vehicle you want to plow the area (default : T1)
- Drone recognition
- Plow Area : it will plow the area with the number of the vehicle you choose with the type of vehicle you choose

## How to use the interface

Follow the steps for a good utilisation of the interface :

    1. Load a graph - Click on one of the area or type one
    2. Type the number of the vehicle you want to use
    3. Select the type of the vehicle
    4. Choose the mode : Drone Recon / Plow Area
    5. It will run automatically after the 4th step

Now you can see that, the program is running. It will generate a report called *drone_report.js* or *plow_report* according to the choosen mode and *.p files that we will use later for the case study 

*WARNING: You cannot change the mode or load an other area if the current area is processing - You have to quit the interface with the button QUIT (it will take some time to close) or shut down manually*

If you see some time that the drone or vehicle jumps some road during the process, it's normal because there's two road in one (two way trafic) where it will be colored when he pass the second time

## How to get the result

For a case study in a pre-defined location with specific parameters, follow this steps :

    1. You have to get the *.p for the location
    2. Run the interface and load the location
    3. Click on Plow Area (number and type of vehicle doesn't matter )
    3.1 Once the .p file has been generated, you can close the interface, no need to see the path
    4. Go to the repository of the case study 
       For example :
        cd src/outremont/
    
    5. Now, it's time to generate the study case
        
        5.1 Type this command to have directly the result with default value budget : 1000 Time : 2 Vehicle (range max vehicle) : 20

            make
        
        5.1.1 If you wish to specify parameters the variable BUDGET TIME VEHICLE can help you :
            
            make BUDGET=10000 TIME=2 VEHICLE=30
        
        Here we want a case study with 10000 budget, 2 time and max range 30 vehicle

A graph will pop up and will show you the best option of this case. You could also the find the result in .png in the directory.

*WARNING*: Careful about the parameters, the more you ask, the longer it takes

## Support

paul.guan@epita.fr

alexandre.weng@epita.fr

william.ye@epita.fr

lalariniaina-prisca.ramanantoanina@epita.fr


## Authors and acknowledgment
Paul GUAN

Lalariniaina Prisca RAMANANTIANINA

Alexandre WENG

William YE

## License
PRIVATE

## Project status
ONGOING ...