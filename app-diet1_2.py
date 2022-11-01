import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn')

st.title('A recipe Recommendation App ')
st.subheader('by Eric & Sirena')
df = pd.read_csv('All_Diets.csv')
df['percentage_protein'] =  100 * df['Protein(g)'] / (df['Protein(g)'] + df['Carbs(g)'] + df['Fat(g)'])
df['percentage_carbs'] = 100 * df['Carbs(g)'] / (df['Protein(g)'] + df['Carbs(g)'] + df['Fat(g)'])
df['percentage_fat'] = 100 * df['Fat(g)'] / (df['Protein(g)'] + df['Carbs(g)'] + df['Fat(g)'])
df_o = df

# add a ration to select eating habits
st.sidebar.subheader('Step 1: Analyze the recipes based on your likes')
diet_filter = st.sidebar.radio("Select You Diet type",('paleo', 'vegan', 'keto', 'mediterranean', 'dash','No specific diet'))

# add a multiselect by cuisine

cuisine_filter = st.sidebar.multiselect('Choose Your Preferred Cuisines', df.Cuisine_type.unique(), ('chinese','american','mediterranean'))

# add sliders to select the nutrients in different recipes
st.sidebar.subheader('Step 2: If you want to regulate your recipes specifically by three nurients based on the advice from your nutritionists or fitness instructor, please drag the sliders below:')
protein_filter = st.sidebar.slider('Percentage of protein', 0, 100, 100)
carbs_filter = st.sidebar.slider('Percentage of carbs', 0, 100, 100)
fat_filter = st.sidebar.slider('Percentage of fat', 0, 100, 100)



# filter by eating habits

if diet_filter == 'paleo':
    df = df[df.Diet_type == 'paleo']
elif diet_filter == 'vegan':
    df = df[df.Diet_type == 'vegan']
elif diet_filter == 'keto':
    df = df[df.Diet_type == 'keto']
elif diet_filter == 'mediterranean':
    df = df[df.Diet_type == 'mediterranean']
elif diet_filter == 'dash':
    df = df[df.Diet_type == 'dash']
elif diet_filter == 'No specific diet':
    df = df
# filter by cuisine

df = df[df.Cuisine_type.isin(cuisine_filter)]


# Function 1 anaylyze the choice

# table: recommended recipes
st.subheader('The table below displays the recommended recipes based on your diets and preferred cuisines.')
st.write(df[['Recipe_name',	'Cuisine_type',	'Protein(g)', 'Carbs(g)', 'Fat(g)']])

st.subheader('Then we will analyze your recipes.')
# fig 3
st.markdown('''##### ~The piechart below may give you a general view on how much each nutrient occupies in your recipes.''')
x = [df.percentage_protein.mean(),df.percentage_carbs.mean(),df.percentage_fat.mean()]
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
fig, ax = plt.subplots(figsize=(5,5))
ax.pie(x,labels = ['Protein','Carbs', 'Fat'], colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
# ax.set_title('The occupation of protein, carbs and fat in your recipes')
st.pyplot(fig)




# fig 2
st.markdown('''##### ~The barcharts below may help you compare the nutrients in different cuisines.''')
labels = df.Cuisine_type.unique()
pp = df.groupby('Cuisine_type').percentage_protein.mean()
pc = df.groupby('Cuisine_type').percentage_carbs.mean()
pf = df.groupby('Cuisine_type').percentage_fat.mean()

x = np.arange(len(labels))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, pp, width, label='Protein')
rects2 = ax.bar(x , pc, width, label='Carbs')
rects3 = ax.bar(x + width, pf, width, label='Fat')
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Percentages')
ax.set_title('Nutrients by Cuisines')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)
fig.tight_layout()

plt.show()

# plt.xticks(rotation=60,fontsize=13)
st.pyplot(fig)

# fig 1

st.markdown('''##### ~The boxplots below may help you analyse the nutritional distribution in your recipes.''')
fig, ax = plt.subplots(1,3,figsize=(12,4))

ax[0].set_title('The boxplot of protein in your recipes') 
ax[1].set_title('The boxplot of carbs in your recipes')     
ax[2].set_title('The boxplot of fat in your recipes')          

df[df.Diet_type == diet_filter].percentage_protein.plot.box(ax=ax[0])
df[df.Diet_type == diet_filter].percentage_carbs.plot.box(ax=ax[1])
df[df.Diet_type == diet_filter].percentage_fat.plot.box(ax=ax[2])
st.pyplot(fig)

# summary
st.markdown('''####  Compared with other recipes,''')
if df.percentage_protein.mean() >= df_o.percentage_protein.mean():
    st.markdown('''* Your favored recipes contains ***more*** protein than average.''')
elif df.percentage_protein.mean() <= df_o.percentage_protein.mean():
    st.markdown('''* Your favored recipes contains ***less*** protein than average.''')
if df.percentage_carbs.mean() >= df_o.percentage_carbs.mean():
    st.markdown('''* Your favored recipes contains ***more*** carbs than average.''')
elif df.percentage_carbs.mean() <= df_o.percentage_carbs.mean():
    st.markdown('''* Your favored recipes contains ***less*** carbs than average.''')
if df.percentage_fat.mean() >= df_o.percentage_fat.mean():
    st.markdown('''* Your favored recipes contains ***more*** fat than average.''')
elif df.percentage_fat.mean() <= df_o.percentage_fat.mean():
    st.markdown('''* Your favored recipes contains ***less*** fat than average.''')





# Function 2 find the recommended recipes

# filter by nutrients

st.subheader('The table below displays the regulated recipes based on the advice from your nutritionists or fitness instructor.')

df = df[df.percentage_protein <= protein_filter]
df = df[df.percentage_carbs <= carbs_filter]
df = df[df.percentage_fat <= fat_filter]

st.write(df[['Recipe_name',	'Cuisine_type',	'Protein(g)', 'Carbs(g)', 'Fat(g)']])
