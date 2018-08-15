Description:
This addon for Blender reduces the amount of work to import csgo's agr and export every model in it as a fbx,
so you can open it in Unreal Engine 4.

Features:
- imports .agr through afx-blender-scripts
- selects all keyframes available
- merging the Run-Animation and Ragdoll-Animation together in one model
- deletes Physics(everything with the name "physics" in it)
- renames the parent-object(afx.*) to root and exports it with childrens as FBX
- exports afxCam as single FBX file
- convert whole csgo model-folders to FBX for UE4

Installation:
You first need to install Blender Source Tools
( http://steamreview.org/BlenderSourceTools/ ) and HLAE's afx-blender-scripts
( https://github.com/advancedfx/afx-blender-scripts/releases )
After that you can install and activate this addon.


Usage for "AGR Import and Export FBX":

1.Delete everything in the scene("a"->"x"), change the Frame Rate to 60 or whatever you recorded.
2.Then open "File"->"Import"->"AGR Import and Export FBX".
3.Input the Path to the CSGO Folder with decompiled models and a Path, where to export it.
4.Open "Window" -> "Toggle System Console" to check the status of the programm, because it will 
  become unresponsive while running the addon.
5.Finally open the .agr file and let the programm do its work

Usage for "AGR Export FBX":

If you want to do other customisations and delete some models or use not all keyframes, 
then you can use the "File"->"Export"->"AGR Export FBX", which will only delete physics and
export every model with its childrens.

Important Notice:
If you get the error:"TypeError: Converting py args to operator properties: : keyword "interKey" unrecognized", you need to update your Blender Source Tools

Changelog:

v1.0.0(04.06.2018)
- Added "all-in-one" Addon into Import
- Added "only Export" Addon into Export

v1.0.1(05.06.2018)
- Added "add_leaf_bones=False" to FBX Export (thx to Devostated.)
- Optimized the Keyframes_end to set to the end of the animation
- Fixed "Preserve SMD Polygons & Normals" being set to always False
- Added check if "AfxCam" is present in the "all-in-one" Addon

v1.1.0(14.06.2018)
- Added "MergeInvAnims" Function to "All-in-one"
- Added Runtime Timer
- Changed "bpy.ops.object.delete()" to "bpy.data.objects.remove(AllObjectsList[i])" 
	in the "Deleting Physics" part
- Fixed Error in "only Export", when a String was input into the File Name Box

v1.2.0(28.07.2018)
- Added "CSGO Model Converter"
- Optimized for-Loops in both Scripts
- "all-in-one" now creates a folder to which the script will export the models

v1.2.1(04.08.2018)
- Bugfix in "CSGO Model Converter", which renamed the parent-object to "root.001" instead of "root"

v1.2.2(15.08.2018)
- fixed Bug in "all-in-one", if there are more than one players with the same model
