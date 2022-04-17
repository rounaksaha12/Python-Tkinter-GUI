#Rounak Saha
#20CS30043

#Imports
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

def plot_visualization(img_np_arr, pred_boxes, pred_masks, pred_class, pred_score, file_path, img_number): # Write the required arguments
  '''
  input arguments:
  img: (3,H,W) numpy array scaled to 0-1 float values
  rest are the results of the segmentor applied on it
  store masked image at filepath+"/mask/"+str(img_number)+".jpg"
  store bboxed image at filepath+"/bbox/"+str(img_number)+".jpg"
  
  '''
  H = img_np_arr.shape[1]
  W = img_np_arr.shape[2]
  img = Image.fromarray(np.uint8(img_np_arr.transpose(1,2,0)*255)) # pil image created out of the numpy array
  masked_img = Image.fromarray(np.uint8(img_np_arr.transpose(1,2,0)*255))

  #iterate through top 3 objects detected
  for idx in range(3):
    if idx+1>len(pred_masks): #check if number of predictions is less than 3
        break
    my_arr = np.zeros((4,H,W)) # RGBA on which the maks would be laid, alpha values for all pixels where there is no mask is set to 0 so that it can be simply blended with the original image
    # iterate through all pixels
    for i in range(H):
      for j in range(W):
        if (pred_masks[idx])[0][i][j] > 0.5: #this pixel is occupied by the idx th mask, 0.5 is an experimental threshhold value
            my_arr[idx][i][j] = (pred_masks[idx])[0][i][j]
            my_arr[3][i][j] = 0.5 #make alpha of this pixel 0 so that the mask is opaque
            #note that when idx is 0 (most confident detection), the first stream of the pixel is assigned non-0 value, hence most confident mask is red
            #similarly 2nd confident mask is Green and 3rd is blue
    img_to_overlay = Image.fromarray(np.uint8(my_arr.transpose(1,2,0)*255))
    masked_img.paste(img_to_overlay,(0,0),mask=img_to_overlay)
    img_new = ImageDraw.Draw(img) #to insert bounding boxes and text
    img_new.rectangle([(pred_boxes[idx][0][0],pred_boxes[idx][0][1]),(pred_boxes[idx][1][0],pred_boxes[idx][1][1])], outline ="#a8ffb5")
    img_new.text((pred_boxes[idx][0][0],pred_boxes[idx][0][1]-15),pred_class[idx]+" "+str(pred_score[idx]))
  
  mask_file_path = file_path+r"\\mask\\"+str(img_number)+".jpg"
  masked_img.save(mask_file_path)

  bbox_file_path = file_path+r"\\bbox\\"+str(img_number)+".jpg"
  img.save(bbox_file_path);

  # The function should plot the predicted segmentation maps and the bounding boxes on the images and save them.
  # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.