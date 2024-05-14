import pandas as pd
import random as rd
import bs4 as bs
from bs4 import BeautifulSoup
import kml_object 
import random as rnd 


def parse_coord_string(coord_string):
    longitudes = []
    latitudes = []

    coord_string = coord_string.replace('\n','')
    coord_string = coord_string.replace('\t','')
    coord_string = coord_string.replace(' ',',')
    coord_string = coord_string[:-1]
    coords = coord_string.split(',')


    for i in range(0,len(coords),3):
        longitudes.append(coords[i])
    for i in range(1,len(coords),3):
        latitudes.append(coords[i])
        
    op = []
    for i in range(len(longitudes)):
        op.append([longitudes[i],latitudes[i]])
    
    return op


def parse_KML(filename):
    file = open(filename, "r")
    contents = file.read()
    soup = BeautifulSoup(contents, 'xml')
    names = soup.find_all('name')

    features = soup.find_all('Placemark')

    #process names
    project_name = str(names[0])[10:-11]

    obj_list = []

    for feature in features:
        
        featurename = str(feature.find_all('name'))[11:-12]
        coords = parse_coord_string(feature.coordinates.text)

        if feature.find('Polygon'):
            featuretype = 'polygon'

        if feature.find('Point'):
            featuretype = 'Point'

        if feature.find('LineString'):
            featuretype = 'LineString'
        
        obj_list.append(kml_object.Object(featurename,coords,featuretype))
        
    return project_name, obj_list




