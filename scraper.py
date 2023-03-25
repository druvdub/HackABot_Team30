import bs4
import requests

url = 'https://8.8.8.8'
# url = 'https://192.168.4.1'
test = """
<html>
  <head>
    <title>MONA and Ball locations</title>
  </head>
  <body>
    <h1>MONA and Ball Locations.</h1>
    <br />C1,1580,966,2.96

    <br />G43,231,535,1.59

    <br />G42,1641,519,-0.05

    <br />M24,507,518,0.4

    <br />M2,1293,372,-0.42

    <br />C0,294,65,-1.5

    <br />B,911,585,0
  </body>
</html>

"""


def get_soup(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(test, 'html.parser')
    return soup


def get_body(soup):
    body = soup.find('body')
    return body

def get_locations(body):
    locations = body.find_all('br')
    locations_text = [loc.next_sibling.strip() for loc in locations]
    return locations_text


if __name__ == "__main__":
    soup = get_soup(url)
    body = get_body(soup)
    locations = get_locations(body)
