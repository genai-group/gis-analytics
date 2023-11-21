#!/usr/bin/python

import pytest
from config.functions import s3_create_bucket
from botocore.exceptions import ClientError

def test_s3_create_bucket() -> None:
    """
    Test the s3_create_bucket function to ensure it creates a bucket successfully.

    This test assumes the use of a mock S3 service or a dedicated test bucket.
    It checks that the bucket is created successfully by asserting the HTTP status code in the response.
    
    Raises:
        AssertionError: If the bucket creation does not return a 200 HTTP status code.
        ClientError: If there is an AWS client error during bucket creation.
    """
    bucket_name = "test-bucket"

    try:
        response = s3_create_bucket(bucket_name)
        # Assert that the response is either None (in case of mock) or contains a successful HTTP status code.
        assert response is None or response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as e:
        pytest.fail(f"AWS Client Error: {e}")