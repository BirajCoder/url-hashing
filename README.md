## Architecture Choice and Reasoning

The provided code is a Flask-based web application designed to hash URLs and track their usage statistics using Amazon DynamoDB as a backend database. Here is an overview of the architecture choice and the reasoning behind it:

**Flask:** Flask is a lightweight and flexible web framework for Python, making it an excellent choice for building web applications. It provides the necessary tools and extensions for developing RESTful APIs and web services. The use of Flask allows for rapid development and easy integration with other libraries and services.

**Amazon DynamoDB:** DynamoDB is a fully managed NoSQL database service provided by AWS. It is highly scalable, reliable, and can handle high-throughput workloads. In this architecture, DynamoDB serves as the backend database for storing hashed URLs, original URLs, and click counts. The decision to use DynamoDB is based on its ability to handle the expected load, as well as its seamless integration with other AWS services.

**Boto3:** Boto3 is the official AWS SDK for Python. It is used in the code to interact with DynamoDB and manage AWS resources. Boto3 simplifies the process of connecting to AWS services and performing operations on them.

**Flask-Limiter:** Flask-Limiter is used to implement rate limiting on certain routes of the application. This helps protect the application from abuse and ensures fair usage of resources. It allows you to set rate limits on a per-minute and per-day basis.


