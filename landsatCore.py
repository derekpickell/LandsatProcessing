import cv2 as cv
import glob
import sys, os
import numpy as np

# CORE LIBRARY: LANDSAT 8 TRUE COLOR IMAGE CONVERTER 
# V1.0 June 1 2020
# CREATED BY DEREK PICKELL

def getTrueColorLandsat(folder):
    """
    Functionality: Converts B&W satellite data into true color image
    Inputs: LANDSAT bands 2-4 and panchromatic band (band 8)
    Outputs: 'HSV sharpened' true color image
    """
    folder = str(folder[0])
    print("folder location:", folder)

    path4 = os.path.join(folder, "*4.TIF") 
    band4 = glob.glob(path4)
    path3 = os.path.join(folder, "*3.TIF")
    band3 = glob.glob(path3)
    path2 = os.path.join(folder, "*2.TIF")
    band2 = glob.glob(path2)
    pathP = os.path.join(folder, "*8.TIF")
    panchromatic = glob.glob(pathP)
    lists = [str(band4[0]), str(band3[0]), str(band2[0]), str(panchromatic[0])]

    # READ IMAGES
    blueImage = cv.imread(lists[0], -1) #-1 flag = "image as is"
    greenImage = cv.imread(lists[1], -1)
    redImage = cv.imread(lists[2], -1)
    panImage = np.array(cv.imread(lists[3],-1), dtype=np.float32)
    panImage /=655.35
    x = panImage.shape[0]
    y = panImage.shape[1]
    
    # IMAGE PROCESSING
    BGR = cv.merge((redImage, greenImage, blueImage)) # merge 3 channels, reads RGB but OpenCV operates in BGR
    BGRresized = cv.resize(BGR, (y, x), interpolation = cv.INTER_LINEAR) # interpolate image size bilinearly for 15m resolution
    img = np.array(BGRresized, dtype=np.float32)
    img /= 65535.0 # scale color image to 32 bit float

    labColor = cv.cvtColor(img, cv.COLOR_BGR2Lab) # convert to LAB color
    L,A,B=cv.split(labColor) # split into channels 
    labColorMerge = cv.merge((panImage, A, B)) # replace intensity channel with 15m band  
    mergedImage = cv.cvtColor(labColorMerge, cv.COLOR_Lab2BGR) # convert back to RGB  
    print("LAB max pixel intensity: ",np.amax(labColor)) # max pixel intensities should be about equal
    print("Sharpened LAB max pixel intensity:", np.amax(labColorMerge))

    return mergedImage


def colorCorrect(colorChannel):
    """
    Functionality: Adjusts Black point for RGB channels to better mirror "true color" 
        and make post-processing easier 
    Input: the merged RGB or LAB Image
    Output: White balanced and lightened image for easier final processing
    """
    histogram, bins = np.histogram(colorChannel.ravel(), 256,[0,1]) # create histogram scaled 0-255
    histogram = histogram[1:] # crop out pure black values
    maxVal = histogram.max() 
    threshold = 0.3*maxVal # threshold 1/3 of max value: all lower bins are cropped

    for i in range(0, len(histogram)):
        if histogram[i] > threshold:
            index = i 
            break

    minVal = index/256 # divide by 256 since float32 type; gives min pix val that isn't cropped
    print("crop index:", index)
    scaledMatrix = np.ravel(colorChannel) - minVal # shift all pixel values left
    croppedMatrix = np.clip(scaledMatrix, 0, None) # negative values floored to 0
    shape = colorChannel.shape
    shapedChannel = np.reshape(croppedMatrix, shape) # reshape to original form
    #plt.hist(newB.ravel(),256,[0,1]); plt.show()
    
    return shapedChannel


def convertToFinal(outputImage, folder):
    """
    Functionality: Gets name from metadata and outputs final image product
    Input: color corrected LAB image
    Output: RBG image
    """

    folder = str(folder[0])
    pathDate = os.path.join(folder, "*.txt") 
    dateTitle = glob.glob(pathDate)
    date = str(dateTitle[0]).split("_")
    title = date[0] + "_" + date[1] + "_" + date[2] + "_" + date[3] + "_" + 'OUTPUT.TIF' 
    path = os.path.join(folder, title) 
    cv.imwrite(path, outputImage) 

if __name__=="__main__":
    application_path = os.path.dirname(os.path.abspath(__file__))
    folder = [application_path]
    try:
        print("merging images...")
        print(application_path)
        mergedImage = getTrueColorLandsat(folder)
        print("color correcting...")
        B, G, R = cv.split(mergedImage)
        Bnew = colorCorrect(B)
        Gnew = colorCorrect(G)
        Rnew = colorCorrect(R)
        colorCorrected = cv.merge((Bnew, Gnew, Rnew))
        print("saving image...")
        convertToFinal(colorCorrected, folder)
        print("processing complete")
        
    except:
        print("failure to launch")