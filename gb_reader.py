import fnmatch
import os
from pamda import pamda as p

# First use AWS CLI to sync the directory you want to work in
# $aws s3 sync "s3://hurricane.gasbuddy.io/Hurricane Ida 2021 Outages/" Hurricane_Ida_Outages --no-sign-request

working_directory = "development/gasbuddy/"
activation_directory = "Hurricane_Ida_Outages/"

# Use directory with all the files
dir_path = os.path.join(os.path.expanduser('~'), working_directory)
data_path = os.path.join(dir_path, activation_directory)

# Temp files to write out
tmp_DMA = os.path.join(dir_path, "Gas_Buddy_DMA_Hurricane_Ida.csv")
tmp_Retail =os.path.join(dir_path, "Gas_Buddy_Retail_Hurricane_Ida.csv")

# process the data every time - list of dictionaries
DMAData = []
RetailStationData = []

# list all the directories in the data_path
dir_list = os.listdir(data_path)

# list all the files in each directory
print("Reading files")
for dir_name in dir_list:
    # Skipping the iteration when directory is '.DS_Store'
    if dir_name == '.DS_Store':
        continue

    path = os.path.join(data_path, dir_name)
    file_list = os.listdir(path)

    # Examples of the file naming structure:
    # GasBuddy Station Outages - Fuel Availability - MS.csv
    # GasBuddy Station Outages - Fuel Availability - LA.csv
    # GasBuddy Station Outages - Fuel Availability Map - MS.kml
    # GasBuddy Station Outages - Fuel Availability Map - LA.kml
    # GasBuddy Station Outages - Fuel Availability DMA Summary - LA.csv
    # GasBuddy Station Outages - Fuel Availability DMA Summary - MS.csv

    for name in file_list:
        # check is the file is csv
        if fnmatch.fnmatch(name, '*.csv'):
            # read data on DMA
            if fnmatch.fnmatch(name, '* DMA *.csv'):
                l = p.read_csv(filename=os.path.join(path,name))

                # l is a list of dictionaries
                # add items to every dictionary in a list of dictionaries

                for d in l:
                    # add key to each dictionary with the state - (state: st)
                    file_name, file_extension = os.path.splitext(name)
                    # Get last 2 characters of file_name
                    d["State"] = file_name[-2:]

                    # add each dictionary to the comprehensive list
                    DMAData.append(d)

                    # add keys from the directory name - date: day; (hour: hr; minute: min)
                    # datetime(year, month, day) "2021-09-06 20-12"; datetime_object = datetime.strptime(dir_name, '%Y-%m-%d %H-%M')
                    # d["DateTime"] = datetime_object; d["Date"] = datetime_object.date; d["Hour"] = datetime_object.hour; d["Minute"] = datetime_object.minute
            else:  # read in the data on gas stations
                # l is a list of dictionaries
                l = p.read_csv(filename=os.path.join(path, name))

                # add items to every dictionary in a list of dictionaries
                for d in l:
                    # rename the first empty key (column) that contains an object_id (I think)
                    new_key = "object_id"
                    old_key = ''
                    d[new_key] = d.pop(old_key)

                    # add key to each dictionary with the state - (state: st)
                    file_name, file_extension = os.path.splitext(name)
                    # Get last 2 characters of file_name
                    d["State"] = file_name[-2:]

                    # add each dictionary to the comprehensive list
                    RetailStationData.append(d)
        else:  # skip the kml files
            ...

# finished reading all the files

# write out the data
print("Writing file:",tmp_DMA)
p.write_csv(filename=tmp_DMA, data=DMAData)
print("Writing file:",tmp_Retail)
p.write_csv(filename=tmp_Retail, data=RetailStationData)
print("Done!")