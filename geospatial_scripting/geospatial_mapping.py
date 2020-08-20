################################### Some Fun Testing with pandas and GeoPandas #####################################################################

import geopandas
import numpy
import pandas
import warnings
from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def averageTwoInPython3():
    first_num = input("What is your first number?")
    second_num = input("What is your second number?")
    return (int(first_num) + int(second_num)) / 2


def createGradebook(student_names, quizzes):
    get_name_size = len(student_names)
    get_quiz_size = len(quizzes)
    grades = numpy.random.randint(0,5,(get_name_size,get_quiz_size))
    gradebook = pandas.DataFrame(grades,index=student_names,columns=quizzes)
    return gradebook


def processGrades(gradebook):
    summary_gradebook = gradebook.copy()
    summary_gradebook["Average"] = summary_gradebook.mean(numeric_only=True, axis=1)
    bad_students = (summary_gradebook.loc[(summary_gradebook["Average"]< 2.5)])
    print("**Warning these students had less than 50%**")
    for i in bad_students.index:
        print(i)


country = geopandas.read_file("gz_2010_us_040_00_5m.json")
country_name = country.set_index("NAME")
country_geom = country_name.loc["Montana"]["geometry"]
crs = {'init': 'epsg:4326'}
polygon = geopandas.GeoDataFrame(index=[0], crs=crs, geometry=[country_geom]) 
polygon.plot()
country = geopandas.read_file("gz_2010_us_040_00_5m.json")
mask = country['NAME'].isin(['District of Columbia','Virginia','Maryland'])
dmv_region = country[mask == True] # Select states not in the list
dmv_region.plot(column="CENSUSAREA", cmap="rainbow", legend=True,
legend_kwds={'label': "DMV Area",
'orientation': "horizontal"})

utm_epsg = {'UTM10N':'26910','UTM11N':'26911','UTM12N':'26912','UTM13N':'26913',
            'UTM14N':'26914','UTM15N':'26915','UTM16N':'26916','UTM17N':'26917',
            'UTM18N':'26918','UTM19N':'26919'}

class WrongName(Exception):
    pass

class WrongColor(Exception):
    pass


def plotState(country_geo, country_nam, color, esp):
    try:
        country_name = country_geo.set_index("NAME")
        if country_name.index.get_level_values('NAME').str.contains(country_nam).any():
            pass
        else:
            raise WrongName(f"Error: Input {country_nam} is Not A Valid State")
        geom = country_name.loc[country_nam]["geometry"]
        polygon = geopandas.GeoDataFrame(index=[0], geometry=[geom])
        my_geoseries = polygon.set_crs(epsg=4326)
        my_polygon = my_geoseries.to_crs("EPSG:{0}".format(esp))
        try:
            my_polygon.plot(cmap='{}'.format(color))
        except:
            raise WrongColor(f"ValueError {color} is neither a valid single color nor a color sequence")
            pass
        return my_polygon
    except WrongColor as e:
        print(e)
    except WrongName as e:
        print(e)


class WrongUnits(Exception):
    pass


def calcArea(state_geom, state_nam, unit):
    try:
        if unit != 'mi' and unit != 'km':
            raise WrongUnits(f"Error: Units Input {unit} are Not Valid Units")
        if unit == 'mi':
            state_area = state_geom.area * 0.0000003861022 
            get_area = state_area.tolist()
            area_from_frame=get_area[0]
        elif unit == 'km':
            state_area = state_geom.area * 0.000001
            get_area = state_area.tolist()
            area_from_frame=get_area[0]
        return area_from_frame
    except WrongUnits as e:
        print(e)


population = pandas.read_csv("state_population_data.csv")
merged = country.set_index("NAME").join(population.set_index("State_Name"))
merged["Pop_Change"] = (merged["Pop_2010"] - merged["Pop_1990"]) / merged["Pop_1990"] * 100
mask = merged.index.isin(['Alaska','Hawaii','Puerto Rico',
'District of Columbia'])
lower_48 = merged[mask == False] # Select lower 48 states
lower_48["Pop_Change"] = (merged["Pop_2010"] - merged["Pop_1990"]) / merged["Pop_1990"] * 100
mask = lower_48.index.isin(['Alaska','Hawaii','Puerto Rico',
'District of Columbia'])
legend_props = {'label': "% Population Change by State 1990-2010",
'orientation': "horizontal"}
lower_48.plot(column="Pop_Change", cmap="plasma", edgecolor="k",
legend=True, legend_kwds=legend_props)

max_total = max(lower_48["Pop_Change"])
min_total = min(lower_48["Pop_Change"])
get_max = lower_48.loc[lower_48['Pop_Change'].idxmax()]
max_state = get_max.name
get_min = lower_48.loc[lower_48['Pop_Change'].idxmin()]
min_state= get_min.name

print(f'The State of {max_state} has the HIGHEST change between 1990 and 2010 = {max_total}%')
print(f'The State of {min_state} has the LOWEST change between 1990 and 2010 = {min_total}%')



lower_48["Pop_Density"]= lower_48['Pop_2010'] / lower_48['CENSUSAREA']
legend_props = {'label': "Population Density by State 2010",
'orientation': "horizontal"}
lower_48.plot(column="Pop_Density", cmap="plasma", edgecolor="k",
legend=True, legend_kwds=legend_props)
max_total = max(lower_48["Pop_Density"])
min_total = min(lower_48["Pop_Density"])
get_max = lower_48.loc[lower_48['Pop_Density'].idxmax()]
max_state = get_max.name
get_min = lower_48.loc[lower_48['Pop_Density'].idxmin()]
min_state= get_min.name

print(f'The State of {max_state} has the HIGHEST change between 1990 and 2010 = {max_total}%')
print(f'The State of {min_state} has the LOWEST change between 1990 and 2010 = {min_total}%')


# Test Input
print("***Part I***")
students = ["AAA","BBB","CCC","DDD","EEE","FFF","GGG","HHH","III","JJJ"]
labs = ["L1","L2","L3","L4","L5","L6","L7"]
gbook = createGradebook(students,labs)
print(gbook)
processGrades(gbook)
print(gbook)
print("***Part II***")
maryland = plotState(country, "Maryland", "Mars Red", utm_epsg["UTM13N"])
maryland = plotState(country, "Jupiter", "Reds", utm_epsg["UTM13N"])
maryland1 = plotState(country, "Maryland", "Reds", utm_epsg["UTM11N"])
maryland2 = plotState(country, "Maryland", "Reds", utm_epsg["UTM18N"])
calcArea(maryland,"Maryland","nm")
md = country[country["NAME"] == "Maryland"]
obs = md["CENSUSAREA"]
print("Observed Area %0.2f mi^2" % obs)
area1 = calcArea(maryland1,"Maryland","mi")
print("Relative Error (UTM11N) = %0.2f%%" % (abs(area1 - obs) / obs * 100))
area2 = calcArea(maryland2,"Maryland","mi")
print("Relative Error (UTM18N) = %0.2f%%" % (abs(area2 - obs) / obs * 100))








    