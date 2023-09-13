from flask import (
    Flask,
    request,
    jsonify,
    render_template,
)
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import hashlib
import time
from wtforms import Form, StringField, validators
from flask_limiter import Limiter


app = Flask(__name__)
limiter = Limiter(
    app,
    default_limits=[
        "10 per minute",
        "100 per day",
    ],
)


@limiter.request_filter
def log_rate_limit_exceeded(key):
    app.logger.warning(f"Rate limit exceeded for key: {key}")
    return False


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request"}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal Server Error"}), 500


# Initialize DynamoDB client
dynamodb = boto3.client("dynamodb", region_name="ap-south-1")
table_name = "URLHashes"


@app.route("/")
def index():
    return render_template("index.html")


class URLForm(Form):
    original_url = StringField(
        "Original URL", [validators.URL(), validators.DataRequired()]
    )


def hash(original_url):
    # Generate a hash for the URL
    hashed_url = hashlib.sha256(original_url.encode()).hexdigest()

    # Get the current timestamp
    timestamp = str(int(time.time()))

    # Store the data in DynamoDB
    dynamodb.put_item(
        TableName=table_name,
        Item={
            "hashed_url": {"S": hashed_url},
            "timestamp": {"N": timestamp},
            "original_url": {"S": original_url},
            "click_count": {"N": "0"},  # Initialize click_count to 0
        },
    )
    return hashed_url


@limiter.limit("10 per minute")
@app.route("/hash", methods=["POST"])
def hash_url():
    form = URLForm(request.form)
    if form.validate():
        original_url = request.form.get("original_url")

        hashed_url = hash(original_url)
        return jsonify({"hashed_url": hashed_url}), 201

    else:
        return jsonify({"error": "Invalid input"}), 400


@limiter.limit("10 per minute")
@app.route("/api/hash", methods=["POST"])
def hash_url_api():
    form = URLForm(request.form)
    if form.validate():
        data = request.get_json()
        original_url = data.get("original_url")
        hashed_url = hash(original_url)
        return jsonify({"hashed_url": hashed_url}), 201

    else:
        return jsonify({"error": "Invalid input"}), 400


@limiter.limit("100 per minute")
@app.route("/<hashed_url>", methods=["GET"])
def redirect_url(hashed_url):
    try:
        # Retrieve the original URL from DynamoDB
        response = dynamodb.get_item(
            TableName=table_name, Key={"hashed_url": {"S": str(hashed_url)}}
        )

        item = response.get("Item")

        if item:
            original_url = item["original_url"]["S"]

            # Increment click_count
            click_count = int(item.get("click_count", {"N": "0"})["N"])
            click_count += 1

            # Update click_count in DynamoDB
            dynamodb.update_item(
                TableName=table_name,
                Key={"hashed_url": {"S": hashed_url}},
                UpdateExpression="SET click_count = :val",
                ExpressionAttributeValues={":val": {"N": str(click_count)}},
            )

            return (
                jsonify({"original_url": original_url}),
                302,
                {"Location": original_url},
            )
        else:
            return jsonify({"error": "URL not found"}), 404

    except ClientError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/dashboard")
def dashboard():
    try:
        response = dynamodb.scan(TableName=table_name)
        items = response.get("Items", [])

        item_details = []

        for item in items:
            original_url = item["original_url"]["S"]
            hashed_url = item["hashed_url"]["S"]
            click_count = int(item.get("click_count", {"N": "0"})["N"])

            item_details.append(
                {
                    "original_url": original_url,
                    "hashed_url": hashed_url,
                    "click_count": click_count,
                }
            )

        return render_template("dashboard.html", items=item_details)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)


# # Initialize AWS Cognito client
# cognito_client = boto3.client("cognito-idp", region_name="ap-south-1")


# def authenticate_user():
#     token = session.get("token")
#     if not token:
#         return False

#     try:
#         # Verify the user's token using AWS Cognito
#         cognito_client.get_user(AccessToken=token)
#         return True
#     except NoCredentialsError:
#         return False


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")

#         # Authenticate the user using AWS Cognito
#         try:
#             response = cognito_client.initiate_auth(
#                 AuthFlow="USER_PASSWORD_AUTH",
#                 AuthParameters={
#                     "USERNAME": username,
#                     "PASSWORD": password,
#                 },
#                 ClientId="3l5hajlkmsk4m4javtgmotnqd5",  # Replace with your Cognito App Client ID
#             )
#             print(response)
#             session["token"] = response["ResponseMetadata"]["RequestId"]
#             return redirect(url_for("index"))  # Redirect to the home page on success
#         except ClientError as e:
#             print("Authentication failed:", str(e))
#             return jsonify({"error": "Authentication failed"}), 401

#     return render_template("login.html")
