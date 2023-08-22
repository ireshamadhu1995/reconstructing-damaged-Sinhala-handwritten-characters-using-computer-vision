import glob
import math
import statistics

import cv2
import numpy
from scipy.ndimage import interpolation as inter
import os

#4
def correct_skew(thresh_images, delta=.1, limit=5):
    rotated_list = []
    rotated_list_bgr = []
    for thresh_image in thresh_images:
        def determine_score(arr, angle):
            # array is rotated according to the angle
            data = inter.rotate(arr, angle, reshape=False, order=0)
            # get sum of 2D data array via horizontally
            histogram = numpy.sum(data, axis=1)
            # subtract the histogram array elements forward from backward and get power of 2 for each and then sum
            score = numpy.sum((histogram[1:] - histogram[:-1]) ** 2)
            return histogram, score

        scores = []
        angles = numpy.arange(-limit, limit + delta, delta)
        print(angles)
        for angle in angles:
            histogram, score = determine_score(thresh_image, angle)
            scores.append(score)

        #go to console
        best_angle = angles[scores.index(max(scores))]

        (h, w) = thresh_image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        rotated = cv2.warpAffine(thresh_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        rotated_bgr = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)
        rotated_list.append(rotated)
        rotated_list_bgr.append(rotated_bgr)
    return rotated_list,rotated_list_bgr


def removeGreenColour(img):
    h, w, c = img.shape

    image_2d = img.reshape(h * w, c).astype(numpy.float32)

    numcolors = 3
    numiters = 10
    epsilon = 2
    attempts = 10

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, numiters, epsilon)
    ret, labels, centers = cv2.kmeans(image_2d, numcolors, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS)

    centers = numpy.uint8(centers)
    newimage = centers[labels.flatten()]
    newimage = newimage.reshape(img.shape)

    newimage2 = newimage.copy()

    for i in range(0, newimage2.shape[0]):
        for j in range(0, newimage2.shape[1]):
            if numpy.all(newimage2[i, j] == [0, 255, 0]) or numpy.all(newimage2[i, j] == [1, 255, 1]):
                newimage2[i, j] = [227, 223, 222]

    return newimage2

#1
def denoisingImage(imgs):
    denoised_array = []
    index = 0
    for img in imgs:
        img = cv2.imread(img)
        green_removed = removeGreenColour(img)
        img2 = cv2.fastNlMeansDenoisingColored(green_removed, None, 10, 10, 7, 21)
        cv2.imwrite("Dataset/Denoised/{0}_denoised.png".format(index),img2)
        index = index + 1
        denoised_array.append(img2)
    return denoised_array

#2
def contrastEqualized(imgs):
    clahe_images_bgr = []
    index = 0
    for img in imgs:
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_image = clahe.apply(gray_image)
        cv2.imwrite("Dataset/Contrast_eq/gray/{0}_contrast_eq.png".format(index),clahe_image)
        clahe_image_rgb = cv2.cvtColor(clahe_image, cv2.COLOR_GRAY2BGR)
        cv2.imwrite("Dataset/Contrast_eq/rgb/{0}_contrast_eq.png".format(index),clahe_image_rgb)
        index = index + 1
        clahe_images_bgr.append(clahe_image_rgb)
    return clahe_images_bgr

#3
def binarizedImage(imgs):
    thresh_list = []
    thresh_list_bgr = []
    
    index = 0
    for img in imgs:
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (_, thresh) = cv2.threshold(gray_image, 160, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite("Dataset/Binarized/{0}_binarized.png".format(index),thresh)
        thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        index = index + 1
        thresh_list.append(thresh)
        thresh_list_bgr.append(thresh_bgr)
    return thresh_list,thresh_list_bgr

#5
def removingPreprintedLines(bin_images):
    result_list = []
    result_list_bgr = []
    for bin_image in bin_images:
        kernelVertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
        kernelHorizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
        detectedVerticalLines = cv2.morphologyEx(bin_image, cv2.MORPH_OPEN, kernelVertical, iterations=2)
        detectedAllLines = cv2.morphologyEx(detectedVerticalLines, cv2.MORPH_OPEN, kernelHorizontal, iterations=2)
        cnts = cv2.findContours(detectedAllLines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(bin_image, [c], -1, (255, 255, 255), 2)
        result_list.append(bin_image)
        result_bgr = cv2.cvtColor(bin_image, cv2.COLOR_GRAY2BGR)
        result_list_bgr.append(result_bgr)
    return result_list,result_list_bgr

#6
def lineSegmentation(binary_image, original_image_path):
    original_image = cv2.imread(original_image_path,1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # morphological processing, define rectangular structure
    closed = cv2.erode(binary_image, None, iterations=5)
    # cv2.imshow('erode',closed)
    height, width = closed.shape[:2]
    # print height, width
    v = [0] * width
    lfg = [[0 for col in range(2)] for row in range(width)]
    box = [0, 0, 0, 0]

    z = [0] * height
    hfg = [[0 for col in range(2)] for row in range(height)]
    # Horizontal projection
    a = 0
    emptyImage1 = numpy.zeros((height, width, 3), numpy.uint8)
    for y in range(0, height):
        for x in range(0, width):
            cp = closed[y, x]
            # if np.any(closed[y,x]):
            if cp == 0:
                a = a + 1
            else:
                continue
        z[y] = a
        # print z[y]
        a = 0
    # Select the line split point according to the horizontal projection value

    inline = 1
    start = 0
    j = 0
    roi_list = []
    for i in range(0, height):
        if (inline == 1 and z[i] >= 150):  # enter the text area from the blank area
            start = i  # record the starting line split point
            # print i
            inline = 0
        elif (i - start > 3) and z[i] < 160 and inline == 0:  # enter the blank area from the text area
            inline = 1
            if start > 5:
                hfg[j][0] = start - 5  # save row split position
            else:
                hfg[j][0] = start
            hfg[j][1] = i + 6
            if hfg[j][0] >= 0 and hfg[j][1] >= 0 and width >= 0:
                roi = original_image[hfg[j][0]:hfg[j][1], 0:width]
                j = j + 1
                cv2.imwrite('M1_data/filtered_line/' + str(i) + '.png', roi)
                #print("ROI ",roi)
                roi_list.append(roi)
    print("ROI LIST",roi_list)
    return (roi_list,j,hfg,closed)

#7
def wordSegmentation(original_image_path, closed_image, green_removed_image, hfg, j):
    print("closed_image ",closed_image)
    print("hfg ", hfg)
    print(" J ",j)
    original_image = cv2.imread(original_image_path)
    segmented_words_list = []
    noiseRemoved_words_seg = []
    a = 0
    renameNumber = 0
    height, width = original_image.shape[:2]
    v = [0] * width
    lfg = [[0 for col in range(2)] for row in range(width)]
    for p in range(0, j):
        for x in range(0, width):
            for y in range(hfg[p][0], hfg[p][1]):
                cp1 = closed_image[y, x]
                if cp1 == 0:
                    a = a + 1
                else:
                    continue
            v[x] = a  # saves the pixel values of each column
            a = 0
        # print width
        # Vertical split point
        incol = 1
        start1 = 0
        j1 = 0
        z1 = hfg[p][0]
        z2 = hfg[p][1]
        for i1 in range(0, width):
            if incol == 1 and i1 + 10 < len(v) and v[i1] >= 20 and v[
                i1 + 10] >= 20:  # enter the text area from the blank area
                start1 = i1  # record the starting column split point
                incol = 0
            elif (i1 - start1 > 3) and i1 + 10 < len(v) and v[i1] <= 20 and v[
                i1 + 10] <= 20 and incol == 0:  # enter the blank area from the text area
                incol = 1
                lfg[j1][0] = start1 - 2  # save column split position
                lfg[j1][1] = i1 + 2
                l1 = start1 - 2
                l2 = i1 + 2
                j1 = j1 + 1
                #cv2.rectangle(original_image, (l1, z1), (l2, z2), (255, 0, 0), 1)
                if z1 >= 0 and z2 >= 0 and l1 >= 0 and l2 >= 0:
                    roi = original_image[z1:z2, l1:l2]
                    roi_noised_removed = green_removed_image[z1:z2, l1:l2]
                    renameNumber = renameNumber + 1
                    cv2.imwrite(
                        'M1_data/filtered_word/' + str(
                            renameNumber) + '.png',
                        roi)
                    segmented_words_list.append(roi)
                    cv2.imwrite(
                        'M1_data/filtered_word/noise_removed/' + str(
                            renameNumber) + '.png', roi_noised_removed)
                    noiseRemoved_words_seg.append(roi_noised_removed)
    return (segmented_words_list,noiseRemoved_words_seg)


def characterSegmentation():
    segmentedWords = [cv2.imread(file) for file in
                      glob.glob(
                          "M1_data/filtered_word/noise_removed/*.png")]

    segmented_noised_words = [cv2.imread(file) for file in
                              glob.glob("M1_data/filtered_word/*.png")]
    segmented_chars = []
    rename_number = 0
    count = 0
    print("segmented words count ",len(segmentedWords))
    print("segmented noised words count ",len(segmented_noised_words))
    file_number = 0
    for original in segmentedWords:
        image = segmented_noised_words[count]
        original_image_copy = original.copy()
        folder_index = 0
        # colour_removed_image = removeGreenColour(original)
        # cv2.imshow('colour_removed_image', colour_removed_image)
        # cv2.waitKey(0)
        # height, width = colour_removed_image.shape[:2]
        # if widthOriginal > 50:
        gray = cv2.cvtColor(original_image_copy, cv2.COLOR_BGR2GRAY)
        (_, thresh) = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
                                           (2, 2))  # morphological processing, define rectangular structure

        dilate = cv2.erode(thresh, None, iterations=1)
        closed = cv2.dilate(dilate, None, iterations=1)

        # cv2.imshow('img', closed)
        # cv2.waitKey(0)
        height, width = closed.shape[:2]
        z = [0] * height
        v = [0] * width
        a = 0
        renameNumber = 0
        for x in range(0, width):
            for y in range(0, height):
                cp1 = closed[y, x]
                if cp1 == 0:
                    a = a + 1
                else:
                    continue
            v[x] = a  # saves the pixel values of each column
            a = 0
        incol = 1
        start1 = 0
        j1 = 0
        z1 = 0
        z2 = height

        widthArr = [0] * width
        for i in range(0, len(v)):
            widthArr[i] = i + 2

        global rateArray
        rateArray = [0] * width

        global pixelarray
        pixelarray = v

        def getThresholdValue():
            if bool(pixelarray):
                median = statistics.median(pixelarray)
                start = True
                last = True
                count = 0
                if median != 0.0:
                    for loop in range(0, len(pixelarray)):
                        if pixelarray[loop] == 0 and start:
                            start = True
                        else:
                            start = False
                            rate = median - pixelarray[loop]
                            rateArray[count] = rate
                            count = count + 1

                reverse_array = rateArray.copy()
                reverse_array.reverse()
                helper_array = reverse_array.copy()
                for value in range(0, len(rateArray)):
                    if len(reverse_array) > value:
                        if helper_array[value] == 0 and last:
                            last = True
                            del reverse_array[0]
                        else:
                            last = False
                            break

                reverse_array.sort(reverse=True)
                biggest_numbers = [0] * int(len(reverse_array) / 6)
                for number in range(0, int(len(reverse_array) / 6)):
                    item = reverse_array[number]
                    biggest_numbers[number] = item
                if bool(biggest_numbers):
                    temp_thresh = statistics.mean(biggest_numbers)
                    threshold = abs(math.floor(temp_thresh) - median)
                    # print(threshold)
                    return threshold
                return 0

        thresholdValue = getThresholdValue()
        file_number = file_number + 1
        path = os.path.join("M1_data/filtered_chars/", str(file_number))
        os.mkdir(path)
        for i1 in range(0, width):
            
            if incol == 1 and v[i1] >= thresholdValue:  # enter the text area from the blank area
                start1 = i1  # record the starting column split point
                incol = 0
            elif (i1 - start1 > 3) and v[
                i1] <= thresholdValue and incol == 0:  # enter the blank area from the text area
                incol = 1
                # startCol = start1 - 2  # save column split position
                # endCol = i1 + 2
                l1 = start1 - 2
                l2 = i1 + 2
                j1 = j1 + 1
                # cv2.rectangle(original, (l1, z1), (l2, z2), (255, 0, 0), 1)
                if z1 >= 0 and z2 >= 0 and l1 >= 0 and l2 >= 0:
                    roi = image[z1:z2, l1:l2]
                    renameNumber = renameNumber + 1
                    #cv2.imwrite(
                    #    'M1_data/filtered_chars/' + str(
                    #        rename_number) + '.png',
                    #    roi)
                    segmented_chars.append(roi)
                    cv2.imwrite(path + "/" + str(rename_number) + '.png', roi)
                    rename_number = rename_number + 1
        count = count + 1
    print("characters length ",len(segmented_chars))
# segmentation("D:/Final Year research/data/damaged_data_set/image2.png")
    return segmented_chars

def display_out(files):
  rgb_converted = []
  for file in files:
    blue,green,red = cv2.split(file)
    img = cv2.merge((red,green,blue))
    print("rgb converted ",img)
    rgb_converted.append(img)
  return rgb_converted

def display_out2(file):
  blue,green,red = cv.split(file)
  img = cv.merge((red,green,blue))
  print(img)
  return img
