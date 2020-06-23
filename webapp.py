import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
@st.cache
def load_data(nrows):
  data = pd.read_csv('WebData/predictionTest.csv')
  data = data.loc[data['ed']>100]
  data.drop(index=data.loc[data['District_Name']=='Adams-Cheshire'].index,inplace=True)
  return data

dat = load_data(10000)
#print(dat.loc[dat['District_Name']=='Adams-Cheshire'])
dat.sort_values(by=['District_Name'],ascending=True,inplace=True)
district_name_all = dat['District_Name'].values
district_name_all_list = list(set(district_name_all))
district_name_all_list.sort()
district_name_all_list.insert(0,"")
#print(district_name_all_list)


st.header('Budget planning for economically disadvantaged students in Massachusetts school districts')
st.subheader('Introduction')
st.write('At the begining of each school year (October 1), school districts make a budget plan for the next school year. A foundation budget is created which is the minimum funding required for each school district. Based on this foundation budget, the state and local administrators will provide needed funding for school districts. The foundation budget also includes additional funding for school districts to support economically disadvantaged students (ED, ~$3500 per student). The current number of enrolled students seen by Oct. 1 is used to calculate the foundation budget, which is often lower than the actual number of ED students in the next school year. This tool provides better budget planning for ED students using realistic enrollment projection.')
st.subheader('Instruction')
st.write('Select the school district on the sidebar menu to see the projected budget for the next school year. The spending per student in the current school year is used to calculate the projected budget. This spending can be adjusted by selecting "Spending adjustment".')
st.subheader('Budget amount')
#district_name = st.text_input("District name", "")
district_name = st.sidebar.selectbox("District name", district_name_all_list)
spending_adj = st.sidebar.slider("Spending adjustment", 0.8, 1.2, 1.0)
print(spending_adj)
district_name = "Amesbury"
#ed_pre = dat.loc[(dat['district']==district_name) & (dat['schoolyear']=='2018-19')]['ed_li_pct_pred']
ed_pre = spending_adj*dat.loc[(dat['District_Name']==district_name) & (dat['schoolyear']=='2020-21')]['bg_ed_only']
#print(dat.loc[(dat['district']==district_name) & (dat['schoolyear']=='2020-21')]['bg_ed_only'])
#dat1 = dat.loc[dat['District_Name']=='Andover']
#print(dat1)
if district_name != "":
  amount = '{:,d}'.format(int(ed_pre.values[0]*1000000))
  print(amount)
  #st.write('Budget amount for ED students in 2020-2021: $' + str(int(ed_pre.values[0]*1000000)))
  st.write('Budget amount for ED students in 2020-2021: $' + amount)
  #dat.loc[dat['district']==district_name].plot.bar(x='schoolyear',y='ell_pct')
  #st.write('Percentage of enrolled economic disadvantage over year: ')
  dat1 = dat.loc[dat['District_Name']==district_name]
  dat1.sort_values(by=['schoolyear'],inplace=True)
  print(dat1.loc[dat1['schoolyear'] == '2020-21']['bg_ed_only'].values)
  print(dat1)
  print('spending_adj: ', spending_adj)
  idx = dat1.loc[dat1['schoolyear'] == '2020-21']['bg_ed_only'].index
  dat1.loc[idx,'bg_ed_only']=dat1.loc[idx,'bg_ed_only']*spending_adj
  print(dat1)
  ax = dat1.plot(x="schoolyear", y=['bg_ed_only'], kind='bar')
  ax.get_legend().remove()
  #ax.legend(['Budget for ED student support'],loc='center left')
  ax.set_ylabel('Budget amount ($1M)')
  #maxval = max(dat1['bg_ed_only'])
  #ax.set_ylim(0,maxval*1.2)
  ax.set_xlabel('School year')
  for tick in ax.get_xticklabels():
    tick.set_rotation('horizontal')
  #ax.legend([''])
  #plt.xticks(rotation='horizontal')
  st.pyplot()
  #dat2 = dat1[['schoolyear','bg_ed_only']]
  #dat2.rename(columns={'schoolyear':'index'}).set_index('index')
  #dat2.set_index('schoolyear')
  #dat2.drop('schoolyear',axis=1,inplace=True)
  #print(dat2)
  #st.line_chart(dat2)
  #c = alt.Chart(dat2).mark_bar().encode(
  #  x=alt.X('schoolyear:Q', axis=alt.Axis(tickCount=dat2.shape[0], grid=False)),
  #  y=alt.Y('bg_ed_only:Q'))
  #st.altair_chart(c)
