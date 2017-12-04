'''
A freeware plugin made by Ted Tinker for the zoologists of UCSB's Cheadle Center
to aid human-assisted-image-processing of entomological specimens. 
This utylizes a WhiteBalanceStretch freeware plugin from Diego Nassetti.
Once installed, Bug-Flipper appears in the GIMP menus under Filters.
Click it, and a dialog-box prompts the user for two folders and some options.
The program will open certain images in the first folder. It can rotate the image 180 degrees,
color correct it, display it for more editing, and open another dialog prompt requesting a name.
If possible, rename the image using the scanner gun on the QR code displayed in the image.
If the photo is so blurry it's difficult to read the labels, mark the checkbox to prepend "bad_pic_" to the filename.
Then the image is saved with that filename in the second folder with the desired compression level. 
 
 ----------------------------------------------------------------
 COPYRIGHT NOTICE
 ----------------------------------------------------------------
 
 This program is free software. You can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation either version 3 of the License, or
 (at your option) any later version.  
 
 View the GNU General Public License version 3 at the web site 
 http://www.gnu.org/licenses/gpl-3.0.html
 Alternatively you can write to the Free Software Foundation, Inc., 675 Mass
 Ave, Cambridge, MA 02139, USA.
 
 -------------------------------------------------------------------
 other info
 -------------------------------------------------------------------
 
'''



#!/usr/bin/env python

from gimpfu import * 	# For interacting with the GIMP
import os		# For pulling files from folders

import gtk		# The gtk code is adapted from Ben Duffield's Ardonis Wordpress. Thanks, Ben!
			# It's used for generating dialog boxes to prompt users for new filenames.
			# It comes with a checkbox marked "Flag bad image?" If checked, "bad_pic_" appended to filename start 

##### 

def responseToDialog(entry, dialog, response):
    dialog.response(response)
def getText(file):
    #base this on a message dialog
    dialog = gtk.MessageDialog(
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        gtk.MESSAGE_QUESTION,
        gtk.BUTTONS_OK,None)
    dialog.set_markup('Edit the photo now. Then enter new file name. Use the scanner-gun on the QR if possible. Leave the space blank to use old file name.')
    checkBlurry = gtk.CheckButton() 	# Add checkmark box
    entry = gtk.Entry()			# Add text-entry box				
    entry.connect("activate", responseToDialog, dialog, gtk.RESPONSE_OK)
    vbox = gtk.VBox(TRUE)						# Vertical box
    hbox1 = gtk.HBox(TRUE)						# First horizontal box has text-entry
    hbox1.pack_start(gtk.Label("New Filename:"), True, True, 0)
    hbox1.pack_end(entry)
    vbox.pack_start(hbox1) 						# Second horizontal box has checkbox
    hbox2 = gtk.HBox(TRUE)
    hbox2.pack_start(gtk.Label("Flag Bad Image:"), True, True, 0)
    hbox2.pack_end(checkBlurry, True, True, 0)
    vbox.pack_end(hbox2)
    vbox.pack_end(gtk.Label(), True, True, 0)				
    dialog.vbox.pack_end(vbox, True, True, 0)				# Done packing
    dialog.show_all()

    dialog.run()
    text = entry.get_text() + ".jpg"
    
    if(text == ".jpg"):			# If the dialog is returned empty, use old file name
	text = file
    if(checkBlurry.get_active()):	# If flagged, start filename with "bad_pic_"
	text = "bad_pic_" + text
    dialog.destroy() 			# Destroy and return filename
    return text

#####


def BugFlipper(OldDir,NewDir,renameMe,rotateMe,correctMe,deleteOld,imageQuality):
	for file in os.listdir(OldDir):						# Checks every file in first folder
		if ((file.endswith(".jpg") or file.endswith(".JPG")) and file.startswith("DSC_")): 	# Selects JPEGS beginning DSC_
			PrepareImage(file,OldDir,NewDir,renameMe,rotateMe,correctMe,imageQuality)	
										# Method for image processing
		if (deleteOld):
			os.remove(OldDir+"/"+file)				# Delete old photos, if selected
	return()

#####	

def PrepareImage(file,OldDir,NewDir,renameMe,rotateMe,correctMe,imageQuality):			# Processes photos
	image = pdb.gimp_file_load(OldDir+"/"+file,OldDir+"/"+file)
	drawable = pdb.gimp_image_get_active_layer(image)			
	if(rotateMe):
		pdb.gimp_drawable_transform_rotate_simple(drawable,ROTATE_180, 1,0,0,1)		# Rotate 180 degrees, if selected
	if(correctMe):
		drawable = pdb.python_fu_WhiteBalanceStretch(image,drawable)			# White/Color balance by Diego Nassetti, if selected
	newFileName = file
	if(renameMe):
		display = pdb.gimp_display_new(image)						# Displays the photo
		newFileName = getText(file) 							# Asks user for new filename
	pdb.file_jpeg_save(image, drawable,NewDir+"/"+newFileName,NewDir+"/"+newFileName,
		imageQuality, 0,0,0,"newFileName",0,1,0,0)					# Save in second folder with new name and quality
	if(renameMe):	
		pdb.gimp_display_delete(display)						# Remove display

#####

register(
   	"Bug-Flipper",						# Name
   	"Made by Ted Tinker for Cheadle Center's zoologists",	# Blurb
   	"Made by Ted Tinker for Cheadle Center's zoologists for human-assisted-image-processing of standardized insect photos.",	# Help
	"Ted Tinker",						# Author
	"Ted Tinker, freeware",					# Copywrite
    	"2017",							# Date
    	"Bug-Flipper",						# Display Name
    	"",      						# No picture required
    [
	(PF_DIRNAME, "OldDir", "Folder with photos:","/Users/herbarium/Desktop/insect-images-for-processing"),	# Method Parameters
	(PF_DIRNAME, "NewDir", "Folder to save photos:", "/Users/katjaseltmann/Public/insect-images-processing/flipped"),
	(PF_BOOL, "renameMe", "Rename/Edit photos?", 1),
	(PF_BOOL, "rotateMe", "Rotate photos 180 degrees?", 1),
	(PF_BOOL, "correctMe", "Run white-balance/color-correction?", 1),
	(PF_BOOL, "deleteOld", "Delete old photos after processing?", 1),
	(PF_SLIDER, "imageQuality", "Saved Image Quality:", .3,(.01,1,.01))
    ],
    [],								# Method Return
    BugFlipper, menu="<Toolbox>/Filters")

main()
