import os
from datetime import datetime

import matplotlib.pyplot as plt

import yaml
import pandas as pd



with open('../config.yaml') as config_file:
    config = yaml.full_load(config_file)
    recorded_commits = config['recorded_commits']




    repos_csv = pd.read_csv(recorded_commits, sep=';')
    for i in range(repos_csv.shape[0]):

        time = repos_csv['time'][i]
        time = time / 1000000000
        ts = datetime.fromtimestamp(time).strftime("%Y-%m-%d %I:%M:%S")

        fixed_critical_vulnerabilities = repos_csv['fixed_critical_vulnerabilities'][i]
        fixed_high_vulnerabilities = repos_csv['fixed_high_vulnerabilities'][i]
        fixed_moderate_vulnerabilities = repos_csv['fixed_moderate_vulnerabilities'][i]
        fixed_low_vulnerabilities = repos_csv['fixed_low_vulnerabilities'][i]

        kept_critical_vulnerabilities = repos_csv['kept_critical_vulnerabilities'][i]
        kept_high_vulnerabilities = repos_csv['kept_high_vulnerabilities'][i]
        kept_moderate_vulnerabilities = repos_csv['kept_moderate_vulnerabilities'][i]
        kept_low_vulnerabilities = repos_csv['kept_low_vulnerabilities'][i]

        new_critical_vulnerabilities = repos_csv['new_critical_vulnerabilities'][i]
        new_high_vulnerabilities = repos_csv['new_high_vulnerabilities'][i]
        new_moderate_vulnerabilities = repos_csv['new_moderate_vulnerabilities'][i]
        new_low_vulnerabilities = repos_csv['new_low_vulnerabilities'][i]

        removed_critical_vulnerabilities = repos_csv['removed_critical_vulnerabilities'][i]
        removed_high_vulnerabilities = repos_csv['removed_high_vulnerabilities'][i]
        removed_moderate_vulnerabilities = repos_csv['removed_moderate_vulnerabilities'][i]
        removed_low_vulnerabilities = repos_csv['removed_low_vulnerabilities'][i]

        revoked_fixed_critical_vulnerabilities = repos_csv['revoked_fixed_critical_vulnerabilities'][i]
        revoked_fixed_high_vulnerabilities = repos_csv['revoked_fixed_high_vulnerabilities'][i]
        revoked_fixed_moderate_vulnerabilities = repos_csv['revoked_fixed_moderate_vulnerabilities'][i]
        revoked_fixed_low_vulnerabilities = repos_csv['revoked_fixed_low_vulnerabilities'][i]

        revoked_removed_critical_vulnerabilities = repos_csv['revoked_removed_critical_vulnerabilities'][i]
        revoked_removed_high_vulnerabilities = repos_csv['revoked_removed_high_vulnerabilities'][i]
        revoked_removed_moderate_vulnerabilities = repos_csv['revoked_removed_moderate_vulnerabilities'][i]
        revoked_removed_low_vulnerabilities = repos_csv['revoked_removed_low_vulnerabilities'][i]

        total_commit_dependencies = repos_csv['total_commit_dependencies'][i]
        total_commit_vulnerabilities = repos_csv['total_commit_vulnerabilities'][i]
        total_fixed_vulnerabilities = repos_csv['total_fixed_vulnerabilities'][i]
        total_kept_vulnerabilities = repos_csv['total_kept_vulnerabilities'][i]
        total_new_vulnerabilities = repos_csv['total_new_vulnerabilities'][i]
        total_removed_vulnerabilities = repos_csv['total_removed_vulnerabilities'][i]
        total_revoked_fixed_vulnerabilities = repos_csv['total_revoked_fixed_vulnerabilities'][i]
        total_revoked_removed_vulnerabilities = repos_csv['total_revoked_removed_vulnerabilities'][i]

        print(ts)