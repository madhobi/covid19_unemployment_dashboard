from bokeh.models import LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.sampledata.us_states import data as us_states
from bokeh.plotting import figure, show, output_file
from bokeh.models import Slider, HoverTool, Select, CustomJS, ColumnDataSource
from bokeh.layouts import widgetbox, row, column
from bokeh.transform import dodge
from bokeh.models.widgets import Panel, Tabs
import pandas as pd
import numpy as np

# https://realpython.com/python-data-visualization-bokeh/

output_file('us_unemployment_dashboard.html')

us_states_df = pd.DataFrame(us_states).T
us_states_df = us_states_df[~us_states_df["name"].isin(['Alaska', "Hawaii"])]
us_states_df["lons"] = us_states_df.lons.values.tolist()
us_states_df["lats"] = us_states_df.lats.values.tolist()
us_states_df = us_states_df.reset_index()
us_states_df["unemployment_rate"] = np.random.randint(3,20,size=len(us_states_df))

print(us_states_df.head())

del us_states["HI"]
del us_states["AK"]
state_xs = [us_states[code]['lons'] for code in us_states]
state_ys = [us_states[code]['lats'] for code in us_states]

state_count = len(us_states_df)
source = ColumnDataSource(
    data = dict(
        lons=state_xs,
        lats=state_ys,
        name=us_states_df.name.values.tolist(),
        unemployment_rate=us_states_df.unemployment_rate.values.tolist(),        
        January=(np.random.randint(3,20,size=state_count)).tolist(),
        February=(np.random.randint(3,20,size=state_count)).tolist(),
        March=(np.random.randint(3,20,size=state_count)).tolist(),
        April=(np.random.randint(3,20,size=state_count)).tolist(),
        May=(np.random.randint(3,20,size=state_count)).tolist(),
        June=(np.random.randint(3,20,size=state_count)).tolist(),
        July=(np.random.randint(3,20,size=state_count)).tolist(),
        August=(np.random.randint(3,20,size=state_count)).tolist(),
        September=(np.random.randint(3,20,size=state_count)).tolist(),
        October=(np.random.randint(3,20,size=state_count)).tolist(),        
    )
)

palette = brewer['OrRd'][8]
palette = palette[::-1]
color_mapper = LinearColorMapper(palette = palette, low = us_states_df.unemployment_rate.min(), high = us_states_df.unemployment_rate.max())
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20,
                         location=(0,0), orientation='horizontal')

fig = figure(plot_width=700, plot_height=500,
             title="United States Unemployment Rate Per State",
             x_axis_location=None, y_axis_location=None,
             tooltips=[
                        ("Name", "@name"), ("Unemployment Rate", "@unemployment_rate"), ("(Long, Lat)", "($x, $y)")
                      ])

fig.grid.grid_line_color = None

fig.patches("lons", "lats", source=source,
            fill_color={'field': 'unemployment_rate', 'transform': color_mapper},
            fill_alpha=0.7, line_color="white", line_width=0.5)



fig.add_layout(color_bar, 'below')

callback = CustomJS(args={'source':source}, code="""
var f = cb_obj.value;
var data = source.data
var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]
data['unemployment_rate'] = data[months[f-1]]
source.change.emit()
""")


slider = Slider(title = 'Month', start = 1, end = 10, step = 1, value = 1, width = 500)
slider.js_on_change('value', callback)
#month_select = Select(title='Select Month',value='March',options=month_list)
#month_select = pnw.Select(name='dataset',options=month_list)
#month_select.js_on_change('value', callback)
#month_select.param.watch(update_plot,'value')


# Puts slider and map figure in same frame
layout = column(slider, row(fig))
# Displays figure in HTML page
show(layout)

