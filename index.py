from sklearn.model_selection import train_test_split
from bokeh.layouts import layout, row, column
from bokeh.plotting import save, figure, output_file, show, Column
from bokeh.models.glyphs import Text, ImageURL
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource,Arrow, OpenHead, NormalHead, VeeHead, HoverTool, Div
from bokeh.models.widgets.buttons import Button
from bokeh.models.widgets import Slider,Select,PreText,Dropdown,TextInput,AutocompleteInput,CheckboxGroup,RadioGroup,RangeSlider
from bokeh.transform import cumsum
from bokeh.io import curdoc
from scipy.misc import imread
import pandas as pd
import numpy as np
import sys
import psutil
import logging
from functools import partial
import warnings

warnings.filterwarnings("ignore")


########### Dropbdown countries ###########

def check_dropdown_update_country(attr, old, new):
	global confirmed
	global deaths
	global recovered
	global dates 
	global tot_confirmed,tot_recovered,tot_recovered, data_df

	if dropdown_countries.value == "World":
		tot_confirmed = [sum(confirmed[d]) for d in dates]
		tot_deaths = [sum(deaths[d]) for d in dates]
		tot_recovered = [sum(recovered[d]) for d in dates]
	else:
		print(dropdown_countries.value)
		confirmed_filter = confirmed[confirmed['Country/Region'] == dropdown_countries.value]
		deaths_filter = deaths[deaths['Country/Region'] == dropdown_countries.value]
		recovered_filter = recovered[recovered['Country/Region'] == dropdown_countries.value]
		tot_confirmed = [sum(confirmed_filter[d]) for d in dates]
		tot_deaths = [sum(deaths_filter[d]) for d in dates]
		tot_recovered = [sum(recovered_filter[d]) for d in dates]
    
	p = figure(plot_width=1000, plot_height=550, x_axis_type="datetime", title="COVID-19 cumulative data (@kpelechrinis) ")
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
	layout.children[1] = p
	layout.children[2] = table

global confirmed
global deaths
global recovered 
global dates
global tot_confirmed,tot_deaths,tot_recovered,data_df

confirmed = pd.read_csv("time_series_19-covid-Confirmed.csv")
deaths = pd.read_csv("time_series_19-covid-Deaths.csv")
recovered = pd.read_csv("time_series_19-covid-Recovered.csv")

dates = list(confirmed.columns[4:len(confirmed.columns)])
tot_confirmed = [sum(confirmed[d]) for d in dates]
tot_deaths = [sum(deaths[d]) for d in dates]
tot_recovered = [sum(recovered[d]) for d in dates]

p = figure(plot_width=1000, plot_height=550, x_axis_type="datetime", title="COVID-19 cumulative data (@kpelechrinis)")

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

div1 = Div(text="""<font size=6><b><h>Coronavirus data</b></h></font></br></br><font size=5>This is a simple time-series visualization of the confirmed cases, deaths and recoveries from the corona virues according to the <a href="https://github.com/CSSEGISandData/COVID-19">John Hopkins dataset</a> that is updated daily.</font><br></br></br><br></br></br>""",width=1950, height=150)


menu_countries = ["World"]+list(np.sort(list(confirmed['Country/Region'].unique())))
dropdown_countries = Select(title = "Country/Region", value = "World", options = menu_countries)
dropdown_countries.on_change('value',check_dropdown_update_country)

layout = layout([[div1,],[p,],[table,],[dropdown_countries,]])
curdoc().add_root(layout)
