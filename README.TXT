Feb 22, 2020
Junchang Ju

How was the list of HLS tiles over land excluding Antarctica derived.

1. Land mask shapefile from
   https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/

   Saved in ne_10m_land/

2. The shapefile of all MGRS tiles created by Sergii Skakun.

   Saved in shape file in all_s2_tiles/

3. QGIS 
     1) To select all land tiles: vector->research tools ->selection by location.

	The land tiles saved in shapefile in S2landstiles/

     2) Then select by polygon to exclude antarctica.

	The land tiles excluding Antarctica saved in shapefile in S2_land_NoAnt/

4. To get a list of resulting land tiles, I don't know how to save the attribute
   table as a text file in QGIS, but the following Linux commands work in combination:  

	strings S2_NoAnt.dbf | 
	  tr "\t " "\n" | 
	  sort -u | 
          grep "^[0-6]" | 
          awk 'length($1) == 5' > HLS.land.tiles.txt

    There are 18501 tiles in HLS.land.tiles.txt. The location of the tiles is 
    shown over a NASA gloval vegetation lat/lon image HLS.land.tiles.txt.jpg.

