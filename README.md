# Queue Management System

This API is part of a system to manage and process messages sent to an SQS Queue. It consists of this API, a PostgreSQL Database and a Lambda function. 

### How it works?

The message containing data about a user will be sent to the SQS Queue,that will trigger the Lambda function that will consume the message and then sent a request to the API to create the user, save the message and then publish to a SNS topic if the execution is sucessful. The project uses [localstack](https://github.com/localstack/localstack) to emulate the AWS environment and make the testing process easier.

### How to run the project?

- Clone the repositories

```
mkdir queue-management
cd queue-management
git clone https://github.com/davodg/message-manager-api
git clone https://github.com/davodg/sqs-processor
```

- Set the .env files for local testing

message-manager-api .env file
```
DB_NAME="message_manager_api"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="postgres"
DB_PORT="5432"
```

record-processor .env file
```
MESSAGE_MANAGER_API_HOST=http://localhost:5001
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:767397894053:record-processing-notifier
```

- To setup the application, you need to install:
[docker](https://docs.docker.com/get-docker/),
[npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm),
serverless: 
```
npm install -g serverless
```


- Give permission to the .sh responsible to start the application

```
chmod +x setup_project.sh
```

- Execute the script to setup the dependencies for the project
```
sudo ./setup_project.sh
```

- Send an SQS Message
```
 aws sqs send-message --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/test_queue --message-body "{'name': 'Lionel Messi', 'age': 36, 'email': 'lionel.messi@gmail.com', 'phone': '11948522847'}"  --endpoint-url http://localhost:4566
```

- Check the lamda logs
```
./get_logs.sh
```

- Get the users
```
curl http://localhost:5001/users
```


### Message Manager API API

This is an API to manage the PostgreSQL database performing CRUD operations. Currently there are 2 endpoints, "/users" and "/messages"

- GET /users

This will return all users. If you want to filter for a specific user, use the query_param 'user_id'. This endpoint supports pagination. The default limit is 20 but you can change it specifying the query_param 'limit' and 'page' to access other pages \
Response:

```
{
    "meta": {
        "total": 1,
        "page": 1,
        "limit": 20
    },
    "data": [
        {
            "id": "0dc46362-4831-4880-92c7-652ffeb02a52",
            "name": "Lionel Messi",
            "email": "lionel.messi@gmail.com",
            "phone": "11948522847",
            "age": 36,
            "creation_date": "2024-04-03 03:08:47",
            "update_date": null
        }
    ]
}
```

- POST /users

This endpoint will create a new user.

Payload:

```
{
    "name": "Lionel Messi",
    "age": 36,
    "email": "lionel.messi@gmail.com",
    "phone": "11948522847"
}
```

Return:

```
{
    "meta": {},
    "data": {
        "id": "90677a30-d934-4636-9de3-8b4e364a8d28",
        "name": "Lionel Messi",
        "email": "lionel.messi@gmail.com",
        "phone": "11948522847",
        "age": 36,
        "creation_date": "2024-04-03T13:35:20.864481",
        "update_date": null
    }
}
```

- PUT /users?user_id=:uuid

This endpoint will update the user specified in the query_param. Simply use the same payload as the POST request updating the attributes

Payload:

```
{
    "name": "Lionel Andrés Messi",
    "age": 36,
    "email": "lionel.messi@gmail.com",
    "phone": "11948522847"
}
```

Return:

```
{
    "meta": {},
    "data": {
        "id": "90677a30-d934-4636-9de3-8b4e364a8d28",
        "name": "Lionel Andrés Messi",
        "email": "lionel.messi@gmail.com",
        "phone": "11948522847",
        "age": 36,
        "creation_date": "2024-04-03T13:35:20.864481",
        "update_date": 2024-04-03T23:13:37.102401
    }
}
```

- DELETE /users?user_id=:uuid

This endpoint will simply delete the user specified in the query_param 'user_id'

- GET /messages

This endpoint will get all the processed messages recorded in the database. If you want to filter for a specific message, use the query_param 'message_id'. This endpoint supports pagination. The default limit is 20 but you can change it specifying the query_param 'limit' and 'page' to access other pages \
Response:

```
{
    "meta": {
        "total": 1,
        "page": 1,
        "limit": 20
    },
    "data": [
        {
            "id": "037565d6-e7aa-423b-95f4-08b4bde52f9a",
            "status": "processed",
            "text": {
                "name": "Lionel Andrés Messi",
                "age": 36,
                "email": "lionel.messi@gmail.com",
                "phone": "11948522847"
            },
            "creation_date": "2024-04-03 14:53:09",
            "update_date": null,
            "error": null
        }
    ]
}
```



- POST /messages

This endpoint will create a new record in the database for a processed message

Payload:

```
{
    "status": "processed",
    "text": {
        "name": "Lionel Andrés Messi",
        "age": 36,
        "email": "lionel.messi@gmail.com",
        "phone": "11948522847"
    }
}
```

Return

```
{
    "meta": {},
    "data": {
        "id": "e9cf88ee-e06a-490f-a58f-f2056e2d90af",
        "status": "processed",
        "text": {
            "name": "Lionel Andrés Messi",
            "age": 36,
            "email": "lionel.messi@gmail.com",
            "phone": "11948522847"
        },
        "creation_date": "2024-04-03T13:54:37.473479"
    }
}
```


- PUT /messages?message_id=:uuid

This endpoint will update the message specified in the query_param. Simply use the same payload as the POST request updating the attributes

Payload:

```
{
    "status": "processed",
    "text": {
        "name": "Lionel Messi",
        "age": 36,
        "email": "lionel.messi@gmail.com",
        "phone": "11948522847"
    }
}
```

Return:

```
{
    "meta": {},
    "data": {
        "id": "e9cf88ee-e06a-490f-a58f-f2056e2d90af",
        "status": "processed",
        "text": {
            "name": "Lionel Messi",
            "age": 36,
            "email": "lionel.messi@gmail.com",
            "phone": "11948522847"
        },
        "creation_date": "2024-04-03T13:54:37.473479",
        "update_date": "2024-04-03T13:58:43.563829",
    }
}
```

- DELETE /messages?message_id=:uuid

This endpoint will simply delete the message specified in the query_param 'message_id'

### Record-processor

This is a simple Lambda function that will consume the messages from the SQS queue
