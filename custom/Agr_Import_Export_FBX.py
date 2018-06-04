# AGR-FBX Export Script by Darkhand
# https://www.youtube.com/user/Darkhandrob
# https://twitter.com/Darkhandrob
# Last change: 04.06.2018

import bpy

class ImpExportAgr(bpy.types.Operator):
	"""CSGO AGR Importer-Exporter"""	  # blender will use this as a tooltip for menu items and buttons.
	bl_idname = "custom.import_agr_to_fbx"     # unique identifier for buttons and menu items to reference.
	bl_label = "CSGO AGR Import-Export FBX" 		# display name in the interface.
	bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
	
	# Properties used by the file browser
	filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	filename_ext = ".agr"
	filter_glob = bpy.props.StringProperty(default="*.agr", options={'HIDDEN'})
	
	def menu_draw_import(self, context):
		layout = self.layout
		layout.operator("custom.import_agr_to_fbx", text="AGR Import and Export FBX")
	
	# Layout for the Properties of the file Browser
	def draw(self, context):
		layout = self.layout
		box_import = layout.box() 
		box_import.prop(self, "assetPath")
		box_import.prop(self, "interKey")
		box_import.prop(self, "global_scale")
		box_import.prop(self, "scaleInvisibleZero")
		box_import.prop(self, "skipRemDoubles")
		
		box_export = layout.box()
		box_export.prop(self, "exportingPath")

	# Custom properties 
	assetPath = bpy.props.StringProperty(
		name="Asset Path",
		description="Directory path containing the (decompiled) assets in a folder structure as in the pak01_dir.pak.",
		default="",
	)
	interKey = bpy.props.BoolProperty(
		name="Add interpolated key frames",
		description="Create interpolated key frames for frames in-between the original key frames.",
		default=False
	)
	global_scale = bpy.props.FloatProperty(
		name="Scale",
		description="Scale everything by this value",
		min=0.000001, max=1000000.0,
		soft_min=0.001, soft_max=1.0,
		default=0.01,
	)    
	scaleInvisibleZero = bpy.props.BoolProperty(
		name="Scale invisible to zero",
		description="If set entities will scaled to zero when not visible.",
		default=False,
	)
	skipRemDoubles = bpy.props.BoolProperty(
		name="Preserve SMD Polygons & Normals",
		description="Import raw (faster), disconnected polygons from SMD files; these are harder to edit but a closer match to the original mesh",
		default=False
	)
	exportingPath = bpy.props.StringProperty(
		name="Export Path",
		description="Directory path to export FBX files",
		default="",
	)
	
	# Open the filebrowser with the custom properties
	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}
	
	# main funktion
	def execute(self, context):
		#import agr with input filepath
		bpy.ops.advancedfx.agr_importer(
			filepath=self.filepath,
			assetPath=self.assetPath,
			interKey =self.interKey,
			global_scale = self.global_scale,
			scaleInvisibleZero=self.scaleInvisibleZero,
			skipRemDoubles=False
		)
		
		# save all objects from list into array
		allobjectslist = list(bpy.data.objects)
		number_of_objects = len(bpy.data.objects)
		# delete physics
		for i in range(number_of_objects): 
			if allobjectslist[i].name.find("physics") != -1:
				allobjectslist[i].select = True
		bpy.ops.object.delete()

		# select and rename hierarchy objects to root
		for x in range(number_of_objects):
			if allobjectslist[x].name.find("afx.") != -1:
				#select all keyframes
				if bpy.data.scenes[0].frame_end < allobjectslist[x].animation_data.action.frame_range[1]:
					bpy.data.scenes[0].frame_end = allobjectslist[x].animation_data.action.frame_range[1]
				# select root
				allobjectslist[x].select = True
				# select childrens
				number_of_childrens = len(allobjectslist[x].children)
				for y in range(number_of_childrens):
					allobjectslist[x].children[y].select = True
				# rename top to root
				current_object_name = allobjectslist[x].name
				allobjectslist[x].name = "root"
				# export single object as fbx
				fullfiles = self.exportingPath + "/" + current_object_name + ".fbx"
				bpy.ops.export_scene.fbx(filepath = fullfiles, use_selection = True, bake_anim_use_nla_strips = False, bake_anim_use_all_actions = False, bake_anim_simplify_factor = 0)
				# undo all changes
				allobjectslist[x].name = current_object_name
				allobjectslist[x].select = False
				for y in range(number_of_childrens):
					allobjectslist[x].children[y].select = False
					
		#export camera
		bpy.data.objects["afxCam"].select = True
		fullfiles_cam = self.exportingPath + "/afxcam.fbx"
		bpy.ops.export_scene.fbx(filepath = fullfiles_cam, use_selection = True, bake_anim_use_nla_strips = False, bake_anim_use_all_actions = False, bake_anim_simplify_factor = 0)
		bpy.data.objects["afxCam"].select = False
		
		print ("FBX-Export script finished")
		return {'FINISHED'} 

def register():
	bpy.utils.register_class(ImpExportAgr)
	bpy.types.INFO_MT_file_import.append(ImpExportAgr.menu_draw_import)
	
def unregister():
	bpy.types.INFO_MT_file_import.remove(ImpExportAgr.menu_draw_import)
	bpy.utils.unregister_class(ImpExportAgr)
		
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
	register()