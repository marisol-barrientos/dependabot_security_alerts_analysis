from datetime import datetime
import seaborn as sns

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import date2num

plt.gcf().subplots_adjust(bottom=0.15)


def main():
    raw_data = pd.read_csv(
        "../input/test2.csv",
        sep=';'
    )
    # raw_data = raw_data[raw_data['commit_author'] == 'dependabot-preview[bot]' ]
    # raw_data = raw_data[raw_data['commit_author'] == 'dependabot[bot]']
    raw_data = raw_data[raw_data['commit_author'] != 'dependabot[bot]']
    # Converting unix timestamp to pandas datetime
    raw_data['date_time'] = raw_data['time'].apply(lambda x: pd.to_datetime(x, unit='ns'))

    # print(raw_data.columns)
    # print(raw_data[['date_time', 'fixed_critical_vulnerabilities']])

    #dependabot - preview[bot]
    # Grouping the data by month
    per_month = raw_data.set_index('date_time').groupby(pd.Grouper(freq='M'))['total_commit_revoked_fixes_norm'].sum()
    print(per_month)

    # Plotting the data
    x = per_month.index
    y = per_month.values

    plt.plot(x, y)

    plt.axvspan(date2num(datetime(2017, 9, 1)), date2num(datetime(2017, 9, 30)),label="2009 Recession", color="green", alpha=0.3)
    plt.axvspan(date2num(datetime(2019, 5, 1)), date2num(datetime(2019, 5, 31)),label="2009 Recession", color="red", alpha=0.3)
    plt.xticks(rotation=55)

    # plt.show()
    #plt.savefig("../output/total_commit_revoked_fixes_norm.png")

    print(raw_data[['total_commit_dependencies_norm', 'total_commit_vulnerabilities_norm']].corr())
    sns.heatmap(raw_data[['total_commit_dependencies_norm', 'total_commit_vulnerabilities_norm']].corr())


if __name__ == "__main__":
    main()