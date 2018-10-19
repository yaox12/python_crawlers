import re
import datetime
import matplotlib.pyplot as plt

plt.switch_backend('agg')

ele_list = list()
get_ele = re.compile('\d+')
with open('log.txt') as infile:
    for line in infile:
        if not line.startswith('剩余电量'):
            continue
        ele_list.append(int(get_ele.findall(line)[0]))

# begin = datetime.date(2018, 6, 16)
# delta = [datetime.timedelta(days=i) for i, _ in enumerate(ele_list)]
# x = [(begin + d).strftime('%m.%d') for d in delta]
x = list(range(len(ele_list)))
plt.plot(x, ele_list)
plt.xlabel('Days')
plt.ylabel('Kilowatt-hour')
plt.savefig('ele.png')
