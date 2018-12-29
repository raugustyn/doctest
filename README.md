## pygeotoolbox
Python Geospatial Toolbox.

[Advanced Logging](#AdvancedLogging)<br>
[Smart Local Configuration](#SmartLocalConfiguration)<br>
[GeoDatabase Wrapper](#GeoDatabaseWrapper)

#### <a name="Advanced logging"></a>Advanced Logging

Simple code as the following:
```python
import pygeotoolbox.sharedtools.log as log

log.openSection("Building source tables...")
for tableName in ["roads", "waters", "buildings"]:
    log.info("Creating table " + tableName)
    # do some action
log.closeSection()
```

Leads to indented logging output:
```
14:31:07 - INFO Create logger c:/temp\logs\default.log.
14:31:07 - INFO create logger default => c:/temp\logs\default.log
14:31:07 - INFO Building source tables...
14:31:07 - INFO     Creating table roads
14:31:07 - INFO     Creating table waters
14:31:07 - INFO     Creating table buildings
14:31:07 - INFO Done.   
```


#### <a name="SmartLocalConfiguration"></a>Smart Local Configuration
1. Declare global variables with default value once in your code:


```python
import pygeotoolbox.sharedtools.config as config


def onConnectionParamsChange():
    # Do some actions
    pass
    
    
config.registerValue("database.name", "gensmd", "Database", "Database name.", onChange=onConnectionParamsChange)
```


2. Use new variable wherewer in your code:
```python
import pygeotoolbox.sharedtools.config as config

print config.database.name
```

3. Create local config.json file wherewer in your project structure: 
```json
{
  "database.name": "mapgen" 
}
```

#### <a name="GeoDatabaseWrapper"></a>GeoDatabase Wrapper
Use GeoDatabase functionality no matter whether stored in PostGIS, Oracle SDE, MySQL Spatial Database or other.

Just define your database connection parameters in local config.json file wherewer in your project structure: 
```json
{
  "database.name": "osm_lund",
  "database.type": "postgis"   
}
```

Then use GeoDatabase functionality:
```python
import pygeotoolbox.sharedtools.log as log
from pygeotoolbox.database import database

log.openSection("Reading public tables...")
for tableName in database.getTableNames("public"):
    log.info(tableName)
log.closeSection()

database.execute("create schema temp;")

log.info("There is %s roads." % database.firstRowFromSelect("select count(*) from public.roads"))

log.openSection("Reading selected road geometries...")
for road in database.loadShapes("select id, geom from public.roads where road_type=6", ["id", "geom"], "geom"):
    log.info("%d:\t%s" % (road.id, str(road.geom)))
log.closeSection()

``` 

Might lead to output like this:
```
14:20:12 - INFO Create logger c:/temp\logs\default.log.
14:20:12 - INFO create logger default => c:/temp\logs\default.log
14:20:12 - INFO Found configuration at C:\Temp\untitled\config.json.
14:20:12 - INFO Reading public tables...
14:20:12 - INFO     geography_columns
14:20:12 - INFO     geometry_columns
14:20:12 - INFO     spatial_ref_sys
14:20:12 - INFO     raster_columns
14:20:12 - INFO     raster_overviews
14:20:12 - INFO     roads
14:20:12 - INFO     data_table
14:20:12 - INFO     graphics
14:20:12 - INFO Done.
14:20:12 - ERROR schema "temp" already exists

create schema temp;
14:20:13 - INFO There is 14557 roads.
14:20:13 - INFO Reading selected road geometries...
14:20:13 - INFO     4448972:    LINESTRING (13.2501759 55.7405605, 13.2480495 55.7393589)
14:20:13 - INFO     4453888:    LINESTRING (13.2219551 55.7132575, 13.2214576 55.7112309, 13.221161 55.7100135)
14:20:13 - INFO     4453934:    LINESTRING (13.1688789 55.6708273, 13.1733132 55.6733194, 13.1751887 55.6743695, 13.1756443 55.6746365, 13.1760739 55.6748748)
14:20:13 - INFO     4454227:    LINESTRING (13.1874259 55.6811468, 13.1891705 55.6820377, 13.1900994 55.6825038, 13.1910983 55.682987, 13.1926854 55.6837864, 13.1935321 55.6842102)
14:20:13 - INFO     4454239:    LINESTRING (13.2221271 55.7132901, 13.2223987 55.7143388, 13.222506 55.7147114)
14:20:13 - INFO Done.  
```

### Dependencies

- [shapely](https://pypi.org/project/Shapely/) for geospatial geometry manipulations
- [psycopg](https://pypi.org/project/psycopg2/) for [PostGre](https://www.postgresql.org/) database connection
- [web](https://pypi.org/project/web/) for CGI web server functionality