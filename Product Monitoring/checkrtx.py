import time
import requests
import smtplib
import email.message
from playsound import playsound
import smtplib
from email.mime.text import MIMEText
email_addr = None
password = None
sent_from = email_addr
to = None
subject = None
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
soldoutbutton = '<button class="btn btn-disabled btn-lg btn-block add-to-cart-button" disabled="" type="button" data-sku-id="6429442" style="padding:0 8px">Sold Out</button>'
howmanysoldouts = []
msg = MIMEText("Program has been started. You're in good hands.")
msg['Subject'] = subject
msg['From'] = sent_from
msg['To'] = to
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(email_addr, password)
server.sendmail(sent_from, to, msg.as_string())
server.close()
playsound("BUY.mp3")
while True:
    try:
        rtxhtml = requests.get("https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442",headers = header)
        rtxhtml = rtxhtml.content.decode()
        i = 0
        emailbody = ""
        if soldoutbutton not in rtxhtml:
            for i in range(10):
                playsound("BUY.mp3")
        elif soldoutbutton in rtxhtml:
            while soldoutbutton in rtxhtml:
                rtxhtml = rtxhtml.replace(soldoutbutton,"", 1)
                i+=1
        if i == 0:
            for j in range(5):
                playsound("BUY.mp3")
            msg = MIMEText("Graphics Cars is probably sold out!")
            msg['Subject'] = subject
            msg['From'] = sent_from
            msg['To'] = to
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(email_addr,password)
            server.sendmail(sent_from, to, msg.as_string())
            server.close()
        howmanysoldouts.append(i)
        if howmanysoldouts[len(howmanysoldouts)-1] != howmanysoldouts[len(howmanysoldouts)-2]:
            print("There is a change in the number of soldout items on the page.")
            emailbody+="There is a change in the number of soldout items on the page.\n\n"
            if i == 0:
                print("There are no soldout items on the page currently. Check it immediately to purchase the graphics card.")
                emailbody += "There are no soldout items on the page currently. Check it immediately to purchase the graphics card.\n\n"
                emailbody += "The soldout indicator appeared "+str(i)+"times.\n\n"
            msg = MIMEText(emailbody)
            msg['Subject'] = subject
            msg['From'] = sent_from
            msg['To'] = to
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(email_addr,password)
            server.sendmail(sent_from, to, msg.as_string())
            server.close()
            playsound("BUY.mp3")
        print("The sold out indicator appeared "+str(i)+" times.\n\n")
        print(emailbody)
        time.sleep(5)
    except:
        print("site not reachable. Internet down.\n\n")
