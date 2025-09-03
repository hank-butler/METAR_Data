import re
from pathlib import Path
import pandas as pd


def create_map(map_file=None, latitude=None, longitude=None, zoom=4):
    '''
    Function to take in geojson file and create a map using Folium with coordinate to center.
    
    Zoom is defaulted to 4 based on trial and error.
    
    =======
    ACCEPTS
    =======
    map_file should be a .geojson file
    latitude and longitude should be coordinates from a pandas dataframe
    
    =======
    RETURNS
    =======
    A folium map centered at coordinates and added to map with a geojson file.
    
    =======
    RAISES
    =======
    ValueError if map_file, latitude, longitude aren't correct data types
    ModuleNotFoundError if json and Folium aren't imported before invoking
    
    '''
    import folium
    import json
    
    if map_file:
        json_map = json.load(open(map_file))

        folium_map = folium.Map(location=[latitude, longitude],
                          zoom_start = zoom)

        folium.GeoJson(json_map).add_to(folium_map)
        
    else:
        folium_map = folium.Map(location=[latitude, longitude],
                          zoom_start = zoom)

    return folium_map

# regex helpers
_wind_re = re.compile(r'^(?P<dir>\d{3}|VRB)(?P<spd>\d{2,3})(?:G(?P<gst>\d{2,3}))?KT$')
_vis_re = re.compile(r'^(?P<vis>(?:\d+\s)?\d?/?\d)SM$')
_sky_re = re.compile(r'^(?P<cov>FEW|SCT|BKN|OVC|CLR|SKC)(?P<ht>\d{3})?$')
_td_re = re.compile(r'^(?P<t>M?\d{1,2})/(?P<d>M?\d{1,2})$')''
_alt_re = re.compile(r'^A(?P<alt>\d{4})$')
_tprec_re = re.compile(r'^T(?P<ts>0|1)(?P<t>\d{3})(?P<ds.0|1)(?P<d>\d{3})$')


def _md_to_c(s):
    if s is None:
        return None
    return -float(s[1]) if s.startswith("M") else float(s)

def _inHg_from_A(aaaa):
    return float(aaaa[:2] + "." + aaaa[2:])

def _c_from_Tgroup(sign, val):
    v = float(val)/10.0
    return -v if sign == '1' else v

def parse_metar_line(line):
    