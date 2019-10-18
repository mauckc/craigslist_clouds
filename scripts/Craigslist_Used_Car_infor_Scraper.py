#!/usr/bin/env python
# coding: utf-8

# In[14]:


# start scraping information from just one page

from urllib.request import urlopen
from bs4 import BeautifulSoup

url='https://sfbay.craigslist.org/search/cta?s=0'

html = urlopen(url)
bs = BeautifulSoup(html.read(),'html.parser')
cars=bs.find_all('li',{ 'class':'result-row'})

scrapedCarsList=[]
for car in cars:
    salesTitle=car.find('a',{'class':'result-title hdrlnk'})
    price=car.find('span',{'class':'result-price'})
    postingDate=car.find('time',{'class':'result-date'})
    #Some listings do not have a price.
    if price!=None:
        new_car=[salesTitle.get_text(),postingDate.get_text(),price.get_text()]
        #print(new_car) #uncomment to see all the cars with a newline
        scrapedCarsList.append(new_car)
print(scrapedCarsList[0:3]) #uncomment to see the list of cars on the first page
len(scrapedCarsList)


# In[15]:


# now let's revise the code to write the results of the first page into a csv file named 'CarCraglist.csv'.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

with open('CarCraglist.csv', 'w',newline='') as myFile:
    writer = csv.writer(myFile)
    writer.writerow(["sales Title", "Listing Date", "Price"])

url='https://sfbay.craigslist.org/search/cta?s=0'
html = urlopen(url)
bs = BeautifulSoup(html.read(),'html.parser')
cars=bs.find_all('li',{ 'class':'result-row'})

scrapedCarsList=[]
for car in cars:
    salesTitle=car.find('a',{'class':'result-title hdrlnk'})
    price=car.find('span',{'class':'result-price'})
    postingDate=car.find('time',{'class':'result-date'})
    #Some listings do not have a price.
    if price!=None:
        new_car=[salesTitle.get_text(),postingDate.get_text(),price.get_text()]
        scrapedCarsList.append(new_car)

with open('CarCraglist.csv', 'a',newline='',encoding='utf-8') as myFile:
    writer = csv.writer(myFile)
    writer.writerows(scrapedCarsList)


# In[16]:


#  create the list of URL's for the most recent 1,200 posting

baseURL='https://sfbay.craigslist.org/search/cta?s='
urlList=[]
for i in range(0,1201,120):
    newURL=baseURL+str(i)
    urlList.append(newURL)

print(urlList[0:50]) #uncomment to see the urls
len(urlList)


# In[17]:


#  trun the scraping script into a function so that it can  takes the page number (0, 120, 240, ...) as input and returns a list of all the cars on the page in a list of lists format.

def craigslistCarsScrape(pageNumber):
    print('*** Scraping cars on page:',int(pageNumber/120+1),'***\n\n')

    baseURL='https://sfbay.craigslist.org/search/cta?s='
    url=baseURL+str(pageNumber)
    html = urlopen(url)
    bs = BeautifulSoup(html.read(),'html.parser')
    cars=bs.find_all('li',{ 'class':'result-row'})
    scrapedCarsList=[]            
    for car in cars:
        salesTitle=car.find('a',{'class':'result-title hdrlnk'})
        price=car.find('span',{'class':'result-price'})
        postingDate=car.find('time',{'class':'result-date'})
        #Some listings do not have a price.
        if price!=None:
            new_car=[salesTitle.get_text(),postingDate.get_text(),price.get_text()]
            scrapedCarsList.append(new_car)
    return scrapedCarsList


# In[11]:


# error handling to make the codes more robust

from urllib.error import HTTPError
from urllib.error import URLError

def craigslistCarsScraper(pageNumber):
    print('*** Scraping cars on page:',int(pageNumber/120+1),'***\n\n')

    baseURL='https://boston.craigslist.org/search/cta?s='
    url=baseURL+str(pageNumber)
    
    try:
        
        html = urlopen(url)
    
    except HTTPError as e:
        print(e)
        print('-----------------------HTTPError----------------------')
        return None
    except URLError as e:
        print('Server cound not be found')
        print('-----------------------URLError----------------------')
        return None
    
    bs = BeautifulSoup(html.read(),'html.parser')
    
    try:
        
        cars=bs.find_all('li',{ 'class':'result-row'})
    
    except AttributeError as e:
        print('Tag was not found')
        print('-----------------------AttributeError----------------------')
    
    else:
        scrapedCarsList=[]
        for car in cars:
            salesTitle=car.find('a',{'class':'result-title hdrlnk'})
            price=car.find('span',{'class':'result-price'})
            postingDate=car.find('time',{'class':'result-date'})
            #Some listings do not have a price.
            if price!=None:
                new_car=[salesTitle.get_text(),postingDate.get_text(),price.get_text()]
                    
                scrapedCarsList.append(new_car)
               
        return scrapedCarsList


# In[18]:


craigslistCarsScraper(600)


# In[20]:


# run the function in a loop and write the resutls on a csv

with open('craigslist_cars_final.csv', 'w',newline='') as myFile:
    writer = csv.writer(myFile)
    writer.writerow(["Listing Title", "Listing Date", "Price"])

with open('craigslist_cars_final.csv', 'a',newline='',encoding='utf-8') as myFile:
    writer = csv.writer(myFile)
    for i in range(0,1201,120):
        scrapedCarsList=craigslistCarsScraper(i)
        writer.writerows(scrapedCarsList)

print('----------------------------------------Well done---------------------------------------------- ')
print('-----------------------------------Scraping completed------------------------------------------ ')
print('------------Please find the csv file in the folder where this scraping file exists------------- ')


# In[44]:


import pandas as pd
import numpy as np


# In[30]:


data = pd.read_csv("craigslist_cars_final.csv") 
data.head()


# In[100]:


original_sum_price = 0
sum_price = 0
price_list = []

# Convert from "$12355" to "12355" with integer type
for price in data['Price']:
    # Clean up price data
    price_list.append(int(price[1:]))
    original_sum_price += int(price[1:])

data['dollars'] = price_list

# Filter out extraneous priced listings
min_listing_amount = 800
max_listing_amount = 90000
data_price_range = data[(data['dollars'] > min_listing_amount ) & (data_price_range['dollars'] < max_listing_amount )]

sum_price = np.sum(data_price_range['dollars'])
avg_price_range = int(data_price_range.dollars.mean())

print('[INFO]: Sum price is: {}'.format(sum_price))
print('[INFO]: Average price is: {}'.format(avg_price_range))


# In[79]:


words = []
for listing_title in data_price_range['Listing Title'].values:
    for word in listing_title.split(' '):
        if word.isnumeric():
            pass
#             print(word)
#             continue
        if word.isalpha():
            print(word)
            words.append(word)
#             continue



# In[122]:


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib import pyplot as plt
import os


# In[116]:


text = data_price_range['Listing Title'].values[1]

# Create and generate a word cloud image:
wordcloud = WordCloud().generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[119]:


wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
# Display the generated image:
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()


# ## Saving File

# In[125]:


output_img_path = 'img'
if not os.path.exists(output_img_path):
    os.mkdir(output_img_path)

# Save the image in the img folder:
wordcloud.to_file("img/first_listing.png")


# You may notice interpolation="bilinear" in the plt.imshow(). This is to make the displayed image appear more smoothly
# 
# more info:
# https://matplotlib.org/gallery/images_contours_and_fields/interpolation_methods.html

# In[159]:


text = " ".join(review for review in data_price_range['Listing Title'])
print ("There are {} target words in the Listing Titles of all cars.".format(len(text)))

num_words = 200
dfwords = pd.DataFrame(words,columns=['word'])

text = " ".join(review for review in dfwords['word'].value_counts().keys()[0:num_words])
print ("There are {} target words in the Listing Titles of all cars.".format(len(text)))


# Put it all together form the giant string of words

# In[157]:


# Create stopword list:
stopwords = set(STOPWORDS)
stopwords.update(["online", "finance", "anyone", "call","text"])

# Generate a word cloud image
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

# Display the generated image:
# the matplotlib way:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# ### Using Pandas

# In[143]:


dfwords = pd.DataFrame(words,columns=['word'])
dfwords['word'].value_counts().keys()[0:num_words]


# In[ ]:




