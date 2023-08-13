from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import datetime
from email.message import EmailMessage
import ssl
import smtplib


service = Service(r"******")
sender = ******
e_pass = ******
receiver = *****
subject = "Daily Stock Price Notification"
contents = """Stock Price Update
"""
context = ssl.create_default_context()


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=service,  options=options)
    driver.get("https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6")
    return driver


def clean_text(text):
    """extract only temp"""
    output = text
    return output


def main():
    driver = get_driver()
    element = driver.find_element(by="xpath", value="/html/body/div[1]/div/section[1]/div/div/div[2]/span[2]")
    output = clean_text(element.text)

    today = datetime.datetime.now().strftime("%d-%m-%Y")
    filename = f"{today}_report.txt"
    with open(filename, "w") as f:
        f.write(str(output))

    if output > '-0.10%':
            em = EmailMessage()
            em['From'] = sender
            em['To'] = receiver
            em['Subject'] = subject
            em.set_content(contents + f"{output}")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender, e_pass)
                smtp.sendmail(sender, receiver, em.as_string())
                print("The email was sent successfully!")

    driver.quit()


if __name__ == "__main__":
    main()








