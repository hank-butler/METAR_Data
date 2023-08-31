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
    
    json_map = json.load(open(map_file))
    
    folium_map = folium.Map(location=[latitude, longitude],
                      zoom_start = zoom)
    
    folium.GeoJson(json_map).add_to(folium_map)
    
    return folium_map