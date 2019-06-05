# CSGO Model Converter to FBX by Darkhand
# https://github.com/Darkhandrob
# https://www.youtube.com/user/Darkhandrob
# https://twitter.com/Darkhandrob
# Last change: 01.06.2019

import bpy,time,os

class CSModelConverter(bpy.types.Operator):
	"""Converts qc-models and smd-animations to FBX"""  	# blender will use this as a tooltip for menu items and buttons.
	bl_idname = "aiox.csgo_model_converter" 	# unique identifier for buttons and menu items to reference.
	bl_label = "CSGO Model Converter"   	  # display name in the interface.
	bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
	
	# Properties used by the file browser
	filepath: bpy.props.StringProperty(subtype="DIR_PATH")
	
	def menu_draw_convert(self, context):
		layout = self.layout
		layout.operator("aiox.csgo_model_converter", text="CSGO Model Converter")
	
	# Layout for the properties of the file browser
	def draw(self, context):
		layout = self.layout
		box_export = layout.box()
		box_export.prop(self, "convMdl")
		box_export.prop(self, "convAnim")
		box_export.prop(self, "chngScale")
		box_export.prop(self, "exportingPath")
		box_export.prop(self, "invSubfld")
		box_export.prop(self, "renMatName")
	
	# Custom properties 
	exportingPath: bpy.props.StringProperty(
		name="Export Path", 
		description="Directory path to export FBX files",
		default="",
	)
	convMdl: bpy.props.BoolProperty(
		name="Convert models",
		description="Convert the .qc model files (e.g. for AGR)",
		default=True,
	)
	convAnim: bpy.props.BoolProperty(
		name="Convert animations",
		description="Convert the .smd animations (e.g. UE4 custom PoV)",
		default=False,
	)
	chngScale: bpy.props.FloatProperty(
		name="Scale",
		description="Scales models and animations",
		min=0.000001, max=100000.0,
		soft_min=0.001, soft_max=1.0,
		default=0.01,
	)
	invSubfld: bpy.props.BoolProperty(
		name="Invert folder for each model",
		description="Moves all files one folder up in the hierarchy; not recommended if animations should be converted too",
		default=False,
	)
	renMatName: bpy.props.BoolProperty(
		name="Rename material slots",
		description="Adds '_mat' to the material slot names to support the HammUer materials importer",
		default=False,
	)
		
	# Open the filebrowser with the custom properties
	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}
	
	 # main funktion
	def execute(self, context):
		# Timing Runtime
		time_start = time.time()
		# Change Filepath, if something is inputted in the File Name Box
		if not self.filepath.endswith("\\"):
			self.filepath = self.filepath.rsplit(sep="\\", maxsplit=1)[0] + "\\"   
		# Recursiv function to search through all folders
		self.ScanFolder(self.filepath)     
		
		# End
		print("Converting Models finished.")
		print(" ")
		print ("CSGO Model Converter finished in %.4f sec." % (time.time() - time_start))
		return {'FINISHED'} 
	
	def FixArms(self, MdlName):
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.data.armatures[0].bones['v_weapon.Bip01_L_Forearm'].select = 1
		bpy.data.armatures[0].bones['v_weapon.Bip01_R_Forearm'].select = 1
		# ctm_heavy arms dont have ForeTwists bones
		if not MdlName.endswith("_heavy"):
			bpy.data.armatures[0].bones['v_weapon.Bip01_L_ForeTwist'].select = 1
			bpy.data.armatures[0].bones['v_weapon.Bip01_R_ForeTwist'].select = 1
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.armature.parent_clear()
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.data.armatures[0].bones['v_weapon.Bip01_L_Forearm'].select = 0
		bpy.data.armatures[0].bones['v_weapon.Bip01_R_Forearm'].select = 0
		if not MdlName.endswith("_heavy"):
			bpy.data.armatures[0].bones['v_weapon.Bip01_L_ForeTwist'].select = 0
			bpy.data.armatures[0].bones['v_weapon.Bip01_R_ForeTwist'].select = 0
		bpy.data.armatures[0].bones['v_weapon'].select = 1
		for bones in bpy.data.armatures[0].bones['v_weapon'].children_recursive:
			bones.select = 1
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.armature.delete()
		bpy.ops.object.mode_set(mode='OBJECT')
	
	def RenameMaterialNames(self):
		for Mdls in bpy.data.objects:
			for Mats in Mdls.material_slots:
				Mats.material.name = Mats.material.name + "_mat"
		
	def ScanFolder(self, ModelPath):
		# Listing all Elements in the Directory
		FolderList = os.listdir(ModelPath)
		QC_Exists = False
		# If Folderlist exists
		if FolderList:
			# Check if a QC File Exists
			for FolderItem in FolderList:
				if FolderItem.endswith(".qc"):
					QC_Exists = True
			# Splitting Directories and Files
			for FolderItem in FolderList:
				SubFolder = os.path.join(ModelPath, FolderItem)
				if os.path.isdir(SubFolder):
					# Scan Sub-Folder
					self.ScanFolder(SubFolder)
				if QC_Exists and self.convMdl and FolderItem.endswith(".qc"):
					self.ImportCSModels(SubFolder, ModelPath, False)
				if not QC_Exists and self.convAnim and FolderItem.endswith(".smd"):
					self.ImportCSModels(SubFolder, ModelPath, True)
					
	
	def ImportCSModels(self, QCFile, ModelPath, ImpAnim):
		# Import QC
		bpy.ops.import_scene.smd(filepath=QCFile, doAnim=ImpAnim)     
		for i in bpy.data.objects: 
			# Change name of parent to root
			if i.name.endswith("skeleton"):
				i.name = "root"
			# Delete Physics
			if i.name.find("physics") != -1:
		
				bpy.data.objects.remove(i)
		for i in bpy.data.objects: 
			# Delete smd_bone_vis
			if i.name.find("smd_bone_vis") != -1:
		
				bpy.data.objects.remove(i)
		# Create Directory
		NewModelPath = ModelPath.split(self.filepath)[1]
		if self.invSubfld:
			NewDirectoryPath = os.path.dirname(NewModelPath)
			CurrentExportingPath = os.path.join(self.exportingPath, NewDirectoryPath)
		else:
			CurrentExportingPath = os.path.join(self.exportingPath, NewModelPath)
		os.makedirs(name=CurrentExportingPath, exist_ok=True)
		
		MdlName = bpy.path.display_name_from_filepath(QCFile)
		
		if self.renMatName:
			self.RenameMaterialNames()
		
		if MdlName.startswith("v_glove") or MdlName.startswith("v_sleeve") or MdlName.startswith("v_bare"):    
			if self.convMdl:
				# Export as fbx
				bpy.ops.export_scene.fbx(
					filepath = os.path.join(
						CurrentExportingPath,
						"agr_" + MdlName + ".fbx"),
					use_selection=False, 
					bake_anim_use_nla_strips = False, 
					bake_anim_use_all_actions = False,
					bake_anim_simplify_factor = 0,
					add_leaf_bones=False,
					global_scale=self.chngScale)
			if self.convAnim: 
				self.FixArms(MdlName)
				# Export as fbx with agr
				bpy.ops.export_scene.fbx(
					filepath = os.path.join(
						CurrentExportingPath,
						MdlName + ".fbx"),
					use_selection=False, 
					bake_anim_use_nla_strips = False, 
					bake_anim_use_all_actions = False,
					bake_anim_simplify_factor = 0,
					add_leaf_bones=False,
					global_scale=self.chngScale)
		else:
			# Export as fbx
			bpy.ops.export_scene.fbx(
				filepath = os.path.join(
					CurrentExportingPath,
					MdlName + ".fbx"),
				use_selection=False, 
				bake_anim_use_nla_strips = False, 
				bake_anim_use_all_actions = False, 
				bake_anim_simplify_factor = 0,
				add_leaf_bones=False,
				global_scale=self.chngScale)

		# Cleanup
		for MdlObjects in bpy.data.objects:
			bpy.data.objects.remove(MdlObjects)
		for MdlActions in bpy.data.actions:
			bpy.data.actions.remove(MdlActions)
		for MdlArmatures in bpy.data.armatures:
			bpy.data.armatures.remove(MdlArmatures)
		for MdlMeshes in bpy.data.meshes:
			bpy.data.meshes.remove(MdlMeshes)
		for MdlMaterials in bpy.data.materials:
			bpy.data.materials.remove(MdlMaterials)
		for MdlCollection in bpy.data.collections:
			bpy.data.collections.remove(MdlCollection)    
		
		
def register():
	bpy.utils.register_class(CSModelConverter)
	bpy.types.TOPBAR_MT_file_import.append(CSModelConverter.menu_draw_convert)
	
def unregister():
	bpy.types.TOPBAR_MT_file_import.remove(CSModelConverter.menu_draw_convert)
	bpy.utils.unregister_class(CSModelConverter)
	 
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
	register()
