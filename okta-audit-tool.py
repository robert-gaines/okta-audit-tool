#!/usr/bin/env python3

_AUTH_ = 'RWG' # 01APR23

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    import pandas as pd
    import xlsxwriter
    import requests
    import getpass
    import time
    import sys
    import os
except Exception as e:
    import sys
    print("[!] Library error: {0}".format(e))

class Window(QWidget):

    def __init__(self,parent=None):
        #
        super().__init__(parent)
        #
        self.next   = True   # Sentinel value for the pagination function
        self.format = 'xlsx' # Default document format 
        #
        QMainWindow.__init__(self)
        QWidget.__init__(self)
        QLabel.__init__(self)
        #
        self.setWindowTitle('Okta Audit Tool')
        self.setGeometry(550,100,750,200)
        self.setStyleSheet("background-color: darkgray; border: 2px black solid")
        #
        '''
        -> Define Labels and Widgets
        '''
        #
        self.domain_label = QLabel("Okta Domain")
        self.domain_label.setStyleSheet("height: 25px; width: 50px; color: White; font-style: bold; font-size: 16px; font-family: Arial")                                    
        self.domain_field = QLineEdit()                                          
        self.domain_field.setPlaceholderText("(Organization Specific Okta Domain)")
        self.domain_field.setStyleSheet("height: 25px; width: 50px; background-color: black; color: White; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 16px; font-family: Arial")
        #
        self.api_key_label = QLabel("API Key")
        self.api_key_label.setStyleSheet("height: 25px; width: 50px; color: White; font-style: bold; font-size: 16px; font-family: Arial")                                    
        self.api_key_field = QLineEdit()                                          
        self.api_key_field.setPlaceholderText("(Okta API Key)")
        self.api_key_field.setStyleSheet("height: 25px; width: 50px; background-color: black; color: White; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 16px; font-family: Arial")
        #
        self.params_button = QPushButton("Embed Parameters", self)
        self.params_button.setGeometry(100,100,600,400)
        self.params_button.setStyleSheet("margin-top: 5px; height: 50px; width: 50px; background-color: black; color: #ff8c00; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")
        #
        self.radio_label = QLabel("Document Format")
        self.radio_label.setStyleSheet("height: 25px; width: 50px; color: White; font-style: bold; font-size: 16px; font-family: Arial")  
        self.radiobutton_xlsx = QRadioButton("XLSX")
        self.radiobutton_xlsx.format = "xlsx"
        self.radiobutton_csv = QRadioButton("CSV")
        self.radiobutton_csv.format = "csv"
        self.radiobutton_xlsx.setStyleSheet("margin-top: 5px; height: 25px; width: 5px; color: White; font-style: bold; font-size: 18px; font-family: Arial")
        self.radiobutton_csv.setStyleSheet("margin-top: 5px; height: 25px; width: 5px; color: White; font-style: bold; font-size: 18px; font-family: Arial")
        #
        self.export_user_button = QPushButton("Export Users", self)
        self.export_user_button.setGeometry(100,100,600,400)
        self.export_user_button.setStyleSheet("margin-top: 5px; height: 50px; width: 50px; background-color: black; color: #ff8c00; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")
        #
        self.export_groups_button = QPushButton("Export Groups", self)
        self.export_groups_button.setGeometry(100,100,600,400)
        self.export_groups_button.setStyleSheet("margin-top: 5px; height: 50px; width: 50px; background-color: black; color: #ff8c00; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")
        #
        self.export_apps_button = QPushButton("Export Applications", self)
        self.export_apps_button.setGeometry(100,100,600,400)
        self.export_apps_button.setStyleSheet("margin-top: 5px; height: 50px; width: 50px; background-color: black; color: #ff8c00; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")
        #
        self.export_group_members_button = QPushButton("Export Group Members", self)
        self.export_group_members_button.setGeometry(100,100,600,400)
        self.export_group_members_button.setStyleSheet("margin-top: 5px; height: 50px; width: 50px; background-color: black; color: #ff8c00; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")
        #
        self.export_app_group_mappings_button = QPushButton("Export Application \n Group Mappings", self)
        self.export_app_group_mappings_button.setGeometry(100,100,600,400)
        self.export_app_group_mappings_button.setStyleSheet("margin-top: 5px; height: 50px; width: 50px; background-color: black; color: #ff8c00; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")
        #
        self.export_app_user_mappings_button = QPushButton("Export Application \n User Mappings", self)
        self.export_app_user_mappings_button.setGeometry(100,100,600,400)
        self.export_app_user_mappings_button.setStyleSheet("margin-top: 5px; height: 50px; width: 50px; background-color: black; color: #ff8c00; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")
        #
        self.cancel_button = QPushButton("Exit", self)
        self.cancel_button.setGeometry(100,100,600,400)
        self.cancel_button.setStyleSheet("margin-top: 5px; height: 50px; width: 50px; background-color: black; color: #ff8c00; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")
        #
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setGeometry(100,100,600,400)
        self.reset_button.setStyleSheet("margin-top: 5px; height: 50px; width: 50px; background-color: black; color: #ff8c00; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 18px; font-family: Arial")
        #
        self.output_window = QPlainTextEdit("")
        self.output_window.setStyleSheet("height: 200px; width: 200px; background-color: black; color: #ff8c00; border: 2px solid black; border-radius: 10px; font-style: bold; font-size: 16px; font-family: Arial")
        self.output_window.resize(200,400)
        self.output_window.ensureCursorVisible()
        self.output_window.insertPlainText("Please enter and embed your domain and authentication data \n")
        #
        '''
        -> Create primary and subordinate layouts
        '''
        #
        main_layout                       = QFormLayout()
        self.vertical_data_box            = QVBoxLayout()
        self.radio_button_hbox            = QHBoxLayout()
        self.horizontal_data_box_one      = QHBoxLayout()
        self.horizontal_data_box_two      = QHBoxLayout()
        self.horizontal_data_box_three    = QHBoxLayout()
        self.horizontal_data_box_four     = QHBoxLayout()
        self.horizontal_data_box_five     = QHBoxLayout()
        #
        '''
        -> Button Actions
        '''
        #
        self.params_button.clicked.connect(self.EmbedAndTestParameters)
        self.radiobutton_xlsx.toggled.connect(self.ProcessRadioButton)
        self.radiobutton_csv.toggled.connect(self.ProcessRadioButton)
        self.export_user_button.clicked.connect(self.CollectAllUsers)
        self.export_groups_button.clicked.connect(self.CollectAllGroups)
        self.export_apps_button.clicked.connect(self.CollectAllApplications)
        self.export_group_members_button.clicked.connect(self.CollectAllGroupMembers)
        self.export_app_user_mappings_button.clicked.connect(self.CollectUserAppMappings)
        self.export_app_group_mappings_button.clicked.connect(self.CollectGroupAppMappings)
        self.reset_button.clicked.connect(self.ClearFields)
        self.cancel_button.clicked.connect(self.Terminate)
        #
        '''
        -> Add widgets to the each layout
        '''
        #
        self.vertical_data_box.addWidget(self.domain_label)
        self.vertical_data_box.addWidget(self.domain_field)
        self.vertical_data_box.addWidget(self.api_key_label)
        self.vertical_data_box.addWidget(self.api_key_field)
        self.vertical_data_box.addWidget(self.params_button)
        self.radio_button_hbox.addWidget(self.radio_label)
        self.radio_button_hbox.addWidget(self.radiobutton_xlsx)
        self.radio_button_hbox.addWidget(self.radiobutton_csv)
        self.horizontal_data_box_one.addWidget(self.export_user_button)
        self.horizontal_data_box_one.addWidget(self.export_groups_button)
        self.horizontal_data_box_two.addWidget(self.export_apps_button)
        self.horizontal_data_box_two.addWidget(self.export_group_members_button)
        self.horizontal_data_box_three.addWidget(self.export_app_user_mappings_button)
        self.horizontal_data_box_three.addWidget(self.export_app_group_mappings_button)
        self.horizontal_data_box_four.addWidget(self.output_window)
        self.horizontal_data_box_five.addWidget(self.cancel_button)
        self.horizontal_data_box_five.addWidget(self.reset_button)
        #
        '''
        -> Add subordinate layouts to the main layout
        '''
        #
        main_layout.addRow(self.vertical_data_box)
        main_layout.addRow(self.radio_button_hbox)
        main_layout.addRow(self.horizontal_data_box_one)
        main_layout.addRow(self.horizontal_data_box_two)
        main_layout.addRow(self.horizontal_data_box_three)
        main_layout.addRow(self.horizontal_data_box_four)
        main_layout.addRow(self.horizontal_data_box_five)
        #
        self.setLayout(main_layout)

    def EmbedAndTestParameters(self):
        '''
        -> Input  : Domain and API text field inputs
        -> Process: 
            -> Instantiate key and domain variable values
            -> Test key, domain, and headers with a single API call        
        -> Output : 
            -> API Key, Domain, and Header values
            -> Parameter validation feedback in the UI
        '''
        try:
            self.key     = self.api_key_field.text()
            self.domain  = self.domain_field.text()
            self.headers = {
                            "Content-Type": "application/json",
                            "Authorization": "SSWS {0}".format(self.key)
                        }
            self.output_window.insertPlainText("Testing authentication and domain data... \n")
            url       = "https://{0}.okta.com/api/v1/users?limit=200".format(self.domain)
            req       = requests.get(headers=self.headers,url=url)
            if(req.status_code == 200):
                self.output_window.insertPlainText("Parameter data is valid! \n")
            else:
                self.output_window.insertPlainText("Parameters are invalid \n")
        except Exception as e: 
            self.output_window.insertPlainText("Exception raised: {0} \n".format(e))

    def ClearFields(self):
        '''
        -> Input:   Button click signal from UI
        -> Process: Clear all text fields
        -> Output:  Vacant text fields
        '''
        try:
            self.domain_field.setText("")
            self.api_key_field.setText("")
            self.output_window.clear()
        except Exception as e:
            self.output_window.insertPlainText("Exception raised: {0} \n".format(e))

    def Terminate(self):
        '''
        -> Input   : Button click signal
        -> Process : Terminate main window
        -> Output  : Application is terminated
        '''
        sys.exit()

    def ProcessRadioButton(self):
        '''
        -> Input   : Radio button click / input
        -> Process : Identify activated radio button / retrieve value
        -> Output  : Document format is set for further processing
        '''
        try:
            self.buttonValue= self.sender()
            if(self.buttonValue.isChecked()):
                self.output_window.insertPlainText("Document format set to: {0}\n".format(self.buttonValue.format))
                self.format = self.buttonValue.format
        except:
            self.output_window.insertPlainText("Exception raised: {0} \n".format(e))

    def ParseHeaders(self,headers):
        '''
        ***
        This function supports pagination.
        Instead of using an integer index, the Okta API returns the link
        for the next API call in the headers of the current call.
        ***
        -> Input   : Headers returned from an API call
        -> Process : 
            -> Parse headers
            -> Identify the 'next' value with the corresponding link
            -> Return link for the next API call
            -> Return False is the link is not located
        -> Output  : link variable is returned with URL value ; link is otherwise False
        '''
        link     = False
        for entry in headers.keys():
            if(entry == 'link' and ("next" in headers[entry])):
                link = headers[entry]
                link = link.split(',')[1]
                link = link.split(';')[0]
                link = link.lstrip(' <')
                link = link.rstrip('>')
                return link
            if(entry == 'link' and ("next" not in headers[entry]) and (self.next == False)):
                link = headers[entry]
                link = link.split(';')[0]
                link = link.lstrip(' <')
                link = link.rstrip('>')
                self.next = True
                return link
        return link

    def GenFileName(self,category):
        '''
        -> Input   : Okta API data category (Users,Apps,etc) ; File format type (csv,xlsx)
        -> Process : Generate a time stamped file name
        -> Output  : Return the filename as a string value
        '''
        file_name        = category+"_"
        timestamp        = time.ctime()
        replace_colons   = timestamp.replace(":",'_')
        final_timestamp  = replace_colons.replace(" ","_")
        file_name       += final_timestamp
        file_name       += '.'
        file_name       += self.format
        self.output_window.insertPlainText("Generated filename: {0}\n".format(file_name))
        return file_name

    def CollectAllUsers(self):
        '''
        -> Input   :
            -> API Key
            -> Domain Value
            -> Headers
        -> Process :
            -> API call to the users endpoint
            -> If the first call is successful, subsequent calls are made via pagination
            -> User data is parsed into either a csv or xlsx format
        -> Output  :
            -> User inventory file in either csv or xlsx format
        '''
        self.output_window.insertPlainText("Collecting Okta users...\n")
        url       = "https://{0}.okta.com/api/v1/users?limit=200".format(self.domain)
        req       = requests.get(headers=self.headers,url=url)
        status    = req.status_code
        next_url  = self.ParseHeaders(req.headers)
        employees = [] 
        fileName  = self.GenFileName('Okta_Users')
        try:
            if(status == 200):
                self.output_window.insertPlainText("Creating the user inventory....\n")
                content = req.json()
                for entry in content:
                    id              = entry['id']
                    status          = entry['status']
                    created         = entry['created']
                    activated       = entry['activated']
                    changed         = entry['statusChanged']
                    lastLogin       = entry['lastLogin']
                    lastUpdated     = entry['lastUpdated']
                    passwordChanged = entry['passwordChanged']

                    employeeDictionary = {
                                            "ID": id,
                                            "Status": status,
                                            "Created": created,
                                            "Activated": activated,
                                            "Status Changed": changed,
                                            "Last Login": lastLogin,
                                            "Last Updated": lastUpdated,
                                            "Password Changed": passwordChanged
                                         }
                    for item in entry['profile'].keys():
                        employeeDictionary[item] = entry['profile'][item]
                    employeeDictionary['Credentials'] = entry['credentials']
                    employeeDictionary['Links']       = entry['_links']
                    employees.append(employeeDictionary)
                while(next_url):
                    url       = "https://{0}.okta.com/api/v1/users?limit=200".format(self.domain)
                    req       = requests.get(headers=self.headers,url=next_url)
                    status    = req.status_code
                    next_url  = self.ParseHeaders(req.headers)
                    content   = req.json()
                    for entry in content:
                        self.output_window.insertPlainText("Located user ID: {0} \n".format(entry['id']))
                        id              = entry['id']
                        status          = entry['status']
                        created         = entry['created']
                        activated       = entry['activated']
                        changed         = entry['statusChanged']
                        lastLogin       = entry['lastLogin']
                        lastUpdated     = entry['lastUpdated']
                        passwordChanged = entry['passwordChanged']

                        employeeDictionary = {
                                                "ID": id,
                                                "Status": status,
                                                "Created": created,
                                                "Activated": activated,
                                                "Status Changed": changed,
                                                "Last Login": lastLogin,
                                                "Last Updated": lastUpdated,
                                                "Password Changed": passwordChanged
                                            }
                        
                        for item in entry['profile'].keys():
                            employeeDictionary[item] = entry['profile'][item]
                        employeeDictionary['Credentials'] = entry['credentials']
                        employeeDictionary['Links']       = entry['_links']
                        employees.append(employeeDictionary)
                try:
                    if(self.format == 'xlsx'):
                        df = pd.DataFrame(employees).to_excel(fileName,sheet_name='Okta_Users',index=False)
                    if(self.format == 'csv'):
                        df = pd.DataFrame(employees).to_csv(fileName,index=False)
                    self.output_window.insertPlainText("Successfully created Okta user inventory \n")
                except Exception as e:
                    self.output_window.insertPlainText("Error: {0}".format(e))
            else:
                self.output_window.insertPlainText("Failed to contact the Okta API endpoint...\n")
        except Exception as e:
            self.output_window.insertPlainText("Exception raised: {0} \n".format(e))

    def CollectAllGroups(self):
        '''
        -> Input   :
            -> API Key
            -> Domain Value
            -> Headers
        -> Process :
            -> API call to the groups endpoint
            -> Group data is parsed into either a csv or xlsx format
        -> Output  :
            -> Group inventory file in either csv or xlsx format
        '''       
        self.output_window.insertPlainText("Collecting Okta groups...\n")
        url       = "https://{0}.okta.com/api/v1/groups".format(self.domain)
        req       = requests.get(headers=self.headers,url=url)
        status    = req.status_code
        fileName  = self.GenFileName('Okta_Groups')
        try:
            if(status == 200):
                content = req.json()
                groups  = {}
                for entry in content:
                    temp_dict = {}
                    temp_list = []
                    for element in entry.keys():
                        temp_dict[element] = entry[element]
                    temp_list.append(temp_dict)
                    groups[entry['profile']['name']] = pd.DataFrame(data=temp_list)
                if(self.format == 'xlsx'):
                    self.output_window.insertPlainText("Creating Okta Groups inventory... \n")
                    writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
                    bad_chars = ['[',']',':','*','?','/','\`']
                    for group in groups.keys():
                        self.output_window.insertPlainText("Processing: {0} \n".format(group))
                        group_name = group
                        if(len(group_name) >= 31):
                            group_name = group[0:30]
                        for char in group_name:
                            if(char in bad_chars):
                                group_name = group_name.replace(char,'_')
                        groups[group].to_excel(writer,sheet_name=group_name,index=False)
                    writer.close()
                    self.output_window.insertPlainText("Successfully created the Okta Groups inventory \n")
                if(self.format == 'csv'):
                    self.output_window.insertPlainText("Creating Okta Groups inventory... \n")
                    df = pd.DataFrame(content)
                    df.to_csv(fileName,index=False)
                    self.output_window.insertPlainText("Successfully created the Okta Groups inventory \n")
            else:
                self.output_window.insertPlainText("Failed to communicate with the Okta API endpoint \n")
        except Exception as e:
                self.output_window.insertPlainText("Exception raised: {0} \n".format(e))

    def CollectAllApplications(self):
        '''
        -> Input   :
            -> API Key
            -> Domain Value
            -> Headers
        -> Process :
            -> API call to the application endpoint
            -> Application data is parsed into either a csv or xlsx format
        -> Output  :
            -> Application inventory file in either csv or xlsx format
            -> XLSX format is broken out into worksheets
        '''
        self.output_window.insertPlainText("Collecting application data \n")
        url = "https://{0}.okta.com/api/v1/apps".format(self.domain)
        req = requests.get(headers=self.headers,url=url)
        content = req.json()
        try:
            if(req.status_code == 200):
                next_url            = self.ParseHeaders(req.headers)
                apps_filename       = self.GenFileName('Okta_Applications')
                okta_apps           = []
                self.output_window.insertPlainText("Creating Okta Application inventory...\n")
                for entry in content:
                    temp_list = []
                    temp_dict = {}
                    self.output_window.insertPlainText("Processing: {0}".format(entry['name']))
                    for item in entry.keys():
                        temp_dict[item] = entry[item]
                    temp_list.append(temp_dict)
                    okta_apps.append(temp_dict) 
                while(next_url):
                    url      = "https://{0}.okta.com/api/v1/apps".format(self.domain)
                    req      = requests.get(headers=self.headers,url=next_url)
                    next_url = self.ParseHeaders(req.headers)
                    content  = req.json()
                    for entry in content:
                        temp_list = []
                        temp_dict = {}
                        self.output_window.insertPlainText("Processing: {0} \n".format(entry['name']))
                        for item in entry.keys():
                            temp_dict[item] = entry[item]
                        okta_apps.append(temp_dict)
                if(self.format == 'xlsx'): 
                    df = pd.DataFrame(okta_apps).to_excel(apps_filename,sheet_name='Okta_Applications',index=False)
                    self.output_window.insertPlainText("Sucessfully created the Okta Application inventory \n")
                if(self.format == 'csv'):
                    df = pd.DataFrame(okta_apps).to_csv(apps_filename,index=False)
                    self.output_window.insertPlainText("Sucessfully created the Okta Application inventory \n")
            else:
                self.output_window.insertPlainText("Failed to contact the Okta API endpoint... \n")
        except Exception as e:
            self.output_window.insertPlainText("Exception raised: {0} \n".format(e))

    def CollectAllGroupMembers(self):
        '''
        -> Input   :
            -> API Key
            -> Domain Value
            -> Headers
        -> Process :
            -> API call to the groups endpoint
            -> Retrieve the members URL from the groups API call
            -> Query the Group Member API with the retrieved link
            -> Group member data is parsed into either a csv or xlsx format
        -> Output  :
            -> Group member inventory file in either csv or xlsx format
        '''       
        self.output_window.insertPlainText("Collecting Okta group members... \n")
        url       = "https://{0}.okta.com/api/v1/groups".format(self.domain)
        req       = requests.get(headers=self.headers,url=url)
        status    = req.status_code
        fileName  = self.GenFileName('Okta_Group_Members')
        groups    = {}
        all_group_members = []
        try:
            if(status == 200):
                content = req.json()
                for entry in content:
                    group     = entry['profile']['name']
                    link      = entry['_links']['users']['href']
                    if(len(group) >= 31):
                        group = group[0:30]
                    self.output_window.insertPlainText("Collecting members for {0} \n".format(group))
                    group_members = []
                    user_req  = requests.get(headers=self.headers,url=link)
                    user_resp = user_req.json()
                    for entry in user_resp:
                        id              = entry['id']
                        status          = entry['status']
                        created         = entry['created']
                        activated       = entry['activated']
                        changed         = entry['statusChanged']
                        lastLogin       = entry['lastLogin']
                        lastUpdated     = entry['lastUpdated']
                        passwordChanged = entry['passwordChanged']
                        employeeDictionary = {
                                                "ID": id,
                                                "Group Name": group,
                                                "Status": status,
                                                "Created": created,
                                                "Activated": activated,
                                                "Status Changed": changed,
                                                "Last Login": lastLogin,
                                                "Last Updated": lastUpdated,
                                                "Password Changed": passwordChanged
                                                }
                        for item in entry['profile'].keys():
                            employeeDictionary[item] = entry['profile'][item]
                        employeeDictionary['Credentials'] = entry['credentials']
                        employeeDictionary['Links']       = entry['_links']
                        group_members.append(employeeDictionary)
                        all_group_members.append(employeeDictionary)
                    groups[group] = pd.DataFrame(data=group_members)
                if(self.format == 'xlsx'):
                    writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
                    for group in groups.keys():
                        self.output_window.insertPlainText("Processing: {0} \n".format(group))
                        groups[group].to_excel(writer,sheet_name=group,index=False)
                    writer.close()
                    self.output_window.insertPlainText("Successfully created the Okta Group Members inventory \n")
                if(self.format == 'csv'):
                    df = pd.DataFrame(all_group_members)
                    df.to_csv(fileName,index=False)
                    self.output_window.insertPlainText("Successfully created the Okta Group Members inventory \n")
            else:
                self.output_window.insertPlainText("Failed to contact the API endpoint \n")
        except Exception as e:
            self.output_window.insertPlainText("Exception raised: {0} \n".format(e))

    def CollectUserAppMappings(self):
        '''
        -> Input   :
            -> API Key
            -> Domain Value
            -> Headers
        -> Process :
            -> API call to the applications endpoint
            -> Retrieve application id values
            -> Query users assigned to each app by appending
               the link value to subsequent app endpoint calls
            -> Application/User mapping data is parsed into 
               either a csv or xlsx format
        -> Output  :
            -> Application/User mapping inventory file in either csv or xlsx format
        '''
        self.output_window.insertPlainText("Collecting user to application mappings... \n")
        fileName  = self.GenFileName('Okta_Apps_User_Mappings_')
        url       = "https://{0}.okta.com/api/v1/apps".format(self.domain)
        req       = requests.get(headers=self.headers,url=url)
        apps      = {}
        inventory = {}
        all_apps  = []
        try:
            if(req.status_code == 200):
                next_url = self.ParseHeaders(req.headers)
                content  = req.json()
                for entry in content:
                    self.output_window.insertPlainText("Located: {0}:{1} \n".format(entry['id'],entry['label']))
                    apps[entry['id']] = entry['label']
                while(next_url):
                    url      = "https://{0}.okta.com/api/v1/apps".format(self.domain)
                    req      = requests.get(headers=self.headers,url=next_url)
                    next_url = self.ParseHeaders(req.headers)
                    content  = req.json()
                    for entry in content:
                        self.output_window.insertPlainText("Located: {0}:{1} \n".format(entry['id'],entry['label']))
                        apps[entry['id']] = entry['label']
                for item in apps.keys():
                    id    = item
                    label = apps[item]
                    self.output_window.insertPlainText("Retrieving users for: {0} \n".format(label))
                    url   = "https://{0}.okta.com/api/v1/apps/{1}/users".format(self.domain,id)
                    req   = requests.get(headers=self.headers,url=url)
                    content = req.json()
                    for item in content:
                        item['Application'] = label
                        all_apps.append(item)
                    inventory[label] = pd.DataFrame(data=content)
                    time.sleep(1)
                if(self.format == 'xlsx'):
                    writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
                    bad_chars = ['[',']',':','*','?','/','\`']
                    for app in inventory.keys():
                        self.output_window.insertPlainText("Processing: {0} \n".format(app))
                        app_name = str(app)
                        if(len(app_name) >= 31):
                            app_name = app_name[0:30]
                        for char in app_name:
                            if(char in bad_chars):
                                app_name = app_name.replace(char,'_')
                        inventory[app].to_excel(writer,sheet_name=app_name,index=False)
                    writer.close()
                    self.output_window.insertPlainText("Successfully created the Okta User Application Mappings inventory \n")
                if(self.format == 'csv'):
                    df = pd.DataFrame(all_apps)
                    df.to_csv(fileName,index=False)
                    self.output_window.insertPlainText("Successfully created the Okta User Application Mappings inventory \n")
        except Exception as e:
            self.output_window.insertPlainText("Exception raised: {0} \n ".format(e))

    def CollectGroupAppMappings(self):
        '''
        -> Input   :
            -> API Key
            -> Domain Value
            -> Headers
        -> Process :
            -> API call to the application endpoint
            -> Retrieve the group URL from the application dictionary
            -> Query groups assigned to the application
            -> Application and group mapping data is parsed into either a csv or xlsx format
        -> Output  :
            -> Application/Group mapping inventory file in either csv or xlsx format
        '''
        self.output_window.insertPlainText("Collecting group to application mappings... \n")
        fileName  = self.GenFileName('Okta_Apps_Group_Mappings_')
        url       = "https://{0}.okta.com/api/v1/apps".format(self.domain)
        req       = requests.get(headers=self.headers,url=url)
        apps      = {}
        inventory = {}
        all_apps  = []
        try:
            if(req.status_code == 200):
                next_url = self.ParseHeaders(req.headers)
                content  = req.json()
                for entry in content:
                    self.output_window.insertPlainText("Located: {0}:{1} \n".format(entry['id'],entry['label']))
                    apps[entry['id']] = entry['label']
                while(next_url):
                    url      = "https://{0}.okta.com/api/v1/apps".format(self.domain)
                    req      = requests.get(headers=self.headers,url=next_url)
                    next_url = self.ParseHeaders(req.headers)
                    content  = req.json()
                    for entry in content:
                        self.output_window.insertPlainText("Located: {0}:{1} \n".format(entry['id'],entry['label']))
                        apps[entry['id']] = entry['label']
                for item in apps.keys():
                    id    = item
                    label = apps[item]
                    self.output_window.insertPlainText("Retrieving groups for: {0} \n".format(label))
                    url     = "https://{0}.okta.com/api/v1/apps/{1}/groups".format(self.domain,id)
                    req     = requests.get(headers=self.headers,url=url)
                    content = req.json()
                    app_groups = []
                    for element in content:
                        group_link = element['_links']['group']['href']
                        group_req  = requests.get(headers=self.headers,url=group_link)
                        group_data = group_req.json()
                        group_data['Application'] = label
                        group_data['Group']       = group_data['profile']['name']
                        app_groups.append(group_data)
                        for item in app_groups:
                            all_apps.append(group_data) 
                    inventory[label] = pd.DataFrame(data=app_groups)
                    time.sleep(1)
                if(self.format == 'xlsx'):
                    writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
                    bad_chars = ['[',']',':','*','?','/','\`']
                    for app in inventory.keys():
                        self.output_window.insertPlainText("Processing: {0} \n".format(app))
                        app_name = str(app)
                        if(len(app_name) >= 31):
                            app_name = app_name[0:30]
                        for char in app_name:
                            if(char in bad_chars):
                                app_name = app_name.replace(char,'_')
                        inventory[app].to_excel(writer,sheet_name=app_name,index=False)
                    writer.close()
                    self.output_window.insertPlainText("Successfully created the Okta Group Application Mappings inventory \n")
                if(self.format == 'csv'):
                    df = pd.DataFrame(all_apps)
                    df.to_csv(fileName,index=False)
                    self.output_window.insertPlainText("Successfully created the Okta Group Application Mappings inventory \n")
        except Exception as e:
            self.output_window.insertPlainText("Exception raised: {0} \n".format(e))

if(__name__ == '__main__'):
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())
