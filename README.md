# Thomson_Reuter_Scraper
This is web crawler written in Python. You will need to install Beautifulsoup and pandas before you can use it.<br />
It crawl through Thomson Reuters company ranking pages and map businesses back to the PermID as available in the data.csv file. It will extract all Industries along with following information and map them back to the PermID or Hierarchical ID:<br />
Ticker, Name, Market Capitalization, TTM Sales, Employees.<br />
From each company listed in the index, it will extract following information of people involved with the business:<br />
Name, Age, Since, Current Position, Description.

# Running Main.py
Download the Main.py file from the repo.<br />
The following command will be used to run Main.py:<br />
python Main.py<br />
Running the script will result in three .csv files.

# Execution Flow
Industry_Data contains Industry and PermID and links of all sectors that contains industry code, getData() function is used to extract the link of sectors, using industry code it call retrieve_company_data() function which retrive the company data i,e., Industry, PermID, Ticker, Name, Market Capitilization, TTM Sales and Employees. Using Ticker that is obtained from retrieve_company_data() retrieve_people_data() function would be called which retrive the people's data i.e., Industry, PermID, Ticker, Name, Age, Since, Current_Position, Description.<br />
Industry_Data= this contains Industry ,PermID and link which contains Industry code.<br />
Industry_Info_Data= this contains Industry, PermID, Ticker, Name, Market Capitalisation, ttm, Employees.<br />
Person_Data= this contains Industry, PermID, Ticker, Name, Age, Since, Current_Position, Descriptions.<br />

# Error
SSL error occurs sometimes due to heavy request on server.
