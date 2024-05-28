# Extraction Steps

Note, you will need to have quite a bit of disk space to do this, as the data is quite large, but the output should be small enough to fit on a Raspberry Pi.

## Step 1: Download the Main Data

 <https://download.geofabrik.de/>, select your region and download the mapping data

## Step 2: Extract the road Data

 Use Osmium to extract the road data, this is not 100% nessisary, but will make the data smaller and easier to work with.

 ```bash
    osmium tags-filter world-latest.osm.pbf w/highway -o world-all-roads.osm.pbf 
 ```

## Step 4: Import data into osmnx

```bash
    python3 gpspi/mapping/importer.py
```
