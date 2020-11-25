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

slider = Slider(title = 'Month',start = 1, end = 10, step = 1, value = 1, width = 500)
slider.js_on_change('value', callback)
#month_list = ['January', 'February', 'March', 'April', 'May', 'June']
#month_select = Select(title='Select Month',value='March',options=month_list)
#month_select = pnw.Select(name='dataset',options=month_list)
#month_select.js_on_change('value', callback)
#month_select.param.watch(update_plot,'value')

us_monthly_unemployment = pd.read_csv('monthly_unemployment_rate_us_2020.csv')
print(us_monthly_unemployment.head())

bar_chart1 = figure(x_range=us_monthly_unemployment['Month'], plot_height=500,
                title = 'Monthly Unemployment in US 2020',
                tooltips=[('Rate', '@Rate')])
bar_chart1.vbar(x = 'Month',
            top = 'Rate',
            source = us_monthly_unemployment,
            fill_color = 'tomato', line_color='tomato', alpha=0.9, width=0.5)
bar_chart1.xaxis.axis_label = 'Month'
bar_chart1.yaxis.axis_label = 'Monthly Unemployment Rate'
tab1 = Panel(child=bar_chart1, title='Total Unemployment')

bar_chart2 = figure(x_range=us_monthly_unemployment['Month'], plot_height=500,
                title = 'Monthly Unemployment in US 2020')
bar_chart2.vbar(x=dodge('Month', -0.25, range=bar_chart2.x_range), top='Men_rate', width=0.2, source=us_monthly_unemployment,
       color="#718dbf", legend_label="Men")
bar_chart2.vbar(x=dodge('Month', 0.0, range=bar_chart2.x_range), top='Women_rate', width=0.2, source=us_monthly_unemployment,
       color="#e84d60", legend_label="Women")
bar_chart2.xaxis.axis_label = 'Month'
bar_chart2.yaxis.axis_label = 'Monthly Unemployment Rate'
bar_chart2.x_range.range_padding = 0.1
bar_chart2.xgrid.grid_line_color = None
bar_chart2.legend.location = "top_left"
bar_chart2.legend.orientation = "horizontal"
tab2 = Panel(child=bar_chart2, title='Unemployment by Gender')

tabs = Tabs(tabs=[ tab1, tab2 ])
#show(bar_chart)


#layout = column(month_select, fig)
layout = column(slider, row(fig, tabs))
#show(fig)
show(layout)
