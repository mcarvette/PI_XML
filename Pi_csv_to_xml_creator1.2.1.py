#
#****************************************************
# *****     Pi XML creator 1.2.1                *****
# *****     Created by Matt Carvette on 9/13/16 *****
# *****     Copyright 2016 Matt Carvette        *****
#****************************************************
#


import csv                                                          #load csv library
import urllib

XML_Conversion = open('/Users/MattCarvette/Documents/MEC_TGA16_V2.xml', "w")

PBLog = urllib.urlopen('https://docs.google.com/spreadsheets/d/15i-T3LQxkusBRSGcwHbVuxQV4YWWq0RhOfXMZx1y2yc/export?format=csv&id=15i-T3LQxkusBRSGcwHbVuxQV4YWWq0RhOfXMZx1y2yc')
#PBLog  = open('/Users/MattCarvette/Documents/TGA2016_1.csv')         #open csv file to import
csv_PBLog = csv.reader(PBLog)                                       #load file

Event = -6                                                          #forces loop to ignore header rows


XML_Conversion.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')     #write first line of XML
XML_Conversion.write('<PiImportList>\n')                                              #write second line of XML



for row in csv_PBLog:                                               #begin loop to read each row



    if Event == -5:                                                 #checks cell B2 to determine if timecode should be Drop-Frame or Non-Drop-Frame
        if 'NDF' in row[1]:
            TCtype = ':'                                            #if timecode is NDF the delimiter is set to ":"
        else:
            TCtype = ';'                                            #if timecode is DF the delimiter is set to ";"
        TrafficPrimary1 = row[7]

    if Event == -4:
        TrafficPrimary2 = row[7]

    if Event == -3:
        TrafficBackup1 = row[7]

    if Event == -2:
        TrafficBackup2 = row[7]
        

            

    if Event >= 0:                                                  #begin main parsing loop

                                          
        RowCheck = ''.join(c for c in row[0] if c.isalpha())        #checks for presence of Act Separator row or a blank row
        if RowCheck != 'ACT' and RowCheck != 'GFX' and RowCheck != 'EXTRA' and RowCheck != 'PRESHOW' and len(row[0]) > 0:                   #if the Act Separator row or blank row does not exist, the loop continues
            
                                                                    #THIS BLOCK EXTRACTS DATA FROM EACH COLUMN IN ROW
            Item = row[0]                                           #"
            Description = row[1]                                    #"
            TCin = row[2]                                           #"
            TCout = row[3]                                          #"
            Duration = row[4]                                       #"
            FileName = row[5]                                       #"
            Notes = row[6]                                          #"
            Traffic = row[7]                                        #"

            if len(Traffic) == 0 or len(Traffic) > 1:               #checks to see if traffic cell is blank or longer than one character
                Traffic = '0'                                       #if traffic cell is blank or longer than one character, then assign channel "0" so Pi will ignore it


            
            if '\n' in FileName:                                    #checks for presence of Matte
                Matte = 1
                NewLineMarker = FileName.find('\n')                 #finds location of line separator between matte and fill filenames
                FileNameFill = FileName[:NewLineMarker]             #extracts filename of fill
                FileNameMatte = FileName[NewLineMarker+1:]          #extracts filename of matte
            else:
                Matte = 0



            TrafficPrimary = Traffic                                #assigns primary playback channel
#            TrafficBackup = chr(ord(Traffic) + 2)                   #assigns backup playback channel
            TrafficBackup = '0'
            if TrafficPrimary == TrafficPrimary1:
                TrafficBackup = TrafficBackup1
            if TrafficPrimary == TrafficPrimary2:
                TrafficBackup = TrafficBackup2
            


            

            if '.' in Item:                                         #checks for presence of "." (decimal) in Item
                DecimalMarker = Item.find('.')                      #finds location of decimal in Item
                LeftOfDecimal = Item[:DecimalMarker]                #extracts data from left of decimal
                RightOfDecimal = Item[DecimalMarker+1:]             #extracts data from right of decimal
                ItemNumber = ''.join(i for i in LeftOfDecimal if i.isdigit())       #extracts numbers from left of decimal
                ItemLetter = ''.join(c for c in LeftOfDecimal if c.isalpha())       #extracts letters from left of decimal
                ItemNumberConverted = ItemNumber.rjust(4, '0')      #adds leading zeroes left of decimal as needed
                if len(ItemLetter) > 0:                             #checks for presence of letter in Item
                    ItemLetterConverted = ItemLetter                #if letter exists, keep it
                else:
                    ItemLetterConverted = 0                         #if letter noes not exist, assign value of zero
                EventNumFormatted = str(ItemNumberConverted) + '.' + str(ItemLetterConverted) + str(RightOfDecimal)     #format EventNumber
            else:                                                       #if "." (decimal) does not exist in Item...
                ItemNumber = ''.join(i for i in Item if i.isdigit())    #extracts numbers from Item
                ItemLetter = ''.join(c for c in Item if c.isalpha())    #extracts letters from Item
                ItemNumberConverted = ItemNumber.rjust(4, '0')          #adds leading zeroes as needed
                if len(ItemLetter) > 0:                                 #checks for presence of letter in Item
                    ItemLetterConverted = ItemLetter                    #if letter exists, keep it
                else:
                    ItemLetterConverted = 0                             #if letter does not exist, assign value of zero
                EventNumFormatted = str(ItemNumberConverted) + '.' + str(ItemLetterConverted)   #format EventNumber
            




                
            XML_Conversion.write('  <Event%s>\n' % (Event))
            XML_Conversion.write('    <EventNum>%s</EventNum>\n' % (EventNumFormatted))
            XML_Conversion.write('    <EventName>%s</EventName>\n' % (Description))



            if TCin == '':                                          #if Timecode cells are blank, then set all zeros as placeholders
                TCin = '00:00:00'
            if TCout == '':
                TCout = '00:00:00'



            if Matte == 1:                                          #if a matte exists...
                XML_Conversion.write('    <C0>%s|%s|%s%s00|%s%s00</C0>\n' % (TrafficPrimary, FileNameFill, TCin, TCtype, TCout, TCtype))
                XML_Conversion.write('    <C1>%s|%s|%s%s00|%s%s00</C1>\n' % (TrafficPrimary + TrafficPrimary, FileNameMatte, TCin, TCtype, TCout, TCtype))
#                XML_Conversion.write('    <C2>%s|%s|%s%s00|%s%s00</C2>\n' % (TrafficBackup, FileNameFill, TCin, TCtype, TCout, TCtype))
#                XML_Conversion.write('    <C3>%s|%s|%s%s00|%s%s00</C3>\n' % (TrafficBackup + TrafficBackup, FileNameMatte, TCin, TCtype, TCout, TCtype))

            if Matte == 0:                                          #if a matte does not exist...
                XML_Conversion.write('    <C0>%s|%s|%s%s00|%s%s00</C0>\n' % (TrafficPrimary, FileName, TCin, TCtype, TCout, TCtype))
#                XML_Conversion.write('    <C1>%s|%s|%s%s00|%s%s00</C1>\n' % (TrafficBackup, FileName, TCin, TCtype, TCout, TCtype))
                


            XML_Conversion.write('  </Event%s>\n' % (Event))


        else:
            Event = Event - 1                                       #If the Act Separator row or blank row exists then adjust Event variable accordingly
                

    Event = Event + 1                                               #advance to next row in csv file and repeat loop


XML_Conversion.write('<PiImportList>\n')                            #write last line of XML

XML_Conversion.close()
PBLog.close()                                                       #close csv file
