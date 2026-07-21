import dearpygui.dearpygui as dpg
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

def create_plot():
    with dpg.plot(tag="plot", parent="window", label="Plot",
                  width=600, height=400,
                  query=True,
                  callback=query_callback):

        x_axis = dpg.add_plot_axis(dpg.mvXAxis, tag="x_axis")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, tag="y_axis")

        dpg.add_line_series(x.tolist(), y.tolist(), parent="y_axis")

def recreate_plot():
    dpg.delete_item("plot")
    create_plot()

def query_callback(sender, app_data):
    (xmin, xmax, ymin, ymax) = app_data[0]

    mask = (
        (x >= xmin) & (x <= xmax) &
        (y >= ymin) & (y <= ymax)
    )

    print(f"Selected {mask.sum()} points")

    # Remove the query rectangle
    recreate_plot()

dpg.create_context()

with dpg.window(tag="window"):
    create_plot()

dpg.create_viewport(title="Recreate Plot")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()