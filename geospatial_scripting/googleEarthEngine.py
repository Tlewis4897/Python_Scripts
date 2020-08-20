###################################################Some Fun Testing and Scripts with Google Earth Engine #########################################################


import ee
import geopandas
import json

ee.Initialize()


# Get Area for geometry
area = ee.Geometry.Polygon( [
          [
            [
              -76.33026123046874,
              40.016111851185435
            ],
            [
              -76.2795352935791,
              40.016111851185435
            ],
            [
              -76.2795352935791,
              40.055869698308086
            ],
            [
              -76.33026123046874,
              40.055869698308086
            ],
            [
              -76.33026123046874,
              40.016111851185435
            ]
          ]
        ])
home_collection = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")

home_AOI = home_collection.filterBounds(area)
print("Images (After Area):",home_AOI.size().getInfo())
# Set date filter
home_date = home_AOI.filterDate('2018-01-01', '2020-1-01')
print("Images (After Date):",home_date.size().getInfo())
# Set least cloudy
least_cloudy = ee.Image(home_date.sort('CLOUD_COVER').first())
print("Selected Image Date:", least_cloudy.getInfo()['properties']['DATE_ACQUIRED'])
# Set RGB
image_rgb = least_cloudy.select(['B4', 'B3', 'B2'])
# Set image for export
image_out = image_rgb.multiply(512).uint8()
# Set batch task to drive
task = ee.batch.Export.image.toDrive(image_out, folder="GEOG656_GEE",
description='My House 2018', dimensions = 720, region=area)

task.start() 

print('RGB Image Task Status:',task.status()['state'])
print("Sattellite ID:", least_cloudy.getInfo()['properties']['SPACECRAFT_ID'])
print("Worldwide Reference System (WRS) Path/Row:", least_cloudy.getInfo()['properties']['WRS_ROW'], "/", 
      least_cloudy.getInfo()['properties']['WRS_PATH'])
print("Image ID:", least_cloudy.getInfo()['properties']['LANDSAT_SCENE_ID'])
print("Image Date", least_cloudy.getInfo()['properties']['DATE_ACQUIRED'])
print("Cloud Cover (%)", least_cloudy.getInfo()['properties']['CLOUD_COVER'])
print("Number of Bands", least_cloudy.bandNames().size().getInfo())
print("List of Band Names", least_cloudy.bandNames().getInfo())
print("Image Resolution (m)", least_cloudy.select('B1').projection().nominalScale().getInfo())

# Ready json from file in directory
home_json = r'C:/Users/Thoma/Desktop/Lab9googleengine/myHome.json'
convert_pandas = geopandas.read_file(home_json)
pandas_to_dict = convert_pandas.to_json()
home_dict = json.loads(pandas_to_dict)
my_home_json = home_dict['features'][0]['geometry']['coordinates']

new_area = ee.Geometry.Polygon(my_home_json)


class NoFile(Exception):
    pass

class WrongExtension(Exception):
    pass

class WrongYear(Exception):
    pass

def getImage(work, geojson, year):
    import json, geopandas, ee, os
    try:
        if os.path.isdir(work) != True:
            raise WrongExtension('Directory does not exist!')
        work= work + '/'            
        if os.path.isfile('./' + geojson) != True:
            raise NoFile('No file exists!')
        if geojson.endswith('.json'):
            pass
        else:
            raise WrongExtension('No valid JSON format')
        if int(year) >= 2013 and int(year) <= 2020:
            pass
        else:
            raise WrongYear('Invalid Year, must be between 2013 and 2020')
        # Open and read json file
        for file_name in [file for file in os.listdir(work) if file.endswith(geojson)]:
          with open(work + file_name) as json_file:
            # Read json file from geopandas
            convert_pandas = geopandas.read_file(json_file)
            pandas_to_dict = convert_pandas.to_json()
            home_dict = json.loads(pandas_to_dict)
            # Get json coordinates
            my_home_json = home_dict['features'][0]['geometry']['coordinates']
            # Calc area
            new_area = ee.Geometry.Polygon(my_home_json)
            home_collection = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
            home_AOI = home_collection.filterBounds(new_area)
            # Filter Date
            home_date = home_AOI.filterDate(f'{year}-01-01', f'{year}-12-31')
            # Least cloudy
            least_cloudy = ee.Image(home_date.sort('CLOUD_COVER').first())
            print("Selected Image Date:", least_cloudy.getInfo()['properties']['DATE_ACQUIRED'])
            print("Selected Cloud Cover:", least_cloudy.getInfo()['properties']['CLOUD_COVER'])
            # Set rgb values
            image_rgb = least_cloudy.select(['B4', 'B3', 'B2'])
            # Convert to 8-bit value
            image_out = image_rgb.multiply(512).uint8()
            task = ee.batch.Export.image.toDrive(image_out, folder="GEOG656_GEE",
            description='Virginia Tech' + ''+ str(year), dimensions = 720, region=new_area)
            task.start()
            print(task.status())
            print("Selected Image", task.status()['description'], "Sent to Google Drive")
            return 
    except NoFile as e:
        print(e)
    except WrongExtension as e:
        print(e)
    except WrongYear as e:
        print(e)

def convertBit(image):
    return image.multiply(512).uint8()

# Set collection geometry 
collection_area = ee.Geometry.Polygon(my_home_json)
home_collection = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
print('Images (All Landsat):', home_collection.size().getInfo())

# Set area boundary
home_AOI = home_collection.filterBounds(area)
print('Images (After Area Filter):', home_AOI.size().getInfo())
# Set filter dates
home_date = home_AOI.filterDate('2013-01-01', '2020-1-01')
print('Images (After Date Filter):', home_date.size().getInfo())
# Get least cloudy (below 5%)
least_cloudy = home_date.filter(ee.Filter.lt('CLOUD_COVER', 5))
print('Images (After Cloud Filter):', least_cloudy.size().getInfo())
image_rgb = least_cloudy.select(['B4', 'B3', 'B2'])
# Set image rgb
# Convert to 8-bit value


def convertBit(image):
    return image.multiply(512).uint8()


collection_output = image_rgb.map(convertBit)
# Set video task
task = ee.batch.Export.video.toDrive(collection_output, folder="GEOG656_GEE", description='My Home Video Collection',
                              dimensions = 720, region=collection_area, framesPerSecond = 12)
task.start()
print('Time Series Video Task Status:',task.status()['state'])

# Calculate normalized difference
new_image = image_out.normalizedDifference()
# Convert the image to 8-bit value
ndvi_output = new_image.multiply(512).uint8()
# set batch task
task = ee.batch.Export.image.toDrive(ndvi_output, folder="GEOG656_GEE",
            description='My Home ndvi' + ''+ str(year), dimensions = 720, region=area)
task.start()
task.status()