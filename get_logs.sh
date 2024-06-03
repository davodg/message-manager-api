LOG_GROUPS_OUTPUT="$(aws logs describe-log-groups --query 'logGroups[?starts_with(logGroupName, `/aws/lambda`) == `true`].logGroupName' --endpoint-url http://localhost:4566)"
read -ra LOG_GROUP_NAMES <<< "$LOG_GROUPS_OUTPUT"

for LOG_GROUP_NAME in "${LOG_GROUP_NAMES[@]}"
do
    echo "********* Logging group $LOG_GROUP_NAME"
    LOG_STREAMS_OUTPUT="$(aws logs describe-log-streams --log-group-name "$LOG_GROUP_NAME" --query 'logStreams[*].logStreamName' --endpoint-url http://localhost:4566)"
    read -ra LOG_STREAM_NAMES <<< "$LOG_STREAMS_OUTPUT"

    for LOG_STREAM_NAME in "${LOG_STREAM_NAMES[@]}"
    do
        echo "+++++++++++++++++++++++++ Logs for $LOG_GROUP_NAME -> $LOG_STREAM_NAME"
        aws logs get-log-events --log-stream-name "$LOG_STREAM_NAME" --log-group-name "$LOG_GROUP_NAME" --query 'events[*].message' --endpoint-url http://localhost:4566 
    done
# sed here is necessary because with text output the logs are (inexplicably) tab-separated
done | sed 's/\t/\n/g'