import bpy
import time

bl_info = {
    "name" : "Render Texts",
    "author" : "Julian Baker (Baked.blend)",
    "description" : "Sends updates to your phone about render progressc via NTFY",
    "blender" : (3, 60, 2),
    "version" : (2, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Render"
}
    
class Variables(bpy.types.PropertyGroup):
    first_frame = bpy.props.IntProperty(
        name="first_frame",
        description="Sample variable 1",
        default=2
    )
    last_frame = bpy.props.IntProperty(
        name="last_frame",
        description="Sample variable 1",
        default=2
    )
    current_frame = bpy.props.IntProperty(
        name="current_frame",
        description="Sample variable 1",
        default=2
    )
    comp_perc = bpy.props.IntProperty(
        name="comp_perc",
        description="Sample variable 1",
        default=2
    )

    
    
    
class SettingsPanel(bpy.types.Panel):
    bl_label = "Render Text Settings"
    bl_idname = "PT_CustomRenderSettings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Render Text Settings'
            

        
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        first_frame = bpy.context.scene.frame_start
        total_frames = bpy.context.scene.frame_end - first_frame
        current_frame = bpy.context.scene.frame_current
        global comp_perc
        comp_perc = (current_frame - first_frame) / total_frames * 100
        
        # Settings Panel
        layout.label(text="Settings for render notifications")
        layout.prop(scene, "Note_Tog", text="Enable Notifications")
        

        
        if scene.Note_Tog:
            layout.prop(scene, "notification_option", text="Interval")
            layout.label(text="Scene Info:")
            layout.label(text="Total Frames: " + str(total_frames))
            layout.label(text="Current Frame: " + str(current_frame))
            layout.label(text="Completion: " + str(int(comp_perc)) + "%")
            
            
        else:
            layout.label(text="Notifications Disabled")
            
            
def render_post_handler(scene):
    print("Percent Complete:")
    print(int(comp_perc))
    
def register():
    bpy.utils.register_class(SettingsPanel)
    bpy.utils.register_class(Variables)
    bpy.app.handlers.render_post.append(render_post_handler)
    
    notification_option = bpy.props.EnumProperty(
        name="Notification Option",
        items=[("25", "Every 25%", "Notify at 25% progress"),
               ("50", "Every 50%", "Notify at 50% progress"),
               ("100", "Only at the end", "Notify only when rendering is complete")],
        default="100"
    )
    Note_Tog = bpy.props.BoolProperty(
        name="Enable/Disable Notifications",
        description="Enables or Disables Notifications",
        default=True
    )

# Custom properties for Toggle
bpy.types.Scene.Note_Tog = bpy.props.BoolProperty(
    name="Enable/Disable Notifications",
    description="Enables or Disables Notifications",
    default=True
)
    # Toggle Functionality
def Note_Tog(self, context):
    scene = context.scene
    scene.Note_Tog = not scene.Note_Tog
    if scene.my_custom_bool:
        print("Notifications enabled")
        return True
    else:
        print("Notifications disabled")
        return False

def unregister():
    bpy.utils.unregister_class(SettingsPanel)
    bpy.utils.unregister_class(Variables)
    bpy.app.handlers.render_post.remove(render_post_handler)

if __name__ == '__main__':
    register()