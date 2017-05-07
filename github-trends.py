import urllib2, json, sys, sendgrid, os, ssl
from datetime import datetime, timedelta
from sendgrid.helpers.mail import *

def sendEmail(subject, body, dest):
    
    sendGrid = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

    fromEmail = Email("airtonzanon@gmail.com")
    toEmail = Email(dest)

    content = Content("text/html", body)

    mail = Mail(fromEmail, subject, toEmail, content)
    response = sendGrid.client.mail.send.post(request_body=mail.get()) 

    if 200 <= response.status_code < 300:
        return 'Email was sent';
    
    return 'Email sent was failed';

def getRepos( daysQty ):

    lastSevenDays = datetime.today() - timedelta(days=daysQty)

    urlRequest = 'https://api.github.com/search/repositories?sort=start&order=desc&q=created:' + lastSevenDays.strftime('%Y-%m-%d')

    jsonResult = urllib2.urlopen(urlRequest).read()

    repos = json.loads(jsonResult)

    reposBody = ''

    for repo in repos['items']:
        reposBody += "%s: %s <br /> %s <br /> %s <br /><br />" % (repo['language'], repo['full_name'], repo['description'], repo['html_url'])

    result = sendEmail('ASOS - From: ' + lastSevenDays.strftime('%Y-%m-%d'), reposBody, 'airtonzanon@yahoo.com.br')

    print(result)
    
if (__name__ == "__main__"):
    getRepos(int(sys.argv[1]))