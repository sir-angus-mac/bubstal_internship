from django.shortcuts import render
from django.http import HttpResponse 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from .models import Email

def index(request):
    email_name = ""
    values = []
    csv = None
    csv_string = ""
    try_again = False
    # op = webdriver.ChromeOptions()
    # op.add_argument('headless') 
    driver = webdriver.Chrome() #(options=op)     
    if request.method == "POST":
        if request.FILES.get("myfile"):
            driver.get("https://copilot.microsoft.com")
            elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "userInput")))
            
            uploaded_file = request.FILES["myfile"]
            content = uploaded_file.read().decode("utf-8") 
            try_again = True

            # Upload the text content
            vegetable = driver.find_element(By.ID, "userInput")
            vegetable.send_keys('Make CSV of five elements in your response so I can webscrape it\r' 
                            + 'For the first element, Please make a string classifying the intent of the below email in detail under "Classify Intent" section. Make sure the suggestion is at least three sentences long. The more sentences the better.\r' 
                            + 'For the second element, Please make a string suggesting the course of actions to take in detail under "Possible Actions" section. Also make sure the suggestion is at least three sentences long. The more sentences the better.\r' 
                            + 'For the third element, Please make a string suggesting how one should reply to the email in detail under "How To Reply" section. Also make sure the suggestion is at least three sentences long. The more sentences the better.\r' 
                            + 'For the fourth element, please make a string identifying the email sender under "Sender" \r'
                            + 'For the fifth element, please make a string identifying the email receiver under "Receiver" \r'
                            + 'For the sixth element, please  make a string identifying the email senders name under "Sender Name" \r' 
                                + '\r' + content.replace('\n', '\r') + '\n') 
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
            time.sleep(15)
            code_elements = driver.find_element(By.TAG_NAME, "code")  
            content = code_elements.text 
            try:
                content = content.split("\n")
                header = content[0].split(',') 
                if len(content) > 2:
                    csv_string = content[1:] 
                    l = content[1:] 
                else: 
                    csv_string = content[1][1:] 
                    l = csv_string.split('","')  
                list = [] 
                for tag in l:
                    if tag[-1] == '"':
                        list += [tag[:-1]]  
                    else:
                        list += [tag] 
                max_len = 0
                for line in list:
                    pow = line.split(". ")
                    values += [pow] 
                    if len(pow) > max_len:
                        max_len = len(pow)

                print(code_elements.text) 
                
                for i in range(len(values)):
                    if len(values[i]) < max_len:
                        values[i] += ["" for i in range(max_len - len(values[i]))] 
                values = [[row[i] for row in values] for i in range(len(values[0]))] 
                try_again = False
                csv = code_elements.text 
                email_name = request.FILES.get("myfile")
            except Exception as e: 
                print(e) 
        elif 'delete_email' in request.POST:
            try:
                myinstance = Email.objects.get(id=request.POST['id']).delete()
                print(myinstance) 
            except Exception as e: 
                print(e) 
        elif 'save_CSV' in request.POST:
            try:
                myinstance = Email.objects.create(email_name=request.POST['email_name'], kanban={"csv": request.POST['csv_actual'].replace('"', '').replace("'", '')}) 
                print(myinstance) 
            except Exception as e: 
                print(e)  

    driver.quit() 
    return render(request, "bubstal_limited/home.html", {"values": values, "csv": csv, "try_again": try_again, "email_name": email_name, "csv_string": csv_string, "list_of_saved_emails": Email.objects.all()}) 
