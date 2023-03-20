# Import 
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


url= 'https://www.sircon.com/ComplianceExpress/Inquiry/consumerInquiry.do?nonSscrb=Y'
browser.visit(url)

# Convert the browser html to a soup object and find the latest title
element = browser.find_option_by_text('Georgia').first.click()
time.sleep(10)
#element.click()


type_element = browser.find_by_xpath('//*[@id="entityTypes"]/div[2]/input[2]').first
type_element.click()
# name_city='ac'

alpa_list=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
licenser=[]
for i in alpa_list:
    for j in alpa_list:
        try:
            
            name_city_name=i+j
            print(name_city_name)
            input_element = browser.find_by_name('lastName')
            input_element.fill(name_city_name)
            time.sleep(1)
            for city_i in alpa_list:
                for city_j in alpa_list:
                    name_city_city    =city_i +city_j 
                    input_element = browser.find_by_name('city')
                    input_element.fill(name_city_city)
                    time.sleep(1)
                    #license type
                    license_element = browser.find_by_xpath('//*[@id="border"]/form[3]/div[6]/div[3]/select/option[21]').first
                    license_element.click()
                    time.sleep(1)
                    #result 100
                    element = browser.find_option_by_text('100').first.click()
                    #//*[@id="resultsPerPage"]/select
                    time.sleep(1)
                    #submit
                    submit_element=browser.find_by_id('submitButton').click()
                    print('submit')
                    time.sleep(30)
                    
                    html = browser.html
                    table_soup = soup(html,'html.parser')
                    inqheader=table_soup.find(class_='inquiriesWelcome').text.replace('/n','').strip()
                    value_inqh="Individual Consumer Inquiry"

                    if inqheader == value_inqh:

                    
                    
                        elements = table_soup.select('tr[class*=ResultTableText]')    

                        for i in range(len(elements)):
                            all_column=elements[i].find_all('td', class_='ResultTableTextColumn')
                            name=all_column[0].text.replace('\n', '')
                            license_num=all_column[1].text.replace('\t', '').replace('\n', '').strip()
                            npn=all_column[5].text.replace('\n', '').strip()
                            city=all_column[6].text.replace('\n', '').strip()
                            state=all_column[7].text.replace('\n', '').strip()
                            name_link = elements[i].find('td', class_='ResultTableTextColumn').a.get('href')
                            abs_link=f'https://www.sircon.com{name_link}'
                            licenser_dic={}
                            licenser_dic["Name"] =name
                            licenser_dic["License_number"] =license_num
                            licenser_dic["NPN"] =npn
                            licenser_dic["City"] =city
                            licenser_dic["State"] =state
                            licenser_dic["Link"] =abs_link
                            licenser.append(licenser_dic)
                        #data_table=table_soup.find_all('table', class_='DataTable')
                        
                    
                    else:   

                        print('if start')
                        data_table=table_soup.find_all('table', class_='DataTable')


                        DataTableLabelColumn =data_table[1].find('td', class_='DataTableLabelColumn').text.replace('\t', '').replace('\n', '').strip()
                    
                        name= data_table[0].find(class_='DataTableHeaderColumn').text.replace('\t', '').replace('\n', '').strip()
                        license_num=data_table[2].find_all('td',class_='DataTableTextColumn')[1].text.replace('\t', '').replace('\n', '').strip()
                        npn=data_table[0].find(class_="DataTableTextColumn").text.replace('\t', '').replace('\n', '').replace('National Producer Number:','').strip()
                        city=data_table[1].find_all('td',class_='DataTableTextColumn')[0].text.replace('\t', '').replace('\n', '').strip()
                        state=city
                        name_link = ""
                        abs_link=f'https://www.sircon.com{name_link}'
                        licenser_dic={}
                        licenser_dic["Name"] =name
                        licenser_dic["License_number"] =license_num
                        licenser_dic["NPN"] =npn
                        licenser_dic["City"] =city
                        licenser_dic["State"] =state
                        licenser_dic["Link"] =abs_link    
                        licenser.append(licenser_dic)
                        browser.find_by_value('Revise Inquiry').first.click()
                        
                
                
                

        except TypeError:
            
            pass        


browser.quit()   
licenser_df=pd.DataFrame(licenser)    
licenser_df.to_csv("licenser.csv")
 