#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import packages
import seaborn as sns
import pandas as pd
import math
import numpy as np
from IPython.display import display_html
from IPython.core.display import display, HTML


# # Let's explore properties in Riga city center, October 2022.
# 1.What's the most commom flat type for sale?
# 2.What's the most expensivest type of flat?
# 3.Does floor affects price?
# 4.Does m2 affects price?
# 5.Rent or buy?

# In[2]:


# import data and explore it
df= pd.read_excel(r'C:\Users\lenovo\Desktop\Project2\flats_rent_sale_edit.xlsx', sheet_name="Sale")
df_rent= pd.read_excel(r'C:\Users\lenovo\Desktop\Project2\flats_rent_sale_edit.xlsx', sheet_name="Rent")


# In[3]:


def display_side_by_side(dfs:list, captions:list):
    """Display tables side by side to save vertical space
    Input:
        dfs: list of pandas.DataFrame
        captions: list of table captions
    """
    output = ""
    combined = dict(zip(captions, dfs))
    for caption, df in combined.items():
        output += df.style.set_table_attributes("style='display:inline'").set_caption(caption)._repr_html_()
        output += "\xa0\xa0\xa0"
    display(HTML(output))


# In[4]:


pd.set_option('display.float_format', '{:,}'.format)


# In[5]:


# clean price column
df["Price"]=df['Price'].str.replace('€', '').str.replace(".", '').str.strip()
df["Price"]=df["Price"] + '.00'
df["Price"]=df['Price'].astype(float)


# In[6]:


#average sales price in eur per nr of rooms
df_mean2=df.groupby(['Rooms'])['Price'].mean().reset_index().astype(int)
ax1=df_mean2.plot.barh( x='Rooms', y= 'Price', color= '#8EB897', figsize=(9,5),width=0.7)
#ax1.grid(linewidth=0.5,axis='x')
ax1.set_title('Riga, Oct 2022', fontsize=11)
ax1.set_ylabel("Number of Rooms", fontsize=10)
ax1.get_legend().remove()
ax1.figure.suptitle('Average Flat Price in Thousands', fontsize=16 )
y=df_mean2['Price']
for index, value in enumerate(y):
    ax1.text(value, index,
             str(value) + "€")


# 5 bedroom flats tend to be the most expensive.

# In[7]:


df.groupby("Rooms").size()


# In[8]:


#correlation coefficient
df.corr()
display_side_by_side([df.corr(), df_rent.corr()], ['Sales','Rentals'])


# We see that when it comes to Sales price correlation coefficient to m2 are higher then for rentals.

# In[9]:


#number of rooms  %
room_count=df.Rooms.value_counts()
ax=room_count.plot.pie(figsize=(6,6), fontsize=12,
                    wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, 
                    colors = ['#4F6272', '#B7C3F3', '#DD7596', '#8EB897', 'grey', 'lightcoral','plum' ],
                      autopct='%.0f%%')
ax.set_title('Number of Rooms in Flat', fontsize=16)
ax.set_ylabel(None)


# Majority of flats available for sale are 2 bedroom and then 3 bedroom.

# In[10]:


#remove whitespace before floor number
df['Floor']=df.Floor.astype(str).str.strip()
print(len(df.Floor[0]))


# In[11]:


#create floor categories func
def floor_to_categories(floor_str):
    num1, num2 = floor_str.split("/")
    if num1 == num2: return "Top"
    elif num1 == "1": return "Ground"
    return "Middle"
#apply func
df["Floor Type"] = df.Floor.apply(floor_to_categories)


# In[12]:


df_sorted= df.sort_values("Price",ascending=False)


# In[13]:


df_sorted.head(10)


# In[ ]:





# In[14]:


df_sorted.tail(10)


# In[15]:


df.groupby("Floor Type").Price.mean().astype(int).reset_index()


# We see that on average top floor tend be be more expensive, however looking at top 10 most expensive properties for sale majority of them are on the middle floor.And the majority of the cheapest properties are on the ground floor.

# In[16]:


sns.set(rc = {'figure.figsize':(10,7)})
sns.violinplot(x="Rooms", y="Price", data=df,
               palette=["lightblue", "lightpink","lightgrey",'beige','lightgreen','lightcoral','plum'])


# One bedroom flats tend to sell around medium price this is still noticeable for two bedroom flats as well , while the other flats very vary in price.

# In[17]:


#create size categories for m2 using condition statements

category = []
for i in df_sorted['m2']:
    if i <=30:
        category.append('Small')   
    elif i <= 80:
        category.append('Normal')
    elif i <= 160:
        category.append('Big')
    else:
        category.append('Huge')

df_sorted['Size Category'] = category
print(df_sorted.head(10))


# When we looked at rentals, top floors were the most expensivest however it's not true for apartments for sales, here size matters more.

# In[18]:


sns.set(rc = {'figure.figsize':(10,7)})
sns.violinplot(x="Size Category", y="Price", data=df_sorted)


# In[ ]:





# In[19]:


#explore price in each size category
df_sorted.groupby('Size Category')[['Price']].aggregate([min, max, 'mean']).astype(int).reset_index()


# In[24]:


function_dictionary = {'m2':'mean','Price':'mean'}
df_sorted.groupby("Rooms").aggregate(function_dictionary).astype(int).reset_index()


# In[21]:


#explore number of flats available in each size category
df_sorted.groupby("Size Category").size()


# In[22]:


#Price-to-Rent Ratio
df['Price'].mean() /(df_rent['Price'].mean() * 12) 


# Price-to-rent ratio of 21 or more indicates it is much better to rent than buy.

# In[ ]:




