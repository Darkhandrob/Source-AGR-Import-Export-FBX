# AGR to FBX Export Script by Darkhand
# https://github.com/Darkhandrob
# https://www.youtube.com/user/Darkhandrob
# https://twitter.com/Darkhandrob
# Last change: 02.02.2019

import bpy,time

class ExportAgr(bpy.types.Operator):
    """Only exports every animation as a FBX"""   # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "aiox.agr_to_fbx"        # unique identifier for buttons and menu items to reference.
    bl_label = "CSGO AGR Export FBX"        # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    
    # Properties used by the file browser
    filepath: bpy.props.StringProperty(subtype="DIR_PATH")
    
    def menu_draw_export(self, context):
        layout = self.layout
        layout.operator("aiox.agr_to_fbx", text="AGR Export FBX")
    
    # Open the filebrowser with the custom properties
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    # main funktion
    def execute(self, context):
        time_start = time.time()
        # Change Filepath, if something is inputted in the File Name Box
        if not self.filepath.endswith("\\"):
            self.filepath = self.filepath.rsplit(sep="\\", maxsplit=1)[0] + "\\"
        # Delete physics
        for i in bpy.data.objects: 
            if i.name.find("physics") != -1:
                bpy.data.objects.remove(i)
                
        print("Deleting Physics finished.")
        # select and rename hierarchy objects to root
        for CurrentModel in bpy.data.objects:
            if CurrentModel.name.find("afx.") != -1:
                # select root
                CurrentModel.select_set(1)
                # select childrens
                for CurrentChildren in CurrentModel.children:
                    CurrentChildren.select_set(1)
                # rename top to root
                CurrentObjectName = CurrentModel.name
                CurrentModel.name = "root"
                # export single object as fbx
                fullfiles = self.filepath + "/" + CurrentObjectName + ".fbx"
                bpy.ops.export_scene.fbx(
                    filepath = fullfiles, 
                    use_selection = True, 
                    bake_anim_use_nla_strips = False, 
                    bake_anim_use_all_actions = False, 
                    bake_anim_simplify_factor = 0,
                    add_leaf_bones=False)
                # undo all changes
                CurrentModel.name = CurrentObjectName
                CurrentModel.select_set(0)
                for CurrentChildren in CurrentModel.children:
                    CurrentChildren.select_set(0)

            # export camera
        if bpy.data.objects.find("afxCam") != -1:
            bpy.data.objects["afxCam"].select_set(1)
            fullfiles = self.filepath + "/afxcam.fbx"
            bpy.ops.export_scene.fbx(
                filepath = fullfiles, 
                use_selection = True, 
                bake_anim_use_nla_strips = False, 
                bake_anim_use_all_actions = False, 
                bake_anim_simplify_factor = 0,
                add_leaf_bones=False)
            bpy.data.objects["afxCam"].select_set(0)
                    
        print(" ")
        print("FBX-Export Script finished in %.4f sec." % (time.time() - time_start))
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExportAgr)
#    bpy.types.TOPBAR_MT_file_export.append(ExportAgr.menu_draw_export)
#    
def unregister():
#    bpy.types.TOPBAR_MT_file_export.remove(ExportAgr.menu_draw_export)
    bpy.utils.unregister_class(ExportAgr)
#        
## This allows you to run the script directly from blenders text editor
## to test the addon without having to install it.
#if __name__ == "__main__":
#    register()
