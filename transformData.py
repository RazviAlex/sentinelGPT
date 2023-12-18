from loadGPT import exportS1Data
import json, sys, signal, argparse, os, re

#data flow: "AgentName IS NOT EMPTY"
#1. send the query in the timeframe wanted /web/api/v2.1/dv/init-query -> retireve queryId
#2. request the events /web/api/v2.1/dv/events or filter direct by a event_type /web/api/v2.1/dv/events/{event_type}
#4. normalize the fields
#5. call chatgpt api
#6. print/save the result

#global var
normalized_data = []
current_directory = os.getcwd()
absolute_path = os.path.join(current_directory, 'outputS1.txt')

def def_handler(sig, frame):
	log.failure("Exiting..")
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


def comandScript(item, output_file):
	if "eventType" in item and "endpointName" in item and "eventTime" in item and \
	 "srcProcParentName" in item  and "srcProcName" in item and "indicatorName" in item and "indicatorMetadata" in item:
	 	output_file.write(f"\nEventType: Command script -> endpoint: en{item['endpointName']} -> Time: {item['eventTime']} -> SourceProcess: {item['srcProcName']} -> Command Script: {item['srcProcCmdScript']}")


def behavioralIndicator(item, output_file):
	if "eventType" in item and "endpointName" in item and "eventTime" in item and \
	 "srcProcParentName" in item  and "srcProcName" in item and "indicatorName" in item and "indicatorMetadata" in item:
	 	output_file.write(f"\nEventType: Behavioral Indicators -> endpoint: en{item['endpointName']} -> Time: {item['eventTime']} -> SourceParentProcess: {item['srcProcParentName']} -> SourceProcess: {item['srcProcName']} -> indicatorName: {item['indicatorName']} -> indicatorMetadata: {item['indicatorMetadata']}")


def crossProcess(item, output_file):
	if "eventType" in item and "endpointName" in item and "eventTime" in item and \
	 "srcProcParentName" in item  and "srcProcName" in item and "tgtProcName" in item and "tgtProcCmdLine" in item and\
	 "tgtProcRelation" in item:
	 	output_file.write(f"\nEventType: Cross Process -> endpoint: en{item['endpointName']} -> Time: {item['eventTime']} -> SourceParentProcess: {item['srcProcParentName']} -> SourceProcess: {item['srcProcName']} -> TargetProcess: {item['tgtProcName']} -> TargetProcCmdLine: {item['tgtProcCmdLine']} -> TargetProcRelation: {item['tgtProcRelation']}")


def login(item, output_file):
	if "eventType" in item and "endpointName" in item and "eventTime" in item and \
	 "srcProcParentName" in item  and "srcProcName" in item and "loginsUserName" in item and "srcMachineIp" in item and\
	 "loginFailureReason" in item  and "loginIsSuccessful" in item:
	 	output_file.write(f"\nEventType: Login-> endpoint: en{item['endpointName']} -> Time: {item['eventTime']} -> SourceParentProcess: {item['srcProcParentName']} -> SourceProcess: {item['srcProcName']} -> LoginUser: {item['loginsUserName']} -> SourceIP: {item['srcMachineIp']} -> LoginFailReason: {item['loginFailureReason']} -> SuccessfulLogin: {item['loginIsSuccessful']}")

def ipConnection(item, output_file):
	if "eventType" in item and "endpointName" in item and "eventTime" in item and \
	 "srcProcParentName" in item  and "srcProcName" in item and "srcIp" in item and "srcPort" in item and\
	 "dstIp" in item  and "dstPort" in item and "netEventDirection" in item and "netConnStatus" in item:
	 	output_file.write(f"\nEventType: IP Connect -> endpoint: en{item['endpointName']} -> Time: {item['eventTime']} -> SourceParentProcess: {item['srcProcParentName']} -> SourceProcess: {item['srcProcName']} -> SourceIP: {item['srcIp']} -> SourcePort: {item['srcPort']} -> DestinationIP: {item['dstIp']} -> DesintationPort: {item['dstPort']} -> networkEventDirection: {item['netEventDirection']} -> networkConnectionStatus: {item['netConnStatus']}")


def processCreation(item, output_file):
	if "eventType" in item and "endpointName" in item and "eventTime" in item and \
	 "srcProcParentName" in item  and "srcProcName" in item and "tgtProcName" in item and "srcProcCmdLine" in item:
 		output_file.write(f"\nEventType: Process Creation -> endpoint: en{item['endpointName']} -> Time: {item['eventTime']} -> SourceParentProcess: {item['srcProcParentName']} -> SourceProcess: {item['srcProcName']} -> TargetProcess: {item['tgtProcName']} -> SourceProcessCommandline: {item['srcProcCmdLine']}")


def normalizeData(events, args):
	pattern = r'(USERS\\+)[^\\]*'
	replacement = r'\1xx'
	with open(absolute_path, 'w') as output_file:

		# Normalizar datos
		for item in events["data"]:
			# Replace data & limit the length from sensitive fields.
			if "eventTime" in item:
				item["eventTime"] = item["eventTime"][:-8]				
			if "fileFullName" in item and item["fileFullName"] is not None:
				item["fileFullName"] = item["fileFullName"].split("\\")[-1]
			if "tgtFilePath" in item and item["tgtFilePath"] is not None:
				item["tgtFilePath"] = item["tgtFilePath"].split("\\")[-1]
			if "endpointName" in item and item["endpointName"] is not None:
				item["endpointName"] = item["endpointName"][-4:]
			if "agentName" in item and item["agentName"] is not None:
				item["agentName"] = item["agentName"][-4:]
			if "srcProcParentUser" in item and item["srcProcParentUser"] is not None:
				item["srcProcParentUser"] = item["srcProcParentUser"][-4:]
			if "srcProcUser" in item and item["srcProcUser"] is not None:
				item["srcProcUser"] = item["srcProcUser"][-4:]
			if "user" in item and item["user"] is not None:
				item["user"] = item["user"][-4:]
			if "agentIp" in item and item["agentIp"] is not None:
				item["agentIp"] = item["agentIp"][-8:]			
			if "srcProcCmdLine" in item and item["srcProcCmdLine"] is not None:
				if len(item["srcProcCmdLine"]) > 100:
					item["srcProcCmdLine"] = item["srcProcCmdLine"][:100]				
					str(item["srcProcCmdLine"]).lower()
					item["srcProcCmdLine"] = str(item["srcProcCmdLine"]).replace("sensitiveData", "xx").replace("program", ".").replace("file", ".").replace("mozilla", ".").replace("microsoft", ".").replace("system32", ".").replace("windows", ".").replace("\"", "'")
					item["srcProcCmdLine"] = re.sub(pattern, replacement, item["srcProcCmdLine"], flags=re.IGNORECASE)
			if "tgtProcCmdLine" in item and item["tgtProcCmdLine"] is not None:
				if len(item["tgtProcCmdLine"]) > 100:
					item["tgtProcCmdLine"] = item["tgtProcCmdLine"][:100]
					str(item["tgtProcCmdLine"]).lower()
					item["tgtProcCmdLine"] = str(item["tgtProcCmdLine"]).replace("sensitiveData", "xx").replace("program", ".").replace("file", ".").replace("mozilla", ".").replace("microsoft", ".").replace("system32", ".").replace("windows", ".").replace("\"", "'")
					item["tgtProcCmdLine"] = re.sub(pattern, replacement, item["tgtProcCmdLine"], flags=re.IGNORECASE)
			if "indicatorMetadata" in item and item["indicatorMetadata"] is not None:
				if len(item["indicatorMetadata"]) > 100:
					item["indicatorMetadata"] = item["indicatorMetadata"][:100]
					item["indicatorMetadata"] = str(item["indicatorMetadata"]).replace("sensitiveData", "xx").replace("program", ".").replace("file", ".").replace("mozilla", ".").replace("microsoft", ".").replace("system32", ".").replace("windows", ".").replace("\"", "'")
					item["indicatorMetadata"] = re.sub(pattern, replacement, item["indicatorMetadata"], flags=re.IGNORECASE)
			if "srcProcCmdScript" in item and item["srcProcCmdScript"] is not None:
				if len(item["srcProcCmdScript"]) > 100:
					item["srcProcCmdScript"] = item["srcProcCmdScript"][:100]
					item["srcProcCmdScript"] = str(item["srcProcCmdScript"]).replace("sensitiveData", "xx").replace("program", ".").replace("file", ".").replace("mozilla", ".").replace("microsoft", ".").replace("system32", ".").replace("windows", ".").replace("\"", "'")
					item["srcProcCmdScript"] = re.sub(pattern, replacement, item["srcProcCmdScript"], flags=re.IGNORECASE)					

			#Append the data to the new dic, so if there is multiple differentevents, append all of them
			normalized_data.append(item)

			#For each event type change the structure of the fields like: key - value, must be "key : value ->"
			if item["eventType"] == "Process Creation":
				processCreation(item, output_file)
			elif item["eventType"] == "IP Connect":
				ipConnection(item, output_file)
			elif item["eventType"] == "Login":
				login(item, output_file)
			elif item["objectType"] == "cross_process":
				crossProcess(item, output_file)			
			elif item["eventType"] == "Behavioral Indicators":
				behavioralIndicator(item, output_file)		
			elif item["eventType"] == "Command Script":
				comandScript(item, output_file)				

	exportS1Data(args)