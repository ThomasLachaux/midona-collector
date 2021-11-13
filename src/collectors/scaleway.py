import boto3
from os import environ


def collect():
    s3_id = environ.get("SCALEWAY_ACCESS_KEY_ID")
    s3_secret = environ.get("SCALEWAY_SECRET_ACCESS_KEY")
    s3 = boto3.client(
        service_name="s3",
        region_name="fr-par",
        use_ssl=True,
        endpoint_url="https://s3.fr-par.scw.cloud",
        aws_access_key_id=s3_id,
        aws_secret_access_key=s3_secret,
    )

    buckets = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in buckets["Buckets"]]

    for bucket in buckets:
        response = s3.list_objects(Bucket=bucket)

        bucket_size = 0
        if "Contents" in response:
            bucket_size = sum(obj["Size"] for obj in response["Contents"])

        yield f"scaleway,bucket={bucket} size={bucket_size}u"


if __name__ == "__main__":
    for i in collect():
        print(i)
