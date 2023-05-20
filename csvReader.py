import csv

def findStationABV(station):
  
    with open('stations.csv') as file_obj:
        
        reader_obj = csv.reader(file_obj)

        for row in reader_obj:
            if row[0] == station.upper():
                value = row[3]
                return value
            if row[3] == station.upper():
                return station
            if row[1] == station:
                value = row[3]
                return value
            if station.upper() in row[0]:
                value = row[3]
                return value
            


