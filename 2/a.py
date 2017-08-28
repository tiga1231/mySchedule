import json
import datetime
from glob import glob

def to24hour(time):
    if time.endswith('PM') and time.split(':')[0]!='12':
        hour = 12 + int(time.split(':')[0])
        return str(hour) +':'+time.split(':')[1][:-2]
    else:
        return time[:-2]


def day2num(day):
    return {'Mo':1,'Tu':2,
            'We':3,'Th':4,
            'Fr':5}[day]


def parse(lines):
    time = lines[3]
    section = lines[1]
    classNumber = int(lines[0])
    
    status = lines[-1]
    if lines[-2] == lines[-3]:
        location = lines[5]
        instructor = lines[7]
        if instructor.endswith(','):
            instructor += ' '+lines[8]
    else:
        location = lines[4]
        instructor = lines[5]

    dayStr = time.split()[0]
    days = []
    if dayStr == 'TBA':
        days = ['TBA', ]
    else:
        for i in range(0, len(dayStr), 2):
            day = dayStr[i:i+2]
            num = day2num(day)
            days.append(num)
    if time == 'TBA':
        start = 'TBA'
        end = 'TBA'
    else:
        start = to24hour(time.split()[1])
        end = to24hour(time.split()[3])
    
    res = { 'start': start,
            'end': end,
            'day': days, 
            'location': location,
            'section': section,
            'classNumber': classNumber,
            'instructor': instructor,
            'status': status }
    return res


def printClass(c):
    print 'loc:', c['location']
    print 'instructor:', c['instructor']
    print '-'*5


if __name__ == '__main__':
    classSections = []
    for fn in glob('class/*.txt'):
        print fn
        with open(fn) as f:
            f = f.readlines()
        className = ''
        i=0
        while i < len(f):
            if f[i].startswith('Collapse section'):
                subject = f[i].split()[2]
                index = f[i].rfind(subject)
                className = f[i][index:].strip()
                i+=2

            if f[i].startswith('Class Section'):
                i+=1
                lines = []
                while f[i].strip() != '':
                    lines.append(f[i].strip())
                    i+=1
                class_i = parse(lines)
                class_i['title'] = ' '.join(className.split(' - ')[1:])
                class_i['code'] = ' '.join(className.split(' - ')[:1])
                classSections.append(class_i)
                
            i+=1
        
        with open('data.js', 'w') as f:
            f.write('var data = \n')
            json.dump(classSections, f, indent=2)
