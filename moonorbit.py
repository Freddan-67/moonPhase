import urllib.request as req
import os
import imageio
import argparse
import subprocess
#this number is actually one bigger than max image number
totalImages = 999
# Argument parser
parser = argparse.ArgumentParser("Download Moon Images and Create Video")
parser.add_argument("-t", "--thinning", default=1, help="Frequency of images to download, e.g. every 10th image")
parser.add_argument("-f", "--ffmpeg", action='store_true', help="Use ffmpeg to create video")
args = parser.parse_args()


def addZeros(imageNumber):
    """Add leading zeros to a number, up to 4 digits."""
    numAdd = 4 - len(str(imageNumber))
    return "0" * numAdd + str(imageNumber)

def getImage(imageNumber, directory):
    """Download an image given an image to an output directory"""
    URL = (
            "https://svs.gsfc.nasa.gov"
            "/vis/a000000/a004600/a004604/frames/"
            "850x850_1x1_30p/orbit.{}.tif"
            ).format(imageNumber)

    imageName = directory + imageNumber + ".tif"
    req.urlretrieve(URL, imageName)
    return

def makeVideo(directory, startNumber, thinning, ffmpeg=False):
    """Create a video with the downloaded images"""
    
    # Get a list of all the files 
    files = [image for image in os.listdir(directory) if ".tif" in image]
    

    # Create a video using ffmpeg command
    if ffmpeg:
        #frameRate = len(files)/60
        #frameRate = min(30,frameRate)
        frameRate = 10
        subprocess.run(
                ["ffmpeg",
                "-r", str(frameRate), 
                "-pattern_type", "glob",
                "-i", "./" + directory + "/*.tif",
                "-vf" , "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2", 
                "-vb", "50M", "moonorbit.mp4"], 
                check=True)
#                "-vf", "scale=1366:768:force_original_aspect_ratio=increase,pad=1366x768"], check=True)
    
    else:
        # Save each image frame to a list
        images = []
        for imageNumber in range(startNumber, totalImages, thinning):
            imageName = directory + addZeros(imageNumber) + ".tif"
            #print("imageName " + imageName);
            images.append(imageio.imread(imageName))

        imageio.mimsave('moon.gif', images)
    return

def main(startNumber=1, thinning=1, ffmpeg=False):
    
    directory = 'orbit/'

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for i, imageNumber in enumerate(range(startNumber, totalImages, thinning)):
        percent = round(imageNumber/totalImages*100)
        imageNumber = addZeros(imageNumber)
        
        # Skip if already downloaded
        if os.path.exists(directory + imageNumber + ".tif"):
            print("Already downloaded " + imageNumber)  
            continue
            
        while True:
            try:
                getImage(imageNumber, directory)
                
                # Create progress bar, we use 0.5*percentage
                # for a shorter bar
                bar = (
                        "["
                        + "#" * int(0.5 * percent)
                        + "-" * int(0.5 * (100 - percent))
                        + "]"
                )
                
                # Clear terminal
                print('\033c')

                # Print progress
                status = "Downloaded {}/{}, {}% ".format(i, totalImages//thinning, percent)
                print(status + bar)

            except Exception as e:
                print(e)
                continue
            break
            
    print("Making video...")
    makeVideo(directory, startNumber, thinning, ffmpeg)
    return


main(1, int(args.thinning), args.ffmpeg)


