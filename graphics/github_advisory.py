import matplotlib.pyplot as plt
import pandas as pd

from src.analysis import config

with open('../config.yaml') as config_file:
    vulnerable_versions_csv = pd.read_csv(config['vulnerable_versions_csv'], sep=';', dtype={"id": int})


cur_ax = plt.gca()
a_gp = (vulnerable_versions_csv.groupby('name')['severity'].count().reset_index().rename(columns={'severity': 'count'}).sort_values(['count'], ascending = False))
#
a_gp[a_gp['count'] > 4].plot(x='name', kind='bar', figsize=(15,7), ax=cur_ax)

cur_ax.set_xlabel('Vulnerable libraries.')
cur_ax.set_title('Ranking vulnerable libraries.')
cur_ax.set_ylabel('No. of vulnerabilities.')

plt.savefig('top_vulnerable_libraries.png')

severities = vulnerable_versions_csv['severity'].to_list()

critical = severities.count(4)
high = severities.count(3)
moderate = severities.count(2)
low = severities.count(1)

print("Critical severity: ", critical)
print("High severity: ", high)
print("Moderate severity: ", moderate)
print("Low severity: ", low)


cur_ax = plt.gca()

x = ['Low', 'Moderate',  'High', 'Critical']
y = [low, moderate, high, critical]
plt.bar(x,y,align="center", color=['g', 'b', 'r', 'k'])
cur_ax.set_xlabel('Severity level.')
cur_ax.set_ylabel('Frequency.')

plt.title("Vulnerabilities.")

plt.savefig('vulnerability_severity_level.png')


cur_ax = plt.gca()

x = ['2017', '2018',  '2019', '2020']
y = [57,325,302,343]
plt.bar(x,y,align="center")
plt.title("New npm and yarn vulnerabilities records.")
cur_ax.set_ylabel('No. of new records')
cur_ax.set_xlabel('Time when it was recorded into GitHub Advisory.')

plt.savefig('npm_yarn_advisory.png')

growth_rate_1 = round(100 * (325 - 57) / 57)
print(str(growth_rate_1) + " %")

growth_rate_2 = round(100 * (302 - 325) / 325)
print(str(growth_rate_2) + " %")

growth_rate_3 = round(100 * (343 - 302) / 302)
print(str(growth_rate_3) + " %")
"""

2020-09-01T21:26:50Z -> Cuando yo lo medí tenía 1027

2020-09-08T21:26:50Z -> Una semana después tiene 

Primer record: 2017-10-24T18:33:35Z

Mirar del 1 de Septiembre al 8 de Sep el numero de nuevos advisories

736 del 31 Agosto al 7 Sep -> new advisories

"""

