bl_info = {
    "name": "Match Render Size to Selected Image",
    "author": "Hideki Saito",
    "version": (1, 2),
    "blender": (3, 0, 0),
    "location": "Compositor > N-Panel > Render Tools",
    "description": "Set render resolution to match selected image node size",
    "category": "Render",
}

import bpy
from bpy.app.translations import pgettext_iface as _

# =========================================================
# Operator
# =========================================================

class MATCHRENDER_OT_from_image(bpy.types.Operator):
    bl_idname = "render.match_size_from_image"
    bl_label = "Match Render Size to Image"
    bl_description = "Set render resolution to match the selected image node"

    def execute(self, context):
        node = context.active_node

        if not node or node.bl_idname != "CompositorNodeImage":
            self.report({'ERROR'}, _("Select an Image node in the compositor"))
            return {'CANCELLED'}

        img = node.image
        if not img:
            self.report({'ERROR'}, _("Image node has no image loaded"))
            return {'CANCELLED'}

        width, height = img.size

        scene = context.scene
        scene.render.resolution_x = width
        scene.render.resolution_y = height

        self.report({'INFO'}, f"{_('Render size set to')} {width} x {height}")
        return {'FINISHED'}


# =========================================================
# Panel
# =========================================================

class MATCHRENDER_PT_panel(bpy.types.Panel):
    bl_label = "Render Tools"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Render Tools"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space and space.tree_type == 'CompositorNodeTree'

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "render.match_size_from_image",
            text=_("Match Render Size to Image"),
            icon="IMAGE_DATA"
        )


# =========================================================
# Translation Dictionary（日本語）
# =========================================================

translation_dict = {
    "ja_JP": {
        # Operator ラベル・説明
        ("*", "Match Render Size to Image"): "画像サイズにレンダー解像度を合わせる",
        ("*", "Set render resolution to match the selected image node"):
            "選択中の画像ノードの解像度にレンダー設定を合わせます",

        # メッセージ類
        ("*", "Select an Image node in the compositor"): "コンポジットで画像ノードを選択してください",
        ("*", "Image node has no image loaded"): "画像ノードに画像が読み込まれていません",
        ("*", "Render size set to"): "レンダー解像度を設定しました：",

        # パネル名・カテゴリ
        ("*", "Render Tools"): "レンダーツール",
    }
}


# =========================================================
# Register
# =========================================================

classes = (
    MATCHRENDER_OT_from_image,
    MATCHRENDER_PT_panel,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.app.translations.register(__name__, translation_dict)

def unregister():
    bpy.app.translations.unregister(__name__)
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()
