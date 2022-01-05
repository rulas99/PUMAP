from requests import get
from flexpolyline import decode

def hereRequestRoutes(origen,destino):
    
    origen = ','.join([str(i) for i in origen])
    destino = ','.join([str(i) for i in destino])
    
    URL = "https://router.hereapi.com/v8/routes"
    api_key = '<token>' # Acquire from developer.here.com
    PARAMS = {'apikey':api_key,'transportMode':'pedestrian','return':'polyline','destination':destino,'origin':origen} 
    
    r = get(url = URL, params = PARAMS) 
    data = r.json()

    polyline = data['routes'][0]['sections'][0]['polyline']

    return decode(polyline)


def hereRequestGeocoding(direccion):
    
    URL = "https://geocode.search.hereapi.com/v1/geocode"
    api_key = 't5feKE8N0lDxz3GCoBJ9A_s-9YSr9Y-aCc3NJbvsvEk' # Acquire from developer.here.com
    PARAMS = {'apikey':api_key,'q':None} 
    
    PARAMS['q'] = direccion
    try:
        r = get(url = URL, params = PARAMS) 
        data = r.json()

        coords = {'lat':data['items'][0]['position']['lat'],'lon': data['items'][0]['position']['lng'],'UBICACION':direccion}

    except:
        coords = {'lat':None,'lon': None,'UBICACION':direccion} 
        
    return coords
