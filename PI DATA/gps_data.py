import gps
import time
import pymongo

session = gps.gps("127.0.0.1", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
client = pymongo.MongoClient('mongodb+srv://sd3bFMC:admin@cluster0.cvfp9.mongodb.net/fmc?retryWrites=true&w=majority')

db=client['fmc']

col = db['gpsdb']


while True:
    try:
        time.sleep(0.5)
        raw_data = session.next()
        latD = ""
        lngD = ""
        altD = ""
        timeD = ""
        if raw_data['class'] == 'TPV':
            if hasattr(raw_data, 'lat'):
                print
                "Latitude is = " + str(raw_data.lat)
                latD = raw_data.lat
        if raw_data['class'] == 'TPV':
            if hasattr(raw_data, 'lon'):
                print
                "Longitude is = " + str(raw_data.lon)
                lngD = raw_data.lon
        if raw_data['class'] == 'TPV':
            if hasattr(raw_data, 'speed'):
                print
                "Vehicle is moving at = " + str(raw_data.speed) + " KPH"
        if raw_data['class'] == 'TPV':
            if hasattr(raw_data, 'alt'):
                print
                "The altitude is = " + str(raw_data.alt) + " m"
                altD = raw_data.alt
        if raw_data['class'] == 'TPV':
            if hasattr(raw_data, 'time'):
                print
                "The current date and time is = " + str(raw_data.time) + "\n"
                timeD = raw_data.time

        data = {'lat': latD, 'lng': lngD, 'alt': altD, 'datetime': timeD}

        col.insert_one(data)

    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print
        "No incoming data from the GPS module"
