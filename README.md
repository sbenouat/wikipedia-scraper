# wikipedia-scraper

Function to extract data from wikipedia using Python libraries requests and BeautifulSoup.

First, creates a list of all the wikipedia links on the page.
Second, gets the source code of the page of each page and creates dictionary from the table on the top right.
Third, extract from the dictionary the data that we are looking for and puts it in a dictionary.
