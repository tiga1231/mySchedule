import json
import datetime

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
    time = lines[4].strip()
    section = lines[2].strip()
    code = int(lines[1].strip())
    location = lines[5].strip()
    instructor = lines[6].strip()
    status = lines[8].strip()

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
            'sectionCode': code,
            'instructor': instructor,
            'status': status }
    return res


if __name__ == '__main__':
    classSections = []
    for fn in ['cs.txt', 'math.txt']:
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
                class_i = parse(f[i:i+10])
                class_i['title'] = ' '.join(className.split(' - ')[1:])
                class_i['code'] = ' '.join(className.split(' - ')[:1])
                classSections.append(class_i)
            i+=1
        
        with open('data.js', 'w') as f:
            f.write('var data = \n')
            json.dump(classSections, f, indent=2)
