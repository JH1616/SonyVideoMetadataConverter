
import xml.etree.ElementTree as xml
import exiftool
import glob
import os


et = exiftool.ExifToolHelper()


files = glob.glob("/Users/jorn/NichtGesichert/SonyVideoConversion/*.XML")


def doconversion(file):
    gps_info = {}
    cam_info = {}
    tree = xml.parse(file)
    root = tree.getroot()
    for child in root:
        if "AcquisitionRecord" in child.tag:
            for group in child:
                if "ExifGPS" in group.attrib.values():
                    for info in group:
                        gps_info.update({info.attrib['name']: info.attrib['value']})
        elif "Device" in child.tag:
            cam_info = child.attrib

    videoname = file.replace('M01.XML', '.MP4')

    if gps_info and 'Latitude' in gps_info:
        def replacer(inputstr):
            grad, m, s = inputstr.split(':')
            return round(int(grad) + int(m)/60 + float(s)/3600, 5)

        Latitude = replacer(gps_info['Latitude'])
        Longitude = replacer(gps_info['Longitude'])

        if gps_info['LatitudeRef'] == 'S':
            Latitude =  -1 * Latitude

        if gps_info['LongitudeRef'] == 'W':
            Longitude =  -1 * Longitude

        
        #for i in gps_info.items():
        #    print(i)
        print(videoname, Latitude, Longitude)

        et.set_tags(videoname, tags={
             "keys:gpscoordinates": [str(Latitude) + " " + str(Longitude)],
             "keys:Make": [cam_info['manufacturer']],
             "keys:Model": [cam_info['modelName']] 
             }, params=["-api", "largefilesupport=1"])

    else:
        print(videoname, "no geodata")

        et.set_tags(videoname, tags={
             "keys:Make": [cam_info['manufacturer']],
             "keys:Model": [cam_info['modelName']]
             }, params=["-api", "largefilesupport=1"])
        
    #met = et.get_metadata(videoname)[0]
    #for i in met.items():
    #    print(i)

    os.remove(file)
    os.remove(file.replace('M01.XML', '.MP4_original'))


for file in files:
    try:
        doconversion(file)
    except:
        print("failed in", file)







