bl_info = {
    "name": "Blender Modular Asset Creator",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Justin Morand",
    "description": "Alternates between given modular options."
}

import bpy

current_object = None
index = 0
asset_location = [0.0, 0.0, 0.0]  # Default location

# Add a StringProperty to store the collection name
def get_collection_name(self):
    return self.collection_name

def set_collection_name(self, value):
    self.collection_name = value

# Créer les collections de bases et met 2 objets interchangables pour l'exemple
def create_base_workspace():
    collection = get_or_create_collection()
    data_collection = get_or_create_data_collection()

    if len(data_collection.objects) > 0:
        return

    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, -5))
    actual_obj = bpy.context.object  # Récupérer l'objet actif (celui qui vient d'être créé)
    data_collection.objects.link(actual_obj)
    bpy.context.scene.collection.objects.unlink(actual_obj)  # Retirer de Scene Collection

    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 2, -5))
    actual_obj = bpy.context.object 
    data_collection.objects.link(actual_obj)
    bpy.context.scene.collection.objects.unlink(actual_obj) 

def get_or_create_collection():
    collection_name = "temp_" + bpy.context.scene.collection_name 
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
    return collection

def get_or_create_data_collection():
    collection_name = bpy.context.scene.collection_name  
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

# Function to add an asset at the chosen location
def add_asset(obj):
    global current_object
    remove_previous_object()
    collection = get_or_create_collection()

    obj_copy = obj.copy()
    obj_copy.location = tuple(asset_location)
    collection.objects.link(obj_copy)   # add to collection

def get_collection_items(self, context):
    return [(col.name, col.name, "") for col in bpy.data.collections]

def update_collection(self, context):
    collection = bpy.data.collections.get(self.collection_picker)
    if collection:
        bpy.context.scene.collection_name = collection.name

# // ------------------------------------- OPERATORS ------------------------------------- \\ #
class COLLECTION_PICKER_PT_Panel(bpy.types.Panel):
    bl_label = "Collection Picker"
    bl_idname = "COLLECTION_PICKER_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Dropdown
        layout.prop(scene, "collection_picker", text="Select Collection")

class OBJECT_OT_create_workspace(bpy.types.Operator):
    bl_idname = "object.create_workspace"
    bl_label = "Create Workspace"
    bl_description = "Create the base workspace"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        create_base_workspace()
        return {'FINISHED'}

class OBJECT_OT_set_location_cursor(bpy.types.Operator):
    bl_idname = "object.set_location_cursor"
    bl_label = "Set Location to Cursor"
    bl_description = "Set asset location to the 3D cursor position"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global asset_location
        asset_location = list(bpy.context.scene.cursor.location)
        self.report({'INFO'}, f"Location set to: {asset_location}")
        return {'FINISHED'}


class OBJECT_OT_prev(bpy.types.Operator):
    bl_idname = "object.prev"
    bl_label = "Previous Object"
    bl_description = "Switch to the previous asset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_asset(get_previous_asset())
        return {'FINISHED'}

class OBJECT_OT_next(bpy.types.Operator):
    bl_idname = "object.next"
    bl_label = "Next Object"
    bl_description = "Switch to the next asset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_asset(get_next_asset())
        return {'FINISHED'}

# // ---------------------------------------- UI ---------------------------------------- \\ #
class VIEW3D_PT_object_toggle_panel(bpy.types.Panel):
    bl_label = "Modular Asset Creator"
    bl_idname = "VIEW3D_PT_object_toggle_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Create"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Instructions section
        layout.label(text="Instructions:")
        layout.label(text="1. Create a collection with all the switchable assets.")
        layout.label(text="2. Pick it with the dropdown below.")
        layout.label(text="3. Use the arrows to switch between assets.")

        # TODO add base collection picker
        layout.prop(scene, "collection_picker", text="Data Collection")

        col = layout.column()
        col.operator(OBJECT_OT_create_workspace.bl_idname, text="Create Workspace")

        layout.label(text="Switch between assets in the data collection")
        # Arrow buttons
        row = layout.row()
        row.operator(OBJECT_OT_prev.bl_idname, text="←")
        row.operator(OBJECT_OT_next.bl_idname, text="→")

        # Location selection options
        col2 = layout.column()
        col2.prop(context.scene, "cursor_location", text="Location Coordinates")
        col2.operator(OBJECT_OT_set_location_cursor.bl_idname, text="Set Location to Cursor")

# // ------------------------- Register and unregister functions --------------------------- \\ #
def register():
    bpy.types.Scene.collection_name = bpy.props.StringProperty(
        name="Collection Name",
        default="justin_plugin",  # Default name
    )

    bpy.utils.register_class(OBJECT_OT_create_workspace)
    bpy.utils.register_class(OBJECT_OT_prev)
    bpy.utils.register_class(OBJECT_OT_next)
    bpy.utils.register_class(OBJECT_OT_set_location_cursor)
    bpy.utils.register_class(VIEW3D_PT_object_toggle_panel)

    bpy.types.Scene.collection_picker = bpy.props.EnumProperty(
        name="Collection Picker",
        description="Pick a collection from the scene",
        items=get_collection_items,  # dynamic update collection list
        update=update_collection,
    )

    bpy.utils.register_class(COLLECTION_PICKER_PT_Panel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_create_workspace)
    bpy.utils.unregister_class(OBJECT_OT_prev)
    bpy.utils.unregister_class(OBJECT_OT_next)
    bpy.utils.unregister_class(OBJECT_OT_set_location_cursor)
    bpy.utils.unregister_class(VIEW3D_PT_object_toggle_panel)
    del bpy.types.Scene.collection_name

    bpy.utils.unregister_class(COLLECTION_PICKER_PT_Panel)
    del bpy.types.Scene.collection_picker

if __name__ == "__main__":
    register()
