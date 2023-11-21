#!/usr/bin/python

from modules import *
from clients import *

###############################
####    Basic Functions    ####
###############################

def map_func(func, *iterables):
    """
    Map a function to a list of iterables.
    """
    
    try:
        return list(map(func, *iterables))
    
    except Exception as e:
        raise ValueError(f"Failed to map function '{func}' to iterables '{iterables}'. Error: {e}")
        return []

def filter_func(func, iterable):
    """
    Filter an iterable using a function.
    """
    try:
        return list(filter(func, iterable))
    
    except Exception as e:
        raise ValueError(f"Failed to filter iterable '{iterable}' using function '{func}'. Error: {e}")
        return []

## Datetime functions

"""
assert to_unix("2023-08-09 12:00:00") == 1691582400
assert from_unix(1691582400) == datetime(2023, 8, 9, 12, 0, tzinfo=timezone.utc)
"""

def to_unix(date_str: str, tz_str: Optional[str] = None) -> int:
    """
    Convert a date string to a timezone aware UNIX timestamp using dateutil parsing.

    :param date_str: String representation of the date.
    :param tz_str: Timezone string. If None, it's treated as UTC.
    :return: UNIX timestamp.
    """

    try:
        # Convert string to datetime object using dateutil parsing
        if isinstance(date_str, str):
            dt = parse(date_str)
        else:
            dt = date_str

        # If the parsed datetime is naive, attach the appropriate timezone
        if dt.tzinfo is None:
            if tz_str:
                import pytz
                tz = pytz.timezone(tz_str)
                dt = tz.localize(dt)
            else:
                dt = dt.replace(tzinfo=timezone.utc)
        
        # Convert datetime to UNIX timestamp
        return int(dt.timestamp())
    
    except Exception as e:
        raise ValueError(f"Failed to convert date string '{date_str}' to UNIX timestamp. Error: {e}")
        return None

def from_unix(unix_timestamp: int, tz_str: Optional[str] = None) -> datetime:
    """
    Convert a UNIX timestamp to a timezone aware datetime object.

    :param unix_timestamp: UNIX timestamp to convert.
    :param tz_str: Timezone string. If None, it's returned as UTC.
    :return: Timezone aware datetime object.
    """

    try:
        # Convert UNIX timestamp to datetime
        dt = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)

        # If timezone is provided, adjust datetime
        if tz_str:
            import pytz
            tz = pytz.timezone(tz_str)
            dt = dt.astimezone(tz)

        return dt
    
    except Exception as e:
        raise ValueError(f"Failed to convert UNIX timestamp '{unix_timestamp}' to datetime. Error: {e}")
        return None


############################
####    S3 Functions    ####
############################

def s3_create_bucket(bucket_name: str, region: Optional[str] = None) -> None:
    """
    Create a new S3 bucket in a specified region.

    Args:
        bucket_name (str): The name of the bucket to create.
        region (str, optional): The AWS region in which to create the bucket. Defaults to None.

    Returns:
        None
    """
    try:
        s3_client = boto3.client('s3', region_name=region)
        if region is None:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print(f"Bucket '{bucket_name}' created")
    except ClientError as e:
        print(f"Error creating bucket: {e}")

def s3_list_items(bucket_name: str) -> None:
    """
    List all items in a specified S3 bucket.

    Args:
        bucket_name (str): The name of the bucket to list items from.

    Returns:
        None
    """
    try:
        s3_client = boto3.client('s3')
        contents = s3_client.list_objects_v2(Bucket=bucket_name).get('Contents', [])
        for item in contents:
            print(item['Key'])
    except ClientError as e:
        print(f"Error listing items in bucket: {e}")

def empty_and_delete_bucket(bucket_name: str) -> None:
    """
    Empty and delete a specified S3 bucket.

    Args:
        bucket_name (str): The name of the bucket to empty and delete.

    Returns:
        None
    """
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete()
        bucket.delete()
        print(f"Bucket '{bucket_name}' emptied and deleted")
    except ClientError as e:
        print(f"Error in emptying and deleting bucket: {e}")

def upload_file(bucket_name: str, file_path: str, object_name: Optional[str] = None) -> None:
    """
    Upload a file to an S3 bucket.

    Args:
        bucket_name (str): The name of the bucket to upload to.
        file_path (str): The file path to upload.
        object_name (str, optional): The object name in the bucket. Defaults to file_path if None.

    Returns:
        None
    """
    if object_name is None:
        object_name = file_path

    try:
        s3_client = boto3.client('s3')
        with open(file_path, 'rb') as file:
            s3_client.upload_fileobj(file, bucket_name, object_name)
        print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}'")
    except ClientError as e:
        print(f"Error uploading file: {e}")

def s3_download_file(bucket_name: str, object_name: str, file_path: Optional[str] = None) -> None:
    """
    Download a file from an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The object name in the bucket to download.
        file_path (str, optional): The local file path to save the downloaded file. Defaults to object_name if None.

    Returns:
        None
    """
    if file_path is None:
        file_path = object_name

    try:
        s3_client = boto3.client('s3')
        with open(file_path, 'wb') as file:
            s3_client.download_fileobj(bucket_name, object_name, file)
        print(f"File '{object_name}' downloaded from '{bucket_name}' to '{file_path}'")
    except ClientError as e:
        print(f"Error downloading file: {e}")

def s3_update_bucket_policy(bucket_name: str, policy: dict) -> None:
    """
    Update the policy of an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        policy (dict): The policy in dictionary format to apply to the bucket.

    Returns:
        None
    """
    policy_json = json.dumps(policy)
    try:
        s3_client = boto3.client('s3')
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy_json)
        print(f"Policy updated for bucket '{bucket_name}'")
    except ClientError as e:
        print(f"Error updating bucket policy: {e}")

def s3_generate_presigned_url(bucket_name: str, object_name: str, expiration: int = 3600) -> None:
    """
    Generate a presigned URL for an S3 object.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The object name in the bucket for which to generate the URL.
        expiration (int, optional): Time in seconds for the presigned URL to remain valid. Defaults to 3600 seconds (1 hour).

    Returns:
        None
    """
    try:
        s3_client = boto3.client('s3')
        url = s3_client.generate_presigned_url('get_object',
                                               Params={'Bucket': bucket_name, 'Key': object_name},
                                               ExpiresIn=expiration)
        print(f"Presigned URL: {url}")
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")

##################################
####    Postgres Functions    ####
##################################


# Postgres Functions

def create_table_from_json(conn, json_data, parent_table=None, parent_key=None):
    """
    Recursively creates tables from a JSON object.

    Args:
    conn (psycopg2.connection): PostgreSQL database connection.
    json_data (dict): A JSON object.
    parent_table (str, optional): Name of the parent table for nested objects.
    parent_key (str, optional): Primary key of the parent table for linking.
    """
    if isinstance(json_data, dict):
        # Determine table name
        table_name = parent_table + "_child" if parent_table else "root_table"
        columns = []
        foreign_key = None
        if parent_table and parent_key:
            foreign_key = parent_key + "_id"
            columns.append(foreign_key + " INTEGER REFERENCES " + parent_table + "(" + parent_key + ")")

        # Process each key in the JSON object
        for key, value in json_data.items():
            if isinstance(value, dict):
                # Recursive call for nested objects
                create_table_from_json(conn, value, table_name, key)
            elif isinstance(value, list):
                # Handle lists (arrays)
                for item in value:
                    if isinstance(item, dict):
                        create_table_from_json(conn, item, table_name, key)
            else:
                # Simple data types
                columns.append(key + " " + get_sql_data_type(value))

        # Create table
        create_table_query = "CREATE TABLE IF NOT EXISTS " + table_name + " (" + ", ".join(columns) + ")"
        execute_sql(conn, create_table_query)

    elif isinstance(json_data, list):
        # Handle JSON arrays
        for item in json_data:
            if isinstance(item, dict):
                create_table_from_json(conn, item, parent_table, parent_key)

def get_sql_data_type(value):
    """
    Maps a Python data type to an SQL data type.
    
    Args:
    value: A Python value.
    
    Returns:
    str: An SQL data type.
    """
    if isinstance(value, int):
        return "INTEGER"
    elif isinstance(value, float):
        return "REAL"
    elif isinstance(value, bool):
        return "BOOLEAN"
    else:
        return "TEXT"

def execute_sql(conn, query):
    """
    Executes an SQL query using the given connection.

    Args:
    conn (psycopg2.connection): PostgreSQL database connection.
    query (str): SQL query to execute.
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()

# Example usage
conn = connect_to_postgres()
json_data = '{"name": "John", "age": 30, "address": {"street": "123 Main St", "city": "Anytown"}, "hobbies": ["reading", "hiking"]}'
create_table_from_json(conn, json.loads(json_data))



def normalize_name(name: str) -> Optional[str]:
    """
    Normalizes a name string by performing various transformations.

    This function performs the following operations:
    1. Trims leading and trailing whitespaces.
    2. Converts the name to lowercase.
    3. Removes diacritics and accents from characters.
    4. Removes punctuation and special characters.
    5. Normalizes whitespaces to single spaces.
    
    Parameters:
    name (str): The name string to be normalized.

    Returns:
    Optional[str]: The normalized name as a string or None if the input is invalid.

    Raises:
    ValueError: If the input is not a string or is an empty string.
    """

    try:
        # Input Validation
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")

        # Trimming, Case Normalization, and Whitespace Normalization
        name = name.strip().lower()

        # Removing Diacritics
        name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')

        # Removing Punctuation and Special Characters
        name = re.sub(r"[^\w\s]", '', name)

        # Whitespace Normalization (Again)
        name = re.sub(r"\s+", ' ', name)

        return name

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
try:
    normalized_name = normalize_name("Dr. María-José O'Neill")
    print(normalized_name)  # Output: 'maria jose oneill'
except ValueError as ve:
    print(f"ValueError: {ve}")



