import paramiko, base64

DOWNLOADSPATH = "/opt/envivio/data/muse/downloads/"
TRACEPATH = DOWNLOADSPATH + "trace*"
SPLICEPATH = DOWNLOADSPATH + "splice*"
ATOLLPATH = DOWNLOADSPATH + "applicationAtoll*"
IPADDR = "localhost"
PORT = 22
USER = "yashi"
PASS =  "yashi"

print "Initializing LogParser.py"
print "Made by Yashi Sharma"
print "1/20/2016"
print "========================="
print ""
print ""

IPADDRIN = raw_input('What IP Address do you want to use? (Default is '+ IPADDR +') ')
PORTIN = raw_input('What port do you want to use? (Default is '+ str(PORT) +') ')
USERIN = raw_input('What username do you want to use? (Default is '+ USER +') ')
PASSIN =  raw_input('What password do you want to use? (Default is '+ PASS +') ')

if (len(IPADDRIN) > 0):
	IPADDR=IPADDRIN
if (len(PORTIN) > 0):
	PORT=PORTIN
if (len(USERIN) > 0):
	USER=USERIN
if (len(PASSIN) > 0):
	PASS=PASSIN

print "Using:"
print "\t "+USER+"@"+IPADDR+":"+str(PORT)
print "\t Tracelog Path: " + TRACEPATH
print "\t Splicelog Path: " + SPLICEPATH
print "\t Atoll Path: " + ATOLLPATH

TraceFile = open("traceOut.html", "w")
SpliceFile = open("spliceOut.html", "w")
AtollFile = open("atollOut.html", "w")


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

ssh = createSSHClient(IPADDR, PORT, USER, PASS)

print "Processing Trace Logs"
stdin, stdout, stderr = ssh.exec_command("cat "+TRACEPATH)
for line in stdout:
		AtollFile.write("<font color=\"red\">")
		AtollFile.write(line)
		AtollFile.write("<br></font>")
		AtollFile.write("\n")

print "Processing Splice Logs"
stdin, stdout, stderr = ssh.exec_command("cat "+SPLICEPATH)
for line in stdout:
		AtollFile.write("<font color=\"red\">")
		AtollFile.write(line)
		AtollFile.write("<br></font>")
		AtollFile.write("\n")

print "Processing Atoll Logs"
stdin, stdout, stderr = ssh.exec_command("cat "+ATOLLPATH)
for line in stdout:
		AtollFile.write("<font color=\"red\">")
		AtollFile.write(line)
		AtollFile.write("<br></font>")
		AtollFile.write("\n")

ssh.close()


print "Finished!"
