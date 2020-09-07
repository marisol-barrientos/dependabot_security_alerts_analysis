import matplotlib.pyplot as plt

x = ['2017', '2018',  '2019', '2020']
y = [57,325,302,343]
plt.bar(x,y,align="center")
plt.title("New npm and yarn vulnerabilities records - GitHub Advisory")
plt.show()
plt.savefig('npm_yarn_advisory.png')

growth_rate_1 = round(100 * (325 - 57) / 57)
print(str(growth_rate_1) + " %")

growth_rate_2 = round(100 * (302 - 325) / 325)
print(str(growth_rate_2) + " %")

growth_rate_3 = round(100 * (343 - 302) / 302)
print(str(growth_rate_3) + " %")
"""

2020-09-01T21:26:50Z -> Cuando yo lo medí tenía 1028

2020-09-08T21:26:50Z -> Una semana después tiene 

Primer record: 2017-10-24T18:33:35Z

Mirar del 1 de Septiembre al 8 de Sep el numero de nuevos advisories

736 del 31 Agosto al 7 Sep -> new advisories

"""

