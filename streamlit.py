import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

map_url = data.us_10m.url
states = alt.topo_feature(map_url, 'states')
state_id = pd.read_csv('https://gist.githubusercontent.com/dantonnoriega/bf1acd2290e15b91e6710b6fd3be0a53/raw/11d15233327c8080c9646c7e1f23052659db251d/us-state-ansi-fips.csv')
pwd = pd.read_csv('map_data.csv')
join = pd.merge(pwd, state_id, left_on='state_name', right_on='stname')
join['id'] = join[' st']
join['percentage'] = join['percentage'].astype(float)/100
join['normal_percent'] = 1-join['percentage']

click = alt.selection_single(on='click', empty='all', fields=['id'])

clarity = alt.condition(click, alt.value(0.9), alt.value(0.5))

map = alt.Chart(states).mark_geoshape().encode(
    color='percentage:Q',
    tooltip=['state_name:N', 'percentage:Q'],
    opacity=clarity
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(join, ' st', ['percentage', 'state_name'])
).project(
    type='albersUsa'
).add_selection(
    click
)

pie_chart = alt.Chart(join).transform_filter(
    click
).transform_fold(
    ['percentage', 'normal_percent'],
    as_=['type', 'value']
).mark_arc().encode(
    theta='mean(value):Q',
    color='type:N',
).properties(
    title='Percentage of Population with a Disability'
)

st.altair_chart(map | pie_chart, theme='streamlit')