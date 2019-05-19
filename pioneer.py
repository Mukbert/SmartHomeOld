import telnetlib

host = "192.168.1.25"
port = 8102
timeout = 100

def talk(cmd):
	session = telnetlib.Telnet(host, port, timeout)
	session.write(cmd + "\n").encode('ascii')
	answ = session.read_until("\r\n")
	session.close()
	return answ