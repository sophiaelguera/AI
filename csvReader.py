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

def findSpecificStation(station): 
    with open('stations.csv') as file_obj:
        values = []
        reader_obj = csv.reader(file_obj)

        for row in reader_obj:
            if row[0] == station.upper():
                values.append(row[0])   
            elif row[3] == station.upper():
                return station
            elif row[1] == station:
                values.append(row[0])            
            elif station.upper() in row[0]:
                values.append(row[0])  
    return values


def findStationLongABV(station):

    with open('stations.csv') as file_obj:

        reader_obj = csv.reader(file_obj)
        next(reader_obj)
        for row in reader_obj:
            if row[0] == station.upper():
                value = row[4]
                return value
            if row[4] == station.upper():
                return station.upper()
            if row[1] == station:
                value = row[4]
                return value
            if station.upper() in row[0]:
                value = row[4]
                return value

