bl_info = {
    "name" : "Render Texts",
    "author" : "Julian Baker (Baked.blend)",
    "description" : "Sends updates to your phone about render progressc via NTFY",
    "blender" : (3, 60, 2),
    "version" : (0, 6, 0),
    "location" : "",
    "warning" : "",
    "category" : "Render"
}

import bpy
import requests

class SettingsPanel(bpy.types.Panel):
    bl_label = "Render Text Settings"
    bl_idname = "PT_CustomRenderSettings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Render Text Settings'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Settings Panel
        layout.label(text="Settings for render notifications")
        layout.prop(scene, "Note_Tog", text="Enable Notifications")
        
        total_frames = bpy.context.scene.frame_end
        current_frame = bpy.context.scene.frame_current
        comp_perc = current_frame / total_frames * 100
        
        if scene.Note_Tog:
            layout.prop(scene, "notification_option", text="Interval")
            layout.label(text="Scene Info:")
            layout.label(text="Total Frames: " + str(total_frames))
            layout.label(text="Current Frame: " + str(current_frame))
            layout.label(text="Completion: " + str(int(current_frame / total_frames * 100)) + "%")
            
        else:
            layout.label(text="Notifications Disabled")

          
def render_complete_handler(scene):
# This function will be called when a render completes
    print("Frame complete")
    if scene.Note_Tog:
        #SettingsPanel.draw(self, context)
        # Update the notification option based on the chosen value
        if scene.notification_option == "25":
            if comp_perc == 25 or 50 or 75 or 99:
                mess_out = "Render is now " + str(comp_perc) + "% complete!"
                notify(mess_out)
        elif scene.notification_option == "50":
            if comp_perc == 50 or 99:
                mess_out = "Render is now " + str(comp_perc) + "% complete!"
                notify(mess_out)
        else:
            if comp_perc == 99:
                notify("Render complete!")
                
  
# Main Toggle On and Off
def Note_Tog(self, context):
    scene = context.scene
    scene.Note_Tog = not scene.Note_Tog
    if scene.my_custom_bool:
        print("Notifications enabled")
        return True
    else:
        print("Notifications disabled")
        return False

# Custom properties for Toggle
bpy.types.Scene.Note_Tog = bpy.props.BoolProperty(
    name="Enable/Disable Notifications",
    description="Enables or Disables Notifications",
    default=True,
    update=Note_Tog
)

    
# Main Notification Code!!
def notify(message):
    print(message)
    #requests.post("https://ntfy.sh/mytopic", data = message)


def register():
    # Render Complete Handler
    bpy.app.handlers.render_complete.append(render_complete_handler)
    
    # Settings Panel
    bpy.utils.register_class(SettingsPanel)
    
    # Interval Options Enum
    bpy.types.Scene.notification_option = bpy.props.EnumProperty(
        name="Notification Option",
        items=[("25", "Every 25%", "Notify at 25% progress"),
               ("50", "Every 50%", "Notify at 50% progress"),
               ("100", "Only at the end", "Notify only when rendering is complete")],
        default="100"
    )
    bpy.types.Scene.notification_interval = bpy.props.FloatProperty(
        name="Notification Interval",
        description="Set the notification interval as a percentage",
        default=1.0,
        min=0.0,
        max=1.0
    )
    
def unregister():
    bpy.app.handlers.render_complete.remove(render_complete_handler)
    bpy.utils.unregister_class(SettingsPanel)
    del bpy.types.Scene.notification_option
    del bpy.types.Scene.notification_interval
    
if __name__ == "__main__":
    register()