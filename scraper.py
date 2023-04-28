import bs4
import requests

url = 'http://192.168.4.1'
test2 = """
<html>
  <head>
    <title>MONA and Ball locations</title>
  </head>
  <body>
    <h1>MONA and Ball Locations.</h1>
    <br/><br />C1,1580,966,2.96

    <br />G43,231,535,1.59

    <br />G42,1641,519,-0.05

    <br />M19,507,518,0.4

    <br />M20,1293,372,-0.42

    <br />C0,294,65,-1.5

    <br />B,911,585,0
  </body>
</html>

"""

test = """
<html>
<head>
<title>
MONA and Ball locations
</title>
</head>
<body>
<h1>
MONA and Ball Locations.
</h1>
<br><br>C1,962,646,1.67

<br>G43,24,377,-0.07

<br>M19,164,348,-0.09

<br>M20,343,331,-0.05

<br>M24,726,276,-1.32

<br>B,559,321,0

</body>
</html>
"""
IDs = ["C1", "G43", "G42", "M19", "M20", "C0", "B"]

def get_soup(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    return soup


def get_body(soup):
    body = soup.find('body')
    return body

def get_locations(body):
    locations = body.find_all('br')
    locations_text = []
    for i in locations:
        if i.next_sibling != None and type(i.next_sibling) == bs4.element.NavigableString:
            locations_text.append(i.next_sibling.strip())
    return locations_text

def save_data(data_list):
    data_full = {}
    i = 0
    for entry in data_list:
        temp = entry.split(",")
        if temp[0] in IDs:
          i = IDs.index(temp[0])
          data_full[IDs[i]] = {"x" : temp[1], "y" : temp[2], "angle": temp[3]}
          # i += 1
    # save to json
    # save_file = open("temp.json","w")
    # json.dump(data_full,save_file)
    # save_file.close()

    return data_full

def scrape_test():
    soup = get_soup(url)
    body = get_body(soup)
    locations = get_locations(body)
    # print(save_data(locations))
    return save_data(locations)
