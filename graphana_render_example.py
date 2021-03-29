#!/usr/bin/env python3.6
import requests
import smtplib
import sys
from PIL import Image
from io import BytesIO
from datetime import datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
# Define these once; use them twice!

FROM = 'graphana@mymymail.com'
if len(sys.argv) > 1:
    TO = sys.argv[1]
else:
    TO = 'me@mymymail.com'
api_key =  'Bearer eyJrIjoiVlVXZU9lT0paU1R0WVFhbmNlQnVOODJ3RGs2ZnRLTkciLCJuIjoicG1pcmEtdGVtcGVyYXR1cmUtcmVuZGVyIiwiaWQiOjF9'
grafana_url = 'https://net-graph.site.local/d/mira_temperature_network/mira-temperature?'
dashboard_url = "https://net-graph.site.local/render/d/mira_temperature_network/mira-temperature?width=1800&height=1020"


def send_mail(FROM,TO,mime_image,grafana_url):
    msg = MIMEMultipart('related')
    msg['Subject'] = 'Server Room Temperature (From Switches)'
    msg['From'] = FROM
    msg['To'] = TO
    msg.preamble = 'multi-part message in MIME format. Contains Server Room Temperature (From Switches)'
    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    msgText = MIMEText('Server Room Temperature (From Switches).HTML didn`t work for the report')
    msgAlternative.attach(msgText)
    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText((f'<b>P.Mira Temperature Dashboard</b><br>'
                        f'<img src="cid:image1" height="92%"><br>'
                        f'<a href="{grafana_url}">Grafana Dashboard</a>'), 'html')
    msgAlternative.attach(msgText)
    # Define the image's ID as referenced above
    mime_image.add_header('Content-ID', '<image1>')
    msg.attach(mime_image)
    # Send the email
    smtp = smtplib.SMTP()
    smtp_handler = smtplib.SMTP('smtp.site_email.local')
    smtp_handler.sendmail(FROM, TO, msg.as_string())
    smtp_handler_quit_status = smtp_handler.quit()
    print(smtp_handler_quit_status)
    pass


def get_dashboard(dashboard_url):
    headers_dict = {'Authorization' : api_key }
    resp = requests.get(dashboard_url, headers=headers_dict, allow_redirects=True)
    return resp.content
    
    
def convert_image_to_mime(http_content):
    image = Image.open(BytesIO(http_content))
    width, height = image.size
    left = 64 + 10
    top = 64
    right = width - left - 798
    bottom = height - top - 145
    image = image.crop((left, top, right, bottom))
    #Create a MIMEImage
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    msgImage = MIMEImage(img_byte_arr)
    return msgImage


if __name__ == '__main__':
    print(f'today {datetime.now()}')
    http_content = get_dashboard(dashboard_url)
    mime_image = convert_image_to_mime(http_content)
    send_mail(FROM,TO,mime_image,grafana_url)
    
