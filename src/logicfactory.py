__author__ = 'imalkov'
import xml.etree.ElementTree as etree
import os

HOME_PATH = '/home/imalkov/Documents/pycharm_workspace/wrkord/'
CONSTAINS_PATH = os.path.join(HOME_PATH, 'metainfo', 'constrains.xml')
WEEKINFO_PATH = os.path.join(HOME_PATH, 'metainfo', 'weekinfo.xml')

if __name__ == '__main__':
    #parse weekdays
    root_week = etree.parse(WEEKINFO_PATH).getroot()
    for i, day in enumerate(root_week.findall('day')):
        # print(day.attrib['name'])
        for j, shift in enumerate(day.findall('shift')):
            pass
            # print('{0} , {1} = {2}'.format(day.attrib['name'], shift.attrib['name'], i * 2 + j))
    #buld logic
    root_logic = etree.parse(CONSTAINS_PATH).getroot()
    for worker in root_logic.findall('worker'):
        print('name = {0} color = {1}'.format(worker['name'], worker['color']))







