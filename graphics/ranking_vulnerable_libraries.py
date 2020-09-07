import matplotlib.pyplot as plt
import pandas as pd

vulnerable_versions_csv = pd.read_csv('../input/vulnerable_versions.csv', sep=';', dtype={"id": int})

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

