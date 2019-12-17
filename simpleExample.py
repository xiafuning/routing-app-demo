import time

from Server import UDP_Server
from signalslot import Slot


def received(packet):
    print("\n=== Received packet ==============")
    print("Timestamp: ", packet.Timestamp)
    print("Command: ", packet.Command)
    print("Contents: ")
    print("  - " + "\n  - ".join(["%s=%s" % x for x in packet.items()]))

def main():
    S = UDP_Server(ip="224.5.6.7", port=50000, ttl=1, type_=2, id_=1)
    print("Server started..")

    # Connect to packet receive call back handle. The function 'received' is executed every time a packet is received.
    S.packet_received.connect(Slot(received))
    print("Receive-Handler established")

    # Send commands.
    S.send_command("set", commandValue1=5)
    time.sleep(1)
    S.send_command("info", commandValue2=8)
    time.sleep(1)
    
    # Send data
    S.send_data(myKey1="myValue1")                  # One key=value pair
    time.sleep(1)
    S.send_data(myKey1="myValue1", myKey2=2)        # Tow key=value pairs
    time.sleep(1)

if __name__ == '__main__':
    main()
