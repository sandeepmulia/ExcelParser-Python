from typing import Dict, Any
import pandas as pd
import datetime

#Object to store processed data and contains helper functions to format display
class Data:
    def __init__(self, rate, quarter):
        self.rate = rate
        self.quarter = quarter

    def print_info(self):
        print("Recorded growth increase of {:.{}f}".format((self.rate * 100),4), "% in the ", self.stringify_date())

    def stringify_date(self):
        return "Year " +  str(self.quarter.year) + " and Quarter #" + str(self.quarter.month / 3) + " i.e. " + datetime.date(1900, self.quarter.month, 1).strftime('%B')

#The core method to process the excel file contents using pandas dataframe and convert the dataframe into a dictionary
#for easy lookup. The population numbers is contained from row 10 (9 in code as counting begins from 0) till row 164
#Logic
#Step 1: Select one column of data and check if the data is related to Male and not the first column
#Step 2: Extract the values in the pandas dataframe converted to dictionary and find the highest quarterly increase
#        using the formula (present - prev)/present
#Step 3: Maintain variables which track the highest rate of increase along with the row index
#Step 4: Use lookup of first column to determine the exact year, month and build a dictionary of
#         Territories versus the highest detected population increase data
#Step 5: Among all the territories for which the highest rate of increase was recorded,compare which territory has
#        record the highest and display the result

def process_data(file):
    global dictionary

    if 'dictionary' not in globals():
        dictionary = {}

    data_frame = pd.read_excel(excelFile, "Data1")
    dictionary = data_frame.to_dict()

    from_index = 9 #Skip first 9 rows containing header
    to_index = data_frame.shape[0] #determine the total number of rows

    #print ("Row = " , from_index , "toIndex ", to_index);
    processed_dictionary = {}
    keyword = "Male"
    exclude_key = "Unnamed"

    for key, values in dictionary.items():
      #print ( "Key =>", key)

      if keyword in key and exclude_key not in key:
          value_data = values
          highest_ratio: int = -1
          index = from_index
          previous_value: int = -1
          qtr_data: int
          rate: int

          for qtr in list(value_data.values())[from_index:to_index]:
             qtr_data = int(qtr)


             if previous_value is -1:
                 previous_value = qtr_data

             rate = (qtr_data - previous_value)/qtr_data

             #print ("Rate ", rate, "Ratio ", highestRatio)

             if highest_ratio < rate:
                highest_ratio = rate
                quarter = lookup(key, index)
                stat_object = Data(highest_ratio, quarter)
                processed_dictionary[key] = stat_object

             previous_value = qtr_data
             index = index + 1

    item = determine_highest_rate_of_increase(processed_dictionary)

    print ("State :", item.split(';')[2].strip())
    processed_dictionary[item].print_info()

#########
#Helpers#
#########

#lookup first column and extract the year month data
def lookup(key, position):
    quarter = list(dictionary["Unnamed: 0"].values())[position]
    #print("Quarter :", quarter)
    return quarter;

#determine the highest rate of population increase by looking up the values in the dictionary
def determine_highest_rate_of_increase(processed_dictionary):
    return max(processed_dictionary.keys(), key=lambda k: processed_dictionary[k].rate)


#################################
#        MAIN PROGRAM           #
#################################

print ("Australian Bureau of Statistics \n");
excelFile = "310104.xls";
print ("Excel File:", excelFile);
process_data(excelFile)


#OUTPUT
#C:\Users\Sandeep\.virtualenvs\ABS-WKpZyvzJ\Scripts\python.exe C:/Users/Sandeep/AppData/Roaming/JetBrains/PyCharmCE2020.1/scratches/scratch.py
#Australian Bureau of Statistics

#Excel File: 310104.xls
#State : Northern Territory
#Recorded growth increase of 1.9830 % in the  Year 1981 and Quarter #3.0 i.e. September

