import json

def to24hours(time):
    if time.endswith('PM') and time.split(':')[0]!='12':

        hour = 12 + int(time.split(':')[0])
        return str(hour) +':'+time.split(':')[1][:-2]
    else:
        return time[:-2]

def printClass(code, tilte, days, start, end, location, instructor):
    print '=='*20
    print code, title
    print days
    print start, end
    print location
    print instructor


weekdays = {'Mo':1, 'Tu':2, 'We':3, 'Th':4, 'Fr':5}
data = []

fn = 'enrolled.txt'
with open(fn) as f:
    lines = [l.strip() for l in f.readlines()]
startIndex = lines.index('Show Waitlisted Classes')
classIndex = startIndex + 1

while classIndex < len(lines)-5:
    code, title = lines[classIndex].split(' - ')
    time = lines[classIndex + 11].split()
    days, start, end = time[0], time[1], time[3]
    days = [weekdays[days[2*i:2*i+2]] for i in range(len(days)/2)]
    start, end = to24hours(start), to24hours(end)

    location = lines[classIndex + 12]
    location = location.replace('Gould-Simpson', 'GS')
    location = location.replace(', Rm', '')
    instructor = lines[classIndex + 13]
    
    printClass(code, title, days, start, end, location, instructor)
    
    for day in days:
        data.append({'start':start, 'end':end, 'day':day, 'tag':[code, title, location, instructor]})
    classIndex += 16


fn = 'plan.txt'
with open(fn) as f:
    lines = [l.strip() for l in f.readlines()]
for i in range(0, len(lines), 8):
    code, title = lines[i].split(' - ')
    code = ' '.join(code.split())
    days = lines[i+1]
    days = [weekdays[days[2*j:2*j+2]] for j in range(len(days)/2)]
    start = to24hours(lines[i+2])
    end = to24hours(lines[i+3])
    location = lines[i+4]

    location = location.replace('Gould-Simpson', 'GS')
    location = location.replace(', Rm', '')
    #if location.startswith('Gould-Simpson'):
    #    location = 'GS' + location[17:]
    instructor = lines[i+5]
    printClass(code, title, days, start, end, location, instructor)
    
    for day in days:
        data.append({'start':start, 'end':end, 'day':day, 'tag':[code, title, location, instructor]})

print '=='*20
with open('data.js', 'w') as f:
    f.write('var data = \n')
    json.dump(data, f, indent=2)
