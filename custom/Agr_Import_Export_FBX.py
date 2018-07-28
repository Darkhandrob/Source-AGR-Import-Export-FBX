# AGR-FBX Import and Export Script by Darkhand
# https://www.youtube.com/user/Darkhandrob
# https://twitter.com/Darkhandrob
# Last change: 22.07.2018

import bpy
import time
import os

class ImpExportAgr(bpy.types.Operator):
    """CSGO AGR Importer-Exporter"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "custom.import_agr_to_fbx"     # unique identifier for buttons and menu items to reference.
    bl_label = "CSGO AGR Import-Export FBX"         # display name in the interface.
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
        default=True
    )
    exportingPath = bpy.props.StringProperty(
        name="Export Path",
        description="Directory path to export FBX files",
        default="",
    )
    
    def MergeInvAnims(self, context):
        # Ragdollanimation .hide_render is set as True at Frame 1
        # But if he was killed before starting recording, it is also the Ragdoll is False and Run is True
        # Each Type of Model gets its own Array inside the Array
        PlayerAnimations = []
        for CurrentModel in bpy.data.objects:
            # Find parents
            if CurrentModel.name.find("afx.") != -1:
                # Find Player Models
                if CurrentModel.name.find("tm") != -1:
                    # Test first and last Keyframe to get RunAnimation
                    bpy.context.scene.frame_set(1.0)
                    if CurrentModel.hide_render == False:    
                        bpy.context.scene.frame_set(CurrentModel.animation_data.action.frame_range[1])
                        if CurrentModel.hide_render == True:
                            # Find RagdollAnimation
                            for CurrentSecondModel in bpy.data.objects:
                                if CurrentModel.name.find("afx.") != -1:
                                    if CurrentSecondModel.name.find(CurrentModel.name.split()[1]) != -1:
                                        # Dont use the same object-model
                                        if CurrentSecondModel.name.find(CurrentModel.name.split()[0]) == -1:
                                            PlayerAnimations.append([CurrentModel,CurrentSecondModel])  
                                                          
        # Edit Animation-strips
        for i in range(len(PlayerAnimations)):
            RagdollStartFrame = PlayerAnimations[i][1].animation_data.action.fcurves[1].range()[0] 
            PlayerAnimations[i][1].keyframe_delete(data_path="hide_render", frame=0.0)
            RunDataAnim = PlayerAnimations[i][0].animation_data.action
            RagdollDataAnim = PlayerAnimations[i][1].animation_data.action
            # Push Action down to new Strip
            PlayerAnimations[i][0].animation_data_clear()
            PlayerAnimations[i][0].animation_data_create()
            PlayerAnimations[i][0].animation_data.nla_tracks.new()
            PlayerAnimations[i][0].animation_data.nla_tracks[0].strips.new(name="RunData", start=0.0, action=RunDataAnim)
            # RunAnim already jumps on the frame, where the first keyframe of RagdollAnim is
            PlayerAnimations[i][0].animation_data.nla_tracks[0].strips[RunDataAnim.name].action_frame_end = RagdollStartFrame - 1
            PlayerAnimations[i][0].animation_data.nla_tracks[0].strips.new(name="RagdollDataAnim", start=RagdollStartFrame, action=RagdollDataAnim)
            # Delete model
            number_of_childrens = len(PlayerAnimations[i][1].children)
            for y in range(number_of_childrens):
                bpy.data.objects.remove(PlayerAnimations[i][1].children[0])
            bpy.data.objects.remove(PlayerAnimations[i][1])
            PlayerAnimations[i][0].name = PlayerAnimations[i][0].name + "RunAndDeathAnim"
        print("Merging Run and DeathAimation finished")
    
    # Open the filebrowser with the custom properties
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    # Main funktion
    def execute(self, context):
        # Timing Runtime
        time_start = time.time()
        # Import agr with input filepath
        bpy.ops.advancedfx.agr_importer(
            filepath=self.filepath,
            assetPath=self.assetPath,
            interKey =self.interKey,
            global_scale = self.global_scale,
            scaleInvisibleZero=self.scaleInvisibleZero,
            skipRemDoubles=self.skipRemDoubles
        )
        # Create Directory
        NewExportPath = os.path.join(self.exportingPath, bpy.path.display_name_from_filepath(self.filepath))
        os.makedirs(name=NewExportPath, exist_ok=True)
        self.exportingPath = NewExportPath
        
        # Execute method
        self.MergeInvAnims(context)
        # Delete physics(maybe include into merge_anim class for runtime)
        for CurrentModel in bpy.data.objects: 
            if CurrentModel.name.find("physics") != -1:
                bpy.data.objects.remove(CurrentModel)
                
        print("Deleting Physics finished.")
        for CurrentModel in bpy.data.objects:
            if CurrentModel.name.find("afx.") != -1:
                #select all keyframes
                if CurrentModel.name.find("RunAndDeathAnim") != -1:
                    bpy.context.scene.frame_end = CurrentModel.animation_data.nla_tracks[0].strips[1].action_frame_end
                else:
                    bpy.context.scene.frame_end = CurrentModel.animation_data.action.frame_range[1]
                # select root
                CurrentModel.select = True
                # select childrens
                for CurrentChildren in CurrentModel.children:
                    CurrentChildren.select = True
                # rename top to root
                CurrentObjectName = CurrentModel.name
                CurrentModel.name = "root"
                # export single object as fbx
                fullfiles = self.exportingPath + "/" + CurrentObjectName + ".fbx"
                bpy.ops.export_scene.fbx(
                    filepath = fullfiles, 
                    use_selection = True, 
                    bake_anim_use_nla_strips = False, 
                    bake_anim_use_all_actions = False, 
                    bake_anim_simplify_factor = 0,
                    add_leaf_bones=False
                    )
                # undo all changes
                CurrentModel.name = CurrentObjectName
                CurrentModel.select = False
                for CurrentChildren in CurrentModel.children:
                    CurrentChildren.select = False
                
        print("Exporting Models finished.")    
        #export camera
        if bpy.data.objects.find("afxCam") != -1:
            bpy.data.objects["afxCam"].select = True
            fullfiles_cam = self.exportingPath + "/afxcam.fbx"
            bpy.ops.export_scene.fbx(
                filepath = fullfiles_cam, 
                use_selection = True, 
                bake_anim_use_nla_strips = False, 
                bake_anim_use_all_actions = False, 
                bake_anim_simplify_factor = 0,
                add_leaf_bones=False)
            bpy.data.objects["afxCam"].select = False
            
        print("Exporting Camera Finished.")
        print(" ")
        print ("FBX-Export script finished in %.4f sec." % (time.time() - time_start))
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
