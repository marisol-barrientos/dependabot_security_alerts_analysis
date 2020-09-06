from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def open_connection(client_url, token):
    """It creates and returns a 'Write API' instance, for an specific client and token.

    :param client_url: It contains InfluxDB server client.
    :type client_url: str

    :param token: It contains your authentication token.
    :type token: str

    :return: Write API instance.
    :rtype: WriteApi
    """
    client = InfluxDBClient(url=client_url, token=token)
    return client.write_api(write_options=SYNCHRONOUS)


def record_point(point, write_api, bucket, org):
    """It writes a point into a InfluxDB Bucket.

        :param point: It represent the Point that is wanted to be added into the bucket.
        :type point: Point

        :param write_api: It represent the API used to write the point on a bucket.
        :type write_api: WriteApi

        :param bucket: It contains the name of the bucket were the point will be written.
        :type bucket: str

        :param org: It contains your organization ID.
        :type org: str
        """
    print(point)
    print("         ~~ INFO:Writing point into '" + bucket + "' ...")

    p = Point("TEST_SUNDAY")\
        .time(point.commited_date, WritePrecision.S)\
        .tag("repo_id", point.repo_id)\
        .tag("commit_hexsha", point.commit_hexsha)\
        .tag("commit_author", point.commit_author) \
        .tag("repo_name", point.repo_name)\
        .tag("repo_owner", point.repo_owner)\
        .field("total_commit_dependencies", point.total_commit_dependencies)\
        .field("new_vulnerabilities", point.new_vulnerabilities)\
        .field("fixed_vulnerabilities", point.fixed_vulnerabilities) \
        .field("revoked_vulnerabilities", point.revoked_vulnerabilities)\
        .field("kept_vulnerabilities", point.kept_vulnerabilities)\
        .field("total_vulnerabilities", point.total_vulnerabilities)\
        .field("critical_severity", point.critical_severity) \
        .field("high_severity", point.high_severity)\
        .field("moderate_severity", point.moderate_severity)\
        .field("low_severity", point.low_severity)\
        .tag("has_config_file", point.has_config_file)

    write_api.write(bucket, org, p, time_precision='s')
