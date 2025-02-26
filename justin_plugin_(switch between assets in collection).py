bl_info = {
    "name": "Object Toggle with Arrows",
    "blender": (2, 80, 0),  # Minimum Blender version
    "category": "Object",
    "author": "Justin Morand",
    "description": "Alternates between a cube and a sphere with arrow buttons."
}

import bpy


current_object = None
index = 0

# Get or create the collection "justin_plugin"
def get_or_create_collection():
    collection_name = "justin_plugin"
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
    return collection

# Get or create the collection "data_justin_plugin"
def get_or_create_data_collection():
    collection_name = "data_justin_plugin"
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
    return collection

def remove_previous_object():
    # Delete all objects in the collection
    for obj in list(get_or_create_collection().objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def get_next_asset():
    global index
    collection = get_or_create_data_collection()
    index += 1

    if len(collection.objects) == index:
        index = 0

    obj = collection.objects[index]
    return obj

def get_previous_asset():
    global index
    collection = get_or_create_data_collection()
    index -= 1

    if 0 > index:
        index = len(collection.objects) - 1
    
    obj = collection.objects[index]
    return obj

# Function to add an asset
def add_asset(obj):
    global current_object
    remove_previous_object()
    collection = get_or_create_collection()

    obj_copy = obj.copy()
    obj_copy.location = (0.0, 0.0, 0.0)
    collection.objects.link(obj_copy)

# Function to add a sphere
def add_sphere():
    global current_object
    remove_previous_object()
    collection = get_or_create_collection()

    # Add a sphere to the collection
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1,
        location=(0, 0, 0)
    )
    new_obj = bpy.context.object
    collection.objects.link(new_obj)
    current_object = new_obj

# Operator to handle left arrow click (Switch to Cube)
class OBJECT_OT_prev(bpy.types.Operator):
    """Switch to Previous Object (Cube)"""
    bl_idname = "object.prev"
    bl_label = "Previous Object (Cube)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_asset(get_previous_asset())
        return {'FINISHED'}

# Operator to handle right arrow click (Switch to Sphere)
class OBJECT_OT_next(bpy.types.Operator):
    """Switch to Next Object (Sphere)"""
    bl_idname = "object.next"
    bl_label = "Next Object (Sphere)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_asset(get_next_asset())
        return {'FINISHED'}

# Panel class UI
class VIEW3D_PT_object_toggle_panel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport"""
    bl_label = "Object Toggle"
    bl_idname = "VIEW3D_PT_object_toggle_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Create"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Switch between assets in data_justin_plugin collection")
        # Arrow buttons
        layout.operator(
            OBJECT_OT_prev.bl_idname,
            text="←",
            icon='TRIA_LEFT'
        )
        layout.operator(
            OBJECT_OT_next.bl_idname,
            text="→",
            icon='TRIA_RIGHT'
        )

# Register and unregister functions
def register():
    bpy.utils.register_class(OBJECT_OT_prev)
    bpy.utils.register_class(OBJECT_OT_next)
    bpy.utils.register_class(VIEW3D_PT_object_toggle_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_prev)
    bpy.utils.unregister_class(OBJECT_OT_next)
    bpy.utils.unregister_class(VIEW3D_PT_object_toggle_panel)

if __name__ == "__main__":
    register()
