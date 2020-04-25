import urllib.request as req
import os
import sys
import imageio
import argparse
import subprocess
import datetime as dt
import shutil

# Argument parser
parser = argparse.ArgumentParser("Download Earth Images and Create Video")
parser.add_argument("-t", "--thinning", default=1, help="Frequency of images to download, e.g. every 10th image")
parser.add_argument("-f", "--ffmpeg", action='store_true', help="Use ffmpeg to create video")
args = parser.parse_args()


def add2Zeros(imageNumber):
    """Add leading zeros to a number, up to 4 digits."""
    numAdd = 2 - len(str(imageNumber))
    return "0" * numAdd + str(imageNumber)

def addZeros(imageNumber):
    """Add leading zeros to a number, up to 4 digits."""
    numAdd = 4 - len(str(imageNumber))
    return "0" * numAdd + str(imageNumber)


def getImage(imageNumber, directory,totalImages,lastImage):
    """Download an image given an image to an output directory"""
    sDays = totalImages/(6*24)
    sDate = dt.datetime.now() - dt.timedelta(days=sDays)
    #print("date initial= " ,sDate)
    sDate = dt.datetime(sDate.year,sDate.month,sDate.day,sDate.hour)
    #print("date zeroed = " ,sDate, " imgnr=", imageNumber, " sdate = ", sDate)
    imgNr = int(imageNumber)
    sDate = sDate + dt.timedelta(minutes=imgNr*10)
    if sDate.hour == 24 and sDate.minute == 0:
         print("hour 24")
         sDate.day = sdate.day +1
         sDate.hour = 0
    #sDate.replace(minute=0,second=0,microsecond=0) 
    #print("date = " ,sDate," ", add2Zeros(str(sDate.year)), add2Zeros(str(sDate.month)), add2Zeros(str(sDate.day)), add2Zeros(str(sDate.hour)), add2Zeros(str(sDate.minute))+"00");
     
    URL1 = (
            "http://rammb.cira.colostate.edu/"
            "ramsdis/online/images/"
            "himawari-8/full_disk_ahi_true_color/full_disk_ahi_true_color_"+
            str(sDate.year)+
            add2Zeros(str(sDate.month))+
            add2Zeros(str(sDate.day))+
            add2Zeros(str(sDate.hour))+
            add2Zeros(str(sDate.minute))+"00.jpg")

    URL2 = (
            "http://rammb.cira.colostate.edu/"
            "ramsdis/online/himaw/"
            "himawari-8/full_disk_ahi_true_color/full_disk_ahi_true_color_"+
            str(sDate.year)+
            add2Zeros(str(sDate.month))+
            add2Zeros(str(sDate.day))+
            add2Zeros(str(sDate.hour))+
            add2Zeros(str(sDate.minute))+"00.jpg")
    imageName = directory + imageNumber + ".jpg"
    #print ("url1=",URL," image=",imageName, " isfile=", os.path.isfile(imageName), " lastImage=", lastImage)
    #print ("url1=",URL," image=",imageName, " isfile=", os.path.isfile(imageName))
    try:
        #print("imageName = ", imageName, " lastImage2a=", imageName)
        req.urlretrieve(URL1, imageName)
    
    except:
        #print("lastImage3a=", lastImage, " error=" , sys.exc_info())
        #print ("check if ", imageName, " isfile=" , os.path.isfile(imageName))
        if( os.path.isfile(imageName) == False):
             print("error retrieveing : " + URL1 + " to " + imageName)
             req.urlretrieve(URL2, imageName)
             print("trying:" + URL2)
             # dublicate last
             # shutil.copyfile(lastImage,imageName)
    finally:
        if( os.path.isfile(imageName) == False):
             print("dublicating ", lastImage, " to ", imageName)
             shutil.copyfile(lastImage,imageName)
          
    lastImage = imageName
    
    return

def makeVideo(directory, startNumber, thinning, ffmpeg=False):
    """Create a video with the downloaded images"""
    
    # Get a list of all the files 
    files = [image for image in os.listdir(directory) if ".jpg" in image]
    

    # Create a video using ffmpeg command
    if ffmpeg:
        frameRate = len(files)/60
        frameRate = min(30,frameRate)
        frameRate = str(frameRate)
        print("framerate %s\n" % (frameRate));
        subprocess.run(
                ["ffmpeg",
                "-r", frameRate, 
                "-pattern_type", "glob",
                "-i", "./" + directory + "*.jpg",
                "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
                "-vb", "20M", "earth-himawari.mp4"], check=True)
    
    else:
        # Save each image frame to a list
        images = []
        for imageNumber in range(startNumber, totalImages, thinning):
            imageName = directory + addZeros(imageNumber) + ".jpg"
            images.append(imageio.imread(imageName))

        imageio.mimsave('earth-himawari.gif', images)
    return

def main(startNumber=1, thinning=1, ffmpeg=False):
    
    directory = 'himaw/'
    totalImages = 2500
    lastImage = "000.jpg"

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for i, imageNumber in enumerate(range(startNumber, totalImages, thinning)):
        percent = round(imageNumber/totalImages*100)
        imageNumber = addZeros(imageNumber)
        
        # Skip if already downloaded
        if os.path.exists(directory + imageNumber + ".jpg"):
            lastImage = directory + imageNumber + ".jpg"
            print("Already downloaded " + imageNumber, "lastImage=",lastImage)  
            continue
            
        loop = 0
        while True:
            try:
                if loop >= 3:
                    return

                loop = loop + 1
                #print("loop=", loop, " image=", imageNumber)
                getImage(imageNumber, directory, totalImages, lastImage)
                lastImage = directory + imageNumber + ".jpg"
                
                # Create progress bar, we use 0.5*percentage
                # for a shorter bar
                bar = (
                        "["
                        + "#" * int(0.5 * percent)
                        + "-" * int(0.5 * (100.1 - percent))
                        + "]"
                )
                
                # Clear terminal
                print('\033c')

                # Print progress
                status = "Downloaded {}/{}, {}% ".format(i, totalImages//thinning, percent)
                print(status + bar)

            except Exception as e:
                print("exception ",e)
                continue
            break
            
    print("Making video...")
    makeVideo(directory, startNumber, thinning, ffmpeg)
    return


main(1, int(args.thinning), args.ffmpeg)


