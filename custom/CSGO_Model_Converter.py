# CSGO Model Converter to FBX by Darkhand
# https://www.youtube.com/user/Darkhandrob
# https://twitter.com/Darkhandrob
# Last change: 04.08.2018

import bpy
import time
import os 

class CSModelConverter(bpy.types.Operator):
    """CSGO default Model Converter"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "custom.csgo_model_converter"     # unique identifier for buttons and menu items to reference.
    bl_label = "CSGO Model Converter"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    
    # Properties used by the file browser
    filepath = bpy.props.StringProperty(subtype="DIR_PATH")
    
    def menu_draw_convert(self, context):
        layout = self.layout
    
    # Layout for the Properties of the file Browser
    def draw(self, context):
        layout = self.layout
        box_export = layout.box()
        box_export.prop(self, "exportingPath")
    
    # Custom properties 
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
        # Timing Runtime
        time_start = time.time()
        # Change Filepath, if something is inputted in the File Name Box
        if not self.filepath.endswith("\\"):
            self.filepath = self.filepath.rsplit(sep="\\", maxsplit=1)[0] + "\\"   
        # Rekursiv Function to search through all folders     
        self.ScannOrdner(self.filepath)  
        # End
        print("Converting Models finished.")
        print(" ")
        print ("CSGO Model Converter finished in %.4f sec." % (time.time() - time_start))
        return {'FINISHED'} 

    def ScannOrdner(self, ModelPath):
        # Listing all Elements in the Directory
        FolderList = os.listdir(ModelPath)
        # If Folderlist exists
        if FolderList:
            # Splitting Directories and Files
            for FolderItem in FolderList:
                SubFolder = os.path.join(ModelPath, FolderItem)
                if os.path.isdir(SubFolder):
                    # Create Directory
                    self.ScannOrdner(SubFolder)
                if FolderItem.endswith(".qc"):
                    print("Subfolder:" + SubFolder)
                    print("ModelPath:" + ModelPath)
                    self.ImportCSModels(SubFolder, ModelPath)
    
    def ImportCSModels(self, QCFile, ModelPath):
        # Import QC
        bpy.ops.import_scene.smd(filepath=QCFile, doAnim=False) 
        for i in bpy.data.objects: 
            # Change name of parent to root
            if i.name.endswith("skeleton"):
                i.name = "root"
            # Delete Physics
            if i.name.find("physics") != -1:
                bpy.data.objects.remove(i)
        
        # Create Directory
        NewModelPath = ModelPath.split(self.filepath)[1]
        NewDirectoryPath = os.path.dirname(os.path.dirname(NewModelPath))
        CurrentExportingPath = os.path.join(self.exportingPath, NewDirectoryPath)
        os.makedirs(name=CurrentExportingPath, exist_ok=True)
        
        # Export as fbx
        bpy.ops.export_scene.fbx(
            filepath = os.path.join(
                CurrentExportingPath,
                bpy.path.display_name_from_filepath(QCFile) + ".fbx"),
            use_selection=False, 
            bake_anim_use_nla_strips = False, 
            bake_anim_use_all_actions = False, 
            bake_anim_simplify_factor = 0,
            add_leaf_bones=False)
        
        # Cleanup
        for MdlObjects in bpy.data.objects:
            bpy.data.objects.remove(MdlObjects)
            
        
def register():
    bpy.utils.register_class(CSModelConverter)
    bpy.types.INFO_MT_file_import.append(CSModelConverter.menu_draw_convert)
    
def unregister():
    bpy.types.INFO_MT_file_import.remove(CSModelConverter.menu_draw_convert)
    bpy.utils.unregister_class(CSModelConverter)
    
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
