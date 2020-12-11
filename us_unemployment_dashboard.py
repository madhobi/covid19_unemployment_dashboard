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
import math

output_file('us_unemployment_dashboard.html')

us_states_df = pd.DataFrame(us_states).T
us_states_df = us_states_df[~us_states_df["name"].isin(['Alaska', "Hawaii"])]
del us_states_df['lons']
del us_states_df['lats']
us_states_df = us_states_df.reset_index()
us_states_df = us_states_df.rename({'index':'State'}, axis='columns')

del us_states["HI"]
del us_states["AK"]
del us_states["DC"]
state_xs = [us_states[code]['lons'] for code in us_states]
state_ys = [us_states[code]['lats'] for code in us_states]

unemployment_by_state = pd.read_csv('unemployment_by_state_2020.csv')
print(unemployment_by_state.head())
unemployment_by_state = unemployment_by_state[~unemployment_by_state['State'].isin(['AK', 'HI'])]
unemployment_by_state = unemployment_by_state.reset_index()
unemployment_by_state = pd.merge(us_states_df, unemployment_by_state, on='State')
unemployment_by_state['unemployment_rate'] = unemployment_by_state['January']

data_vulnerability = pd.read_csv('VulnerabilityIndexByStateUPDATED.csv')
data_vulnerability = pd.merge(us_states_df, data_vulnerability, on='State')
data_vulnerability['vulnerability_index'] = data_vulnerability['January']

###################### Start US Map #####################

source_unemployment = ColumnDataSource(
    data = dict(
        lons=state_xs,
        lats=state_ys,
        name=unemployment_by_state.name.values.tolist(),
        unemployment_rate=unemployment_by_state.January.values.tolist(),        
        January=unemployment_by_state.January.values.tolist(),
        February=unemployment_by_state.February.values.tolist(),
        March=unemployment_by_state.March.values.tolist(),
        April=unemployment_by_state.April.values.tolist(),
        May=unemployment_by_state.May.values.tolist(),
        June=unemployment_by_state.June.values.tolist(),
        July=unemployment_by_state.July.values.tolist(),
        August=unemployment_by_state.August.values.tolist(),
        September=unemployment_by_state.September.values.tolist(),               
    )
)

source_vulnerability_index = ColumnDataSource(
    data = dict(
        lons=state_xs,
        lats=state_ys,
        name=data_vulnerability.name.values.tolist(),
        vulnerability_index=data_vulnerability.January.values.tolist(),        
        January=data_vulnerability.January.values.tolist(),
        February=data_vulnerability.February.values.tolist(),
        March=data_vulnerability.March.values.tolist(),
        April=data_vulnerability.April.values.tolist(),
        May=data_vulnerability.May.values.tolist(),
        June=data_vulnerability.June.values.tolist(),
        July=data_vulnerability.July.values.tolist(),
        August=data_vulnerability.August.values.tolist(),
        September=data_vulnerability.September.values.tolist(),               
    )
)

palette = brewer['OrRd'][8]
palette = palette[::-1]
#color_mapper = LinearColorMapper(palette = palette, low = merged_df.unemployment_rate.min(), high = merged_df.unemployment_rate.max())
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 25)
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20,
                         location=(0,0), orientation='horizontal')

map_unemployment = figure(plot_width=500, plot_height=300,
             title="Unemployment Rate Per State (US 2020)",
             x_axis_location=None, y_axis_location=None,
             tooltips=[
                        ("Name", "@name"), ("Unemployment Rate", "@unemployment_rate"), ("(Long, Lat)", "($x, $y)")
                      ])

map_unemployment.patches("lons", "lats", source=source_unemployment,
            fill_color={'field': 'unemployment_rate', 'transform': color_mapper},
            fill_alpha=0.7, line_color="black", line_width=0.5)

map_unemployment.grid.grid_line_color = None
map_unemployment.add_layout(color_bar, 'below')

usmap_tab1 = Panel(child=map_unemployment, title='State Wide Unemployment')


palette_vindex = brewer['GnBu'][8]
palette_vindex = palette_vindex[::-1]
color_mapper_vindex = LinearColorMapper(palette = palette_vindex, low = 0, high = 20)
color_bar_vindex = ColorBar(color_mapper=color_mapper_vindex, label_standoff=8, width=500, height=20,
                         location=(0,0), orientation='horizontal')

map_vindex = figure(plot_width=500, plot_height=300,
             title="vulnerability Index Per State (US 2020)",
             x_axis_location=None, y_axis_location=None,
             tooltips=[
                        ("Name", "@name"), ("Vulnerability Index", "@vulnerability_index"), ("(Long, Lat)", "($x, $y)")
                      ])

map_vindex.patches("lons", "lats", source=source_vulnerability_index,
            fill_color={'field': 'vulnerability_index', 'transform': color_mapper_vindex},
            fill_alpha=0.7, line_color="black", line_width=0.5)

map_vindex.grid.grid_line_color = None
map_vindex.add_layout(color_bar_vindex, 'below')

usmap_tab2 = Panel(child=map_vindex, title='State Wide Vunerability Index')

callback_slider = CustomJS(args={'source':source_unemployment, 'source2':source_vulnerability_index}, code="""
var f = cb_obj.value;
var data = source.data
var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]
data['unemployment_rate'] = data[months[f-1]]
source2.data['vulnerability_index'] = source2.data[months[f-1]]
source.change.emit()
source2.change.emit()
""")

slider = Slider(title = 'Month',start = 1, end = 9, step = 1, value = 1, width = 500)
slider.js_on_change('value', callback_slider)

usmap_tabs = Tabs(tabs=[usmap_tab1, usmap_tab2 ])

###################### End US Map #####################


us_monthly_unemployment = pd.read_csv('monthly_unemployment_rate_us_2020.csv')
print(us_monthly_unemployment.head())

###################### Start Bar Chart #####################

bar_chart1 = figure(x_range=us_monthly_unemployment['Month'], plot_width=730, plot_height=430,
                title = 'Nationwide Unemployment Data(US 2020)',
                tooltips=[('Rate', '@Rate')])
bar_chart1.vbar(x = 'Month',
            top = 'Rate',
            source = us_monthly_unemployment,
            fill_color = 'tomato', line_color='tomato', alpha=0.9, width=0.5)
bar_chart1.xaxis.axis_label = 'Month'
bar_chart1.yaxis.axis_label = 'Monthly Unemployment Rate'
tab1 = Panel(child=bar_chart1, title='Total Unemployment')

bar_chart2 = figure(x_range=us_monthly_unemployment['Month'], plot_width=730, plot_height=400,
                title = 'Nationwide Unemployment Data (US 2020)')
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

####################### End Bar Chart #######################
#show(bar_chart)

###################### Start Line Chart #####################

data_unemployment = pd.read_csv('unemployment_by_state_2020.csv', index_col='State')
print(data_unemployment.head())
data_unemployment_t = data_unemployment.T
print(data_unemployment_t.head())

data_covid_case = pd.read_csv('covid_by_state_2020.csv', index_col='State')
print(data_covid_case.head())
data_covid_case_t = data_covid_case.T
print(data_covid_case_t.head())

source_unemployment = ColumnDataSource(data=data_unemployment_t)
source_covid_case = ColumnDataSource(data=data_covid_case_t)

Curr = ColumnDataSource(
    data = dict(
        Month = [1,2,3,4,5,6,7,8,9],            
        Unemployment_rate = data_unemployment_t['AL'],
        Covid_count = data_covid_case_t['AL']
    )
)

#plot and the menu is linked with each other by this callback function
callback_dropdown = CustomJS(args=dict(source1=source_unemployment, source2=source_covid_case, sc=Curr), code="""
var f = cb_obj.value
sc.data['Unemployment_rate'] = source1.data[f] 
sc.data['Covid_count'] = source2.data[f]
sc.change.emit();
""")
state_menu = Select(options=list(data_unemployment.index.values),value='AL', title = 'State', width = 500)  # drop down menu
unemployment_line_graph=figure(plot_width=500, plot_height=300, x_axis_label ='Month', y_axis_label = 'Unemployment Rate (in %)',
tooltips=[('Unemployment Rate', '@Unemployment_rate')],
title='Unemployment Info on Selected State') #creating figure object 
unemployment_line_graph.line(x='Month', y='Unemployment_rate', color='red', source=Curr)
unemployment_line_graph.xaxis.ticker = [1, 2, 3, 4, 5, 6, 7, 8, 9]

covid_line_graph=figure(plot_width=500, plot_height=300, x_axis_label ='Month', y_axis_label = 'Covid Count',
tooltips=[('COVID Cases', '@Covid_count')],
title='COVID Cases on Selected State')
covid_line_graph.line(x='Month', y='Covid_count', color='red', source=Curr)
covid_line_graph.xaxis.ticker = [1, 2, 3, 4, 5, 6, 7, 8, 9]

state_menu.js_on_change('value', callback_dropdown)



###################### End Line Chart #####################

################## Start Income Change Chart ##############

data_income = pd.read_csv('IndustryByUS.csv')
#print(data.head())
data_earning_by_industry = data_income.iloc[23:51]
data_earning_by_industry['change_in_quarter'] = data_earning_by_industry['20Q1Change']
bar_color = []
for x in data_earning_by_industry['20Q1Change']:
    if x > 0:
        bar_color.append('green')
    else:
        bar_color.append('tomato')
print(bar_color)
data_earning_by_industry['bar_color'] = bar_color
#print(data_earning_by_industry)

#color_mapper = LogColorMapper(palette=palette)
source_income_change = ColumnDataSource(data_earning_by_industry)

quarters = ['19Q1Change', '19Q2Change', '19Q3Change', '19Q4Change', '20Q1Change', '20Q2Change']

bar_chart_income = figure(x_range=data_earning_by_industry['Description'], plot_width=730, plot_height=550,
                title = 'Change in Income by Industry in US 2020',                
                tooltips=[('Industry Name', '@Description')]
                )
bar_chart_income.vbar(x = 'Description',
            top = 'change_in_quarter',
            source = source_income_change,
            fill_color = 'bar_color', line_color='tomato', alpha=0.9, width=0.5)
bar_chart_income.xaxis.axis_label = 'Industry'
bar_chart_income.yaxis.axis_label = 'Change in the income'

callback_quarter = CustomJS(args=dict(sc=source_income_change), code="""
var f = cb_obj.value
sc.data['change_in_quarter'] = sc.data[f]
var x;
var color = [];
for (x of sc.data[f]) {
    if (x > 0) {
        color.push('green');
    } else {
        color.push('tomato');
    }
}
sc.data['bar_color'] = color;
sc.change.emit();
""")
menu_quarter = Select(options=list(quarters),value='20Q1Change', title = 'Select Quarter')  # drop down menu
menu_quarter.js_on_change('value', callback_quarter) # calling the function on change of selection

bar_chart_income.xaxis.major_label_orientation = math.pi/4

################## End Income Change Chart ##############

layout = column(row(slider, state_menu), row(usmap_tabs, unemployment_line_graph, covid_line_graph), row(tabs, column(menu_quarter,bar_chart_income)))
show(layout)
