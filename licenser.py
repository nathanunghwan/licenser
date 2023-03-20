# Import 
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
#url = 'https://www.sircon.com/index.jsp/'
url= 'https://www.sircon.com/ComplianceExpress/Inquiry/consumerInquiry.do?nonSscrb=Y'
browser.visit(url)
time.sleep(60)

# Convert the browser html to a soup object and find the latest title
element = browser.find_option_by_text('Georgia').first.click()
time.sleep(10)


#indiviual select

type_element = browser.find_by_xpath('//*[@id="entityTypes"]/div[2]/input[2]').first
type_element.click()

#final
alpa_list=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
licenser=[]
for i in alpa_list:
    for j in alpa_list:
        try:
            name_city=i+j
            print(name_city)
            input_element = browser.find_by_name('lastName')
            input_element.fill(name_city)
            time.sleep(3)
            
            input_element = browser.find_by_name('city')
            input_element.fill(name_city)
            time.sleep(3)
            #license type
            license_element = browser.find_by_xpath('//*[@id="border"]/form[3]/div[6]/div[3]/select/option[21]').first
            license_element.click()
            time.sleep(3)
            #result 100
            element = browser.find_option_by_text('100').first.click()
            #//*[@id="resultsPerPage"]/select
            time.sleep(3)
            #submit
            submit_element=browser.find_by_id('submitButton').click()
            time.sleep(120)

            
            # Parse the HTML
            html = browser.html
            table_soup = soup(html,'html.parser')
            data_table=table_soup.find('table', class_='DataTable')
            
            if data_table is True:
                name_one= data_table.find(class_='DataTableHeaderColumn').text
                license_num=data_table.find_by_xpath('/html/body/table/tbody/tr[3]/td/form/table[4]/tbody/tr[2]/td[2]').text
                npn=data_table.find_by_xpath('/html/body/table/tbody/tr[3]/td/form/table[2]/tbody/tr[2]/td').text
                city=data_table.find_by_xpath('/html/body/table/tbody/tr[3]/td/form/table[3]/tbody/tr[1]/td[2]').text
                state=data_table.find_by_xpath('/html/body/table/tbody/tr[3]/td/form/table[3]/tbody/tr[1]/td[2]').text
                name_link = ""
                abs_link=f'https://www.sircon.com{name_link}'
                licenser_dic={}
                licenser_dic["Name"] =name
                licenser_dic["License_number"] =license_num
                licenser_dic["NPN"] =npn
                licenser_dic["City"] =city
                licenser_dic["State"] =state
                licenser_dic["Link"] =abs_link
            #     for key, value in licenser_dic.items():
            #         licenser_dic[key] = value.replace('\n', '')

                licenser.append(licenser_dic)
                state=table_soup.find_by_xpath('/html/body/table/tbody/tr[3]/td/form/div[4]/table[2]/tbody/tr[2]/td/input').click()
            # even=table_soup.find_all(class_='ResultTableTextEvenRow')
            # odd=table_soup.find_all(class_='ResultTableTextOddRow')
            else:
            # for i in range(len(even)):
            #     all_column=even[i].find_all('td', class_='ResultTableTextColumn')
            #     name=all_column[0].text
            #     license_num=all_column[1].text
            #     npn=all_column[5].text
            #     city=all_column[6].text
            #     state=all_column[7].text
            #     name_link = even[i].find('td', class_='ResultTableTextColumn').a.get('href')
            #     print(name)
        
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
                #     for key, value in licenser_dic.items():
                #         licenser_dic[key] = value.replace('\n', '')

                    licenser.append(licenser_dic)
        except TypeError:
        # Handle the case where item is None
            pass        

licenser_df=pd.DataFrame(licenser)    
licenser_df.to_csv("licenser.csv")

browser.quit()

        ## Scraping
        # name = hemi_soup.find('h2', class_='title').text
        #name_link = table_soup.find('td').a.get('href')
        #name_link=table_soup.find('td', class_='ResultTableTextColumn').a.get('href')
        #name_name=table_soup.find_all('td', class_='ResultTableTextColumn')
        # lic_num = hemi_soup.find('li').a.get('href')
        # npn = hemi_soup.find('li').a.get('href')
        # city = hemi_soup.find('li').a.get('href')
        # state = hemi_soup.find('li').a.get('href')

        #print(name_link)




        # # Store findings into a dictionary and append to list
        # hemispheres = {}
        # hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        # hemispheres['title'] = title
        # hemisphere_image_urls.append(hemispheres)

        # # Browse back to repeat
        # browser.back()
        
