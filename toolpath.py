import numpy as np
import matplotlib.pyplot as plt
import math

############ method for estimating the time of the toolpath ############
def estimateTimeForToolPaths(toolpaths, scanSpeed):
    updatedToolPath = [[0, toolpaths[0][0], toolpaths[0][1]]]
    for toolpath in toolpaths[1:]:
        time = np.sqrt((toolpath[0] - updatedToolPath[-1][1])**2 + (toolpath[1] - updatedToolPath[-1][2])**2)/scanSpeed
        updatedToolPath.append([time, toolpath[0], toolpath[1]])
    return updatedToolPath

##########################################
########Toolpath Generation Params########
##########################################

scanSpeed = 0.9 # in m/s
layerHeight = 40e-6 # in m
hatchSpacing = 0.1e-3
layerNumbers = 2
laserStatus = 1

toolpathXOffset = 200e-6
toolpathYOffset = 200e-6


x_dimension = 2.5e-3
y_dimension = 2.5e-3
z_dimension = 4.5e-3

hole_radius = 2.03e-3
hole_center = [2.5e-3, 2.5e-3]

############### Generation of circular hole locus ###############
#################################################################

initial_x_location = x_dimension - hole_radius
x_location_1 = np.arange(initial_x_location, x_dimension+hatchSpacing, hatchSpacing)
y_location_1 = - np.sqrt(hole_radius**2 - (x_location_1 - hole_center[0])**2) + hole_center[1]
# print(x_location_1)
# print(y_location_1)

initialYLocationLength = int(initial_x_location/hatchSpacing)
y_location_0 = np.full(initialYLocationLength, y_location_1[0], dtype=float)
# print(y_location_0)

y_location = np.append(y_location_0, y_location_1)
x_location = np.arange(0, x_dimension+hatchSpacing, hatchSpacing)
# print(len(y_location), len(x_location))


############### Updating toolpath with return paths ##############
##################################################################

toolpath=[[0, 0]]
for i in range(len(x_location)):
    if (i%2 == 0 and i>0):
        toolpath.append([x_location[i-1], 0])
        toolpath.append([x_location[i], 0])
        toolpath.append([x_location[i], y_location[i]])
    else:
        toolpath.append([x_location[i], y_location[i]])

if (len(x_location)%2 == 0):
    toolpath.append([x_location[-1], 0])

plt.figure()
plt.plot(*zip(*toolpath))
plt.savefig('toolpath.png')

toolpath = estimateTimeForToolPaths(toolpath, scanSpeed)

################# Writing the toolpath ##########################
##################################################################

with open("MultiLayerTest.crs", "w") as file:
    # formattedLine = f"{0:4.8f} {0:4.8f} {0:4.8f} {0:4.8f} {0}\n"
    # file.write(formattedLine)
    scanTime = 0
    for i in range(layerNumbers):
        layerDepth = layerHeight*(i+1)
        scanTimeOffset = 5e-4*i
        initialScanTime = scanTime + scanTimeOffset + toolpath[0][0]
        formattedLine = f"{initialScanTime:4.8f} {toolpath[0][2]+toolpathYOffset:4.8f} {toolpath[0][1]+toolpathXOffset:4.8f} {layerDepth:4.8f} {0}\n"
        file.write(formattedLine)
        for time, x, y in toolpath[1:]:
            scanTime = scanTimeOffset + scanTime + time
            formattedLine = f"{scanTime:4.8f} {y+toolpathYOffset:4.8f} {x+toolpathXOffset:4.8f} {layerDepth:4.8f} {laserStatus}\n"
            file.write(formattedLine)
        