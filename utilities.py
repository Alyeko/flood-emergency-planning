import sys
from shapely.geometry import Point
import geopandas
from pyproj import CRS
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton 
from PyQt5.QtGui import QIcon

def call_gui():
    app = QApplication([]) 
 
    rootWindow = QWidget() 
    rootWindow.setWindowTitle("Shortest Path GUI") 
    rootWindow.resize(200, 200) 
    gridLayout = QGridLayout(rootWindow) 
    rootWindow.setWindowIcon(QIcon('icon.png'))

    coordinates_value = QLabel("Enter a valid British National Grid coordinate in the form x,y: ")
    gridLayout.addWidget(coordinates_value, 0, 0) 
    coordinates_value = QLineEdit() 
    gridLayout.addWidget(coordinates_value, 2, 0) 
    closeButton = QPushButton('Next') 
    gridLayout.addWidget(closeButton, 2, 1) 

    closeButton.clicked.connect(rootWindow.close) 

    rootWindow.show() 
    app.exec_() 
    return coordinates_value.text()

def water_or_land(elevation, x, y):
    """ Task 6.1: Identify whether the user's coordinate is in water or on land

    With user inputting the coordinates, find the corresponded elevation value.
    If elevation is less than or equal to 0, it means the input coordinate is in water.
    Our algorithm is only plausible when people on isle need guide for evacuation facing flooding hazard.

    Therefore, we set 1 for the input coordinate with an elevation value greater than 0; 0 for for the input coordinate
    with an elevation value less than or equal to 0.

    Args:
        x, y -- user input coordinate
        elevation -- elevation raster file read by rasterio.open()

    Return:
        1 or 0

    """
    ele_array = elevation.read(1)
    row_user, col_user = elevation.index(x, y)
    elevation_user = ele_array[row_user][col_user]
    if elevation_user > 0:
        return 1
    else:
        print('The coordinates entered by the user are in the sea. Please double check the input.')
        return 0


def position_check(elevation, coord, crs, box_c1, box_c2):
    """ Task 6.2: Dealing with the special case when input coordinate outside the box but on isle

    First, if input coordinate is inside the box, this program directly return the coordinate in geoseries format.
    However, when input coordinate is outside the box but still on the isle, which mean the elevation > 0, we still need
    to continue the program to find the shortest (fastest) path to the closest peak.

    The only situation for this program to quit is when the input coordinate is outside the bounding box also has the
    elevation value <= 0, which mean the user is in the water or something wrong with the input coordinate.

    Args:
        coord -- A list containing X, Y of user input
        elevation -- elevation raster file read by rasterio.open()
        crs -- coordinate system information. British National Grid is the default.
        box_c1 & box_c2 -- defined in task 1

    Return:
        A geoseries tuple of the user's coordnitate

    """
    coordinate = geopandas.GeoSeries(Point(coord[0], coord[1]), crs=crs)

    if not (all(x >= y for x, y in zip(coord, box_c1)) and all(x <= y for x, y in zip(coord, box_c2))):
        if water_or_land(elevation, coord[0], coord[1]) == 0:
            sys.exit("Coordinate outside the box")
        else:
            print("Coordinate accepted although it is outside of the bounding box.")
            return coordinate
    else:
        print("Coordinate accepted.")
        return coordinate


def user_coords(elevation, box_coords=None):
    """Task 1: Checks whether the user-inputted coordinate exists inside the box.

    If user_coords() is called with 0 arugments, it will use the coordinates for the INNER BOX
    noted in the specification. Otherwise, it will use whatever coordinates are passed in as
    box_coords.
    
    Args:
        box_coords -- A list of coordinates for the inner box of the raster elevation.
        elevation -- elevation raster file read by rasterio.open

    Return:
        A geoseries tuple of the user's coordnitate
    """

    from location import get_user_coords

    #  c3.......c2
    #  :        :
    #  :        :
    #  c1.......c4
    # if coords of inner box are provided, use them
    X1 = 430000
    X2 = 465000
    Y1 = 80000
    Y2 = 95000

    box_c1 = box_coords[0] if box_coords != None else (X1, Y1)
    box_c2 = box_coords[1] if box_coords != None else (X2, Y2)
    crs = CRS.from_wkt(
        'PROJCS["OSGB 1936 / British National Grid",GEOGCS["OSGB 1936",DATUM["OSGB_1936",SPHEROID["Airy 1830",6377563.396,299.3249646,AUTHORITY["EPSG","7001"]],AUTHORITY["EPSG","6277"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",49],PARAMETER["central_meridian",-2],PARAMETER["scale_factor",0.999601272],PARAMETER["false_easting",400000],PARAMETER["false_northing",-100000],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]')

    choice = int(input(
        '----------------CHOICES-------------''\n''1. I know my coordinates''\n''2. I don\'t know my coordinates '))
    if choice == 1:  # user enters their coordinates
        next_option = int(input('\n''How would you like to proceed?''\n''1. Terminal ''\n''2. GUI '))
        if next_option ==1:
            values = input("Enter a valid British National Grid coordninate in the form 'x,y': ")
            coord = [int(x) for x in values.split(",")]
            
        elif next_option == 2:
            coord = [int(x) for x in call_gui().split(",")]
            
        else:
            print('Invalid input, options can only be 1 or 2...')
        return position_check(elevation, coord, crs, box_c1, box_c2)

    elif choice == 2:  # user's coordinates are obatined by the software
        coord = get_user_coords()
        return position_check(elevation, coord, crs, box_c1, box_c2)
    
    else: 
        print('Invalid input, options are either one or two...')
# if __name__==  "__main__":
# print(user_coords())
