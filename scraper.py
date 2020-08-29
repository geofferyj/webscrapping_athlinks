# import selenium for webscrapping 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# import other utility modules
import time, re, pandas as pd


print("---------------------------- BEGIN PROCESSING ----------------------------")


# set options for the chrome driver 
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument("--start-maximized")
options.add_argument('window-size=2560,1440')

# open a headless browser with chrome driver in current directory
browser1 = webdriver.Chrome("./chromedriver", options=options)

# set delay on browser to allow page load data
browser1.implicitly_wait(10)

# make request to the results page
browser1.get("https://www.athlinks.com/event/18578/results/Event/901227/Course/1763149/Results")

# store page source in this variable
source = ""
x = 0
while True:
    x += 1
    
    # pause for additional 5 seconds to make sure page has loaded completely
    time.sleep(5)
    
    source += browser1.page_source
    print(f"copied page {x}")
    
    # try to find next button 
    # if found:  
    try:
        
        # find the button
        next_button = browser1.find_element_by_xpath('//button[text()=">"]')
        
        # click it
        browser1.execute_script("arguments[0].click();", next_button)
    except NoSuchElementException:
        # if not found (i.e at the last page)
        # break out of (exit) the loop
        break

# close the browser
browser1.quit()

# find and extract all bibs from page source
bibs = re.findall("(?<=/event/18578/results/Event/901227/Course/1763149/Bib/)\d+", source)
print(len(bibs))
# bibs = ['732', '709', '305', '687', '730', '799', '408', '684', '525', '731', '210', '165', '713', '7', '376', '834', '474', '634', '572', '590', '734', '448', '88', '546', '600', '384', '435', '402', '767', '16', '431', '602', '837', '589', '288', '498', '737', '814', '690', '688', '813', '167', '743', '544', '8', '613', '633', '805', '812', '724', '433', '374', '700', '506', '593', '87', '626', '777', '903', '534', '552', '140', '372', '559', '660', '680', '411', '404', '194', '432', '610', '720', '902', '398', '308', '467', '735', '554', '654', '277', '157', '750', '539', '798', '780', '710', '405', '635', '683', '471', '510', '96', '476', '494', '708', '555', '694', '598', '582', '771', '462', '838', '465', '366', '422', '839', '627', '322', '699', '678', '816', '337', '551', '636', '469', '27', '38', '452', '282', '236', '765', '513', '62', '493', '707', '764', '566', '473', '682', '527', '570', '763', '401', '656', '427', '802', '122', '817', '512', '28', '92', '511', '367', '321', '563', '652', '540', '836', '722', '564', '389', '828', '843', '65', '220', '644', '776', '514', '795', '693', '686', '696', '20', '383', '543', '228', '135', '736', '760', '625', '364', '586', '804', '164', '104', '67', '778', '221', '302', '373', '796', '773', '360', '420', '99', '854', '246', '791', '301', '171', '588', '545', '352', '327', '623', '155', '822', '356', '561', '800', '717', '658', '490', '663', '768', '665', '782', '808', '385', '243', '497', '276', '518', '399', '761', '576', '528', '361', '579', '548', '501', '485', '19', '390', '111', '370', '29', '507', '622', '811', '279', '278', '396', '195', '801', '826', '789', '460', '51', '298', '719', '603', '492', '89', '71', '357', '733', '334', '702', '725', '810', '451', '647', '833', '766', '458', '692', '259', '829', '809', '152', '577', '108', '251', '655', '250', '222', '562', '556', '728', '819', '264', '310', '181', '840', '825', '132', '217', '242', '502', '585', '757', '347', '110', '444', '214', '774', '484', '105', '509', '265', '697', '421', '549', '353', '330', '488', '391', '345', '677', '480', '400', '781', '691', '446', '792', '638', '230', '240', '500', '648', '596', '571', '22', '646', '521', '515', '139', '18', '375', '472', '331', '676', '464', '779', '759', '24', '198', '76', '844', '662', '177', '328', '329', '740', '695', '535', '339', '201', '584', '806', '312', '202', '66', '208', '714', '803', '275', '437', '36', '440', '793', '668', '901', '430', '112', '479', '698', '815', '726', '203', '608', '158', '91', '216', '253', '769', '42', '124', '653', '55', '706', '343', '701', '33', '640', '35', '326', '12', '190', '712', '78', '98', '21', '449', '787', '418', '447', '601', '522', '523', '147', '363', '403', '75', '439', '371', '368', '49', '744', '137', '313', '661', '541', '542', '248', '318', '553', '715', '289', '671', '31', '516', '517', '350', '166', '595', '756', '762', '672', '204', '666', '125', '753', '81', '670', '842', '499', '667', '299', '123', '456', '607', '642', '785', '524', '675', '162', '659', '450', '340', '704', '150', '151', '786', '127', '519', '47', '50', '587', '274', '409', '557', '342', '54', '624', '599', '429', '503', '483', '739', '443', '309', '550', '565', '807', '775', '820', '291', '463', '269', '475', '413', '738', '594', '412', '705', '344', '520', '292', '466', '645', '718', '908', '477', '70', '637', '434', '77', '227', '827', '219', '126', '619', '410', '380', '788', '323', '673', '237', '797', '141', '643', '168', '650', '716', '628', '325', '674', '592', '294', '505', '119', '835', '244', '131', '581', '547', '315', '314', '174', '319', '729', '681', '235', '306', '307', '606', '295', '614', '824', '419', '80', '468', '397', '205', '341', '182', '495', '144', '455', '454', '23', '424', '180', '393', '25', '783', '784', '536', '533', '573', '841', '61', '56', '758', '569', '415', '39', '130', '15', '215', '57', '723', '560', '317', '772', '346', '159', '657', '821', '751', '679', '199', '72', '73', '238', '831', '629', '620', '300', '790', '639', '615', '770', '711', '286', '641', '618', '531', '532', '213', '303', '436', '617', '830', '153']
# chunks = [bibs[x:x+50] for x in range(0, len(bibs), 50)]


# open another browser
browser2 = webdriver.Chrome("./chromedriver", options=options)
browser2.implicitly_wait(5)

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

# iterate over the list of bibs and make requests

for bib in bibs:
    
    browser2.get(f"https://www.athlinks.com/event/18578/results/Event/901227/Course/1763149/Bib/{bib}")
    
    while True:
        try:

            # select the name of participant from page
            name = browser2.find_element_by_id("athlete-profile-link")
            
            # select the gender of participant from page
            gender = browser2.find_element_by_id("ageGender")
            
            # select the city/state of participant from page
            city_state = browser2.find_element_by_id("IRPUserLocation")
            
            # select the chip start time of participant from page
            chip_start_time = browser2.find_element_by_xpath('//div[text()="Chip Start Time"]/following-sibling::div[1]')
            
            # select the gun time of participant from page
            gun_time = browser2.find_element_by_xpath('//div[text()="Gun time"]/following-sibling::div[1]')
            
            # select the 10K time of participant from page
            _10k = browser2.find_element_by_xpath('//div[text()="10K"]/following-sibling::div[last()]')
            
            # select the half time of participant from page
            half = browser2.find_element_by_xpath('//div[text()="HALF"]/following-sibling::div[last()]')
            
            # select the 30K time of participant from page
            _30k = browser2.find_element_by_xpath('//div[text()="30K"]/following-sibling::div[last()]')
            
            # select the full course time of participant from page
            full_course = browser2.find_element_by_xpath('//div[text()="Full Course"]/following-sibling::div[last()]')
            break
        except NoSuchElementException:
            
            time.sleep(2)
            
    
    
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
    
    
    print(f"---> Entry for {name.text} created")

# close second browser
browser2.quit()

# convert results dict to a panda dataframe
df = pd.DataFrame(results_dict)

# convert pandas dataframe to a csv file 
df.to_csv(f"times.csv", index=False)

print(f"---------------------------- END OF PROCESSING FOR CHUNK ----------------------------")