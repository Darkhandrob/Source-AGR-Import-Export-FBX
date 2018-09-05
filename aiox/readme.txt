Description:
This addon for Blender reduces the amount of work to import csgo's agr and export every model in it as a fbx,
so you can open it in Unreal Engine 4.

Features:
- imports .agr(recorded animations with hlae)
- fixes "record invisible"-option through merging run-animations and ragdoll-animations together
- deletes useless physics for moviemaking
- exports every animation as .fbx
- converts decompiled models as fbx

Installation:
You first need to install Blender Source Tools
( http://steamreview.org/BlenderSourceTools/ ) and HLAE's afx-blender-scripts
( https://github.com/advancedfx/afx-blender-scripts/releases )
After that you can install and activate this addon.

Important Note:
If you get the error:"TypeError: Converting py args to operator properties: : keyword "interKey" unrecognized", you need to update your afx-blender-scripts


Usage for "AGR Import and Export FBX":

1.Delete everything in the scene("a"->"x").
2.Then open "File"->"Import"->"AGR Import and Export FBX".
3.Input the path to the CSGO folder with decompiled models and a path, where to export it.
4.Open "Window" -> "Toggle System Console" to check the status of the programm, because it will 
  become unresponsive while running the addon.
5.Finally open the .agr file and let the programm do its work

Usage for "AGR Export FBX":

If you want to do other customisations and delete some models or use not all keyframes, 
then you can use the "File"->"Export"->"AGR Export FBX", which will only delete physics and
export every model with its childrens.

Usage for "CSGO Model Converter":

The animation needs a model on which to apply to in UE4. This script goes through all the folders and subfolders of the inputted filepath(usually the decompiled source files)
and converts every smd file as a fbx. If a .qc file is present in the folder, the script only imports this file instead to support combined models.


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

v1.2.3(16.08.2018)
- Model Converter now exports only one folder above to counter Crowbar's folder for each model
- added the option that the input filepath is used if no exporting path was given
- added framerate-changer to importer of "all-in-one"
- "all-in-one" now switches the exported filename, so the afx.X part is at the end for better usability

v1.3.0(19.08.2018)
- moved the script folder from "custom" to "aiox"
- added importing .smd animations-option to "CSGO Model Converter"

v1.3.1(20.08.2018)
- made "inverting folder for each model from crowbar" optional from "CSGO Model Converter"

v1.3.2(23.08.2018)
- added behaviour of v_glove and v_sleeve models for the default v_weapon animations in "CSGO Model Converter"
- fixed memory leak in "CSGO Model Converter"

v1.3.3(05.09.2018)
- fixed logical error in "only Export"