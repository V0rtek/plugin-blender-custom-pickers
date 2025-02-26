# Plugin data:
bl_info = {
    "name": "Simple Cube Creator", 
    "blender": (2, 80, 0),          # Minimum Blender version
    "category": "Object",          
    "author": "Justin Morand",        
    "description": "Adds a cube to the scene with a custom button."
}

# Blender Python API
import bpy

# Custom function to add a cube
class OBJECT_OT_add_cube(bpy.types.Operator):
    """Add a Cube"""                    # Tooltip description
    bl_idname = "object.add_cube"       
    bl_label = "Add Cube"               
    bl_options = {'REGISTER', 'UNDO'}   # Be undoable n show in history panel

    def execute(self, context):
        # Add a cube
        bpy.ops.mesh.primitive_cube_add(
            size=2,                     
            enter_editmode=False,      
            align='WORLD',              # Align cube to world coordinates
            location=(0, 0, 0)   
        )

        # Info popup
        self.report({'INFO'}, "Cube Added Successfully!")
        
        return {'FINISHED'}

# Panel class UI
class VIEW3D_PT_cube_creator_panel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport"""
    bl_label = "Cube Creator"
    bl_idname = "VIEW3D_PT_cube_creator_panel"
    bl_space_type = 'VIEW_3D'                   # Display panel in Viewport
    bl_region_type = 'UI'                       # Place panel in UI sidebar
    bl_category = "Create"                      # Sidebar name

    # Panel's content
    def draw(self, context):
        layout = self.layout  # panel's layout object

        # Button
        layout.operator(
            OBJECT_OT_add_cube.bl_idname,   # Reference the function
            text="Create Cube",             
            icon='CUBE'                    
        )

# When the addon is enabled or disabled
def register():
    bpy.utils.register_class(OBJECT_OT_add_cube)
    bpy.utils.register_class(VIEW3D_PT_cube_creator_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_cube)
    bpy.utils.unregister_class(VIEW3D_PT_cube_creator_panel)

if __name__ == "__main__":
    register()
