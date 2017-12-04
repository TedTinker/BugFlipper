# A freeware plugin by Diego Nassetti for color/white balance. Put it in the plugins folder.
# This is used by the BugFlipper plugin automatically. 
'''

 Filter to implement the stretching of each colour in the INPUT IMAGE
 to ensure a white balancing effect
 Similar to Gimp Auto White Balance, but being callable from a filter
 ....................................................................
  Prerequisites:
 - none (uses std Gimp environment)
 ....................................................................
 
 Release 1.0   initial
 Release 1.0.1 fixed a bug
 
 Flow implemented to get the final result:       
 
 1. Verify the requested percentage of erratic dark values in Red, Green, Blue
    (limit = 0.05%) to exclude
 2. Verify the requested percentage of erratic bright values in Red, Green, Blue
    (limit = 0.05%) to exclude
 3. Apply the Levels adjustments using min-max previously detected
 
 ----------------------------------------------------------------
 COPYRIGHT NOTICE
 ----------------------------------------------------------------
 
 This program is free software you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation either version 3 of the License, or
 (at your option) any later version.  
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program if not, you can view the GNU General Public
 License version 3 at the web site http://www.gnu.org/licenses/gpl-3.0.html
 Alternatively you can write to the Free Software Foundation, Inc., 675 Mass
 Ave, Cambridge, MA 02139, USA.
 
 -------------------------------------------------------------------
 other info
 -------------------------------------------------------------------
 
'''
#!/usr/bin/env python
from gimpfu import *
#==================================================================================================
# MAIN MODULE
#-------------------------------------------------------------------------------------------------- 
def WhiteBalanceStretch (inImage, inDrawable) :

    pdb.gimp_context_push
    currFG = pdb.gimp_context_get_foreground()
    currBG = pdb.gimp_context_get_background()
    
    # Set up an undo group, so the operation will be undone in one step.
    pdb.gimp_image_undo_group_start(inImage)
    
    name = inDrawable.name
    if '.' in name:
        split = name.split(".", 1)
        name = split[0]

    # =============================
    # REMOVE ERRATIC EXTREME VALUES
    # =============================
    
    erraticPercent = 0.05
    nonerratic = 0.10
    
    # RED 

    # =========== 
    # ZERO QUOTE
    # ===========  
    
    fromV = 0
    toV = 1
    percent = 0
    while (percent < erraticPercent) :  
        (mean, std_dev, median, pixels, count, percentile) = pdb.gimp_histogram (inDrawable, HISTOGRAM_RED, fromV, toV)
        percent = percentile * 100
        toV += 1
    #gimp.message ("percent dark RED erratic = " + str(percent))
    if percent < nonerratic :
        MinRED = toV - 1
    else :
        MinRED = max (0, toV-2)

    # =========== 
    # 255 QUOTE
    # ===========  
    
    fromV = 254
    toV = 255
    percent = 0
    while (percent < erraticPercent) :  
        (mean, std_dev, median, pixels, count, percentile) = pdb.gimp_histogram (inDrawable, HISTOGRAM_RED, fromV, toV)
        percent = percentile * 100  
        fromV -= 1
    #gimp.message ("percent bright RED errratic = " + str(percent))
    if percent < nonerratic :
        MaxRED = fromV + 1
    else :
        MaxRED = min (255, fromV+2)
    
    # GREEN 

    # =========== 
    # ZERO QUOTE
    # ===========  
    
    fromV = 0
    toV = 1
    percent = 0
    while (percent < erraticPercent) :  
        (mean, std_dev, median, pixels, count, percentile) = pdb.gimp_histogram (inDrawable, HISTOGRAM_GREEN, fromV, toV)
        percent = percentile * 100  
        toV += 1
    #gimp.message ("percent dark GREEN erratic = " + str(percent))
    if percent < nonerratic :
        MinGREEN = toV - 1
    else :
        MinGREEN = max (0, toV-2)

    # =========== 
    # 255 QUOTE
    # ===========  
    
    fromV = 254
    toV = 255
    percent = 0
    while (percent < erraticPercent) :  
        (mean, std_dev, median, pixels, count, percentile) = pdb.gimp_histogram (inDrawable, HISTOGRAM_GREEN, fromV, toV)
        percent = percentile * 100  
        fromV -= 1
    #gimp.message ("percent bright GREEN erratic = " + str(percent))
    if percent < nonerratic :
        MaxGREEN = fromV + 1
    else :
        MaxGREEN = min (255, fromV+2)
    
    # BLUE 

    # =========== 
    # ZERO QUOTE
    # ===========  
    
    fromV = 0
    toV = 1
    percent = 0
    while (percent < erraticPercent) :  
        (mean, std_dev, median, pixels, count, percentile) = pdb.gimp_histogram (inDrawable, HISTOGRAM_BLUE, fromV, toV)
        percent = percentile * 100  
        toV += 1
    #gimp.message ("percent dark BLUE erratic = " + str(percent))
    if percent < nonerratic :
        MinBLUE = toV - 1
    else :
        MinBLUE = max (0, toV-2)

    # =========== 
    # 255 QUOTE
    # ===========  
    
    fromV = 254
    toV = 255
    percent = 0
    while (percent < erraticPercent) :  
        (mean, std_dev, median, pixels, count, percentile) = pdb.gimp_histogram (inDrawable, HISTOGRAM_BLUE, fromV, toV)
        percent = percentile * 100  
        fromV -= 1
    #gimp.message ("percent bright BLUE erratic = " + str(percent))
    if percent < nonerratic :
        MaxBLUE = fromV + 1
    else :
        MaxBLUE = min (255, fromV+2)
    
    #gimp.message ("RED range = "+str(MinRED)+"-"+str(MaxRED))
    #gimp.message ("GREEN range = "+str(MinGREEN)+"-"+str(MaxGREEN))
    #gimp.message ("BLUE range = "+str(MinBLUE)+"-"+str(MaxBLUE))
    
    # =============================
    # APPLY MODIFICATIONS TO LEVELS
    # =============================
    
    pdb.gimp_levels (inDrawable, 1, MinRED, MaxRED, 1, 0, 255)
    pdb.gimp_levels (inDrawable, 2, MinGREEN, MaxGREEN, 1, 0, 255)
    pdb.gimp_levels (inDrawable, 3, MinBLUE, MaxBLUE, 1, 0, 255)
    
    # Close the undo group.
    
    pdb.gimp_image_undo_group_end(inImage)
    
    pdb.gimp_context_pop
    pdb.gimp_context_set_foreground(currFG)
    pdb.gimp_context_set_background(currBG)

    inDrawable.name = name+" auto white balanced"

    pdb.gimp_displays_flush
    
    return(inDrawable)

# This is the plugin registration function
register(
    "WhiteBalanceStretch",    
    "perform a white balance stratch of a drawable",   
    "This script removes erratic extremes values of R,G,B and stretches the remaining values",
    "Diego", 
    "Diego Nassetti ", 
    "September 2016",
    "WhiteBalanceStretch", 
    "RGB*", 
    [
      (PF_IMAGE, "image", "Input image", None),
      (PF_DRAWABLE, "drawable", "Input drawable", None),
    ], 
    [
      (PF_DRAWABLE, "outdrawable", "Output drawable", None),
    ],
    WhiteBalanceStretch,
    menu="<Image>/Filters",
    )

main()
