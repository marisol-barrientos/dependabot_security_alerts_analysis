from influxdb_client import InfluxDBClient, WritePrecision, Point
from influxdb_client.client.write_api import SYNCHRONOUS


def open_connection(client_url, token):
    """It creates and returns a new 'WriteApi' instance for an specific client and token.

    :param client_url: It contains a InfluxDB server client.
    :type client_url: str

    :param token: It contains the authentication token.
    :type token: str

    :return: It returns a new WriteApi instance.
    :rtype: WriteApi
    """
    client = InfluxDBClient(url=client_url, token=token)
    return client.write_api(write_options=SYNCHRONOUS)


def record_point(point, write_api, bucket, org):
    """It writes a point into a InfluxDB Bucket.

        :param point: It represents the Point that will be added inside the bucket. For more information about 'Point' look 'DB Point' module.
        :type point: InfluxPoint

        :param write_api: It represents the API used to write the point on a bucket.
        :type write_api: WriteApi

        :param bucket: It contains the name of the bucket were the point will be written.
        :type bucket: str

        :param org: It contains the organization ID.
        :type org: str
        """
    print(point)
    print("\n         ~~ INFO:Writing point into '" + bucket + "' ...")

    p = Point("Commit_09_09")\
        .time(point.commited_date, WritePrecision.S)\
        .tag("repo_id", point.repo_id)\
        .tag("commit_hexsha", point.commit_hexsha)\
        .tag("commit_author", point.commit_author) \
        .tag("repo_name", point.repo_name)\
        .tag("repo_owner", point.repo_owner)\
        .tag("email", point.email)\
        .tag("commit_message",point.commit_message)\
        .tag("has_config_file", point.has_config_file)\
        .field("total_commit_dependencies", point.total_commit_dependencies)\
        .measurement("critical_severity")\
            .field("new_critical_vulnerabilities", len(point.critical_severity["new_vulnerabilities"])) \
            .field("fixed_critical_vulnerabilities", len(point.critical_severity["fixed_vulnerabilities"])) \
            .field("removed_critical_vulnerabilities", len(point.critical_severity["removed_vulnerabilities"])) \
            .field("revoked_fixed_critical_vulnerabilities", len(point.critical_severity["revoked_fixed_vulnerabilities"])) \
            .field("revoked_removed_critical_vulnerabilities", len(point.critical_severity["revoked_removed_vulnerabilities"])) \
            .field("kept_critical_vulnerabilities", len(point.critical_severity["kept_vulnerabilities"])) \
        .measurement("high_severity") \
            .field("new_high_vulnerabilities", len(point.high_severity["new_vulnerabilities"])) \
            .field("fixed_high_vulnerabilities", len(point.high_severity["fixed_vulnerabilities"])) \
            .field("removed_high_vulnerabilities", len(point.high_severity["removed_vulnerabilities"])) \
            .field("revoked_fixed_high_vulnerabilities", len(point.high_severity["revoked_fixed_vulnerabilities"])) \
            .field("revoked_removed_high_vulnerabilities", len(point.high_severity["revoked_removed_vulnerabilities"])) \
            .field("kept_high_vulnerabilities", len(point.high_severity["kept_vulnerabilities"])) \
        .measurement("moderate_severity") \
            .field("new_moderate_vulnerabilities", len(point.moderate_severity["new_vulnerabilities"])) \
            .field("fixed_moderate_vulnerabilities", len(point.moderate_severity["fixed_vulnerabilities"])) \
            .field("removed_moderate_vulnerabilities", len(point.moderate_severity["removed_vulnerabilities"])) \
            .field("revoked_fixed_moderate_vulnerabilities", len(point.moderate_severity["revoked_fixed_vulnerabilities"])) \
            .field("revoked_removed_moderate_vulnerabilities", len(point.moderate_severity["revoked_removed_vulnerabilities"])) \
            .field("kept_moderate_vulnerabilities", len(point.moderate_severity["kept_vulnerabilities"])) \
        .measurement("low_severity") \
            .field("new_low_vulnerabilities", len(point.low_severity["new_vulnerabilities"])) \
            .field("fixed_low_vulnerabilities", len(point.low_severity["fixed_vulnerabilities"])) \
            .field("removed_low_vulnerabilities", len(point.low_severity["removed_vulnerabilities"])) \
            .field("revoked_fixed_low_vulnerabilities", len(point.low_severity["revoked_fixed_vulnerabilities"])) \
            .field("revoked_removed_low_vulnerabilities", len(point.low_severity["revoked_removed_vulnerabilities"])) \
            .field("kept_low_vulnerabilities", len(point.low_severity["kept_vulnerabilities"])) \
        .measurement("summary") \
            .field("total_new_vulnerabilities", len(point.summary["new_vulnerabilities"])) \
            .field("total_fixed_vulnerabilities", len(point.summary["fixed_vulnerabilities"])) \
            .field("total_removed_vulnerabilities", len(point.summary["removed_vulnerabilities"])) \
            .field("total_revoked_fixed_vulnerabilities", len(point.summary["revoked_fixed_vulnerabilities"])) \
            .field("total_revoked_removed_vulnerabilities", len(point.summary["revoked_removed_vulnerabilities"])) \
            .field("total_kept_vulnerabilities", len(point.summary["kept_vulnerabilities"])) \
            .field("total_commit_vulnerabilities", len(point.summary["total"]))

    write_api.write(bucket, org, p, time_precision='s')
