import boto3


def get_aws_session(config=None, region_name=None, aws_access_key_id=None, aws_secret_access_key=None,
                    profile_name=None):
    if config is None:
        config = {
            "region_name": region_name,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "profile_name": profile_name}
    return boto3.session.Session(**config)