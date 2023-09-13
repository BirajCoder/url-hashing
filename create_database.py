import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client("dynamodb", region_name="ap-south-1")

# Define the table schema
table_name = "URLHashes"
key_schema = [
    {"AttributeName": "hashed_url", "KeyType": "HASH"},  # Partition key
]

attribute_definitions = [
    {"AttributeName": "hashed_url", "AttributeType": "S"},  # String
]

# Create the table
dynamodb.create_table(
    TableName=table_name,
    KeySchema=key_schema,
    AttributeDefinitions=attribute_definitions,
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)

# Wait for the table to be created (this may take a few seconds)
dynamodb.get_waiter("table_exists").wait(TableName=table_name)

print(f"Table {table_name} created successfully!")
