import dearpygui.dearpygui as dpg

import DearPyGui_DragAndDrop as dpg_dnd

dpg.create_context()
dpg_dnd.initialize()
dpg.create_viewport(title="Drag and drop example", width=600, height=600)


def drop(data, keys):
    print(f'{data}')
    print(f'{keys}')


dpg_dnd.set_drop(drop)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

