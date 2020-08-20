#################################################### Script for analyzing Wildfires utilizing statistical analysis ####################################################

import arcpy
import os
import sys


def wildFireAnalysis():
    try:
        work = raw_input(r"Enter the full path of WildlandFires.gdb: ")
        if arcpy.Exists(work):
            y = raw_input ("WARNING! This file exists! Overwrite? (Y or N):")
            if y == 'N' or y!= 'Y':
                raise overwriteError('Program Ended... No Feature Class Created')
        else:
            raise existsError('Path does not exist!')
        arcpy.env.workspace = work # Set the workspace to the geodatabase
        iFile = raw_input(r"Enter the full path of wildfire text file:  ")
        if not os.path.exists(iFile):
            raise existsError('Path does not exist!')
        f = open(iFile, 'r')
        line = f.readline()
        newConfid= line.split(',')
        confidName = newConfid[2]
        setConfidVal = confidName.strip("\n")
        lstFires = f.readlines()
        f.close()
        featName = raw_input("Enter the name of the output feature class: ")
        if arcpy.Exists(featName):
            y = raw_input ("WARNING! This file exists! Overwrite? (Y or N):")
            if y == 'N' or y!= 'Y':
                raise overwriteError('Program Ended... No Feature Class Created')
        int_a = input("Specify the minimum confidence threshold (0-100):")
        arcpy.CreateFeatureclass_management(work, featName, "Point")
        arcpy.AddField_management(featName, setConfidVal, "LONG", 4)
        fields = ["SHAPE@", setConfidVal]
        cur = arcpy.da.InsertCursor(featName, fields)
        cntr = 0
        counter = 0
        while True:
            int_a = int(int_a)
            if (0 <= int_a <= 100):
                # Correct number, break the while loop
                break
            # Wrong number
            int_a = input("Warning...Threshold must be between 0 and 100...Re-enter:")

        # Here int_a is in the correct range
        fc = 'C:\Users\Thoma\Desktop\Lab5GEOG656\Lab 8 Data\WildlandFires.gdb\NationalParks'
        counter = 0 
        with arcpy.da.SearchCursor(fc, ['Name','SHAPE@']) as cursor:
            for row in cursor:
                name = row[0]
                geom = row[1]

        for fire in lstFires:
            if 'Latitude' in fire: # Skip the header
                continue
            pnt = arcpy.Point()
            pointGeom = fire.split(',')
            lstValues = pointGeom
            latitude = pointGeom[0]
            longitude = pointGeom[1]
            confidence = pointGeom[2]
            confid = int(confidence)
            pnt.X = float(longitude)
            pnt.Y = float(latitude)
            if confid > int_a:
                row = [pnt, confid]
                cur.insertRow(row)
                cntr = cntr + 1
                print "Record # " + str(cntr) + " written to feature class"
                if pnt.within(geom) is True:
                    counter = counter + 1
        print('There were {} fires in {}'.format(counter, name))
        del cur
        nn_output = arcpy.AverageNearestNeighbor_stats(featName, "EUCLIDEAN_DISTANCE", "NO_REPORT", "#")
        zScore=float((nn_output.getOutput(1)))
        roundZscore = (round(zScore, 2))
        if roundZscore < -1.65:
            print('The fire incidents are *significantly clustered* (z-score = {})'.format(roundZscore))
        elif roundZscore > 1.65:
            print('The fire incidents are *significantly dispersed* (z-score = {})'.format(roundZscore))
        elif roundZscore > -1.65 and roundZscore < 1.65:
            print('The fire incidents are * spatially random* (z-score = {})'.format(roundZscore))

except overwriteError as e:
    print "Error: " + str(e) # Prints Python-related errors


except existsError as e:
    print "Error: " + str(e) # Prints Python-related errors
