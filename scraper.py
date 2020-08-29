# import selenium for webscrapping 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from concurrent.futures.thread import ThreadPoolExecutor

# import other utility modules
import time, os, re, pandas as pd


print("---------------------------- BEGIN PROCESSING ----------------------------")


# set options for the chrome driver 
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument("--start-maximized")
options.add_argument('window-size=2560,1440')

# open a headless browser with chrome driver in current directory
browser = webdriver.Chrome("./chromedriver84", options=options)

# set delay on browser to allow page load data
browser.implicitly_wait(10)

# make request to the results page
browser.get("https://www.athlinks.com/event/18578/results/Event/901227/Course/1763149/Results")

# store page source in this variable
source = ""
x = 0
while True:
    x += 1
    
    # pause for additional 5 seconds to make sure page has loaded completely
    time.sleep(5)
    
    source += browser.page_source
    print(f"copied page {x}")
    
    # try to find next button 
    # if found:  
    try:
        
        # find the button
        next_button = browser.find_element_by_xpath('//button[text()=">"]')
        
        # click it
        browser.execute_script("arguments[0].click();", next_button)
    except NoSuchElementException:
        # if not found (i.e at the last page)
        # break out of (exit) the loop
        break

# close the browser
browser.quit()

# find and extract all bibs from page source
bibs = re.findall("(?<=/event/18578/results/Event/901227/Course/1763149/Bib/)\d+", source)
print(len(bibs))

chunks = [bibs[x:x+50] for x in range(0, len(bibs), 50)]


# open another browser
browser1 = webdriver.Chrome("./chromedriver", options=options)
browser2 = webdriver.Chrome("./chromedriver", options=options)
browser3 = webdriver.Chrome("./chromedriver", options=options)
browser4 = webdriver.Chrome("./chromedriver", options=options)
browser5 = webdriver.Chrome("./chromedriver", options=options)
browser6 = webdriver.Chrome("./chromedriver", options=options)
browser7 = webdriver.Chrome("./chromedriver", options=options)
browser8 = webdriver.Chrome("./chromedriver", options=options)
browser9 = webdriver.Chrome("./chromedriver", options=options)
browser10 = webdriver.Chrome("./chromedriver", options=options)
browser11 = webdriver.Chrome("./chromedriver", options=options)
browser12 = webdriver.Chrome("./chromedriver", options=options)

browsers = [browser1,browser2,browser3,browser4,browser5,browser6,browser7,browser8,browser9,browser10,browser11,browser12]

print(len(browsers), len(chunks), len(range(len(browsers))))


# iterate over the list of bibs and make requests

def thread_func(browser, x, chunk):
    print(f"---------------------------- BEGIN PROCESSING FOR CHUNK {x} ----------------------------")
    # dictionary to hold data for each participant
    results_dict = {"Bib":[],
               "Name":[],
               "Gender":[],
               "City/State":[],
               "Chip Start Time":[],
               "Gun Time":[],
               "10K Time":[],
               "Half Time":[],
               "30K Time":[],
               "Full Course Time":[]}
    
    browser.implicitly_wait(6)
    
    for bib in chunk:
        
        browser.get(f"https://www.athlinks.com/event/18578/results/Event/901227/Course/1763149/Bib/{bib}")
        
    
        # select the name of participant from page
        name = browser.find_element_by_id("athlete-profile-link")
        
        # select the gender of participant from page
        gender = browser.find_element_by_id("ageGender")
        
        # select the city/state of participant from page
        city_state = browser.find_element_by_id("IRPUserLocation")
        
        # select the chip start time of participant from page
        chip_start_time = browser.find_element_by_xpath('//div[text()="Chip Start Time"]/following-sibling::div[1]')
        
        # select the gun time of participant from page
        gun_time = browser.find_element_by_xpath('//div[text()="Gun time"]/following-sibling::div[1]')
        
        # select the 10K time of participant from page
        _10k = browser.find_element_by_xpath('//div[text()="10K"]/following-sibling::div[last()]')
        
        # select the half time of participant from page
        half = browser.find_element_by_xpath('//div[text()="HALF"]/following-sibling::div[last()]')
        
        # select the 30K time of participant from page
        _30k = browser.find_element_by_xpath('//div[text()="30K"]/following-sibling::div[last()]')
        
        # select the full course time of participant from page
        full_course = browser.find_element_by_xpath('//div[text()="Full Course"]/following-sibling::div[last()]')            
        
    
        # -------- create entry for participant in results_dict
        results_dict["Bib"].append(bib)
        results_dict["Name"].append(name.text)
        results_dict["Gender"].append(gender.text[0])
        results_dict["City/State"].append(city_state.text)
        results_dict["Chip Start Time"].append(chip_start_time.text)
        results_dict["Gun Time"].append(gun_time.text)
        results_dict["10K Time"].append(_10k.text)
        results_dict["Half Time"].append(half.text)
        results_dict["30K Time"].append(_30k.text)
        results_dict["Full Course Time"].append(full_course.text)
        
        
        print(f"---> Entry for {name.text} created in chuck {x}")

    # close second browser
    browser.quit()

    # convert results dict to a panda dataframe
    df = pd.DataFrame(results_dict)

    # convert pandas dataframe to a csv file 
    df.to_csv(f"result/times_{x}.csv", index=False)

    print(f"---------------------------- END OF PROCESSING FOR CHUNK {x} ----------------------------")
    
#  Added concurrency for performance boost
with ThreadPoolExecutor() as executor:
    
    [executor.submit(thread_func, b,x, chunk) for (b, x, chunk) in zip(browsers[0:3], range(len(browsers))[0:3], chunks[0:3])]


with ThreadPoolExecutor() as executor:
    
    [executor.submit(thread_func, b,x, chunk) for (b, x, chunk) in zip(browsers[3:6], range(len(browsers))[3:6], chunks[3:6])]


with ThreadPoolExecutor() as executor:
    
    [executor.submit(thread_func, b,x, chunk) for (b, x, chunk) in zip(browsers[6:9], range(len(browsers))[6:9], chunks[6:9])]


with ThreadPoolExecutor() as executor:
    
    executor.submit(thread_func, browsers[11], range(len(browsers))[11], chunks[11])


# concatenate all chucks into one file
df_list = os.listdir("result")
result_frame = pd.concat((pd.read_csv(f"result/{f}") for f in df_list))
result_frame.to_csv("data.csv", index=False)