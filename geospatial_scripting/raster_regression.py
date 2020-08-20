############################################# Custom Scripts for Raster Regression analysis ####################################################


import random as r
import math as m
import numpy as np
import matplotlib.pyplot as pyplot
import arcpy
from arcpy.sa import *
import time


def estimate_pi_python(darts_thrown):
    '''Estimate Pi with random darts using python'''
    # Number of darts that land inside.
    set_count_inside = 0
    # Total number of darts to throw.
    # Iterate for the number of darts.
    for i in range(0, darts_thrown):
        # Generate random x, y between -.5 and .5.
        x2 = r.uniform(-.5,.5)
        y2 = r.uniform(-.5,.5)
        # Increment if inside unit circle.
        if m.sqrt(x2**2 + y2**2) <= 0.5:
            set_count_inside += 1

    # PI Equation inside / total = pi / 4
    pi_result = (float(set_count_inside) / darts_thrown) * 4
    return pi_result


def estimate_pi_numpy(darts_thrown):
    '''Estimate Pi with random darts using numpy module'''
    X = np.random.uniform(-.5, .5, darts_thrown) 
    Y = np.random.uniform(-.5, .5, darts_thrown)  
    dist = np.sqrt(X**2+Y**2) 
    in_circle = np.sum(dist <= .5)
    numpy_pi_result = (float(in_circle)/darts_thrown)*4
    return numpy_pi_result


def plot_darts(darts_thrown):
    """Draw a scatter plot of thrown darts, coloring those inside and outside the unit circle differently"""
    for i in range(0, darts_thrown):
        # Generate random x, y between -.5 and .5.
        x2 = r.uniform(-.5,.5)
        y2 = r.uniform(-.5,.5)
        # Increment if inside unit circle.
        if m.sqrt(x2**2 + y2**2) <= 0.5:
            pyplot.scatter(x2,y2,c='#000000')
        else:
            pyplot.scatter(x2,y2,c='#FF7F50')
    pyplot.show()


class EmptyArray(Exception):
    pass

class ArrayDiff(Exception):
    pass

def rmse(obs_input, pred_input):
    '''1. Subtract obs - pred to get error
       2. **2 to get Squared Error
       3. Get the mean square error of calculation
       4. Get Square Root'''
    try:
        if obs_input.size == 0 or pred_input.size == 0:
            raise EmptyArray('An array is empty!')
        if len(obs_input) != len(pred_input):
            raise ArrayDiff('Error: Your input arrays are not the same length!')
        return np.sqrt(((obs_input - pred_input) ** 2).mean())
    except EmptyArray as e:
        print(e)
    except ArrayDiff as e:
        print(e)



def r_squared(obs_data, predicted_data):
    try:
        if obs_data.size == 0 or predicted_data.size == 0:
            raise EmptyArray('An array is empty!')
        if len(obs_data) != len(predicted_data):
            raise ArrayDiff('Error: Your input arrays are not the same length!')
        # Get sum of squares of vertical distances from points
        ssRes = sum((obs_data - predicted_data)**2)
        # Get length of obs data array and subtract by 1
        # Get variance and set value of divisor to 1 ie(N-1)
        # Multiply the vars together to get total natural variance
        ssTot = (len(obs_data) - 1) * np.var(obs_data, ddof=1)
        # Calc R Squared value
        r2_score = 1 - (ssRes / ssTot)
        return r2_score
    except EmptyArray as e:
        print(e)
    except ArrayDiff as e:
        print(e)



def raster_regression(workspace, exp_var, dep_variable):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = workspace
    exp_var = exp_var
    dep_var = dep_variable
    exp_raster = Raster(exp_var)
    dep_raster = Raster(dep_var)
    exp_arr = arcpy.RasterToNumPyArray(exp_raster)
    dep_arr = arcpy.RasterToNumPyArray(dep_raster)
    exp_1d=exp_arr.flatten()
    dep_1d=dep_arr.flatten()
    model=np.polyfit(exp_1d, dep_1d, 1)
    predict = np.poly1d(model)
    print('{} = {} * {} + {}').format(dep_var, round(predict.c[0], 3), exp_var, round(predict.c[1],3))
    # Y observered Biomass raster
    # Convert to Array
    x_predict = np.array(range(30))/100.0
    y_predict = predict(x_predict)
    # Make a prediction based on X ie(Lidar data)
    # Still recieving very off numbers
    print("RMSE = {}").format(rmse(x_predict,y_predict))
    print("R^2 = {}").format(r_squared(x_predict,y_predict))
    print('Model--->{}').format(model)
    return model


def plot_regression(workspace,explan_var,depend_var,model,sample_num):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = workspace
    workspace = arcpy.env.workspace
    arcpy.CheckOutExtension("Spatial")
    exp_var = explan_var
    dep_var = depend_var
    input_sample=sample_num
    arcpy.CreateRandomPoints_management(workspace, "samplepoints", 
                                        "", exp_var, input_sample, "", 
                                        "POINT")
    ExtractValuesToPoints("samplepoints", exp_var, "exp_points"
                        "", "")
    ExtractValuesToPoints("samplepoints", dep_var, "dep_points"
                        "", "")
    exp_array =  arcpy.da.FeatureClassToNumPyArray("exp_points", "RASTERVALU")
    dep_array = arcpy.da.FeatureClassToNumPyArray("dep_points", "RASTERVALU")
    pyplot.scatter(exp_array, dep_array)
    pyplot.show()
    return
    

# Test Input 
print "***Part I***"
n_samples = 1000000
actual = np.pi
start = time.clock()
pi_est = estimate_pi_python(n_samples)
python_runtime = time.clock() - start
print 'Estimated value (Python):', pi_est
print 'Percent (%) error (Python):', np.abs(pi_est - actual) / actual * 100
print 'Total CPU time (sec) to run (Python):', python_runtime
start = time.clock()
pi_est = estimate_pi_numpy(n_samples)
numpy_runtime = time.clock() - start
print 'Estimated value (NumPy):', pi_est
print 'Percent (%) error (NumPy):', np.abs(pi_est - actual) / actual * 100
print 'Total CPU time (sec) to run (NumPy):', numpy_runtime
print 'Using NumPy is',python_runtime / numpy_runtime, 'times faster than standard Python!'
n_samples = 5000
plot_darts(n_samples)
print "***Part II***"
y_predicted = np.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
y_observed = np.array([1.9, 2.8, 3.7, 4.6, 5.5, 6.4, 7.3, 8.2, 9.1])
model_rmse = rmse(y_predicted,y_observed)
print "RMSE:",model_rmse
model_r_2 = r_squared(y_predicted,y_observed)
print "R^2:",model_r_2
y_empty = np.array([])
y_error = np.array([42])
model_rmse = rmse(y_predicted,y_empty)
model_r_2 = r_squared(y_error,y_observed)
print "***Part III***"
workspace = r"C:\Users\Thoma\Desktop\lab7Numpy\biomass_lidar.gdb"
biomassRaster = "biomass_mgha"
lidarRaster1 = "lidar_med_z"
lidarRaster2 = "lidar_max_z"
model1 = raster_regression(workspace,lidarRaster1,biomassRaster)
model2 = raster_regression(workspace,lidarRaster2,biomassRaster)
plot_regression(workspace,lidarRaster1,biomassRaster,model1,1000)
plot_regression(workspace,lidarRaster2,biomassRaster,model2,1000)