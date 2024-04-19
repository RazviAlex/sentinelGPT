from extractS1Data import retrieveTelemetry
import argparse, sys

if __name__ == '__main__':

        #Get the argument for the user input
        ascii_sentinelGPT = '''
  ____             _   _            _  ___              ____ ____ _____
 / ___|  ___ _ __ | |_(_)_ __   ___| |/ _ \ _ __   ___ / ___|  _ \_   _|
 \___ \ / _ \ '_ \| __| | '_ \ / _ \ | | | | '_ \ / _ \ |  _| |_) || |
  ___) |  __/ | | | |_| | | | |  __/ | |_| | | | |  __/ |_| |  __/ | |
 |____/ \___|_| |_|\__|_|_| |_|\___|_|\___/|_| |_|\___|\____|_|    |_|

 '''


        print(ascii_sentinelGPT)
        parser = argparse.ArgumentParser(description='SentinelOneGPT script. v.1.1')
        parser.add_argument("--model", help="Choose the GPT model. Available ones are - 'gpt-3.5T, gpt-4-32k or gpt-4-preview'")
        parser.add_argument("--query", help="Specific the query to execute")
        parser.add_argument("--timeFrom", help="Specific the query time from. E.g. 2023-01-16T10:49")
        parser.add_argument("--timeTo", help="Specific the query time to. E.g. 2023-01-16T12:49 ")
        #parser.add_argument("--statusQuery", help="Query the status of the execution - 'queryId'")
        #parser.add_argument("--cancelQuery", help="Cancel the query - 'queryId'")
        parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
        args = parser.parse_args()

        if args.query:
                retrieveTelemetry(args)
        #elif args.statusQuery:
        #       statusQuery()
        #elif args.cancelQuery:
        #       cancelQuery()
        else:
                print("Invalid argument.")
