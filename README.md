# image_processing
Using <a href="https://imagemagick.org/index.php" target="_blank">ImageMagick</a> to batch crop and create montages


Requires: web browser screen shots of 4 panel dispays accessible at:
<a href="https://veritas.nws.noaa.gov/blend/conus.php" target="_blank">https://veritas.nws.noaa.gov/blend/conus.php</a>


This script crops the 4 panes, and creates mosaics for each forecast hour containing the different forecast 
sources as well as verification with data arranged in the panels as follows:
   
     top  left : NDFD
     top right : NBMv32
   bottom left : observed dataset (URMA, NOHRSC, etc.)
   bottom left : NBMv31

NBM viewer settings
                   Type : Event Review
               Location : GRR or MI
    Analysis Hour (UTC) : 12Z works the best
                  Range : Mid 
   NDFD Issuance offset : 06 to reflect the forecast
                          being based on 6 hours earlier guidance

Use Paint or some other application to find the x,y pixel
coordinates for the top left corners of the crop areas associated
with top left and bottom right panes in the screen shot
The filenames of these screen-captured images need to follow this example:
    
    SnowAmt24_20191113-12Z_F72.PNG
    
      SnowAmt24 : forecast element (easiest to emulate NBM naming
                  convention; in this case, 24 hour snowfall)
       20191113 : verifying date
            12Z : verifying hour
            F72 : hours in future from forecast time

