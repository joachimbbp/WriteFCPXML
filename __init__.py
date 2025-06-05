from bs4 import BeautifulSoup
import os
# I don't love OOP but this feels like the best way to do it?
class LtcChangeTable:
    #Ignoring halfStep
    def __init__(self):
        self.increment_frame_count = None
        self.increment_value = None
        self.end_frame_count = None
        self.end_value = None
    def printout(self):
        print('     incremement frame count: ', self.increment_frame_count)
        print('     increment value: ', self.increment_value)
        print('     end frame count: ', self.end_frame_count)
        print('     end value: ', self.end_value)
class Clip:
    def __init__(self):
        self.source_file = None
        self.creation_date = None
        self.timecode_fps = None
        self.ltc_change_table = LtcChangeTable()
    def printout(self):
        print('source file name: ', self.source_file)
        print('creation date: ', self.creation_date)

        self.ltc_change_table.printout()
def extract(field: str, soup, attr = 'value'):
    field_tag = soup.find(field)
    if field_tag and field_tag.has_attr(attr):
       return field_tag[attr] 

def parse_xml(file: str):
    clip = Clip()
    clip.source_file = file
    with open(file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'xml')
        clip.creation_date = extract('CreationDate', soup)
        clip.timecode_fps = extract('LtcChangeTable', soup, 'tcFps')
        ltc_changes = soup.find_all('LtcChange')
        for change in ltc_changes:
            value = change.get('status')
            if change.get('status') == 'increment':
                clip.ltc_change_table.increment_frame_count = change.get('frameCount')
                clip.ltc_change_table.increment_value = change.get('value')
            if change.get('status') == 'end':
                clip.ltc_change_table.end_frame_count = change.get('frameCount')
                clip.ltc_change_table.end_value = change.get('value') 
    return clip

camera_folder = '/Users/joachimpfefferkorn/Desktop/test_clips' 
clips = []
for file in os.listdir(camera_folder):
    if file.endswith('.XML'):
        clips.append(parse_xml("{}/{}".format(camera_folder, file)))
for clip in clips:
    clip.printout()
print("Finished")
