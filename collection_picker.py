bl_info = {
    "name": "Collectio Picker",
    "blender": (2, 82, 0),
    "category": "Object",
}

import bpy

def get_collection_items(self, context):
    return [(col.name, col.name, "") for col in bpy.data.collections]

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


def update_collection(self, context):
    collection = bpy.data.collections.get(self.collection_picker)
    if collection:
        # Do shits
        print(f"Selected collection: {collection.name}")


def register():
    bpy.types.Scene.collection_picker = bpy.props.EnumProperty(
        name="Collection Picker",
        description="Pick a collection from the scene",
        items=get_collection_items,  # dynamic update collection list
        update=update_collection,
    )

    bpy.utils.register_class(COLLECTION_PICKER_PT_Panel)


def unregister():
    bpy.utils.unregister_class(COLLECTION_PICKER_PT_Panel)
    del bpy.types.Scene.collection_picker


if __name__ == "__main__":
    register()
