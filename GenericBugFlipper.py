'''
A freeware plugin made by Ted Tinker for the zoologists of UCSB's Cheadle Center
to aid human-assisted-image-processing of entomological specimens. 

This utylizes a WhiteBalanceStretch freeware plugin from Diego Nassetti.

Once installed, Bug-Flipper appears in the GIMP menus under Filters.
Click it, and a dialog-box prompts the user for two folders and some options.
The program will open specified images in the first folder. It can rotate each image in increments of 90 degrees,
color correct them, display them for more editing, and open new dialog prompts requesting new filenames.
If possible, rename each image using the scanner gun on the QR code displayed in the image.
If a photo is so blurry it's difficult to read the labels, mark the checkbox to prepend "bad_pic_" to the filename.
Then each image is saved with their new filename in the second folder with the desired compression level. 
 
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


#####


#!/usr/bin/env python

from gimpfu import * 	# For interacting with the GIMP
import os		# For pulling files from folders

import gtk		# Used for generating dialog boxes to prompt users for new filenames.
			# It comes with a checkbox marked "Flag bad image?" If checked, "bad_pic_" prepended to filename 

##### 

def responseToDialog(entry, dialog, response):		# This makes renaming with the scanner gun quite fast, as the gun hits enter
	dialog.response(response)
def getText(file):					# Brings up dialog box for renaming
	dialog = gtk.MessageDialog(
		None,
		gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		gtk.MESSAGE_QUESTION,
		gtk.BUTTONS_OK,None)
	dialog.set_markup('Edit the photo now. Then enter new file name. Use the scanner gun on the QR if possible. If no text is entered, the old filename will be used.')
	checkBlurry = gtk.CheckButton() 					# Add checkmark box
	entry = gtk.Entry()							# Add text-entry box				
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
	text = entry.get_text()
	
	if(text == ""):			# If the dialog is returned empty, use old file name
		text = file
	else:
		text = text + ".jpg"
	
	if(checkBlurry.get_active()):	# If checkbox flagged, start filename with "bad_pic_"
		text = "bad_pic_" + text

	dialog.destroy() 			
	return text				# Otherwise just return

#####


def BugFlipper(OldDir,NewDir,begins,ends,renameMe,rotateMe,correctMe,deleteOld,imageQuality):
	for file in os.listdir(OldDir):						# Checks every file in first folder
		if (file.endswith(ends) and file.startswith(begins)): 		# Selects files with prefix and suffix
			PrepareImage(file,OldDir,NewDir,renameMe,rotateMe,correctMe,imageQuality)	
										# Method for image processing
		if (deleteOld):
			os.remove(OldDir+"/"+file)				# Delete old photos, if selected
	return()

#####	

def PrepareImage(file,OldDir,NewDir,renameMe,rotateMe,correctMe,imageQuality):			# Processes photos
	image = pdb.gimp_file_load(OldDir+"/"+file,OldDir+"/"+file)
	drawable = pdb.gimp_image_get_active_layer(image)			
	if(rotateMe!=3):
		pdb.gimp_image_rotate(image,rotateMe)						# Rotate desired amount
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
	"Generic-Bug-Flipper",					# Name
	"Made by Ted Tinker for Cheadle Center's zoologists",	# Blurb
	"Made by Ted Tinker for Cheadle Center's zoologists for human-assisted-image-processing of standardized insect photos.",	# Help
	"Ted Tinker",						# Author
	"Ted Tinker, freeware",					# Copywrite
	"2017",							# Date
	"Generic-Bug-Flipper",					# Display Name
	"",      						# No picture required
	[								# Method Parameters
		(PF_DIRNAME, "OldDir", "Folder with photos:","C:\\"),		# First Folder; replace C:\\ with default
		(PF_DIRNAME, "NewDir", "Folder to save photos:", "C:\\"),	# Second Folder; replace C:\\ with default
		(PF_STRING, "begins", "Filenames begin with...", "DSC_"),	# Prefix. Default to opening raw camera photos, which start this way
		(PF_STRING, "ends", "Filenames end with...", ".jpg"),		# Suffix. Default to opening raw camera photos, which are jpegs
		(PF_BOOL, "renameMe", "Rename/Edit photos?", 1),		# Should the image be displayed for editing/renaming?
		(PF_RADIO, "rotateMe", "Rotate photos?", 3, (			# Choose rotation, default none
			("No", 3),
			("Clockwise 90 degrees",0),
			("Rotate 180 degrees",1),
			("Counterclockwise 90 degrees",2))),
		(PF_BOOL, "correctMe", "Run white-balance/color-correction?", 1),	# Color correct? Default yes
		(PF_BOOL, "deleteOld", "Delete old photos after processing?", 0),	# Delete old photos? Default no
		(PF_SLIDER, "imageQuality", "Saved Image Quality:", .3,(.01,1,.01))	# Choose compression level. 1 is no compression, .01 is most compressed.
										# Default of .3 is almost as clear as uncompressed image, but saves memory.
	],
	[],								# Method Return
	BugFlipper, menu="<Toolbox>/Filters")

main()
