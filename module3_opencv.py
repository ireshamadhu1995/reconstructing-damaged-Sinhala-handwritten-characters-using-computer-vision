## EDITED

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import os
import csv
import glob
from csv import writer
import base64
import pathlib
import imutils
from PIL import Image
from skimage.morphology import thin, skeletonize
from skimage.util import invert
from colorama import init
from termcolor import colored
import math
from skimage import util

################################### find Suitable EndTip Couples (Utility)#################################
def findDamages(img):
  ends = []
  for row in range(img.shape[0]):
    for col in range(img.shape[1]):
      if((img[row,col][0] == 0 and img[row,col][1] == 0 and img[row,col][2] == 255) or (img[row,col][0] == 255 and img[row,col][1] == 0 and img[row,col][2] == 0)):
        ends.append([row,col])
  return ends

def getForegroundPixels(img):
  foregrond_pixels = []
  for row in range(img.shape[0]):
    for col in range(img.shape[1]):
      if((img[row,col][0] == 0 and img[row,col][1] == 0 and img[row,col][2] == 255) or (img[row,col][0] == 0 and img[row,col][1] == 255 and img[row,col][2] == 0)):
        foregrond_pixels.append([row,col])
  return foregrond_pixels


def calc_distance(p1, p2):
  return round(np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)) # Pythagorean theorem


def calc_damage_percentage(miss_pixels,fore_pixels):
  return round(miss_pixels/(miss_pixels+fore_pixels)*100)


def decideposneg(end,img):
  if(img[end[0]-1,end[1]-1][0] == 0 and img[end[0]-1,end[1]-1][1] == 255 and img[end[0]-1,end[1]-1][2] == 0):
    # return ([0,0])#opposite shape
    return ([[1,0],[0,1],[1,1]])
  
  elif(img[end[0]-1,end[1]][0] == 0 and img[end[0]-1,end[1]][1] == 255 and img[end[0]-1,end[1]][2] == 0):
    # return ([0,0])
    return ([[1,0],[0,1],[1,1]])

  elif(img[end[0]-1,end[1]+1][0] == 0 and img[end[0]-1,end[1]+1][1] == 255 and img[end[0]-1,end[1]+1][2] == 0):
    # return ([0,1])
    return ([[1,0],[0,0],[1,1]])

  elif(img[end[0],end[1]-1][0] == 0 and img[end[0],end[1]-1][1] == 255 and img[end[0],end[1]-1][2] == 0):
    # return ([0,0])
    return ([[1,0],[0,1],[1,1]])

  elif(img[end[0],end[1]+1][0] == 0 and img[end[0],end[1]+1][1] == 255 and img[end[0],end[1]+1][2] == 0):
    # return ([0,1])
    return ([[1,0],[1,1],[0,0]])

  elif(img[end[0]+1,end[1]-1][0] == 0 and img[end[0]+1,end[1]-1][1] == 255 and img[end[0]+1,end[1]-1][2] == 0):
    # return ([1,0])
    return ([[1,1],[0,1],[0,0]])

  elif(img[end[0]+1,end[1]][0] == 0 and img[end[0]+1,end[1]][1] == 255 and img[end[0]+1,end[1]][2] == 0):
    # return ([1,0])
     return ([[1,1],[0,1],[0,0]])

  elif(img[end[0]+1,end[1]+1][0] == 0 and img[end[0]+1,end[1]+1][1] == 255 and img[end[0]+1,end[1]+1][2] == 0):
    # return ([1,1])
     return ([[0,0],[0,1],[1,0]])


def decideposneg2(p,end,img):
  if((end[0]-p[0] > 0) and (end[1]-p[1] > 0)):
    return ({'point': end, 'pattern':[1,1]})

  if((end[0]-p[0] > 0) and (end[1]-p[1] < 1)):
    return ({'point': end, 'pattern':[1,0]})

  if((end[0]-p[0] < 1) and (end[1]-p[1] > 0)):
    return ({'point': end, 'pattern':[0,1]})

  if((end[0]-p[0] < 1) and (end[1]-p[1] < 1)):
    return ({'point': end, 'pattern':[0,0]})




def findDistance(image,damaged_pixels,p):
  distance_array = []
  closest_point = None
  closest_distance = None
  points = [i for i in damaged_pixels if i != p]
  for point in points:
    distance = ((point[0] - p[0])**2 + (point[1] - p[1])**2)**0.5
    distance_array.append({'point': point, 'distance':distance})
  return distance_array
  


def inverse(i):
  if(i[0] == 1):
    i[0] = 0
  else:
    i[0] = 1
  if(i[1] == 1):
    i[1] = 0
  else:
    i[1] = 1
  return([i[0],i[1]])

def directionMapping(end,img,b):
  if(img[end[0]-1,end[1]-1][0] == 0 and img[end[0]-1,end[1]-1][1] == 255 and img[end[0]-1,end[1]-1][2] == 0):
    if(b == False):
      return 1
    else:
      return ({'point': end, 'direction':1})
  elif(img[end[0]-1,end[1]][0] == 0 and img[end[0]-1,end[1]][1] == 255 and img[end[0]-1,end[1]][2] == 0):
    if(b == False):
      return 2
    else:
      return ({'point': end, 'direction':2})

  elif(img[end[0]-1,end[1]+1][0] == 0 and img[end[0]-1,end[1]+1][1] == 255 and img[end[0]-1,end[1]+1][2] == 0):
    if(b == False):
      return 3
    else:
      return ({'point': end, 'direction':3})

  elif(img[end[0],end[1]-1][0] == 0 and img[end[0],end[1]-1][1] == 255 and img[end[0],end[1]-1][2] == 0):
    if(b == False):
      return 4
    else:
      return ({'point': end, 'direction':4})

  elif(img[end[0],end[1]+1][0] == 0 and img[end[0],end[1]+1][1] == 255 and img[end[0],end[1]+1][2] == 0):
    if(b == False):
      return 5
    else:
      return ({'point': end, 'direction':5})

  elif(img[end[0]+1,end[1]-1][0] == 0 and img[end[0]+1,end[1]-1][1] == 255 and img[end[0]+1,end[1]-1][2] == 0):
    if(b == False):
      return 6
    else:
      return ({'point': end, 'direction':6})

  elif(img[end[0]+1,end[1]][0] == 0 and img[end[0]+1,end[1]][1] == 255 and img[end[0]+1,end[1]][2] == 0):
    if(b == False):
      return 7
    else:
      return ({'point': end, 'direction':7})

  elif(img[end[0]+1,end[1]+1][0] == 0 and img[end[0]+1,end[1]+1][1] == 255 and img[end[0]+1,end[1]+1][2] == 0):
    if(b == False):
      return 8
    else:
      return ({'point': end, 'direction':8})


def positiveNegative(image,damaged_pixels,p):
  pos_neg_array = []
  points = [i for i in damaged_pixels if i != p]
  considered_pattern_array = decideposneg(p,image)
  # considered_pattern_inverse = inverse(considered_pattern)
  for point in points:
    res = decideposneg2(p,point,image)
    pos_neg_array.append(res)
  return (considered_pattern_array,pos_neg_array)
  


def findDirection(image,damaged_pixels,p):
  direction_array = []
  points = [i for i in damaged_pixels if i != p]
  considered_direction = directionMapping(p,image,False)
  for point in points:
    res = directionMapping(point,image,True)
    direction_array.append(res)
  return (considered_direction,direction_array)



def findMatchingCouple(distance_array,positive_negative_data,direction_data,ratio,max_ratio):
  min_dis_obj = min(distance_array, key=lambda x: x['distance'])
  if(min_dis_obj['distance'] <= ratio):
    return min_dis_obj['point']
  else:
    min_dis_pos_neg = [item for item in positive_negative_data[1] if item.get('point')==min_dis_obj['point']]
    min_dis_pos_neg_direction = [item for item in direction_data[1] if item.get('point')==min_dis_pos_neg[0]['point']]
    if(min_dis_pos_neg[0]['pattern'] in positive_negative_data[0]):
      if(direction_data[0] != min_dis_pos_neg_direction[0]['direction']):
        return min_dis_obj['point']
      else:
        remain = [item for item in distance_array if item['point'] != min_dis_obj['point']]
        if(len(remain) == 0):
          return None
        return findMatchingCouple(remain,positive_negative_data,direction_data,ratio,max_ratio)
    else:
      remain = [item for item in distance_array if item['point'] != min_dis_obj['point']]
      if(len(remain) == 0):
        return None
    return findMatchingCouple(remain,positive_negative_data,direction_data,ratio,max_ratio)

###################################################################################################################




################################### find Suitable EndTip Couples ##############################################
def final_suitable_mapping(images):
  output = []
  couples_list = []
  damage_presentage = []
  logs = []
  for img in images:
    image = cv.imread(img)
    damaged_pixels = findDamages(image)
    forground_pixes = getForegroundPixels(image)
    resolved_pixels = []
    not_resolved = []
    couples = []
    dp = 0
    r_val = round(math.sqrt(image.shape[0] ** 2 + image.shape[1] ** 2))
    ratio = r_val/100*12.5
    max_ratio = r_val/100*28
    img_copy = image.copy()
    if(len(damaged_pixels) == 0):
      print("cannot reconstruct thre are no any damaged end tips")
    elif(len(damaged_pixels) == 1):
      print("cannot reconstruct there is only one damaged end tip")
    elif(len(damaged_pixels) == 2):
      print("has only two damaged end tips")
      first_point = damaged_pixels[0]
      second_point = damaged_pixels[1]
      couples.append([first_point,second_point])
      distance = calc_distance(first_point, second_point)
      dp = calc_damage_percentage(distance,len(forground_pixes))
      print("damaged_percentage",dp)
      cv.line(img_copy, (damaged_pixels[0][1],damaged_pixels[0][0]), (damaged_pixels[1][1], damaged_pixels[1][0]), [255, 0, 0], 1)
    else:
      print("has multiple damaged end tips")
      for i in damaged_pixels:
        if i not in resolved_pixels:
          list_difference1 = [item for item in damaged_pixels if item not in resolved_pixels]
          if(len(list_difference1) == 1):
            not_resolved.append(list_difference1[0])
          if(len(not_resolved) != 1):
            distance_array = findDistance(image, list_difference1, i)
            positive_negative_data  = positiveNegative(image, list_difference1, i)
            direction_data  = findDirection(image, list_difference1, i)
            result = findMatchingCouple(distance_array,positive_negative_data,direction_data,ratio,max_ratio)
            if(result != None):
              couples.append([i,result])
              resolved_pixels.append(i)
              resolved_pixels.append(result)
              distance = calc_distance(i, result)
              damaged_percentage = calc_damage_percentage(distance,len(forground_pixes))
              # print("damaged_percentage",damaged_percentage)
              dp = dp +damaged_percentage
              cv.line(img_copy, (i[1],i[0]), (result[1], result[0]), [255, 0, 0], 1)
            if((result == None)):
              not_resolved.append(i)
      list_difference2 = [item for item in not_resolved if item not in resolved_pixels]
      if(len(list_difference2) == 2):
        couples.append([list_difference2[0],list_difference2[1]])
        distance = calc_distance(list_difference2[0], list_difference2[1])
        damaged_percentage = calc_damage_percentage(distance,len(forground_pixes))
        # print("damaged_percentage",damaged_percentage)
        dp = dp+damaged_percentage
        resolved_pixels.append(list_difference2[0])
        resolved_pixels.append(list_difference2[1])
        cv.line(img_copy, (list_difference2[0][1],list_difference2[0][0]), (list_difference2[1][1], list_difference2[1][0]), [255, 0, 0], 1)
    text = ""
    for couple in couples:
      text = text + str(couple)
    output.append(img_copy)
    couples_list.append(">> " + text + "\n")
    damage_presentage.append(dp)
    logs.append(">> " + text + "\n" + ">> Damage Presentage: " + str(dp) + "%\n\n")
  return (output,logs)

#methana suitable couples = couples_list print wenna one
#methana total damage percentage = dp

##################################################################################################################

########################################### Linkling (Utilities) ############################################################
def findDamages_linking(img):
  ends = []
  for row in range(img.shape[0]):
    for col in range(img.shape[1]):
      if((img[row,col][0] == 0 and img[row,col][1] == 0 and img[row,col][2] == 255) or (img[row,col][0] == 255 and img[row,col][1] == 0 and img[row,col][2] == 0)):
        ends.append([row,col])
  return ends

def getForegroundPixels_linking(img):
  foregrond_pixels = []
  for row in range(img.shape[0]):
    for col in range(img.shape[1]):
      if((img[row,col][0] == 0 and img[row,col][1] == 0 and img[row,col][2] == 255) or (img[row,col][0] == 0 and img[row,col][1] == 255 and img[row,col][2] == 0)):
        foregrond_pixels.append([row,col])
  return foregrond_pixels


def calc_distance_linking(p1, p2):
  return round(np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))


def calc_damage_percentage_linking(miss_pixels,fore_pixels):
  return round(miss_pixels/(miss_pixels+fore_pixels)*100)


def decideposneg_linking(end,img):
  if(img[end[0]-1,end[1]-1][0] == 0 and img[end[0]-1,end[1]-1][1] == 255 and img[end[0]-1,end[1]-1][2] == 0):
    # return ([0,0])#opposite shape
    return ([[1,0],[0,1],[1,1]])
  
  elif(img[end[0]-1,end[1]][0] == 0 and img[end[0]-1,end[1]][1] == 255 and img[end[0]-1,end[1]][2] == 0):
    # return ([0,0])
    return ([[1,0],[0,1],[1,1]])

  elif(img[end[0]-1,end[1]+1][0] == 0 and img[end[0]-1,end[1]+1][1] == 255 and img[end[0]-1,end[1]+1][2] == 0):
    # return ([0,1])
    return ([[1,0],[0,0],[1,1]])

  elif(img[end[0],end[1]-1][0] == 0 and img[end[0],end[1]-1][1] == 255 and img[end[0],end[1]-1][2] == 0):
    # return ([0,0])
    return ([[1,0],[0,1],[1,1]])

  elif(img[end[0],end[1]+1][0] == 0 and img[end[0],end[1]+1][1] == 255 and img[end[0],end[1]+1][2] == 0):
    # return ([0,1])
    return ([[1,0],[1,1],[0,0]])

  elif(img[end[0]+1,end[1]-1][0] == 0 and img[end[0]+1,end[1]-1][1] == 255 and img[end[0]+1,end[1]-1][2] == 0):
    # return ([1,0])
    return ([[1,1],[0,1],[0,0]])

  elif(img[end[0]+1,end[1]][0] == 0 and img[end[0]+1,end[1]][1] == 255 and img[end[0]+1,end[1]][2] == 0):
    # return ([1,0])
     return ([[1,1],[0,1],[0,0]])

  elif(img[end[0]+1,end[1]+1][0] == 0 and img[end[0]+1,end[1]+1][1] == 255 and img[end[0]+1,end[1]+1][2] == 0):
    # return ([1,1])
     return ([[0,0],[0,1],[1,0]])


def decideposneg2_linking(p,end,img):
  if((end[0]-p[0] > 0) and (end[1]-p[1] > 0)):
    return ({'point': end, 'pattern':[1,1]})

  if((end[0]-p[0] > 0) and (end[1]-p[1] < 1)):
    return ({'point': end, 'pattern':[1,0]})

  if((end[0]-p[0] < 1) and (end[1]-p[1] > 0)):
    return ({'point': end, 'pattern':[0,1]})

  if((end[0]-p[0] < 1) and (end[1]-p[1] < 1)):
    return ({'point': end, 'pattern':[0,0]})




def findDistance_linking(image,damaged_pixels,p):
  distance_array = []
  closest_point = None
  closest_distance = None
  points = [i for i in damaged_pixels if i != p]
  for point in points:
    distance = ((point[0] - p[0])**2 + (point[1] - p[1])**2)**0.5
    distance_array.append({'point': point, 'distance':distance})
  return distance_array
  


def inverse_linking(i):
  if(i[0] == 1):
    i[0] = 0
  else:
    i[0] = 1
  if(i[1] == 1):
    i[1] = 0
  else:
    i[1] = 1
  return([i[0],i[1]])

def directionMapping_linking(end,img,b):
  if(img[end[0]-1,end[1]-1][0] == 0 and img[end[0]-1,end[1]-1][1] == 255 and img[end[0]-1,end[1]-1][2] == 0):
    if(b == False):
      return 1
    else:
      return ({'point': end, 'direction':1})
  elif(img[end[0]-1,end[1]][0] == 0 and img[end[0]-1,end[1]][1] == 255 and img[end[0]-1,end[1]][2] == 0):
    if(b == False):
      return 2
    else:
      return ({'point': end, 'direction':2})

  elif(img[end[0]-1,end[1]+1][0] == 0 and img[end[0]-1,end[1]+1][1] == 255 and img[end[0]-1,end[1]+1][2] == 0):
    if(b == False):
      return 3
    else:
      return ({'point': end, 'direction':3})

  elif(img[end[0],end[1]-1][0] == 0 and img[end[0],end[1]-1][1] == 255 and img[end[0],end[1]-1][2] == 0):
    if(b == False):
      return 4
    else:
      return ({'point': end, 'direction':4})

  elif(img[end[0],end[1]+1][0] == 0 and img[end[0],end[1]+1][1] == 255 and img[end[0],end[1]+1][2] == 0):
    if(b == False):
      return 5
    else:
      return ({'point': end, 'direction':5})

  elif(img[end[0]+1,end[1]-1][0] == 0 and img[end[0]+1,end[1]-1][1] == 255 and img[end[0]+1,end[1]-1][2] == 0):
    if(b == False):
      return 6
    else:
      return ({'point': end, 'direction':6})

  elif(img[end[0]+1,end[1]][0] == 0 and img[end[0]+1,end[1]][1] == 255 and img[end[0]+1,end[1]][2] == 0):
    if(b == False):
      return 7
    else:
      return ({'point': end, 'direction':7})

  elif(img[end[0]+1,end[1]+1][0] == 0 and img[end[0]+1,end[1]+1][1] == 255 and img[end[0]+1,end[1]+1][2] == 0):
    if(b == False):
      return 8
    else:
      return ({'point': end, 'direction':8})


def positiveNegative_linking(image,damaged_pixels,p):
  pos_neg_array = []
  points = [i for i in damaged_pixels if i != p]
  considered_pattern_array = decideposneg_linking(p,image)
  # considered_pattern_inverse = inverse(considered_pattern)
  for point in points:
    res = decideposneg2_linking(p,point,image)
    pos_neg_array.append(res)
  return (considered_pattern_array,pos_neg_array)
  


def findDirection_linking(image,damaged_pixels,p):
  direction_array = []
  points = [i for i in damaged_pixels if i != p]
  considered_direction = directionMapping_linking(p,image,False)
  for point in points:
    res = directionMapping_linking(point,image,True)
    direction_array.append(res)
  return (considered_direction,direction_array)



def findMatchingCouple_linking(distance_array,positive_negative_data,direction_data,ratio,max_ratio):
  min_dis_obj = min(distance_array, key=lambda x: x['distance'])
  if(min_dis_obj['distance'] <= ratio):
    return min_dis_obj['point']
  else:
    min_dis_pos_neg = [item for item in positive_negative_data[1] if item.get('point')==min_dis_obj['point']]
    min_dis_pos_neg_direction = [item for item in direction_data[1] if item.get('point')==min_dis_pos_neg[0]['point']]
    if(min_dis_pos_neg[0]['pattern'] in positive_negative_data[0]):
      if(direction_data[0] != min_dis_pos_neg_direction[0]['direction']):
        return min_dis_obj['point']
      else:
        remain = [item for item in distance_array if item['point'] != min_dis_obj['point']]
        if(len(remain) == 0):
          return None
        return findMatchingCouple_linking(remain,positive_negative_data,direction_data,ratio,max_ratio)
    else:
      remain = [item for item in distance_array if item['point'] != min_dis_obj['point']]
      if(len(remain) == 0):
        return None
    return findMatchingCouple_linking(remain,positive_negative_data,direction_data,ratio,max_ratio)

def plotPoints_linking(img,damageded_couple):
  for i in range(len(damageded_couple)):
    plt.text(damageded_couple[i][1], damageded_couple[i][0], 'P' + str(i), color='r')
  return(img)

def midpoint_linking(y1, y2, x1, x2):
  return(((y1 + y2) // 2), ((x1 + x2) // 2))

def line_intersection_linking(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    if((x < 0) or (y <0)):
      out = midpoint_linking(line1[1][0],line2[1][0], line1[1][1],line2[1][1])
      x = out[0]
      y = out[1]


    return x, y


def findmc_linking(p1,p2):
  p1_y = p1[0]
  p1_x = p1[1]
  p2_y = p2[0]
  p2_x = p2[1]
  m = (p2_y-p1_y)/(p2_x-p1_x)
  c = p2_y-(m*p2_x)
  return [m,c]






def PointTest_linking(img, X_coord, Y_coord):
  for i in range(len(X_coord)):
    plt.text(X_coord[i], Y_coord[i], 'P' + str(i), color='r')  
  return img



def BezierPoint_linking(img, X_coord, Y_coord, xFinal, yFinal):
    for i in range(len(X_coord)):
      plt.text(X_coord[i], Y_coord[i], 'P' + str(i), color='r')
    for i in range(len(xFinal)):
      plt.plot(xFinal[i],yFinal[i],'*')
    return img


def getValue_linking(x1,x2,t):
    return x1+(x2-x1)*t

def Draw_linking_linking(X_coord,Y_coord,num, xFinal, yFinal, cnt,i):
  if num==3:
    x0 = getValue_linking(X_coord[0], X_coord[1], i / cnt)
    y0 = getValue_linking(Y_coord[0], Y_coord[1], i / cnt)
    x1 = getValue_linking(X_coord[1], X_coord[2], i / cnt)
    y1 = getValue_linking(Y_coord[1], Y_coord[2], i / cnt)

    xFinal.append(getValue_linking(x0, x1, i / cnt))
    yFinal.append(getValue_linking(y0, y1, i / cnt))
  return(xFinal, yFinal)
    
def findnewIntersect(original,intersect_point):
  if((intersect_point[0] < original.shape[0] and intersect_point[0] > 0) and (intersect_point[1] < original.shape[1] and intersect_point[1] > 0)):
    return(intersect_point)
  else:
    new_intersect_y = 0
    new_intersect_x = 0
    if(intersect_point[0] <= original.shape[0]-1 and intersect_point[0] >= 0):
      new_intersect_y = intersect_point[0]
    if(intersect_point[1] <= original.shape[1]-1 and intersect_point[1] >= 0):
      new_intersect_x = intersect_point[1]
    if(intersect_point[0] >= original.shape[0]):
      new_intersect_y = original.shape[0]-1
    if(intersect_point[1] >= original.shape[1]):
      new_intersect_x = original.shape[1]-1
    if(intersect_point[0] < 0):
      new_intersect_y = 0
    if(intersect_point[1] < 0):
      new_intersect_x = 0
    intersect_point = [new_intersect_y,new_intersect_x]
    return(intersect_point)



#to do
#bezier curve 8 curve patterns
def findPattern_linking(img, points):
  control_points = []
  pattern = []
  if(points):
    for end in points:
      if(end[0] == img.shape[0]-1 or end[1] == img.shape[1]-1):
        return img

      else:
        if(img[end[0]-1,end[1]-1][0] == 0 and img[end[0]-1,end[1]-1][1] == 255 and img[end[0]-1,end[1]-1][2] == 0):
          line = []
          line.append(end)
          c1 = end[0]-1,end[1]-1
          c2 = end
          m = findmc_linking(c1,c2)[0]
          c = findmc_linking(c1,c2)[1]
          intercept_x_axis = ((img.shape[0]-1)-c)/m
          if((intercept_x_axis > img.shape[1]-1)):
            intercept_y_axis = ((img.shape[1]-1)*m)+c
            if((intercept_y_axis < img.shape[0]-1) and (intercept_y_axis >= 0)):
              line.append([intercept_y_axis,img.shape[1]-1])
            else:
              return img
          else:
            line.append([img.shape[0]-1,intercept_x_axis])
          control_points.append(line)
          pattern.append(1)

        elif(img[end[0]-1,end[1]][0] == 0 and img[end[0]-1,end[1]][1] == 255 and img[end[0]-1,end[1]][2] == 0):
          line = []
          line.append(end)
          line.append([img.shape[0]-1,end[1]])
          control_points.append(line)
          pattern.append(2)
      
        elif(img[end[0]-1,end[1]+1][0] == 0 and img[end[0]-1,end[1]+1][1] == 255 and img[end[0]-1,end[1]+1][2] == 0):
          line = []
          line.append(end)
          c1 = end[0]-1,end[1]+1
          c2 = end
          m = findmc_linking(c1,c2)[0]
          c = findmc_linking(c1,c2)[1]
          intercept_x_axis = ((img.shape[0]-1)-c)/m
          if((intercept_x_axis > img.shape[0]-1)):
            intercept_y_axis = c
            if((intercept_y_axis < img.shape[0]-1) and (intercept_y_axis >= 0)):
              line.append([c,0])
            else:
              return img
          else:
            line.append([(img.shape[0]-1),((img.shape[0]-1)-c)/m])
          control_points.append(line)
          pattern.append(3)

        elif(img[end[0],end[1]-1][0] == 0 and img[end[0],end[1]-1][1] == 255 and img[end[0],end[1]-1][2] == 0):
          line = []
          line.append(end)
          line.append([end[0],img.shape[1]])
          control_points.append(line)
          pattern.append(4)

        elif(img[end[0],end[1]+1][0] == 0 and img[end[0],end[1]+1][1] == 255 and img[end[0],end[1]+1][2] == 0):
          line = []
          line.append(end)
          line.append([end[0],0])
          control_points.append(line)
          pattern.append(5)
      
        elif(img[end[0]+1,end[1]-1][0] == 0 and img[end[0]+1,end[1]-1][1] == 255 and img[end[0]+1,end[1]-1][2] == 0):
          line = []
          line.append(end)
          c1 = end[0]+1,end[1]-1
          c2 = end
          m = findmc_linking(c1,c2)[0]
          c = findmc_linking(c1,c2)[1]
          intercept_x_axis = -c/m
          if((intercept_x_axis > img.shape[1]-1)):
            intercept_y_axis = m*(img.shape[1]-1)+c
            if((intercept_y_axis < img.shape[0]-1) and (intercept_y_axis >= 0)):
              line.append([round(m*(img.shape[1]-1)+c),img.shape[1]-1])
            else:
              return img
          else:
            line.append([0,round(-c/m)])
          control_points.append(line)
          pattern.append(6)
      
        elif(img[end[0]+1,end[1]][0] == 0 and img[end[0]+1,end[1]][1] == 255 and img[end[0]+1,end[1]][2] == 0):
          line = []
          line.append(end)
          line.append([img.shape[0],end[1]])
          control_points.append(line)
          pattern.append(7)
      
        elif(img[end[0]+1,end[1]+1][0] == 0 and img[end[0]+1,end[1]+1][1] == 255 and img[end[0]+1,end[1]+1][2] == 0):
          line = []
          line.append(end)
          c1 = end[0]+1,end[1]+1
          c2 = end
          m = findmc_linking(c1,c2)[0]
          c = findmc_linking(c1,c2)[1]
          intercept_x_axis = (img.shape[0]-1)-c
          if((intercept_x_axis < img.shape[0]-1)):
            intercept_y_axis = c/m
            if((intercept_y_axis < img.shape[0]-1) and (intercept_y_axis >= 0)):
              line.append([intercept_y_axis,0])
            else:
              
              return img
          else:
            line.append([img.shape[0]-1,intercept_x_axis])
          control_points.append(line)
         
          pattern.append(8)
        else:
         
          return img
    res =  line_intersection_linking(control_points[0], control_points[1])
    print("intersect_point_before",res)
    if(res != False):
      res = findnewIntersect(img,res)
    print("intersect_point_after",res)

    if(res == False):
      cv.line(img, (points[0][1], points[0][0]), (points[1][1], points[1][0]), [255, 0, 0], 1)
      return(img)
    else:
      points.insert(1, list(res))
      X_coord = []
      Y_coord = []
      xFinal=[]
      yFinal=[]
      cnt = 10
      test = img.copy()
      for coord in points:
        X_coord.append(coord[1])
        Y_coord.append(coord[0])

      # res1 = PointTest(test, X_coord, Y_coord)
      # res2 = BezierPoint(img, X_coord, Y_coord, xFinal, yFinal)

      for i in range(cnt+1):
        if len(X_coord)==3:
          x0 = getValue_linking(X_coord[0], X_coord[1], i / cnt)
          y0 = getValue_linking(Y_coord[0], Y_coord[1], i / cnt)
          x1 = getValue_linking(X_coord[1], X_coord[2], i / cnt)
          y1 = getValue_linking(Y_coord[1], Y_coord[2], i / cnt)

          xFinal.append(getValue_linking(x0, x1, i / cnt))
          yFinal.append(getValue_linking(y0, y1, i / cnt))

      curve_coordinates = []
      for index,y in enumerate([round(num) for num in yFinal]):
        coordinate = []
        coordinate.append(y)
        coordinate.append([round(num) for num in xFinal][index])
        curve_coordinates.append(coordinate)

      for i in range(len(curve_coordinates)):
        if(curve_coordinates[i][0] <= img.shape[0]-1 and curve_coordinates[i][0] > 0 and curve_coordinates[i][1] <= img.shape[1]-1 and curve_coordinates[i][1] > 0):
          img[curve_coordinates[i][0]][curve_coordinates[i][1]] = [255,0,0]

     
      pts = np.array([(sub[1], sub[0]) for sub in curve_coordinates],np.int32)
     
      isClosed = False
      color = (255, 0, 0)
      thickness = 1
      linked = cv.polylines(img, [pts], isClosed, color, thickness)
     
      return(linked)



def decideLinkMethod_linking(ratio, distance, img, points):
  sp = None
  if(distance <= ratio):
    sp = True
    cv.line(img, (points[0][1],points[0][0]), (points[1][1], points[1][0]), [255, 0, 0], 1)
  else:
    findPattern_linking(img, points)
    sp = False
  return (img,sp)

  

##############################################################################################################

####################################### final function for one image #############################################
def final_linking(images,tresh =12.5):
  result_list = []
  damage_presentage = []
  linking_list = []
  for img in images:
    image = cv.imread(img)
    damaged_pixels = findDamages_linking(image)
    forground_pixes = getForegroundPixels_linking(image)
    resolved_pixels = []
    not_resolved = []
    couples = []
    dp = 0
    shape = []
    r_val = round(math.sqrt(image.shape[0] ** 2 + image.shape[1] ** 2))
    ratio = r_val/100*tresh
    max_ratio = r_val/100*28
    img_copy = image.copy()
    if(len(damaged_pixels) == 0):
      print("cannot reconstruct thre are no any damaged end tips")
    elif(len(damaged_pixels) == 1):
      print("cannot reconstruct there is only one damaged end tip")
    elif(len(damaged_pixels) == 2):
      print("has only two damaged end tips", damaged_pixels[0], " ## ", damaged_pixels[1] )
      first_point = damaged_pixels[0]
      second_point = damaged_pixels[1]
      print("BBBBBBBBBB",first_point)
      couples.append([first_point,second_point])
      distance = calc_distance_linking(first_point, second_point)
      dp = calc_damage_percentage_linking(distance,len(forground_pixes))
      res = decideLinkMethod_linking(ratio, distance, img_copy, [first_point,second_point])
      img_copy = res[0]
      if(res[1] == True):
        shape.append([damaged_pixels , ' ===> links with straight line'])
      else:
        shape.append([damaged_pixels , ' ===> links with curve shape'])
    else:
      print("has multiple damaged end tips")
      for i in damaged_pixels:
        if i not in resolved_pixels:
          list_difference1 = [item for item in damaged_pixels if item not in resolved_pixels]
          if(len(list_difference1) == 1):
            not_resolved.append(list_difference1[0])
          if(len(not_resolved) != 1):
            distance_array = findDistance_linking(image, list_difference1, i)
            positive_negative_data  = positiveNegative_linking(image, list_difference1, i)
            direction_data  = findDirection_linking(image, list_difference1, i)
            result = findMatchingCouple_linking(distance_array,positive_negative_data,direction_data,ratio,max_ratio)
            if(result != None):
              couples.append([i,result])
              resolved_pixels.append(i)
              resolved_pixels.append(result)
              distance = calc_distance_linking(i, result)
              damaged_percentage = calc_damage_percentage_linking(distance,len(forground_pixes))
              # print("damaged_percentage",damaged_percentage)
              dp = dp +damaged_percentage
              res = decideLinkMethod_linking(ratio, distance, img_copy, [i,result])
              img_copy = res[0]
              if(res[1] == True):
                shape.append([damaged_pixels , ' ===> links with straight line'])
              else:
                shape.append([damaged_pixels , ' ===> links with curve shape'])
            if((result == None)):
              not_resolved.append(i)
      list_difference2 = [item for item in not_resolved if item not in resolved_pixels]
      if(len(list_difference2) == 2):
        couples.append([list_difference2[0],list_difference2[1]])
        distance = calc_distance_linking(list_difference2[0], list_difference2[1])
        damaged_percentage = calc_damage_percentage_linking(distance,len(forground_pixes))
        # print("damaged_percentage",damaged_percentage)
        dp = dp+damaged_percentage
        resolved_pixels.append(list_difference2[0])
        resolved_pixels.append(list_difference2[1])
        res = decideLinkMethod_linking(ratio, distance, img_copy, [list_difference2[0],list_difference2[1]])
        img_copy = res[0]
        if(res[1] == True):
          shape.append([damaged_pixels , ' ===> links with straight line'])
        else:
          shape.append([damaged_pixels , ' ===> links with curve shape'])
    # print("DP", dp)
    result_list.append(img_copy)
    damage_presentage.append(dp)
    linking_list.append(">> " + str(shape) + "\n\n")
  return result_list,linking_list

#methana log ekak wadinna one linking method = linking_list
##################################################################################################################

######################################### Increase Thickness ##############################################
def increase_thickness(images):
  thicked_list = []
  for img in images:
    kernel = np.ones((2,2),np.uint8)
    output = cv.dilate(img,kernel,iterations = 1)
    thicked_list.append(output)
  return thicked_list
###########################################################################################################

############################################################Binding Damage Part (Utility) ##########################
def getMissingpart(img):
  missing = []
  for row in range(img.shape[0]):
    for col in range(img.shape[1]):
      if((img[row,col][0] == 0 and img[row,col][1] == 0 and img[row,col][2] == 255) or (img[row,col][0] == 255 and img[row,col][1] == 0 and img[row,col][2] == 0)):
        missing.append([row,col])
  return missing
#####################################################################################################################

###################################################Binding Damage Part###################################################
def pasteSuitableArea(thicked, module02out):
  constructed_list = []
  for i in range(0,len(thicked)):
    new = getMissingpart(thicked[i])
    module02out_img = cv.imread(module02out[i])
    module02out_copy = module02out_img.copy()
    for i in new:
      module02out_copy[i[0], i[1]] = [0,0,255]
    constructed_list.append(module02out_copy)
  return constructed_list
#############################################################################################################


    
################################################### Black & White Convert ######################################
def findMarkedDamagedPixels(img):
  ends = []
  for row in range(img.shape[0]):
    for col in range(img.shape[1]):
      if(img[row,col][0] == 0 and img[row,col][1] == 255 and img[row,col][2] == 0):
        ends.append([row,col])
  return ends

def removeIndividuals(y,x,test_image):
  count = 0
  mask3 = ([y-1,x-1],[y-1,x],[y-1,x+1],[y,x-1],[y,x+1],[y+1,x-1],[y+1,x],[y+1,x+1])
  for m in mask3:
    if((test_image[m[0],m[1]][0] == 0 and test_image[m[0],m[1]][1] == 255 and test_image[m[0],m[1]][2] == 0) or (test_image[m[0],m[1]][0] == 255 and test_image[m[0],m[1]][1] == 0 and test_image[m[0],m[1]][2] == 0) and m[0] >= 0 and m[0] < test_image.shape[0] and m[1] >= 0 and test_image.shape[1]):
      count = count + 1
  if(count == 1):
    test_image[y,x] = [255,255,255]
  return test_image;

def bwConvertitng(test_images):
  result_bnw = []
  for image in test_images:
    test_image = image.copy()
    damaged_marked_pixels = findMarkedDamagedPixels(test_image)
    for i in damaged_marked_pixels:
      test_image = removeIndividuals(i[0],i[1],test_image)
    for row in range(test_image.shape[0]):
      for col in range(test_image.shape[1]):
        if((test_image[row,col][0] == 0 and test_image[row,col][1] == 0 and test_image[row,col][2] == 0) or
           (test_image[row,col][0] == 0 and test_image[row,col][1] == 0 and test_image[row,col][2] == 255) or
           (test_image[row,col][0] == 255 and test_image[row,col][1] == 0 and test_image[row,col][2] == 0) or
           (test_image[row,col][0] == 0 and test_image[row,col][1] == 255 and test_image[row,col][2] == 0) or
           (test_image[row,col][0] == 255 and test_image[row,col][1] == 255 and test_image[row,col][2] == 0)):
          test_image[row][col] = [0,0,0]
        if(test_image[row,col][0] == 255 and test_image[row,col][1] == 255 and test_image[row,col][2] == 255):
          test_image[row][col] = [255,255,255]
    result_bnw.append(test_image)
  return result_bnw
#############################################################################################################


################################################# USE TO SHOW IN UI ####################################
def display_out(files):
  rgb_converted = []
  for file in files:
    blue,green,red = cv.split(file)
    img = cv.merge((red,green,blue))
    print(img)
    rgb_converted.append(img)
  return rgb_converted
