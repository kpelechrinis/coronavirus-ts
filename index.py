from bokeh.layouts import layout, row, column
from bokeh.plotting import save, figure, output_file, show, Column
from bokeh.models.glyphs import Text, ImageURL
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource,Arrow, OpenHead, NormalHead, VeeHead, HoverTool, Div
from bokeh.models.widgets.buttons import Button
from bokeh.models import Tabs, Panel
from bokeh.models.widgets import Slider,Select,PreText,Dropdown,TextInput,AutocompleteInput,CheckboxGroup,RadioGroup,RangeSlider
from bokeh.transform import cumsum
from scipy.misc import imread
from bokeh.io import curdoc
import pandas as pd
import numpy as np

########### Dropbdown countries ###########

def check_dropdown_update_country(attr, old, new):
	global confirmed
	global panels
	global deaths
	global recovered
	global dates 
	global tot_confirmed,tot_recovered,tot_recovered, data_df

	if dropdown_countries.value == "World":
		tot_confirmed = [sum(confirmed[d]) for d in dates]
		tot_deaths = [sum(deaths[d]) for d in dates]
		tot_recovered = [sum(recovered[d]) for d in dates]
	else:
		reg = dropdown_countries.value.split(": ")
		if (len(reg) == 1):
			confirmed_filter = confirmed[confirmed['Country/Region'] == dropdown_countries.value]
			deaths_filter = deaths[deaths['Country/Region'] == dropdown_countries.value]
			recovered_filter = recovered[recovered['Country/Region'] == dropdown_countries.value]
		else:
			confirmed_filter = confirmed[(confirmed['Country/Region'] == reg[0]) & (confirmed['Province/State'] == reg[1])]
			deaths_filter = deaths[(deaths['Country/Region'] == reg[0]) & (deaths['Province/State'] == reg[1])]
			recovered_filter = recovered[(recovered['Country/Region'] == reg[0]) & (recovered['Province/State'] == reg[1])]
		tot_confirmed = [sum(confirmed_filter[d]) for d in dates]
		tot_deaths = [sum(deaths_filter[d]) for d in dates]
		dates_recovered = list(recovered.columns[4:len(recovered.columns)])
		tot_recovered = [sum(recovered_filter[d]) for d in dates_recovered]
		if len(tot_recovered) != len(tot_confirmed):
			tot_recovered = tot_recovered + ["-"]
    	
	panels = []
	for axis_type in ["linear", "log"]:
		p = figure(plot_width=1000, plot_height=550, y_axis_type = axis_type, x_axis_type="datetime", title="COVID-19 cumulative data (@kpelechrinis) ")
		panel = Panel(child=p, title=axis_type)
		panels.append(panel)
		tabs = Tabs(tabs=panels)
		data_df = pd.DataFrame({'Date':dates, 'Confirmed': tot_confirmed, 'Deaths': tot_deaths, 'Recovered': tot_recovered})
		data_df['Date'] = pd.to_datetime(data_df['Date'])
		p.line(x=data_df['Date'], y=tot_confirmed, line_width=4, color="red", alpha=0.8,legend="Confirmed")
		p.line(x=data_df['Date'], y=tot_deaths, line_width=4, color="black", alpha=0.8,legend="Deaths")
		p.line(x=data_df['Date'], y=tot_recovered, line_width=4, color="green", alpha=0.8,legend="Recovered")
		p.legend.location = "top_left"
		nsource = ColumnDataSource({
			'Date': list(dates), 'Confirmed': list(data_df['Confirmed']), 'Deaths': list(data_df['Deaths']), 'Recovered': list(data_df['Recovered'])
		})
	columns = [TableColumn(field="Date", title="Date"),
		TableColumn(field="Confirmed", title="Confirmed"),
		TableColumn(field="Deaths", title="Deaths"),
		TableColumn(field="Recovered",title="Recovered")]
	table = DataTable(source=nsource, columns=columns, editable=True, height=550)
	layout.children[1] = tabs
	layout.children[3] = table

global confirmed
global deaths
global recovered 
global panels
global dates
global tot_confirmed,tot_deaths,tot_recovered,data_df

#confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
#deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
#recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")

confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")


dates = list(confirmed.columns[4:len(confirmed.columns)])
tot_confirmed = [sum(confirmed[d]) for d in dates]
tot_deaths = [sum(deaths[d]) for d in dates]
dates_recovered = list(recovered.columns[4:len(recovered.columns)])
tot_recovered = [sum(recovered[d]) for d in dates_recovered] 

if len(tot_recovered) != len(tot_confirmed):
	tot_recovered = tot_recovered + ["-"]

panels = []

for axis_type in ["linear", "log"]:
	p = figure(plot_width=1000, plot_height=550, y_axis_type = axis_type, x_axis_type="datetime", title="COVID-19 cumulative data (@kpelechrinis)")
	panel = Panel(child=p, title=axis_type)
	panels.append(panel)
	tabs = Tabs(tabs=panels)
	data_df = pd.DataFrame({'Date':dates, 'Confirmed': tot_confirmed, 'Deaths': tot_deaths, 'Recovered': tot_recovered})
	data_df['Date'] = pd.to_datetime(data_df['Date'])
	p.line(x=data_df['Date'], y=data_df['Confirmed'],  line_width=4, color="red", alpha=0.8, legend="Confirmed")
	p.line(x=data_df['Date'], y=data_df['Deaths'],  line_width=4, color="black", alpha=0.8, legend="Deaths")
	p.line(x=data_df['Date'], y=data_df['Recovered'],  line_width=4, color="green", alpha=0.8, legend="Recovered")
	p.legend.location = "top_left"

	source = ColumnDataSource({
		'Date': list(dates), 'Confirmed': list(data_df['Confirmed']), 'Deaths': list(data_df['Deaths']), 'Recovered': list(data_df['Recovered'])
	})

columns = [TableColumn(field="Date", title="Date"),
           TableColumn(field="Confirmed", title="Confirmed"),
           TableColumn(field="Deaths", title="Deaths"),
           TableColumn(field="Recovered",title="Recovered")]

table = DataTable(source=source, columns=columns, editable=True, height=550)

#############################
logo = imread("pitt-sci.png")
## there is a bug in bokeh image_rgba to be used later that requires the following flipping
## https://github.com/bokeh/bokeh/issues/1666
logo = logo[::-1]
plogo = figure(x_range=(0,25),y_range=(0,15), tools = [], plot_width=450,plot_height=350)
plogo.xgrid.grid_line_color = None
plogo.ygrid.grid_line_color = None
plogo.image_rgba(image=[logo],x=[0], y=[0], dw = [25], dh = [15])
plogo.xaxis.visible = False
plogo.yaxis.visible = False

div1 = Div(text="""<font size=6><b><h>Coronavirus data</b></h></font></br></br><font size=5>This is a simple time-series visualization of the confirmed cases, deaths and recoveries from the coronavirus according to the <a href="https://github.com/CSSEGISandData/COVID-19">Johns Hopkins dataset</a> that is updated daily. The data are updated automatically (approximately once every day). <br><br>Visualization from, K. Pelechrinis (@kpelechrinis) - School of Computing and Information, University of Pittsburgh. </font><br></br></br><br></br></br>""",width=800, height=250)

menu_countries = ["World"]+list(np.sort(list(confirmed['Country/Region'].unique())))
menu_china = list(np.sort(list(confirmed[confirmed['Country/Region'] == "China"]['Province/State'].unique())))
menu_china = ["China: "+m for m in menu_china]
#menu_us = list(np.sort(list(confirmed[confirmed['Country/Region'] == "US"]['Province/State'].unique())))
#menu_us = ["US: "+m for m in menu_us]
menu_canada = list(np.sort(list(confirmed[confirmed['Country/Region'] == "Canada"]['Province/State'].unique())))
menu_canada = ["Canada: "+m for m in menu_canada]
menu_australia = list(np.sort(list(confirmed[confirmed['Country/Region'] == "Australia"]['Province/State'].unique())))
menu_australia = ["Australia: "+m for m in menu_australia]
dropdown_countries = Select(title = "Country/Region", value = "World", options = menu_countries+menu_china+menu_canada+menu_australia)
dropdown_countries.on_change('value',check_dropdown_update_country)

layout = layout([[div1,plogo],[tabs,],[dropdown_countries,],[table,]])
curdoc().add_root(layout)
