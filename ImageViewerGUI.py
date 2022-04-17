####### REQUIRED IMPORTS FROM THE PREVIOUS ASSIGNMENT #######
from my_package.model import InstanceSegmentationModel
from my_package.data import Dataset
from my_package.analysis import plot_visualization
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage


####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from functools import partial
import os


# Define the function you want to call when the filebrowser button is clicked.
def fileClick(clicked, dataset, segmentor):

	####### CODE REQUIRED (START) #######
	# This function should pop-up a dialog for the user to select an input image file.
	# Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
	# Hint: Call the segmentor from here, then compute the output images from using the `plot_visualization` function and save it as an image.
	# Once the output is computed it should be shown automatically based on choice the dropdown button is at.
	# To have a better clarity, please check out the sample video.
	global filename
	cwd = os.path.dirname(os.path.realpath(__file__))
	filename = filedialog.askopenfilename(initialdir = cwd+r"/data/imgs/", title = "Select a File", filetypes = (("jpg files","*.jpg*"),))
	e.delete(0,END)
	if not filename:
		e.insert(0,"No file selected")
		return
	img_number = int((((filename.replace("/","\\")).replace(cwd+"\data\imgs\\","")).replace(".jpg","")).strip())
	e.insert(0,"Image-"+str(img_number))
	dict = dataset[img_number]
	img_np_arr = dict["image"]
	pred_boxes, pred_masks, pred_class, pred_score = segmentor(img_np_arr)
	file_path = cwd+r'/Outputs';
	plot_visualization(img_np_arr, pred_boxes, pred_masks, pred_class, pred_score, file_path, img_number)
	####### CODE REQUIRED (END) #######

# `process` function definition starts from here.
# will process the output when clicked.
def process(clicked):

	####### CODE REQUIRED (START) #######
	# Should show the corresponding segmentation or bounding boxes over the input image wrt the choice provided.
	# Note: this function will just show the output, which should have been already computed in the `fileClick` function above.
	# Note: also you should handle the case if the user clicks on the `Process` button without selecting any image file.
	global filename
	if not filename:
		print("Select a file first!")
		return
	if clicked.get() == "Segmentation":
		mod_img_dir = r"\\mask\\"
	else:
		mod_img_dir = r"\\bbox\\"
	org_img = ImageTk.PhotoImage(Image.open(filename))
	img_label_1.configure(image=org_img)
	img_label_1.photo = org_img
	#now we need to determine the path of the corresponding masked/boxed image and place it in img_label_2
	img_number = int((((filename.replace("/","\\")).replace(cwd+"\data\imgs\\","")).replace(".jpg","")).strip())
	mod_img_path = os.path.dirname(os.path.realpath(__file__))+r"\\Outputs\\"+mod_img_dir+str(img_number)+".jpg"
	mod_img = ImageTk.PhotoImage(Image.open(mod_img_path))
	img_label_2.configure(image=mod_img)
	img_label_2.photo = mod_img
	img_label_1.grid(column=0, row=1, padx="10", pady="5", columnspan=4)
	img_label_2.grid(column=4, row=1, padx="10", pady="5")
	####### CODE REQUIRED (END) #######

# `main` function definition starts from here.
if __name__ == '__main__':

	####### CODE REQUIRED (START) ####### (2 lines)
	# Instantiate the root window.
	# Provide a title to the root window.
	root = Tk()
	root.title("Python GUI Assignment | SWE Lab | 20CS30043")
	root.config(background = "#E9E8E8")
	####### CODE REQUIRED (END) #######

	# Setting up the segmentor model.
	cwd = os.path.dirname(os.path.realpath(__file__))
	annotation_file = cwd+r'/data/annotations.jsonl'
	transforms = []

	# Instantiate the segmentor model.
	segmentor = InstanceSegmentationModel()
	# Instantiate the dataset.
	dataset = Dataset(annotation_file, transforms=transforms)

	
	# Declare the options.
	options = ["Segmentation", "Bounding-box"]
	clicked = StringVar()
	clicked.set(options[0])

	e = Entry(root,font=("TkFixedFont"), width=70)
	e.grid(row=0, column=0)

	####### CODE REQUIRED (START) #######
	# Declare the file browsing button
	file_explore = Button(root, text = ". . .", font=("TkFixedFont"),command = partial(fileClick,clicked,dataset,segmentor), padx="20")
	filename = ""
	file_explore.grid(column = 1, row = 0, padx="5", pady="5")
	####### CODE REQUIRED (END) #######

	####### CODE REQUIRED (START) #######
	# Declare the drop-down button
	dropdown = OptionMenu(root,clicked,*options)
	dropdown.config(font=("TkFixedFont"))
	dropdown.grid(column = 2,row = 0, padx="5", pady="5")
	img_label_1 = Label(root) # label that would contain the original image
	img_label_2 = Label(root) # label with the masked/boxed image
	# both the image labels would be made visible when a file is selected
	####### CODE REQUIRED (END) #######

	# This is a `Process` button, check out the sample video to know about its functionality
	myButton = Button(root, text="Process", font=("TkFixedFont"), command=partial(process, clicked))
	myButton.grid(row=0, column=3)

	
	####### CODE REQUIRED (START) ####### (1 line)
	# Execute with mainloop()
	root.mainloop()
	####### CODE REQUIRED (END) #######