import matplotlib.pyplot as plt
import cv2
#from google.colab.patches import cv2_imshow
import numpy as np
#from keras.models import Sequential
#from keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
#from tensorflow.keras.optimizers import SGD, Adam
#from keras.callbacks import ReduceLROnPlateau, EarlyStopping
#from tensorflow.keras.utils import to_categorical
import pandas as pd
import numpy as np
#from sklearn.model_selection import train_test_split
#from sklearn.utils import shuffle
import tensorflow as tf
from tensorflow import keras
import numpy as np
#from kerastuner import RandomSearch
#from kerastuner.engine.hyperparameters import HyperParameters
#from keras_tuner import RandomSearch
#from keras_tuner.engine.hyperparameters import HyperParameters
#from keras import callbacks
import glob
#import tensorflow as tf

"""final working code"""

def getSubFolders(rootfolder):
  subfolderpath =[]
  rootdir=rootfolder
  for path in glob.glob(f'{rootdir}/*/'):
    subfolderpath.append(path+'*.*')
  #print(subfolder)
  return subfolderpath

word_dict = {0:"ආ",1:"ක්",2:"ම්",3:"ව්",4:"ප්",5:"අ",6:"බ",7:"චී",8:"ද",9:"එ",10:"ග",11:"ගි",12:"ල්",13:"න්",14:"හ",15:"ගෙ",16:"ඉ",17:"ජ",18:"ක",19:"කෙ",20:"කි",21:"කු",22:"ල",23:"ලු",24:"මා",25:"ඔ",26:"ධ",27:"ම",28:"මි",29:"ණ",30:"න",31:"නි",32:"ඔ",33:"පා",34:"ප",35:"පු",36:"ර",37:"රි",38:"රු",39:"ස",40:"සී",41:"සි",42:"සු",43:"ට",44:"ත",45:"ති",46:"උ",47:"වි",48:"යා",49:"ය"}

def prepare(filepath):
  img = cv2.imread(filepath)
  img_copy = img.copy()
  #cv2_imshow(img)
  grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  #cv2_imshow(grayImage)
  (thresh, blackwhite) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
  #img_binary = cv2.threshold(grayImage, thresh, 255, cv2.THRESH_BINARY)[1]
  #cv2_imshow(blackwhite)
  img_final = cv2.resize(blackwhite, (28,28))
  #cv2_imshow(img_final) 
  #print("Resize image shape:",img_final.shape)
  img_final =np.reshape(img_final , (1,28,28,1)) # apply to
  return img_final


def predictCharacter(img):
  imgL=img
  model = tf.keras.models.load_model("FYP/SHCR_CNN.model")
  prediction =word_dict[np.argmax(model.predict([prepare(imgL)]))] 
  return prediction
#pred =predictCharacter()
#print(pred)

def getImageAndPredict(path):
  path=path
  ch =[]
  for file in glob.glob(path):
    img= cv2.imread(file)
    pred=predictCharacter(file)
    ch.append(pred)
  return ch

def getRootDir(rootdir):
  org_images = []
  sub = getSubFolders(rootdir)
  for i in sub:
    sub_imgs = []
    for file in glob.glob(i):
      img= cv2.imread(file)
      sub_imgs.append(img)
    rgb_converted = []
    for file in sub_imgs:
      blue,green,red = cv2.split(file)
      img = cv2.merge((red,green,blue))
      #print(img)
      rgb_converted.append(img)
    org_images.append(rgb_converted)
  return sub,org_images
  

def PredictionProcess(sub):
  clist=[]
  wlist=[]
  for i in sub:
    #path= getfpath(sub)
    clist= getImageAndPredict(i)
    print("character list",clist)
    wlist.append(clist)
  print("word list", wlist)
  return wlist
      

def main():
  clist=[]
  wlist=[]
  rootdir = 'FYP/ProjectOutput/'
  sub = getSubFolders(rootdir)
  print(sub)
  #path= getfpath(sub)
  for i in sub:
    #path= getfpath(sub)
    clist= getImageAndPredict(i)
    print("character list",clist)
    wlist.append(clist)

    #path=getPath(sub)
    #imglist=getImage(path)
  print("sub folder ",sub)
  print("wish list", wlist)
  with open('your_file.txt', 'w',encoding='utf-8') as f:
    for item in wlist:
      for i in item:
        f.write("%s" % i)
      f.write(" ")
    
#main()


