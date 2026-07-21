import dearpygui.dearpygui as dpg

def update():
    if dpg.is_item_hovered("plot"):
        x, y = dpg.get_plot_mouse_pos()
        print(f"x={x:.3f}, y={y:.3f}")

dpg.create_context()

with dpg.window():
    dpg.add_text("", tag="mouse_text")

    with dpg.plot(tag="plot", width=600, height=400):
        x_axis = dpg.add_plot_axis(dpg.mvXAxis)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis)

dpg.create_viewport()
dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    update()
    dpg.render_dearpygui_frame()

dpg.destroy_context()