import numpy as np
import cv2 as cv
import glob
import imutils
import matplotlib.pyplot as plt
import os
from skimage import io
from skimage.morphology import thin, skeletonize
from skimage.util import invert


lower_green = np.array([36, 50, 70])
upper_green = np.array([89, 255, 255])
indexs = []

############################################################ DENOISING ############################################################
def denoisingImage(image_list):
  global indexs
  indexs.clear()
  deNoizedImage_with_border = []
  for image in image_list:
    segment_image = cv.imread(image)
    indexs.append(os.path.basename(image.split('.')[0]))
    print("image name",os.path.basename(image.split('.')[0]))
    deNoizedImage = cv.fastNlMeansDenoisingColored(segment_image,None,10,10,7,21)
    deNoizedImage_with_border.append(cv.copyMakeBorder(deNoizedImage,1,1,1,1,cv.BORDER_CONSTANT,value=[255,255,255]))
  return (deNoizedImage_with_border)
######################################################################################################################################

############################################################ Clustering ##################################################################
def clustering_image(denoised):
  clustered_images = []
  for d_image in denoised:
    image = d_image
    h, w, c = image.shape
    image_2d = image.reshape(h*w, c).astype(np.float32)

    numcolors = 3
    numiters = 10
    epsilon = 2
    attempts = 10

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, numiters, epsilon)
    ret, labels, centers = cv.kmeans(image_2d, numcolors, None, criteria, attempts, cv.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    newimage = centers[labels.flatten()]
    clustered_image = newimage.reshape(image.shape)
    clustered_images.append(clustered_image)
  #cv.imwrite("drive/MyDrive/Project Dataset/Clustered/{0}_clustered.png".format(index), clustered_image)
  #cv.imwrite("drive/MyDrive/Project Dataset/Result-without deNoizing/Clustered/{0}_clustered.png".format(index), clustered_image)
  #plt.imshow(clustered_image)
  return (clustered_images)
##############################################################################################################################################


####################################################### EXTRACT DAMAGED BOUNDARIES ######################################################
def extract_damage_boundaries(clustered_images):
  global lower_green,upper_green
  log_array = []
  with_contours_list = []

  for clustered_image in clustered_images:
    log_text = ""
    hsv_image = cv.cvtColor(clustered_image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_image, lower_green, upper_green)
    #plt.imshow(mask)
    count = np.sum(np.nonzero(mask))
    if count==0:
      print("No damaged Area")
      log_text = log_text + ">>> Segment has No Damaged Area\n"
    else:
      print("Has damaged Area")
      log_text = log_text + ">>> Segment has Damaged Area\n"
    damaged_area = cv.bitwise_and(clustered_image, clustered_image, mask=mask)
    #plt.imshow(damaged_area)
    gray_image = cv.cvtColor(damaged_area, cv.COLOR_BGR2GRAY)
    #plt.imshow(gray_image)
    et, binary = cv.threshold(gray_image, 100, 255, cv.THRESH_OTSU)
    inverted_binary_image = ~binary
    ib1 = inverted_binary_image.copy();
    #plt.imshow(binary)
    contours, hierarchy = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    clustered_image_gray = cv.cvtColor(clustered_image, cv.COLOR_BGR2GRAY)
    ret, binary_map = cv.threshold(clustered_image_gray,127,255,0)
    character_area = cv.cvtColor(binary_map, cv.COLOR_GRAY2BGR)
    #plt.imshow(character_area)
    with_contours = cv.drawContours(character_area, contours, -1,(255,0,255),1)
    #plt.imshow(with_contours)
    #cv.imwrite("drive/MyDrive/Project Dataset/Boundaries/{0}_damaged boundaries.png".format(index),with_contours)
    #cv.imwrite("drive/MyDrive/Project Dataset/Result-without deNoizing/Boundaries/{0}_damaged boundaries.png".format(index),with_contours)
    with_contours_list.append(with_contours)
    log_array.append(log_text)
  return (with_contours_list,log_array)
#################################################################################################

#edge_pixels = [] 
def mask3(y,x,with_contours,edge_pixels):
  
  #edge_pixels.clear()
  #availability = False
  mask3 = ([y-1,x-1],[y-1,x],[y-1,x+1],[y,x-1],[y,x+1],[y+1,x-1],[y+1,x],[y+1,x+1])
  for m in mask3:
    if(with_contours[m[0],m[1]][0] == 255 and with_contours[m[0],m[1]][1] == 0 and with_contours[m[0],m[1]][2] == 255 and m[0] >= 0 and m[0] < with_contours.shape[0] and m[1] >= 0 and with_contours.shape[1]):
      #availability = True
      with_contours[y,x] = [0,255,0]
      edge_pixels.append([y,x])
      # cv.line(test_image, (x,y), (m[1],m[0]), [255, 0, 0], 1)
  return(with_contours,edge_pixels)
######################################################################################################################################################################################


####################################################################### FIND DAMAGE EDGES ######################################################################
def find_damaged_edges(with_contours_list):
  global indexs
  index = 0
  log_array = []
  
  with_damaged_edges = []
  for with_contours in with_contours_list:
    edge_pixels = []
    log_text = ""
    foreground_pixels = []
    for row in range(with_contours.shape[0]):
      for col in range(with_contours.shape[1]):
        if(with_contours[row,col][0] == 0 and with_contours[row,col][1] == 0 and with_contours[row,col][2] == 0):
          foreground_pixels.append([row,col])
    print(foreground_pixels)
    for edge in foreground_pixels:
      res1 = mask3(edge[0], edge[1],with_contours,edge_pixels)
      
    print("edge pixels ",edge_pixels)
    if not edge_pixels:
      log_text = log_text + ">>> Character has No Damaged Edges\n"
    else:
      log_text = log_text + ">>> Character has Damaged Edges\n"
    result_image = with_contours.copy()
    for row in range(0,result_image.shape[0]):
      for col in range(0,result_image.shape[1]):
        if(with_contours[row][col][0] == 255 and with_contours[row][col][1] == 0 and with_contours[row][col][2] == 255):
          result_image[row][col][0] = 255
          result_image[row][col][1] = 255
          result_image[row][col][2] = 255
    cv.imwrite("M2_data/Result/"+indexs[index]+"_result.png",result_image)
    with_damaged_edges.append(result_image)
    log_array.append(log_text)
    index = index + 1
  return (with_damaged_edges,log_array)

########################################### Thinning utility func #################################################################################################
def otzu_after_gaussian(img):
  blur = cv.GaussianBlur(img,(5,5),0)
  ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
  return th3


def BinaryTORGB(img):
  image = invert(img)
  return image


def close(points, new_point):
  points = [i for i in points]
  closest_point = None
  closest_distance = None
  for point in points:
    distance = ((point[0] - new_point[0])**2 + (point[1] - new_point[1])**2)**0.5
    if closest_distance is None or distance < closest_distance:
      closest_point = point
      closest_distance = distance
  return (closest_point)



def mask_for_thinning(y,x,test_image):
  count = 0
  pixel = None
  mask3 = ([y-1,x-1],[y-1,x],[y-1,x+1],[y,x-1],[y,x+1],[y+1,x-1],[y+1,x],[y+1,x+1])
  for m in mask3:
    if((test_image[m[0],m[1]][0] == 0 and test_image[m[0],m[1]][1] == 255 and test_image[m[0],m[1]][2] == 0) or (test_image[m[0],m[1]][0] == 255 and test_image[m[0],m[1]][1] == 0 and test_image[m[0],m[1]][2] == 0) and m[0] >= 0 and m[0] < test_image.shape[0] and m[1] >= 0 and test_image.shape[1]):
      count = count + 1
      pixel = m
  return ([count,pixel]);


########################################################################################################################################################################################################


############################################################################### FIND END TIPS ####################################################################
def thinning_result(with_damaged_edges):
  global indexs
  log_array = []
  thininng_result_list = []
  index = 0
  for damged_edges_image in with_damaged_edges:
    log_text = ""
    foregrond_pixels = []
    corner_end_tips = []
    damaged_point_pixels = []
    response = []
    is_damaged = False
    img = damged_edges_image
    image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    for row in range(img.shape[0]):
      for col in range(img.shape[1]):
        if(img[row,col][0] == 0 and img[row,col][1] == 255 and img[row,col][2] == 0):
          damaged_point_pixels.append([row,col])
    otzu = otzu_after_gaussian(image)
    binary = BinaryTORGB(otzu)
    c = binary / 255
    skeletonizedImage = thin(c)
    blank_image = np.zeros((skeletonizedImage.shape[0],skeletonizedImage.shape[1],3), np.uint8)
    for row in range(skeletonizedImage.shape[0]):
      for col in range(skeletonizedImage.shape[1]):
        if(skeletonizedImage[row,col] == True):
          foregrond_pixels.append([row,col])
          blank_image[row,col] = [0,255,0]
    test_image = blank_image.copy()
    for a in damaged_point_pixels:
      res = close(foregrond_pixels,a)
      if res not in response:
        response.append(res)
        test_image[res[0],res[1]] = [255,0,0]
    for i in response:
      out = mask_for_thinning(i[0], i[1], test_image)[0]
      if(out > 1):
        test_image[i[0],i[1]] = [0,255,0]
      if(out == 1):
        p = mask_for_thinning(i[0], i[1], test_image)[1]
        test_image[i[0],i[1]] = [0,0,0]
        test_image[p[0],p[1]] = [255,0,0]
        is_damaged = True

    if is_damaged:
      log_text = log_text + ">>> Character is exactly a Damaged character\n"
    else:
      log_text = log_text + ">>> Character is exactly not a Damaged character\n"
    #damage_presentage(test_image)
    thininng_result_list.append(test_image)
    log_array.append(log_text)
    cv.imwrite("M2_data/Thinned Result/"+indexs[index]+"_Thinned_Result.png",test_image)
    index = index+1
  return (thininng_result_list,log_array)
###################################################################################################################################################################

def display_out(files):
  rgb_converted = []
  for file in files:
    blue,green,red = cv.split(file)
    img = cv.merge((red,green,blue))
    print(img)
    rgb_converted.append(img)
  return rgb_converted
