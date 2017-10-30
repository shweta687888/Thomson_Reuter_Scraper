
# coding: utf-8

# In[1]:

import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup


# In[2]:

#call this to retrieve company data
def retrieve_company_data(industry_code):
    Tickers=[]
    Names=[]
    Market_Capitalization=[]
    Ttm=[]
    Employee=[]
    
    try:

        base_url="https://www.reuters.com/sectors/industries/rankings?industryCode="
        url=base_url+str(industry_code)+"&page=-1"
        source_code=requests.get(url)
        text_code=source_code.content
        soup=BeautifulSoup(text_code,'html.parser')
        company_soup=soup.find(class_='column1 gridPanel grid8')
        All_company_section=company_soup.find(class_='dataSmall')
        All_company=All_company_section.findAll('tr')

        for company in All_company:
            company_td_all=company.findAll("td")
            for i,company_td in enumerate(company_td_all):
                if i==0:
                    ticker=company_td.find('a')
                    if ticker is not None:
                        Tickers.append(ticker.string)
                elif i==1:
                    name=company_td.find('a')
                    if name is not None:
                        Names.append(name.string)
                elif i==2:
                    Market_Capitalization.append(company_td.string)
                elif i==3:
                    Ttm.append(company_td.string)
                else:
                    Employee.append(company_td.string)

        data=list(zip(Tickers,Names,Market_Capitalization,Ttm,Employee))
        return data
    except:
        print("Some Error Occured")
        data=list(zip(Tickers,Names,Market_Capitalization,Ttm,Employee))
        return data


# In[3]:

#call this to retrieve people data
def retrieve_people_data(ticker_no):
    
    Name=[]
    Age=[]
    Since=[]
    Current_position=[]
    Descriptions=[]

    try:
        base_url="https://www.reuters.com/finance/stocks/company-officers/"
        url=base_url+ticker_no
        source_code=requests.get(url)
        text_code=source_code.content
        soup=BeautifulSoup(text_code,'html.parser')
        people=soup.find(class_='column1 gridPanel grid8')
        All_people=people.find(class_='dataSmall')
        if All_people is None:
            return []
        All_people=All_people.findAll('tr')

        for person in All_people:
            person_td=person.findAll("td")
            for i,per_td in enumerate(person_td):
                name=per_td.find('a',class_='link')
                if name is not None:
                    Name.append(name.string.strip())
                if i==1:
                    Age.append(per_td.string)
                elif i==2:
                    Since.append(per_td.string)
                elif per_td.string is not None:
                    Current_position.append(per_td.string.strip())

        description=people.findAll(class_='dataSmall')[1]
        for about in description.find_all('tr'):
            about_td=about.findAll('td')
            for i,abt in enumerate(about_td):
                if i==1:
                    Descriptions.append(abt.string.strip())
        return list(zip(Name,Age,Since,Current_position,Descriptions))
    except:
        print("Error occured")
        return list(zip(Name,Age,Since,Current_position,Descriptions))


# In[7]:

#get the sector information
def getSectors(url):

    sectors=[]
    try:
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')

        #sectors = []

        sectors_section=soup.find(id="tab1")
        sectors_section_table=sectors_section.find("tbody")
        sectors_tr=sectors_section_table.find_all("tr")
        for i in sectors_tr:
            sector_tag=i.find("td").find("a")
            sectors.append("https://www.reuters.com/"+sector_tag.get("href"))
        return sectors
    except:
        print("Error Occured")
        return sectors
#Parsing direct link
def scrap_first_link(url):
    # Get Source Code
    data={}
    try:
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')

    #    data={}
        header = soup.find(class_="sectionRelatedTopics").find("ul")
        link=header.find("li")
        data[link.find("a").string]="https://www.reuters.com"+link.find("a").get("href")
        return data
    except:
        print("Error Occured")
        return data
#Parsing related links
def get_related_industries(url):

    # Get Source Code
    related_industries_data={}
    try:
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')

       # related_industries_data = {}

        header=soup.find(class_="sectionRelatedTopics relatedIndustries").find("ul")
        for links in header.find_all("li"):
            related_industries_data[links.string]="https://www.reuters.com"+links.find("a").get("href")

        return related_industries_data
    except:
        print("Error Occured")
        return read_industries_data
#this function will be called to get industry data
def getData():
    # Getting data of sectors
    links_data={}
    try:

        sectors_data = getSectors("https://www.reuters.com/sectors/industries/significant?industryCode=4")
        #links_data={}

        for sector in sectors_data:
            link=scrap_first_link(sector)
            links_data.update(link)


        links_data["Healthcare Reform"]="https://www.reuters.com/sectors/industries/overview?industryCode=151"

        related_links_data = {}
        #Parsing related links
        for key, value in links_data.items():
            link = get_related_industries(value)
            related_links_data.update(link)

        links_data.update(related_links_data)

        return links_data
    except:
        print("Error Occured")
        return links_data


# In[8]:

#Given data in csv format
data=pd.read_csv('data.csv')


# In[9]:

data


# In[10]:

#Extracting the Industry and PermID
Industry=[]
PermID=[]
New_Data=[]
for index,d in data.iterrows():
    if d['INDUSTRY'] is not None:
        Industry.append(d['INDUSTRY'])
        PermID.append(d['PermID'])
New_Data=list(zip(Industry,PermID))
Data_Dictionary=dict(New_Data)
Data_Dictionary


# In[17]:

#parsing the all sector data
sector=getData()


# In[18]:


Industry_Data=[] # this contains Industry ,PermID and link which contains Industry code
for industry,permid in Data_Dictionary.items():
    if industry in sector:
        Industry_Data.append(tuple((industry,permid,sector[industry])))     
    else :
        Industry_Data.append(tuple((industry,permid,'None')))


# In[19]:

df=pd.DataFrame(Industry_Data)#collecting it to a dataframe


# In[20]:

df=df.drop(0)#dropping unneccesary column


# In[21]:

df.to_csv('Industry_Data.csv',header=['Industry','PermID','Link'])#saving to a csv


# In[22]:

read_industry_data=pd.read_csv('Industry_Data.csv')
read_industry_data


# In[23]:

#Collecting Industries Detail


# In[24]:

Industry_Info_Data=[] # this contains 'Industry','PermID','Ticker','Name','Market Capitalisation','ttm','Employees'
for i,d in enumerate(Industry_Data):
    if d[2]!='None':
        #print(d[2])
        code=d[2].split("=")[1].strip()
        #print(code)
        c_data=retrieve_company_data(code)
       # print(c_data)
        if c_data is not None:
            for c in c_data:
                single_industry_val=tuple((d[0],d[1],c[0],c[1],c[2],c[3],c[4]))
                Industry_Info_Data.append(single_industry_val)
Industry_Info_Data


# In[25]:

df=pd.DataFrame(Industry_Info_Data) #converting info data to a dataframe


# In[26]:

#writing to csv
df.to_csv('Industry_Info_Data.csv',header=['Industry','PermID','Ticker','Name','Market Capitalisation','ttm','Employees'])


# In[27]:

df=pd.read_csv('Industry_Info_Data.csv')
df


# In[ ]:

Person_Data=[] # this contains 'Industry','PermID','Ticker','Name','Age','Since','Current_Position','Descriptions'
for i,d in enumerate(Industry_Info_Data):
    if d[2] is not None:
        #print(d[2])
        p_data=retrieve_people_data(d[2])
        if p_data is not None:
            for p in p_data:
                Person_Data.append(tuple((d[0],d[1],d[2],p[0],p[1],p[2],p[3],p[4])))
Person_Data


# In[ ]:

df=pd.DataFrame(Person_Data)


# In[ ]:

#writing to a csv
df.to_csv('Person_Data.csv',header=['Industry','PermID','Ticker','Name','Age','Since','Current_Position','Descriptions'],encoding='utf-8')


# In[ ]:

df=pd.read_csv('Person_Data.csv',encoding='utf-8')
df


# In[ ]:



