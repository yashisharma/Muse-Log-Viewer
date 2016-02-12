import paramiko, base64, webbrowser

DOWNLOADSPATH = "/opt/envivio/data/muse/downloads/"
TRACEPATH = DOWNLOADSPATH + "trace*"
SPLICEPATH = DOWNLOADSPATH + "splice*"
ATOLLPATH = DOWNLOADSPATH + "applicationAtoll*"
IPADDR = "localhost"
PORT = 22
USER = "root"
PASS =  "yashi"

infoCount = 0
warningCount = 0
errorCount = 0
outCount = 0
inCount = 0
timeSignalCount = 0
requestCount = 0
responseCount = 0
createCount = 0
deleteCount = 0

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


print "Initializing LogParser.py"
print "Made by Yashi Sharma"
print "1/20/2016"
print "========================="
print ""
print ""

IPADDRIN = raw_input('What IP Address do you want to use? (Default is '+ IPADDR +') ')
USERIN = raw_input('What username do you want to use? (Default is '+ USER +') ')
PASSIN =  raw_input('What password do you want to use? (Default is '+ PASS +') ')

if (len(IPADDRIN) > 0):
	IPADDR=IPADDRIN
if (len(USERIN) > 0):
	USER=USERIN
if (len(PASSIN) > 0):
	PASS=PASSIN

print "Using:"
print "\t "+USER+"@"+IPADDR+":"+str(PORT)
print "\t Tracelog Path: " + TRACEPATH
print "\t Splicelog Path: " + SPLICEPATH
print "\t Atoll Path: " + ATOLLPATH

#TraceFile = open("traceOut.html", "w")
SpliceFile = open("spliceOut.html", "w")
#AtollFile = open("atollOut.html", "w")


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

ssh = createSSHClient(IPADDR, PORT, USER, PASS)

#print "Processing Trace Logs"
#tdin, stdout, stderr = ssh.exec_command("cat "+TRACEPATH)
#for line in stdout:
#	color = "black"
#	if "INFO" in line or "info" in line or "Info" in line:
#		color = "black"
#		infoCount += 1
#	if "WARNING" in line or "warning" in line or "Warning" in line:
#		color = "orange"
#		warningCount += 1
#	if "ERROR" in line or "error" in line or "Error" in line:
#		color = "red"
#		errorCount += 1
#
#	TraceFile.write("<font color=\""+color+"\">")
#	TraceFile.write(line)
#	TraceFile.write("<br></font><br>")
#	TraceFile.write("\n")
#
#print "\t Information Events: " + str(infoCount)
#print "\t Warning Events: " + str(warningCount)
#print "\t Envivio Events: " + str(errorCount)
#
#infoCount = 0
#warningCount = 0
#errorCount = 0

print "Processing Splice Logs"
stdin, stdout, stderr = ssh.exec_command("cat "+SPLICEPATH)

for line in stdout:
	color = "brown"
	if "esam.signal.splice" in line:
		if "type=out" in line:
			color = "LawnGreen"
			outCount += 1
		if "type=in" in line:
			color = "salmon"
			inCount += 1
		if "type=time_signal" in line:
			color = "blue"
			timeSignalCount += 1
	if "esam.signal.request" in line:
		color = "black"
		requestCount += 1
	if "esam.signal.response" in line:
		color = "Fuchsia"
		responseCount += 1
	if "esam.signal.notif.create" in line:
		if "type=out" in line:
			color = "green"
			outCount += 1
		if "type=in" in line:
			color = "Green"
			inCount += 1
		if "type=time_signal" in line:
			color = "Black"
			timeSignalCount += 1
	if "esam.signal.notif.delete" in line:
		color = "red"
		deleteCount += 1 

	SpliceFile.write("<font color=\""+color+"\">")
	
	#SpliceFile.write(html_escape(line))

	for element in line.split():
		for subelement in element.split():
			if not "<" in subelement[:1]:
				if not "acq_signal" in subelement:
					if not "_pts" in subelement:
						if not "data=" in subelement:
							if not "url=" in subelement:
								if not "version=" in subelement:
									if not "encoding=" in subelement:
										if not "xmlns" in subelement:
											if not "acquisition" in subelement:
												if not "signalType" in subelement:
													if not "timeType" in subelement:
														if not "timeValue" in subelement:
															if not "standalone=" in subelement:
																if not "len" in subelement:
																	if not "elapsed_time=" in subelement:
																		if not "signal_point_id=" in subelement:
																			if not "zoneIdentity=" in subelement:
																				SpliceFile.write(html_escape(subelement.strip("/>").strip(">")))
																				SpliceFile.write("<br>")

	SpliceFile.write("<br></font><br>")
	SpliceFile.write("\n")

print "\t OUT messages: " + str(outCount)
print "\t IN messages: " + str(inCount)
print "\t TIME_SIGNAL messages: " + str(timeSignalCount)
print "\t REQUEST messages: " + str(requestCount)
print "\t RESPONSE messages: " + str(responseCount)
print "\t CREATE messages: " + str(createCount)
print "\t DELETE messages: " + str(deleteCount)

outCount = 0
inCount = 0
timeSignalCount = 0
requestCount = 0
responseCount = 0
createCount = 0
deleteCount = 0
SpliceFile.write("</body>")
SpliceFile.write("</html>")

#print "Processing Atoll Logs"
#stdin, stdout, stderr = ssh.exec_command("cat "+ATOLLPATH)
#for line in stdout:
#	color = "black"
#	if "INFO" in line or "info" in line or "Info" in line:
#		color = "black"
#		infoCount += 1
#	if "WARNING" in line or "warning" in line or "Warning" in line:
#		color = "orange"
#		warningCount += 1
#	if "ERROR" in line or "error" in line or "Error" in line:
#		color = "red"
#		errorCount += 1
#	AtollFile.write("<font color=\""+color+"\">")
#	AtollFile.write(line)
#	AtollFile.write("<br></font><br>")
#	AtollFile.write("\n")
#
#print "\t Information Events: " + str(infoCount)
#print "\t Warning Events: " + str(warningCount)
#print "\t Envivio Events: " + str(errorCount)
#
#infoCount = 0
#warningCount = 0
#errorCount = 0

#TraceFile.close()
SpliceFile.close()
#AtollFile.close()
ssh.close()

webbrowser.open(SpliceFile.name)

raw_input('Finished! Press enter to exit.')
