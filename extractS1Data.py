from transformData import normalizeData
import requests, json, sys, signal, argparse, time

#data flow:
#1. send the query in your timeframe /web/api/v2.1/dv/init-query -> you will receive a queryId
#2. request the events using that queryId /web/api/v2.1/dv/events
#4. normalize/anonymize the fields
#5. save the output in a file
#5. call chatgpt api
#6. print/save the chatgpt response

#global variables
serverURI  = 'https://xxx.sentinelone.net'
create_initial_query = '/web/api/v2.1/dv/init-query'
get_events = '/web/api/v2.1/dv/events'
token = 'xxx'
limit = "1000" # If required, change the limit of returned data. Max is 1000.

def def_handler(sig, frame):
        log.failure("Exiting..")
        sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


def retrieveTelemetry(args):
        #recieve the value of the user input
        queryArguments = args.query
        timeFromArguments = args.timeFrom
        timeTo = args.timeTo

        #header data
        headers = {
        "Content-type": "application/json",
        "Authorization": "APIToken " + token
        }
        #post data
        post_data = {
                "limit": limit,
                "isVerbose": "true",
                "query": queryArguments+" AND EventType In (\"Process Creation\", \"IP Connect\", \"Login\", \"Behavioral Indicators\", \"Command Script\", \"Duplicate Process Handle\", \"Open Remote Process Handle\")",
                "toDate": timeTo+":00.000000Z",
                "fromDate": timeFromArguments+":00.000000Z"
        }

        json_data = json.dumps(post_data)
        if args.verbose:
                print("\nSending post data: "+json_data)

        #First request to retrieve the 'queryId'
        first_response = requests.post(serverURI + create_initial_query, data=json_data, headers=headers)

        if args.verbose:
                print("\nReturning queryId: "+first_response.text)
                print("\nRetrive SentinelOne events...")
        #Get the queryId value
        response_data = first_response.json()
        query_id = response_data["data"]["queryId"]
        time.sleep(3) #delay added between init query and retrieve events query

        #Second request to get the telemetry
        second_response = requests.get(serverURI + get_events + "?queryId=" + query_id + "&limit=" + limit + "&sortOrder=asc", headers=headers)
        data = second_response.json()
        normalizeData(data, args)
