import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pandasql as ps


url="https://raw.githubusercontent.com/rishabhbhardwaj1995/wealthindex/main/df.csv"
df =pd.read_csv(url)

df['Rural_Urban'] = df['Rural/Urban']

df['District_U_R'] =   df['District'] + df['Rural/Urban']

st.set_page_config(layout="wide")


st.sidebar.header("Wealth Index Quintile")
wealth_index_quintile = st.sidebar.multiselect('Wealth Index Quintile from 1 to 5', [1,2,3,4,5], default = [5], key = 'wealth_index')

st.sidebar.header("Rural/Urban")
urban_rural = st.sidebar.selectbox('Rural or Urban', list(df['Rural/Urban'].unique()), key = 'rural_urban')


df1 = df.loc[df['wealth_index_quantile'].isin([int(i) for i in wealth_index_quintile])] #quintile level


df2 = df1.loc[df1['Rural/Urban'] == (urban_rural)] # urban rural level



st.sidebar.header("District Name")
district = st.sidebar.selectbox('District', list(df['District'].unique()), index = 0,key = 'district')


df3 = df1.loc[df1['District'] == district] # district level but not split into rural or urban


df4 = df2.loc[df2['District']== district] # district level split into rural or urban


st.sidebar.header("Tehsil Name")
tehsil_name = st.sidebar.selectbox('Tehsil Name', list(df3['Tehsil Name'].unique()), index = 0,key = 'tehsil')



df5 = df3.loc[df3['Tehsil Name'] == tehsil_name] # district level but not split into rural or urban


df6 = df4.loc[df4['Tehsil Name']== tehsil_name] # district level split into rural or urban

df_district = df.loc[df['District'] == district]


whole_state_level_histogram = px.histogram(df1, x='sanitation_quantile')

whole_state_level_histogram_rural_urban = px.histogram(df2, x='sanitation_quantile')

district_level_histogram = px.histogram(df3, x='sanitation_quantile')

tehsil_level_histogram = px.histogram(df5, x='sanitation_quantile')


Rural = len(df.loc[df['Rural_Urban'] == 'Rural'])

Urban = len(df.loc[df['Rural_Urban'] == 'Urban'])

Total = len(df)


Rural_query_1 = f"""
SELECT 
CAST(count(wealth_index_quantile) as FLOAT) as quint,
wealth_index_quantile,
District
from
df
where 
Rural_Urban = 'Rural'
group by 
wealth_index_quantile, District
"""


rural_df_dist_1 = ps.sqldf(Rural_query_1, locals())




Rural_query_2 = f"""
SELECT 
CAST(count(*) as FLOAT) as rows,
wealth_index_quantile,
District
from
df
where 
Rural_Urban = 'Rural'
group by 
District
"""


rural_df_dist_2 = ps.sqldf(Rural_query_2, locals())



Rural_query_3 = f"""
SELECT 
a.*,
cast((a.quint/b.rows) as FLOAT) as Dist
from
rural_df_dist_1 as a
left join 
rural_df_dist_2 as b
on
a.District = b.District
"""



rural_df_dist = ps.sqldf(Rural_query_3, locals())


rural_df_dist['Dist'] = rural_df_dist['Dist'].round(5)


rural_df_dist =  pd.pivot_table(rural_df_dist, values = 'Dist' , index = 'District', columns= 'wealth_index_quantile')




Urban_query_1 = f"""
SELECT 
CAST(count(wealth_index_quantile) as FLOAT) as quint,
wealth_index_quantile,
District
from
df
where 
Rural_Urban = 'Urban'
group by 
wealth_index_quantile, District
"""


urban_df_dist_1 = ps.sqldf(Urban_query_1, locals())



Urban_query_2 = f"""
SELECT 
CAST(count(*) as FLOAT) as rows,
wealth_index_quantile,
District
from
df
where 
Rural_Urban = 'Urban'
group by 
District
"""


urban_df_dist_2 = ps.sqldf(Urban_query_2, locals())



Urban_query_3 = f"""
SELECT 
a.*,
cast((a.quint/b.rows) as FLOAT) as Dist
from
urban_df_dist_1 as a
left join 
urban_df_dist_2 as b
on
a.District = b.District
"""



urban_df_dist = ps.sqldf(Urban_query_3, locals())


urban_df_dist['Dist'] = urban_df_dist['Dist'].round(5)


urban_df_dist =  pd.pivot_table(urban_df_dist, values = 'Dist' , index = 'District', columns= 'wealth_index_quantile')



Overall_query_1 = f"""
SELECT 
CAST(count(wealth_index_quantile) as FLOAT) as quint,
wealth_index_quantile,
District
from
df
group by 
wealth_index_quantile, District
"""


Overall_df_dist_1 = ps.sqldf(Overall_query_1, locals())




Overall_query_2 = f"""
SELECT 
CAST(count(*) as FLOAT) as rows,
wealth_index_quantile,
District
from
df
group by 
District
"""


Overall_df_dist_2 = ps.sqldf(Overall_query_2, locals())



Overall_query_3 = f"""
SELECT 
a.*,
cast((a.quint/b.rows) as FLOAT) as Dist
from
Overall_df_dist_1 as a
left join 
Overall_df_dist_2 as b
on
a.District = b.District
"""



Overall_df_dist = ps.sqldf(Overall_query_3, locals())


Overall_df_dist['Dist'] = Overall_df_dist['Dist'].round(5)


Overall_dist =  pd.pivot_table(Overall_df_dist, values = 'Dist' , index = 'District', columns= 'wealth_index_quantile')



df_district['Tehsil_Name'] = df_district['Tehsil Name']

Total_dist = len(df_district)


Tehsil_query_1 = f"""
SELECT 
CAST(count(wealth_index_quantile) as FLOAT) as quint,
wealth_index_quantile,
Tehsil_Name
from
df_district
group by 
wealth_index_quantile, Tehsil_Name
"""



Tehsil_df_dist_1 = ps.sqldf(Tehsil_query_1, locals())


Tehsil_query_2 = f"""
SELECT 
CAST(count(*) as FLOAT) as rows,
wealth_index_quantile,
Tehsil_Name
from
df_district
group by 
Tehsil_Name
"""



Tehsil_df_dist_2 = ps.sqldf(Tehsil_query_2, locals())




Tehsil_query_3 = f"""
SELECT 
a.*,
cast((a.quint/b.rows) as FLOAT) as Dist
from
Tehsil_df_dist_1 as a
left join 
Tehsil_df_dist_2 as b
on
a.Tehsil_Name = b.Tehsil_Name
"""



Tehsil_df_dist_3 = ps.sqldf(Tehsil_query_3, locals())


Tehsil_df_dist_3['Dist'] = Tehsil_df_dist_3['Dist'].round(5)


Tehsil_dist =  pd.pivot_table(Tehsil_df_dist_3, values = 'Dist' , index = 'Tehsil_Name', columns= 'wealth_index_quantile')



st.title("Wealth Index and Sanitation Index Exploration Tool")





st.header("Distribution of Wealth Index Quintile")

st.subheader("District level Wealth Index Distribution (each row sum to 100%)")
st.dataframe(Overall_dist.style.highlight_max(axis=1).format('{:.1%}'))

st.markdown("***")
st.subheader("District level Wealth Index Distribution Only Urban (each row sum to 100%)")
st.dataframe(urban_df_dist.style.highlight_max(axis=1).format('{:.1%}'))


st.markdown("***")
st.subheader("District level Wealth Index Distribution Only Rural (each row sum to 100%)")
st.dataframe(rural_df_dist.style.highlight_max(axis=1).format('{:.1%}'))


st.markdown("***")  
st.subheader("Tehsil level Wealth Index Distribution (each row sum to 100%)")
st.dataframe(Tehsil_dist.style.highlight_max(axis=1).format('{:.1%}'))

st.markdown("***")

st.header("Visiual Representation of Sanitation Index Quintiles for the selected Wealth Index Quintile")


col1, col2 = st.beta_columns((1, 1))

with col1:
    st.subheader("State level whole")
    st.plotly_chart(whole_state_level_histogram, use_column_width=True)

with col2:
    st.subheader("State level Rural/Urban")
    st.plotly_chart(whole_state_level_histogram_rural_urban, use_column_width=True)


    

col3, col4 = st.beta_columns((1, 1))

with col3:
    st.subheader("District Level whole")
    st.plotly_chart(district_level_histogram, use_column_width=True)
    
    
with col4:
    st.subheader("Tehsil Level whole")
    st.plotly_chart(tehsil_level_histogram, use_column_width=True)
    

    
