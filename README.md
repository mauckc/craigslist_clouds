# Craigslist Clouds
Word Clouds from Craigslist Scraping

## Reference
Code built off of https://github.com/YangLei2586/Craigslist_UsedCar_Scraper

# Examples


#### First Cloud from 1 Listing
```Python3
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
# Display the generated image:
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
```
![First Cloud](https://github.com/mauckc/craigslist_clouds/blob/master/doc/first_listing.png)


#### Full Cloud of 200 Listings
```Python3
# Generate a word cloud image
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
wordcloud.to_file("img/full_listing.png")
# Display the generated image:
# the matplotlib way:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
```
![Full Cloud](https://github.com/mauckc/craigslist_clouds/blob/master/doc/full_listing.png)
