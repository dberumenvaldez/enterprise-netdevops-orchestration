import socket
import pymssql
import os
from dotenv import load_dotenv

load_dotenv()

conn = pymssql.connect(server='10.10.20.100', 
                       user='sa', 
                       password=os.getenv("DB_PASSWORD"), 
                       database='NetworkTelemetry', 
                       autocommit=True)
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

    # Classify 
    if "%OSPF-5-ADJCHG" in message:
        category = "OSPF_ROUTING"
    elif "%PM-4-ERR_DISABLE" in message or "PORT_SECURITY" in message or "%SECURITY-2-PORTSWIPE" in message:
        category = "PORT_SECURITY"
    elif "%HSRP-5-STATECHANGE" in message:
        category = "HSRP_REDUNDANCY"
    elif "%TRACK-6-STATE" in message:
        category = "OBJECT_TRACKING"
    elif "DHCP_SNOOPING" in message or "DAI" in message or "%IP-4-DUPADDR" in message:
        category = "LAYER2_SECURITY"
    elif "%LINK-3-UPDOWN" in message or "%LINEPROTO-5-UPDOWN" in message:
        category = "INTERFACE_STATE"
    else:
        category = "GENERAL"

    # Print on console and save on Sql 
    print(f"Log from {addr[0]}: {message}")

    try:
        query = """INSERT INTO SyslogEvents (SourceIP, Severity, MessageText, EventCategory)
                    VALUES (%s, %s, %s, %s)"""
        cursor.execute(query,(addr[0], 'INFO', message,category))
    except Exception as e:
        print(f"[ERROR SQL] {e}")
    
