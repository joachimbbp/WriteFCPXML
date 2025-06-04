from bs4 import BeautifulSoup
import os
print("xml file parsing program")

class Clip:
    def __init__(self):
        self.creation_date = None
        self.capture_fps = None
        
def extract(field: str, soup, attr = 'value'):
    field_tag = soup.find(field)
    if field_tag and field_tag.has_attr(attr):
       return field_tag[attr] 

def parse_xml(file: str):
    clip = Clip()
    with open(file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'xml')
        clip.creation_date = extract('CreationDate', soup)

        print("creation date: ", clip.creation_date)

camera_folder = '/Users/joachimpfefferkorn/Desktop/test_clips' 

for file in os.listdir(camera_folder):
    if file.endswith('.XML'):
        print("file: ", file)
        parse_xml("{}/{}".format(camera_folder, file))
print("Finished")
