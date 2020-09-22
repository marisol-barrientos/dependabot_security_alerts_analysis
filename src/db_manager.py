from influxdb import InfluxDBClient, DataFrameClient
from influxdb_client.client.write_api import SYNCHRONOUS
USER = 'root'
PASSWORD = 'root'
DBNAME = 'mydb'

def record_point(point, bucket, org):
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

    host = 'localhost'
    port = 8086

    print(point)
    print("\n         ~~ INFO:Writing point into '" + DBNAME + "' ...")
    client = InfluxDBClient(host=host, port=port, username=USER, password=PASSWORD, database=DBNAME)
    json_body = [
        {
            "measurement": 'Record',
            "time": point.commited_date,
            "tags": {
                "repo_id": str(point.repo_id),
                "commit_hexsha":  str(point.commit_hexsha) ,
                "commit_author":  str(point.commit_author) ,
                "repo_name":  str(point.repo_name) ,
                "repo_owner": str(point.repo_owner) ,
                "email": str(point.email) ,
                "commit_message": str(point.commit_message) ,
                "has_config_file": str(point.has_config_file)
            },
            "fields": {
                "total_commit_dependencies": point.total_commit_dependencies,
                "new_critical_vulnerabilities": len(point.critical_severity["new_vulnerabilities"]),
                "fixed_critical_vulnerabilities": len(point.critical_severity["fixed_vulnerabilities"]),
                "removed_critical_vulnerabilities": len(point.critical_severity["removed_vulnerabilities"]),
                "revoked_fixed_critical_vulnerabilities": len(point.critical_severity["revoked_fixed_vulnerabilities"]),
                "revoked_removed_critical_vulnerabilities": len(point.critical_severity["revoked_removed_vulnerabilities"]),
                "kept_critical_vulnerabilities": len(point.critical_severity["kept_vulnerabilities"]),
                "new_high_vulnerabilities": len(point.high_severity["new_vulnerabilities"]),
                "fixed_high_vulnerabilities": len(point.high_severity["fixed_vulnerabilities"]),
                "removed_high_vulnerabilities": len(point.high_severity["removed_vulnerabilities"]),
                "revoked_fixed_high_vulnerabilities": len(point.high_severity["revoked_fixed_vulnerabilities"]),
                "revoked_removed_high_vulnerabilities": len(point.high_severity["revoked_removed_vulnerabilities"]),
                "kept_high_vulnerabilities": len(point.high_severity["kept_vulnerabilities"]),
                "new_moderate_vulnerabilities": len(point.moderate_severity["new_vulnerabilities"]),
                "fixed_moderate_vulnerabilities": len(point.moderate_severity["fixed_vulnerabilities"]),
                "removed_moderate_vulnerabilities": len(point.moderate_severity["removed_vulnerabilities"]),
                "revoked_fixed_moderate_vulnerabilities": len(point.moderate_severity["revoked_fixed_vulnerabilities"]),
                "revoked_removed_moderate_vulnerabilities": len(point.moderate_severity["revoked_removed_vulnerabilities"]),
                "kept_moderate_vulnerabilities": len(point.moderate_severity["kept_vulnerabilities"]),
                "new_low_vulnerabilities": len(point.low_severity["new_vulnerabilities"]),
                "fixed_low_vulnerabilities": len(point.low_severity["fixed_vulnerabilities"]),
                "removed_low_vulnerabilities": len(point.low_severity["removed_vulnerabilities"]),
                "revoked_fixed_low_vulnerabilities": len(point.low_severity["revoked_fixed_vulnerabilities"]),
                "revoked_removed_low_vulnerabilities": len(point.low_severity["revoked_removed_vulnerabilities"]),
                "kept_low_vulnerabilities": len(point.low_severity["kept_vulnerabilities"]),
                "total_new_vulnerabilities": len(point.summary["new_vulnerabilities"]),
                "total_fixed_vulnerabilities": len(point.summary["fixed_vulnerabilities"]),
                "total_removed_vulnerabilities": len(point.summary["removed_vulnerabilities"]),
                "total_revoked_fixed_vulnerabilities": len(point.summary["revoked_fixed_vulnerabilities"]),
                "total_revoked_removed_vulnerabilities": len(point.summary["revoked_removed_vulnerabilities"]),
                "total_kept_vulnerabilities": len(point.summary["kept_vulnerabilities"]),
                "total_commit_vulnerabilities": len(point.summary["total"])
            }
        }
    ]

    client.write_points(json_body, time_precision='s', protocol='json', database='mydb')
    #client_df = DataFrameClient(host=host, port=port, username=USER, password=PASSWORD, database=DBNAME)
    #results_df = client_df.query('SELECT * FROM Commit_22')
