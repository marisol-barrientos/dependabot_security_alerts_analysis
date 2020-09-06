import point
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def open_connection(client, token):
    client = InfluxDBClient(url=client, token=token)
    return client.write_api(write_options=SYNCHRONOUS)


def record_point(repo_id
                , commited_date
                , commit_hexsha
                , commit_author
                , repo_name
                , repo_owner
                , total_commit_dependencies
                , new_vulnerabilities
                , fixed_vulnerabilities
                , revoked_vulnerabilities
                , kept_vulnerabilities
                , total_vulnerabilities
                , critical_severity
                , high_severity
                , moderate_severity
                , low_severity
                , has_config_file
                , write_api
                , bucket
                , org):

    aux_point = point.Point(repo_id
                    , commited_date
                    , commit_hexsha
                    , commit_author
                    , repo_name
                    , repo_owner
                    , total_commit_dependencies
                    , new_vulnerabilities
                    , fixed_vulnerabilities
                    , revoked_vulnerabilities
                    , kept_vulnerabilities
                    , total_vulnerabilities
                    , critical_severity
                    , high_severity
                    , moderate_severity
                    , low_severity
                    , has_config_file)
    print(aux_point)
    print("         ~~ INFO:Writing point into '" + bucket + "' ...")

    p = Point("TEST_SUNDAY")\
        .time(commited_date, WritePrecision.S)\
        .tag("repo_id", repo_id)\
        .tag("commit_hexsha", commit_hexsha)\
        .tag("commit_author", commit_author) \
        .tag("repo_name", repo_name)\
        .tag("repo_owner", repo_owner)\
        .field("total_commit_dependencies", total_commit_dependencies)\
        .field("new_vulnerabilities", new_vulnerabilities)\
        .field("fixed_vulnerabilities", fixed_vulnerabilities) \
        .field("revoked_vulnerabilities", revoked_vulnerabilities)\
        .field("kept_vulnerabilities", kept_vulnerabilities)\
        .field("total_vulnerabilities", total_vulnerabilities)\
        .field("critical_severity", critical_severity) \
        .field("high_severity", high_severity)\
        .field("moderate_severity", moderate_severity)\
        .field("low_severity", low_severity)\
        .tag("has_config_file", has_config_file)

    write_api.write(bucket, org, p, time_precision='s')
