# CSGO-AGR-Import-Export-FBX
Addon for Blender to export csgo's AGR to FBX files for UE4

## Features:
- imports .agr through afx-blender-scripts
- selects all keyframes available
- deletes Physics(everything with the name "physics" in it)
- renames the parent-object(afx.*) to root and exports it with its childrens as FBX
- exports afxCam as single FBX file

## [Downloads are on the release page](https://github.com/Darkhandrob/CSGO-AGR-Import-Export-FBX/releases)

## Installation:
You first need to install Blender Source Tools
( http://steamreview.org/BlenderSourceTools/ ) and HLAE's afx-blender-scripts
( https://github.com/advancedfx/afx-blender-scripts/releases )
After that you can install and activate this addon.


### Usage for "AGR Import and Export FBX":
Delete everything in the scene(a->x), change the Frame Rate to 60 or whatever you recorded.
Then open File->Import->AGR Import and Export FBX.
Input the Path to the CSGO Folder with decompiled models and a Path, where to export it.
Open Window -> Toggle System Console to check the status of the programm, because it will 
become unresponsive while running the addon.
Finally open the .agr file and let the programm do its work

### Usage for "AGR Export FBX":
If you want to do other customisations and delete some models or use not all keyframes, 
then you can use the File->Export->AGR Export FBX, which will only delete physics and
export every model with its childrens.



## Changelog:

v1.0.0(04.06.2018)
- Added "All-in-one" Addon into Import
- Added "only Export" Addon into Export
