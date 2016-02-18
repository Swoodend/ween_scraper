import requests
import smtplib
import sys
from bs4 import BeautifulSoup
from itertools import izip

#email stuff
from_addr = 'your email'
to_addr = 'some email'
password = 'your password'

#scraper stuff
URL = 'http://www.bandsintown.com/Ween'
html = requests.get(URL).text
soup = BeautifulSoup(html, 'html.parser')

#functions
def get_locations(soup):
  '''takes a soup obj and returns list of locations --- in this case locations are found
  with the itemprop addressLocality'''
  locations = soup.find_all(itemprop='addressLocality')
  return locations

def get_dates(soup):
  '''takes a soup obj and returns a list of dates --- in this case dates are found within table data tags
  with the class of date'''
  dates = soup.find_all('td', class_='date')
  return dates

def collect_show_info():
  '''collects location and city info form the site. this data is then zipped into a tuple containing
  (locaiton, date) pairs and appended to the shows array'''
  date_list = []
  location_list = []
  shows = []

  dates = get_dates(soup)
  locations = get_locations(soup)

  for date in dates: 
    date_list.append(date.text.replace('\n', ''))

  for location in locations:
    location_list.append(location.text)

  for i in izip(location_list, date_list):
    if i[0] == 'Toronto':
      shows.append(i)

  return shows

def create_email_msg(msg=''):
  '''creates a string that will be used as the body of the email you intend to send'''
  shows = collect_show_info()

  if shows:
    msg+= '\nWEEN :)\n\n'
    for show in shows:
      msg+= "{0} {1}\n".format(show[0], show[1])
  else:
    sys.exit('no shows :(')

  return msg

def send_email(from_addr, to_addr, password):
  '''sends an email from X to Y with msg'''
  msg = create_email_msg()
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()
  server.login(from_addr, password)
  server.sendmail(from_addr, to_addr, msg)
  server.quit()
  return

#run
if __name__ == '__main__':
  send_email(from_addr, to_addr, password)
