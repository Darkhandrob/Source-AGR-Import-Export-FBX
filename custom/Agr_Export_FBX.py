# AGR-FBX Export Script by Darkhand
# https://www.youtube.com/user/Darkhandrob
# https://twitter.com/Darkhandrob
# Last change: 05.06.2018

import bpy

class ExportAgr(bpy.types.Operator):
	"""CSGO AGR Exporter"""	  # blender will use this as a tooltip for menu items and buttons.
	bl_idname = "custom.agr_to_fbx" 	   # unique identifier for buttons and menu items to reference.
	bl_label = "CSGO AGR Export FBX" 		# display name in the interface.
	bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
	
	# Properties used by the file browser
	filepath = bpy.props.StringProperty(subtype="DIR_PATH")
	
	def menu_draw_export(self, context):
		layout = self.layout
		layout.operator("custom.agr_to_fbx", text="AGR Export FBX")
	
	# Open the filebrowser with the custom properties
	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}
	
	# main funktion
	def execute(self, context):
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
				fullfiles = self.filepath + "/" + current_object_name + ".fbx"
				bpy.ops.export_scene.fbx(
                    filepath = fullfiles, 
                    use_selection = True, 
                    bake_anim_use_nla_strips = False, 
                    bake_anim_use_all_actions = False, 
                    bake_anim_simplify_factor = 0,
                    add_leaf_bones=False)
				# undo all changes
				allobjectslist[x].name = current_object_name
				allobjectslist[x].select = False
				for y in range(number_of_childrens):
					allobjectslist[x].children[y].select = False

			#export camera
			if allobjectslist[x].name.find("afxCam") != -1:
				bpy.data.objects["afxCam"].select = True
				fullfiles = self.filepath + "/afxcam.fbx"
				bpy.ops.export_scene.fbx(
                    filepath = fullfiles, 
                    use_selection = True, 
                    bake_anim_use_nla_strips = False, 
                    bake_anim_use_all_actions = False, 
                    bake_anim_simplify_factor = 0,
                    add_leaf_bones=False)
		
		print ("FBX-Export script finished")
		return {'FINISHED'} 

def register():
	bpy.utils.register_class(ExportAgr)
	bpy.types.INFO_MT_file_export.append(ExportAgr.menu_draw_export)
	
def unregister():
	bpy.types.INFO_MT_file_export.remove(ExportAgr.menu_draw_export)
	bpy.utils.unregister_class(ExportAgr)
		
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
