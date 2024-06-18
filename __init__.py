# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

bl_info = {
    "name" : "Simple Text Tool",
    "author" : "Clement C",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D > Text",
    "description": "Small tool to create and edit text quickly",
    "warning" : "",
    "category" : "3D View"
}

class MyProperties(bpy.types.PropertyGroup):
    text_to_create : bpy.props.StringProperty(name = "Body Text", default = "Default text", description="Content of the text object")
    text_extrude_size : bpy.props.FloatProperty(name= "Extrude", min = 0, soft_min = 0, default = 0, precision=4, unit="LENGTH", description="Length of the depth added in the local Z direction along the curve, perpendicular to its normal")
    text_font_size : bpy.props.FloatProperty(name= "Font Size", min= 0.0001, soft_min = 0.010, soft_max = 10, default = 1, precision=3, description="Font size")
    text_font_shear : bpy.props.FloatProperty(name= "Shear", min= -1, max = 1, default = 0, precision=3, description="Italic angle of the characters")
    look_at_camera : bpy.props.BoolProperty(name = "Look at camera", description="Should the text face towards the viewport's camera")
    text_align_x : bpy.props.EnumProperty(name=("Horizontal Alignment"), items=[
        ('LEFT', 'Left', '', 'ALIGN_LEFT', 1),
        ('CENTER', 'Center', '', 'ALIGN_CENTER', 2),
        ('RIGHT', 'Right', '', 'ALIGN_RIGHT', 3),
        ('JUSTIFY', 'Justify', '', 'ALIGN_JUSTIFY', 4),
        ('FLUSH', 'Flush', '', 'ALIGN_FLUSH', 5),
    ], default='CENTER', description="Text horizontal alignment from the object center")
    text_align_y : bpy.props.EnumProperty(name=("Vertical Alignment"), items=[
        ('TOP', 'Top', '', 'ALIGN_TOP', 1),
        ('TOP_BASELINE', 'Top Baseline', '', 'ALIGN_TOP', 2),
        ('CENTER', 'Middle', '', 'ALIGN_MIDDLE', 3),
        ('BOTTOM_BASELINE', 'Bottom Baseline', '', 'ALIGN_BOTTOM', 4),
        ('BOTTOM', 'Bottom', '', 'ALIGN_BOTTOM', 5),
    ], default='CENTER', description="Text vertical alignment from the object center")

class TEXTTOOL_PT_TextCreation(bpy.types.Panel):
    bl_label = "Text Creation"
    bl_idname = "TEXTTOOL_PT_createText"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Text"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        text_tool = scene.text_tool
        
        layout.prop(text_tool, "text_to_create")
        layout.prop(text_tool, "text_extrude_size")
        layout.prop(text_tool, "text_font_size")
        layout.prop(text_tool, "text_font_shear")
        layout.prop(text_tool, "text_align_x")
        layout.prop(text_tool, "text_align_y")
        layout.prop(text_tool, "look_at_camera")
        
        row = layout.row()
        row.operator("texttool.op_create", icon="PLUS")
        #row = layout.row()
        #row.operator("texttool.op_debug", icon="EXPERIMENTAL")

class TEXTTOOL_PT_TextEditing(bpy.types.Panel):
    bl_label = "Text Editing"
    bl_idname = "TEXTTOOL_PT_editText"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Text"
    
    def draw(self, context):
        layout = self.layout
        
        currObject = bpy.context.object

        if(currObject != None):
            return
        
        if(currObject.type != "FONT"):
            layout.label(text = "Current object is not a font", icon="ERROR")
            return

        layout.prop(currObject.data, "body")
        layout.prop(currObject.data, "extrude")
        layout.prop(currObject.data, "size")
        layout.prop(currObject.data, "shear")
        layout.prop(currObject.data, "align_x")
        layout.prop(currObject.data, "align_y")
        
        row = layout.row()
        row.operator("texttool.op_lookatcamera", icon="OUTLINER_OB_CAMERA")
        row = layout.row()
        row.operator("texttool.op_movetocursor", icon="ORIENTATION_CURSOR")
        row = layout.row()
        row.operator("texttool.op_rotatelikecursor", icon="PIVOT_CURSOR")

def lookAtCamera(obj):
    currArea = bpy.context.area
    viewMat = currArea.spaces[0].region_3d.view_matrix.inverted().to_euler()
    obj.rotation_euler = viewMat

        
class TEXTTOOL_OT_CreateText(bpy.types.Operator):
    """Create a font object with all previous parameters"""
    bl_label = "Create Text"
    bl_idname = "texttool.op_create"
    
    def execute(self, context):
        scene = context.scene
        text_tool = scene.text_tool

        currObject = bpy.context.object

        currObject.data.body = text_tool.text_to_create
        currObject.data.extrude = text_tool.text_extrude_size
        currObject.data.size = text_tool.text_font_size
        currObject.data.align_x = text_tool.text_align_x
        currObject.data.align_y = text_tool.text_align_y
        
        if(text_tool.look_at_camera):
            lookAtCamera(bpy.context.object)
        
        return {'FINISHED'}
        
class TEXTTOOL_OT_LookAtCamera(bpy.types.Operator):
    """Makes the selected font look at the viewport's camera"""
    bl_label = "Look at Camera"
    bl_idname = "texttool.op_lookatcamera"
    
    def execute(self, context):
        lookAtCamera(bpy.context.object)
        
        return {'FINISHED'}
        
class TEXTTOOL_OT_MoveToCursor(bpy.types.Operator):
    """Moves the selected font to the cursor"""
    bl_label = "Move to Cursor"
    bl_idname = "texttool.op_movetocursor"
    
    def execute(self, context):
        bpy.context.object.location = bpy.context.scene.cursor.location
        
        return {'FINISHED'}
        
class TEXTTOOL_OT_RotateToCursor(bpy.types.Operator):
    """Copies the cursor's rotation and applies it to the selected font"""
    bl_label = "Rotate like Cursor"
    bl_idname = "texttool.op_rotatelikecursor"
    
    def execute(self, context):
        bpy.context.object.rotation_euler = bpy.context.scene.cursor.rotation_euler
        
        return {'FINISHED'}
        
class TEXTTOOL_OT_Debug(bpy.types.Operator):
    """Debug button"""
    bl_label = "Debug"
    bl_idname = "texttool.op_debug"
    
    def textFunction(self):
        print("It works")
    
    def execute(self, context):
        currArea = bpy.context.area
        print(currArea.type)
        
        self.textFunction()
        
        print(currArea.spaces[0].region_3d.view_matrix.to_euler())
        
        return {'FINISHED'}



classes = [MyProperties,
           TEXTTOOL_PT_TextCreation,
           TEXTTOOL_PT_TextEditing,
           TEXTTOOL_OT_CreateText,
           TEXTTOOL_OT_LookAtCamera,
           TEXTTOOL_OT_MoveToCursor,
           TEXTTOOL_OT_RotateToCursor,
           TEXTTOOL_OT_Debug]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        bpy.types.Scene.text_tool = bpy.props.PointerProperty(type= MyProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
        del bpy.types.Scene.text_tool


if __name__ == "__main__":
    register()