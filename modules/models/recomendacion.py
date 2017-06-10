import pandas as pd
import csv
import numpy as np
import webbrowser
from urllib.request import urlopen,quote
import simplejson
places="AIzaSyCsgMwi_tzAVkae-8Rq9v2A_kjeJF5L2kU"
radius=50

types=pd.read_csv('types.csv',header=None)
df = pd.read_csv('cosa.csv')

types=types.values.tolist()[0]
locations='['
nombres='var nombres = ['
tipos='var tipos = ['
for i in range(len(df)-1):
    lat=df.loc[i]['lat']
    lon=df.loc[i]['lon']
    locations=locations+'{lat: '+str(lat)+', lng: '+str(lon)+'},'
    if (df.loc[i]['type']==0):
        tipos=tipos+'"nivel1",'
        nombres=nombres+'"casa/trabajo/escuela"'+','

    else: 
        tipos=tipos+'"nivel2",'
        nombres=nombres+'"Lugar frecuente"'+','

    for j in types:
        url_places="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(lat)+","+str(lon)+"&rankby=prominence"+"&radius="+str(500)+"&type="+j+"&key="+places
        with urlopen(url_places) as response:
               result= simplejson.load(urlopen(url_places))
        if(len(result['results'])>0):
            locations=locations+'{lat: '+str(result['results'][0]['geometry']['location']['lat'])+', lng: '+str(result['results'][0]['geometry']['location']['lng'])+'},'            
            tipos=tipos+'"'+j+'",'
            nombres=nombres+'"'+result['results'][0]['name']+'"'+','
        
locations=locations+'{lat: '+str(df.loc[i+1]['lat'])+', lng: '+str(df.loc[i+1]['lon'])+'}]'
if (df.loc[i+1]['type']==0):
        tipos=tipos+'"nivel1"];'
        nombres=nombres+'"casa/trabajo/escuela"];'

else: 
    tipos=tipos+'"nivel2"];'
    nombres=nombres+'"Lugar frecuente"];'
input_form = """
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Marker Clustering</title>
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>

      function initMap() {

        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 3,
          center: {lat: -28.024, lng: 140.887}
        });

        var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';


        var markers = locations.map(function(location, i) {"""+tipos+nombres+"""

    
        
        switch(tipos[i]) {
	case "accounting":
		var icon='src/icons/accounting.svg'
		break;
	case "nivel1":
		var icon='http://maps.google.com/mapfiles/ms/icons/red-dot.png'
		break;
	case "nivel2":
		var icon='http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
		break;
	case "airport":
		var icon='src/icons/airport.svg'
		break;
	case "amusement_park":
		var icon='src/icons/amusement-park.svg'
		break;
	case "aquarium":
		var icon='src/icons/aquarium.svg'
		break;
	case "art_gallery":
		var icon='src/icons/art-gallery.svg'
		break;
	case "atm":
		var icon='src/icons/atm.svg'
		break;
	case "bakery":
		var icon='src/icons/bakery.svg'
		break;
	case "bank":
		var icon='src/icons/bank.svg'
		break;
	case "bar":
		var icon='src/icons/bar.svg'
		break;
	case "beauty_salon":
		var icon='src/icons/beauty-salon.svg'
		break;
	case "bicycle_store":
		var icon='src/icons/bicycle-store.svg'
		break;
	case "book_store":
		var icon='src/icons/book-store.svg'
		break;
	case "bowling_alley":
		var icon='src/icons/bowling-alley.svg'
		break;
	case "bus_station":
		var icon='src/icons/bus-station.svg'
		break;
	case "cafe":
		var icon='src/icons/cafe.svg'
		break;
	case "campground":
		var icon='src/icons/campground.svg'
		break;
	case "car_dealer":
		var icon='src/icons/car-dealer.svg'
		break;
	case "car_rental":
		var icon='src/icons/car-rental.svg'
		break;
	case "car_repair":
		var icon='src/icons/car-repair.svg'
		break;
	case "car_wash":
		var icon='src/icons/car-wash.svg'
		break;
	case "casino":
		var icon='src/icons/casino.svg'
		break;
	case "cemetery":
		var icon='src/icons/cemetery.svg'
		break;
	case "church":
		var icon='src/icons/church.svg'
		break;
	case "city_hall":
		var icon='src/icons/city-hall.svg'
		break;
	case "clothing_store":
		var icon='src/icons/clothing-store.svg'
		break;
	case "convenience_store":
		var icon='src/icons/convenience-store.svg'
		break;
	case "courthouse":
		var icon='src/icons/courthouse.svg'
		break;
	case "dentist":
		var icon='src/icons/dentist.svg'
		break;
	case "department_store":
		var icon='src/icons/department-store.svg'
		break;
	case "doctor":
		var icon='src/icons/doctor.svg'
		break;
	case "electrician":
		var icon='src/icons/electrician.svg'
		break;
	case "electronics_store":
		var icon='src/icons/electronics-store.svg'
		break;
	case "embassy":
		var icon='src/icons/embassy.svg'
		break;
	case "fire_station":
		var icon='src/icons/fire-station.svg'
		break;
	case "florist":
		var icon='src/icons/florist.svg'
		break;
	case "funeral_home":
		var icon='src/icons/funeral-home.svg'
		break;
	case "furniture_store":
		var icon='src/icons/furniture-store.svg'
		break;
	case "gas_station":
		var icon='src/icons/gas-station.svg'
		break;
	case "gym":
		var icon='src/icons/gym.svg'
		break;
	case "hair_care":
		var icon='src/icons/hair-care.svg'
		break;
	case "hardware_store":
		var icon='src/icons/hardware-store.svg'
		break;
	case "hindu_temple":
		var icon='src/icons/hindu-temple.svg'
		break;
	case "hospital":
		var icon='src/icons/hospital.svg'
		break;
	case "insurance_agency":
		var icon='src/icons/insurance-agency.svg'
		break;
	case "jewelry_store":
		var icon='src/icons/jewelry-store.svg'
		break;
	case "laundry":
		var icon='src/icons/laundry.svg'
		break;
	case "lawyer":
		var icon='src/icons/lawyer.svg'
		break;
	case "library":
		var icon='src/icons/library.svg'
		break;
	case "liquor_store":
		var icon='src/icons/liquor-store.svg'
		break;
	case "locksmith":
		var icon='src/icons/locksmith.svg'
		break;
	case "lodging":
		var icon='src/icons/lodging.svg'
		break;
	case "mosque":
		var icon='src/icons/mosque.svg'
		break;
	case "movie_rental":
		var icon='src/icons/movie-rental.svg'
		break;
	case "movie_theater":
		var icon='src/icons/movie-theater.svg'
		break;
	case "moving_company":
		var icon='src/icons/moving-company.svg'
		break;
	case "museum":
		var icon='src/icons/museum.svg'
		break;
	case "night_club":
		var icon='src/icons/night-club.svg'
		break;
	case "painter":
		var icon='src/icons/painter.svg'
		break;
	case "park":
		var icon='src/icons/park.svg'
		break;
	case "parking":
		var icon='src/icons/parking.svg'
		break;
	case "pet_store":
		var icon='src/icons/pet-store.svg'
		break;
	case "pharmacy":
		var icon='src/icons/pharmacy.svg'
		break;
	case "physiotherapist":
		var icon='src/icons/physiotherapist.svg'
		break;
	case "plumber":
		var icon='src/icons/plumber.svg'
		break;
	case "police":
		var icon='src/icons/police.svg'
		break;
	case "post_office":
		var icon='src/icons/post-office.svg'
		break;
	case "restaurant":
		var icon='src/icons/restaurant.svg'
		break;
	case "roofing_contractor":
		var icon='src/icons/roofing-contractor.svg'
		break;
	case "rv_park":
		var icon='src/icons/rv-park.svg'
		break;
	case "school":
		var icon='src/icons/school.svg'
		break;
	case "shopping_mall":
		var icon='src/icons/shopping-mall.svg'
		break;
	case "spa":
		var icon='src/icons/spa.svg'
		break;
	case "stadium":
		var icon='src/icons/stadium.svg'
		break;
	case "storage":
		var icon='src/icons/storage.svg'
		break;
	case "store":
		var icon='src/icons/store.svg'
		break;
	case "subway_station":
		var icon='src/icons/subway-station.svg'
		break;
	case "synagogue":
		var icon='src/icons/synagogue.svg'
		break;
	case "taxi_stand":
		var icon='src/icons/taxi-stand.svg'
		break;
	case "train_station":
		var icon='src/icons/train-station.svg'
		break;
	case "transit_station":
		var icon='src/icons/transit-station.svg'
		break;
	case "travel_agency":
		var icon='src/icons/travel-agency.svg'
		break;
	case "university":
		var icon='src/icons/university.svg'
		break;
	case "veterinary_care":
		var icon='src/icons/veterinary-care.svg'
		break;
	case "zoo":
		var icon='src/icons/zoo.svg'
		break;
	default:
		var icon = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'
}
          return new google.maps.Marker({
            position: location,
            icon: icon,
            title : nombres[i % nombres.length]
            });
        });

        var markerCluster = new MarkerClusterer(map, markers,
            {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
      }
      var locations = """+locations+"""
    </script>
    <script src="https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/markerclusterer.js">
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB-yjSWzs0WVI822X6a68P5JpsqjLVCxHk&callback=initMap">
    </script>
  </body>
</html>
"""
Html_file= open("cosa.html","w")
Html_file.write(input_form)
Html_file.close()

