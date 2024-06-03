curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
/aws/install

npm install -g serverless

cd ../sqs-processor
serverless plugin install --name serverless-python-requirements
serverless plugin install --name serverless-localstack
cd ../

cd message-manager-api
docker compose up --detach --build --remove-orphans
sleep 10

container_id=$(docker ps -qf "name=message-manager-api")
docker exec -it "$container_id" bash -c "make migrate-up"

cd ../sqs-processor

AWS_ACCESS_KEY_ID="dummy"
AWS_SECRET_ACCESS_KEY="dummy"
AWS_DEFAULT_REGION="us-east-1"
AWS_DEFAULT_OUTPUT="text"

echo "aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}" | sh
echo "aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}" | sh
echo "aws configure set default.region ${AWS_DEFAULT_REGION}" | sh
echo "aws configure set default.output ${AWS_DEFAULT_OUTPUT}" | sh


aws --endpoint-url http://localhost:4566 --region us-east-1 sqs create-queue --queue-name test_queue --attributes DelaySeconds=5
aws --endpoint-url http://localhost:4566 --region us-east-1 sns create-topic --name record-processing-notifier

export SERVERLESS_ACCESS_KEY="dummy"
serverless deploy --stage local