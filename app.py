import os.path
from datetime import datetime
from micropyGPS import MicropyGPS

if __name__ == "__main__":
	sentence_count = 0
	processed_count = 0

	nowtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	#READ FILE
	filename="vuelo_1.nmea"
	with open(filename) as f:
		content = f.readlines()
		content = [x.strip() for x in content]

	my_GeoJSONfilePoint=""
	my_GeoJSONobjPoint=""

	my_GeoJSONfilePath=""
	my_GeoJSONobjPath=""
	
	my_gps = MicropyGPS(location_formatting='dd')

	#DECODE NMEA
	for GGA_sentence in content:
		sentence_count += 1
	 	for y in GGA_sentence:
	 		sentence = my_gps.update(y)

	 	if(sentence=='GPGGA'):
	 		processed_count +=1
	 		print('Parsed a', sentence, 'Sentence')
	 		print('Parsed Strings', my_gps.gps_segments)
	 		print('Sentence CRC Value:', hex(my_gps.crc_xor))
	 		print('Longitude', my_gps.longitude)
	 		print('Latitude', my_gps.latitude)
	 		print('Latitude:', my_gps.latitude_string())
	 		print('Longitude:', my_gps.longitude_string())
	 		print('UTC Timestamp:', my_gps.timestamp)
	 		print('Fix Status:', my_gps.fix_stat)
	 		print('Altitude:', my_gps.altitude)
	 		print('Height Above Geoid:', my_gps.geoid_height)
	 		print('Horizontal Dilution of Precision:', my_gps.hdop)
	 		print('Satellites in Use by Receiver:', my_gps.satellites_in_use)
	 		print('')
	 		longitud=0
			if(my_gps.longitude[1]=='W'):
	 			longitud=my_gps.longitude[0]*-1
	 		else:
	 			longitud=my_gps.longitude[0]
	 		latitud=0
			if(my_gps.latitude[1]=='S'):
	 			latitud=my_gps.latitude[0]*-1
	 		else:
	 			latitud=my_gps.latitude[0]
	 		my_GeoJSONobjPoint+='{"type": "Feature","properties": {'
	 		my_GeoJSONobjPoint+='"oid":'+str(processed_count)
	 		my_GeoJSONobjPoint+=', "hdop":'+str(my_gps.hdop)
	 		my_GeoJSONobjPoint+=', "sats":'+str(my_gps.satellites_in_use)
	 		my_GeoJSONobjPoint+=', "height":'+str(my_gps.geoid_height)
	 		my_GeoJSONobjPoint+=', "altitude":'+str(my_gps.altitude)
	 		my_GeoJSONobjPoint+=', "timestamp":"'+str(my_gps.timestamp)+'"'
	 		my_GeoJSONobjPoint+=', "fix_stat":'+str(my_gps.fix_stat)
	 		my_GeoJSONobjPoint+=', "orginalfile":"'+str(filename)+'"'
	 		my_GeoJSONobjPoint+=', "processed":"'+str(nowtime)+'"'
	 		my_GeoJSONobjPoint+='},"geometry": {"type": "Point","coordinates": ['+str(longitud)+','+str(latitud)+']}},'

	 		my_GeoJSONobjPath+='['+str(longitud)+','+str(latitud)+'],'

	#WRITE POINT FILE
	my_GeoJSONfilePoint+='{ "type": "FeatureCollection","features": ['
	#Removing Last character from string
	my_GeoJSONfilePoint+=my_GeoJSONobjPoint[:-1]
	my_GeoJSONfilePoint+=']}'
	print(my_GeoJSONfilePoint)
	file = open( filename.split(".")[0]+'_point.geojson' , 'w')
	file.write(my_GeoJSONfilePoint)
	file.close()

	#WRITE PATH FILE
	my_GeoJSONfilePath+='{ "type": "FeatureCollection","features": [{"type": "Feature","properties": { "orginalfile":"'+str(filename)+'" , "numpoints":"'+str(processed_count)+'" ,  "processed":"'+str(nowtime)+'" },"geometry": {"type": "LineString","coordinates": ['
	#Removing Last character from string
	my_GeoJSONfilePath+=my_GeoJSONobjPath[:-1]
	my_GeoJSONfilePath+=' ] } } ] }'
	print(my_GeoJSONfilePath)
	file = open( filename.split(".")[0]+'_path.geojson' , 'w')
	file.write(my_GeoJSONfilePath)
	file.close()

