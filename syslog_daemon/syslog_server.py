import socket
import pymssql

conn = pymssql.connect(server='10.10.20.100', user='sa', password='NetDevOps_2026!', database='NetworkTelemetry', autocommit=True)
cursor = conn.cursor()


UDP_IP = "0.0.0.0"
UDP_PORT = 514

#Init socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

print(f"[*] Daemons Syslog active adn SQL connected. Listening ...")

while True:
    data, addr = sock.recvfrom(2048)
    message = data.decode('utf-8',errors='ignore').strip()

    # Print on console and save on Sql 
    print(f"Log from {addr[0]}: {message}")

    try:
        cursor.execute("""
            INSERT INTO SyslogEvents (SourceIP, Severity, MessageText)
            VALUES (%s, %s, %s)
        """,(addr[0], 'INFO', message))
    except Exception as e:
        print(f"[ERROR SQL] {e}")
    
