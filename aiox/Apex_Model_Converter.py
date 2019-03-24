# Apex Model Converter to FBX by Darkhand
# https://github.com/Darkhandrob
# https://www.youtube.com/user/Darkhandrob
# https://twitter.com/Darkhandrob
# Last change: 17.03.2019

import bpy,time,os

class ALModelConverter(bpy.types.Operator):
    """Converts qc-models and smd-animations to FBX"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "aiox.apex_model_converter"     # unique identifier for buttons and menu items to reference.
    bl_label = "Apex Model Converter"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    
    # Properties used by the file browser
    filepath: bpy.props.StringProperty(subtype="DIR_PATH")
    
    def menu_draw_convertAL(self, context):
        layout = self.layout
        layout.operator("aiox.apex_model_converter", text="Apex Model Converter")
    
    # Layout for the properties of the file browser
    def draw(self, context):
        layout = self.layout
        box_export = layout.box()
        box_export.prop(self, "chngScale")
        box_export.prop(self, "exportingPath")
        box_export.prop(self, "invSubfld")
        box_export.prop(self, "rnRootBone")
        box_export.prop(self, "prefixFiles")
    
    # Custom properties 
    exportingPath: bpy.props.StringProperty(
        name="Export Path", 
        description="Directory path to export FBX files",
        default="",
    )
    chngScale: bpy.props.FloatProperty(
        name="Scale",
        description="Scales models and animations",
        min=0.000001, max=100000.0,
        soft_min=0.01, soft_max=1.0,
        default=1,
    )
    invSubfld: bpy.props.BoolProperty(
        name="Invert folder for each model",
        description="Moves all files one folder up in the hierarchy; not recommended if animations should be converted too",
        default=False,
    )
    rnRootBone: bpy.props.BoolProperty(
        name="Renames the Root Bone to 'root'",
        description="",
        default=True,
    )
    prefixFiles: bpy.props.BoolProperty(
        name="Converts specific Apex Legends Files",
        description="Converts only files which starts with pilot_, pov_, ptpov_ und w_",
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
        print ("Apex Legends Model Converter finished in %.4f sec." % (time.time() - time_start))
        return {'FINISHED'} 

                    
    def ScanFolder(self, ModelPath):
        # Listing all Elements in the Directory
        FolderList = os.listdir(ModelPath)
        # If Folderlist exists
        if FolderList:
            # Splitting Directories and Files
            if self.prefixFiles:
                for FolderItem in FolderList:
                    SubFolder = os.path.join(ModelPath, FolderItem)
                    if os.path.isdir(SubFolder) and (FolderItem.startswith("pilot_") or FolderItem.startswith("pov_") 
                    or FolderItem.startswith("ptpov_") or FolderItem.startswith("w_") ):
                        # Scan Sub-Folder
                        self.ScanFolder(SubFolder)
                    if FolderItem.endswith(".smd"):
                        self.ImportModels(SubFolder, ModelPath, True)
            else:
                for FolderItem in FolderList:
                    SubFolder = os.path.join(ModelPath, FolderItem)
                    if os.path.isdir(SubFolder):
                        # Scan Sub-Folder
                        self.ScanFolder(SubFolder)
                    if FolderItem.endswith(".smd"):
                        self.ImportModels(SubFolder, ModelPath, True)
                
    
    def ImportModels(self, MDLFile, ModelPath, ImpAnim):
        # Import Model
        bpy.ops.import_scene.smd(filepath=MDLFile, doAnim=ImpAnim)
        if self.rnRootBone:
            for i in bpy.data.objects: 
                # Change name of parent to root
                if i.name.endswith("skeleton"):
                    i.name = "root"
                # Delete Physics
                if i.name.find("physics") != -1:
                    bpy.data.objects.remove(i)
            # Delete smd_bone_vis
            if i.name.find("smd_bone_vis") != -1:
        
                bpy.data.objects.remove(i)
        else:
            for i in bpy.data.objects: 
                # Delete Physics
                if i.name.find("physics") != -1:
                    bpy.data.objects.remove(i)
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
        
        MdlName = bpy.path.display_name_from_filepath(MDLFile)
        
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
        
        
def register():
    bpy.utils.register_class(ALModelConverter)
    bpy.types.TOPBAR_MT_file_import.append(ALModelConverter.menu_draw_convertAL)
    
def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(ALModelConverter.menu_draw_convertAL)
    bpy.utils.unregister_class(ALModelConverter)
     
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
