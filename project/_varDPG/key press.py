from dearpygui.dearpygui import *
show_logger()
show_debug()
add_text('enter your name:')
add_input_text('##name_input')

set_render_callback("poll_callback")

def poll_callback(sender, data):
    if is_key_pressed(mvKey_Return) and is_item_active("##name_input"):
        log_debug("Do Something here")
        #Do Something here
start_dearpygui()