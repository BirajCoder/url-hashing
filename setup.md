### Prerequisites

Before using the application, ensure that you have the following prerequisites installed:

- Python 3.x
- Flask
- Boto3 (AWS SDK for Python)
- Flask-Limiter
- Amazon Web Services (AWS) account with configured credentials (Access Key and Secret Key)
- DynamoDB table named "URLHashes" created in the AWS region specified in the code (ap-south-1 by default)

### Configuration

You need to set up your AWS credentials before running the application. You can do this by using the AWS Command Line Interface (CLI) or by configuring the credentials in the `~/.aws/credentials` file.

### Running the Application

1. Clone the repository or download the provided code.

2. Navigate to the project directory.

3. Install the required Python packages:

   ```
   pip install Flask boto3 flask-limiter wtforms
   ```

4. Run the Flask application:

   ```
   python app.py
   ```

   The application should now be running locally on `http://localhost:5000`.

5. Access the application using a web browser or use API requests to interact with it.

### Routes

- `/`: The homepage of the application.
- `/hash` (POST): Hashes a provided URL and stores it in DynamoDB.
- `/api/hash` (POST): API endpoint to hash a URL.
- `/<hashed_url>` (GET): Redirects to the original URL associated with the hashed URL and increments the click count.
- `/dashboard`: Displays a dashboard showing statistics of hashed URLs and click counts.