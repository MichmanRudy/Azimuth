# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import os
import sys
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

emptyWord = 'empty'
pointsDelta = [emptyWord, emptyWord]

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('creds/azimuth1-0e58a3cdb4e1.json', scope)

# authorize the clientsheet
client = gspread.authorize(creds)

sheet = client.open('testdata')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)


# get the total number of columns
print(sheet_instance.col_count)

# get the value at the specific cell
homePointCoordsAutotest = [sheet_instance.cell(4, 2).value, sheet_instance.cell(4, 3).value]
print(homePointCoordsAutotest)
# val = worksheet.acell('B1').value
# https://docs.gspread.org/en/latest/user-guide.html

for counter in range(8):
    targetPointCoordsAutotest = [sheet_instance.cell(4 + counter, 4).value, sheet_instance.cell(4 + counter, 5).value]
    for i in range(2):
        pointsDelta[i] = float(targetPointCoordsAutotest[i].replace(',', '.'))-float(homePointCoordsAutotest[i].replace(',', '.'))

    if pointsDelta[0] > 0:
        if pointsDelta[1] > 0:
            azimuth = math.degrees(math.atan(pointsDelta[0]/pointsDelta[1]))
            print('A condition worked')
        else:
            azimuth = 90 + abs(math.degrees(math.atan(pointsDelta[1]/pointsDelta[0])))
            print('C condition worked')
    if pointsDelta[0] == 0:
        if pointsDelta[1] > 0:
            azimuth = 0
            print('D condition worked')
        if pointsDelta[1] == 0:
            print('Home and Target coords are the same')
            print('E condition worked')
        if pointsDelta[1] < 0:
            azimuth = 180.0
            print('F condition worked')
    if pointsDelta[0] < 0:
        if pointsDelta[1] >= 0:
            azimuth = 270 + abs(math.degrees(math.atan(pointsDelta[1]/pointsDelta[0])))
            print('G condition worked')
        else:
            azimuth = 180 + abs(math.degrees(math.atan(pointsDelta[0]/pointsDelta[1])))
            print('I condition worked')
    sheet_instance.update_cell(4+counter, 11, azimuth)


def check_input_correct(keyboard_input: str, empty_word):
    number_commas_in_input = 0
    for character in keyboard_input:
        if character == ',':
            number_commas_in_input = number_commas_in_input+1
    if number_commas_in_input == 0:
        print('Input was made incorrectly, no any COMMA found \nmake sure you separate latitude and longitude with '
              'COMMA')
        return emptyWord
    if number_commas_in_input > 1:
        print('Too much COMMAS \nThere should be only one COMMA separating latitude and longitude')
        return emptyWord
    if number_commas_in_input == 1:
        print('Input contains one comma')
        checked_coords = keyboard_input.split(',')
        for counter in range(2):
            try:
                float(checked_coords[counter])
                pass
            except TypeError:
                print('coords contain wrong symbols')
                return empty_word
        print(checked_coords)
        return checked_coords


emptyWord = 'empty'
pointsDelta = [emptyWord, emptyWord]
homePointInputCorrect: bool = False
while True:
    homePointInputString = input('type Home point like: 50.345678,30.234567 \nHome point coords: ')
    if not homePointInputString:
        sys.exit('Exit because Home point not specified')
    homePointCoordsList = check_input_correct(homePointInputString, emptyWord)
    print(homePointCoordsList)
    if homePointCoordsList != emptyWord:
        break

while True:
    while True:
        targetPointInputString = input('type Target point like: 50.345678,30.234567 \nTarget point coords: ')
        if not targetPointInputString:
            sys.exit('Exit because Target point not specified')
        targetPointCoordsList = check_input_correct(targetPointInputString, emptyWord)
        print(targetPointCoordsList)
        if targetPointCoordsList != emptyWord:
            break
    for i in range(2):
        pointsDelta[i] = float(targetPointCoordsList[i])-float(homePointCoordsList[i])
    print(homePointCoordsList)
    print(targetPointCoordsList)
    print(pointsDelta)
    if pointsDelta[0] > 0:
        if pointsDelta[1] > 0:
            azimuth = math.degrees(math.atan(pointsDelta[0]/pointsDelta[1]))
            print('A condition worked')
        else:
            azimuth = 90 + abs(math.degrees(math.atan(pointsDelta[1]/pointsDelta[0])))
            print('C condition worked')
    if pointsDelta[0] == 0:
        if pointsDelta[1] > 0:
            azimuth = 0
            print('D condition worked')
        if pointsDelta[1] == 0:
            print('Home and Target coords are the same')
            print('E condition worked')
        if pointsDelta[1] < 0:
            azimuth = 180.0
            print('F condition worked')
    if pointsDelta[0] < 0:
        if pointsDelta[1] >= 0:
            azimuth = 270 + abs(math.degrees(math.atan(pointsDelta[1]/pointsDelta[0])))
            print('G condition worked')
        else:
            azimuth = 180 + abs(math.degrees(math.atan(pointsDelta[0]/pointsDelta[1])))
            print('I condition worked')
    print('azimuth = ', azimuth)
    os.system('pause')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
