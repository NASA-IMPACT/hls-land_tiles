import json
import requests
import xmltodict

from collections import OrderedDict

S2_kml = requests.get("https://sentinel.esa.int/documents/247904/1955685/S2A_OPER_GIP_TILPAR_MPC__20151209T095117_V20150622T000000_21000101T000000_B00.kml/ec05e22c-a2bc-4a13-9e84-02d5257b09a8").text

s2_tiles = xmltodict.parse(S2_kml)

objects = s2_tiles["kml"]["Document"]["Folder"][0]["Placemark"]

s2_grid = OrderedDict({"type": "FeatureCollection", "features": []})

for obj in objects:
    feature = OrderedDict({"type": "Feature",
                           "properties":{"type":"S2"},"geometry":{}
                           })
    feature["properties"]["identifier"] = obj["name"]
    feature["geometry"]["type"] = "MultiPolygon"
    feature["geometry"]["coordinates"] = []
    polys = obj["MultiGeometry"]["Polygon"]
    polys = [polys] if not isinstance(polys, list) else polys

    for poly in polys:
        boundary = poly["outerBoundaryIs"]["LinearRing"]["coordinates"]
        boundary = boundary.split(" ")
        coordinates = []
        for coord in boundary:
            ll = [float(x) for x in coord.split(",")]
            coordinates.append([ll[0], ll[1], ll[2]])
        feature["geometry"]["coordinates"].append([coordinates])
    s2_grid["features"].append(feature)


with open("s2_grid.json", "w") as f:
    json.dump(s2_grid, f)
