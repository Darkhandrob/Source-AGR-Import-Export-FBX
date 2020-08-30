# AGR-Input-Output-FBX(AIOX) by Darkhand
# https://github.com/Darkhandrob
# https://www.youtube.com/user/Darkhandrob
# https://twitter.com/Darkhandrob
# Last change: 30.08.2020

bl_info = {
    "name": "Source AGR Importer to FBX Exporter(AIOX)",
    "category": "Import-Export",
    "author": "Darkhand",
    "version": (1, 5, 8),
    "blender": (2, 83, 0),
    "description": "Imports AGR and Exports every animation as its own FBX",
    "location": "File > Import/Export"
    }

import bpy

from . import Agr_Import_Export_FBX, Agr_Export_FBX, CSGO_Model_Converter, Apex_Model_Converter

def menu_draw_import(self, context):
    self.layout.operator("aiox.import_agr_to_fbx", text="AGR Import and Export FBX")
    
def menu_draw_export(self, context):
    self.layout.operator("aiox.agr_to_fbx", text="AGR Export FBX")
    
def menu_draw_convert(self, context):
    self.layout.operator("aiox.csgo_model_converter", text="Convert CSGO Models to FBX")
    
def menu_draw_convertAL(self, context):
    self.layout.operator("aiox.apex_model_converter", text="Convert Apex Models to FBX")
    
classes = (
    Agr_Import_Export_FBX.ImpExportAgr,
    Agr_Export_FBX.ExportAgr,
    CSGO_Model_Converter.CSModelConverter,
    Apex_Model_Converter.ALModelConverter
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
    bpy.types.TOPBAR_MT_file_import.append(menu_draw_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_draw_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_draw_convert)
    bpy.types.TOPBAR_MT_file_import.append(menu_draw_convertAL)
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
        
    bpy.types.TOPBAR_MT_file_import.remove(menu_draw_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_draw_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_draw_convert)
    bpy.types.TOPBAR_MT_file_import.remove(menu_draw_convertAL)
    
if __name__ == "__main__":
    unregister()
    register()
