import datetime
import fiona
import json
import requests
import xmltodict

from shapely.geometry import Polygon


class hls_land_tiles:

    def __init__(self):
        with open("params.json") as f:
            params = json.load(f)
        land_shpfile = params["path_to_gshhs_shp"]
        kml_url = params["S2_kml_url"]
        self.land_polys = []
        self.get_land_mask(land_shpfile)
        self.get_S2grid_from_kml(kml_url)
        self.write_s2_hls_grid()

    def get_land_mask(self,land_shpfile):
        shape = fiona.open(land_shpfile)
        for tile in shape:
            self.land_polys.append(Polygon(tile["geometry"]["coordinates"][0]).buffer(0.01,cap_style=3,join_style=3))

    def get_S2grid_from_kml(self,kml_url):
        S2_complete_grid = xmltodict.parse(requests.get(kml_url).text)
        objects = S2_complete_grid["kml"]["Document"]["Folder"][0]["Placemark"]
        self.hls_grid = set()
        for obj in objects:
            s2_polys = obj["MultiGeometry"]["Polygon"]
            s2_polys = [s2_polys] if not isinstance(s2_polys, list) else s2_polys
            for s2_poly in s2_polys:
                boundary = s2_poly["outerBoundaryIs"]["LinearRing"]["coordinates"]
                boundary = boundary.split(" ")
                coordinates = []
                for coord in boundary:
                    ll = [float(x) for x in coord.split(",")]
                    coordinates.append([ll[0], ll[1], ll[2]])
                s2_bounds = Polygon(coordinates)
                for land_bounds in self.land_polys:
                    if land_bounds.intersects(s2_bounds):
                        self.hls_grid.add(obj["name"])
                        print(obj["name"])
                        break
        print(len(self.hls_grid))

    def write_s2_hls_grid(self):
        with open("HLS.land.tiles.txt", "w") as f:
            f.writelines(["%s\n" % tile for tile in sorted(self.hls_grid)])


if __name__ == "__main__":
    print(f"Started at: {datetime.datetime.now()}")
    hls_land_tiles()
    print(f"Finished at: {datetime.datetime.now()}")
