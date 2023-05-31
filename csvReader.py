import csv


#Method to read through csv and match user input to correct station name and abbreviation for web scraping
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

# Method to help deal with user input ambiguity, returns a list of all stations that match the name parameter
def findSpecificStation(station): 
    with open('stations.csv') as file_obj:
        values = []
        reader_obj = csv.reader(file_obj)

        for row in reader_obj:
            if station == 'London':
                return station
            if row[0] == station.upper():
                values.append(row[0])   
            elif row[3] == station.upper():
                return station
            elif row[1] == station:
                values.append(row[0])            
            elif station.upper() in row[0]:
                values.append(row[0])  
    return values


# method that matches station name with station long abreviation
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

