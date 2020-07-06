# testPython/PVAPY_NTNSA_Viewer Status 2020.07.06

## limits should not be a separate window

This is now done.

## move image window

### If images are actively being generated than can't move image window.

Not fixed.

### Image window goes back to original position.

Mark says:
After moving image window, as soon as I restart in the viewer or medm the window goes back to its original position.

I also seen this.

It appears that the only way to make it work is to:
1) have either the viewer of medm stopped
2) move the image window
3) close the image window via the close button on the image title bar.


## zoom image window

Note that change was made to temporily stop channel monitors while a zoom is in progress.
So zoom should work even if images are being generated.

Mark reports:
The problem is that the second zoom is not correct.  If I am displaying a single peak and I zoom in on it it seems to work OK.  But if I try to zoom in more on that peak I am no longer seeing the peak at all.  It looks like the part of the image actually being displayed is wrong.  I suspect the transformation from coordinates in the image display to original pixel coordinates is wrong.

Let me pursue this again.


## manualMinimum and manualMaximum

If images are being generated then new image is generated after each character is pressed.
If images are NOT being generated then a new image is only generated when return is entered.

I suspect it is a problem with the way QApplication threading.
I don't know what to do.

## display the cursor X/Y position and the pixel intensity at the cursor position in the main window

Nothing done so far.

## resize image window

Nothing done so far.




