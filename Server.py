from signalslot import Signal, Slot
import sys, os, struct
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
try:
    import clr
except:
    import clr
clr.AddReference('UDP-Communications')
import UDP_Communications
import System

class Packet(dict):
    def __init__(self, dotNetPaket):
        attrs = ['isAck', 'isCommand', 'isExecuteAck', 'isHint', 'isIDSearch', 'isInvalid', 'isReceiveAck', 'isServerMessage', 'isStatus', 'Command', 'Packetnumber', 'Outgoing', 'receiveID', 'SenderID', 'SenderType', 'receiveType', 'Timeout', 'Timestamp', 'Type']
        for a in attrs:
            setattr(self, a, getattr(dotNetPaket, a))

        for c in dotNetPaket.Content:
            self[c.Key] = c.Value

    def __str__(self):
        return "Packet, %s from %s,%s." % (self.Timestamp, self.SenderID, self.SenderType)

class UDP_Server(object):
    def __init__(self, ip, port, ttl, type_, id_):
        handler = UDP_Communications.UDP_Server.SenderHandler(self.__packet_received)
        self._server = UDP_Communications.UDP_Server(handler)
        # debug=True for more outputs in the Python command line.
        self._server.debug = True
        # Turn off local adapter filter; Let it switched off
        self._server.adapter_filter(False)
        self._server.init_udp(ip, port, ttl, System.Byte(type_), System.Byte(id_), True)

        if not self._server.udp_active():
            raise RuntimeError("Server is not running!")
        pass

    def send_command(self, command, **kwargs):
        data = ['command', str(command)]
        for k, v in kwargs.items():
            data.append(str(k))
            data.append(str(v))
        result = self._server.send_command(data)
        return result

    def send_data(self, **kwargs):
        data = []
        for k, v in kwargs.items():
            data.append(str(k))
            data.append(str(v))
        self._server.send_data(data)        

    def send_command_wait_for_reply(self, command, data=None, **kwargs):
        dataCmd = ['command', str(command)]
        if data is not None:
            for k, v in data.items():
                dataCmd.extend([k, v])
        for k, v in kwargs.items():
            dataCmd.append(str(k))
            dataCmd.append(str(v))
        method = self._server.send_command.Overloads[System.Array[System.String], System.String("").GetType().MakeByRefType()]
        res = method(dataCmd, "")
        return res[1]

    def start_stream(self, rxType, rxId):
        result = self._server.startStream(System.Byte(rxType), System.Byte(rxId))
        return result

    def stop_stream(self, rxType, rxId):
        self._server.stopStream(System.Byte(rxType), System.Byte(rxId))

    def stop(self):
        self._server.stop_udp()

    def send_stream(self, rxType, rxId, data):
        result = self._server.write(data.tobytes(), System.Byte(rxType), System.Byte(rxId))
        return result
    
    def stream_data_available(self, rxType, rxId):
        result = self._server.StreamDataAvailable(System.Byte(rxType), System.Byte(rxId))
        
        # Is any data available
        if result[0]:
            # Is it data from the desired stream?
            if result[1]!=rxType or result[2]!=rxId:
                return False
        
        # Return result
        return result[0]
    
    def get_stream_data(self, rxType, rxId):
        streamData = self._server.getStreamData(System.Byte(rxType), System.Byte(rxId))
        if streamData is None:
            return
        dataArray = []
        # NOTE: This is very inefficient; Has to be improved
        # The problem is conversion from System.Byte to e.g. numpy data type
        #for x in streamData:
        #    dataArray.append(x)
        # NOTE: For now we just convert the first 10 elements. However, everything is received.
        for x in range(9):
            dataArray.append(streamData[x])

        return dataArray

    def __packet_received(self, server, event):
        paket = event.Paket
        if paket is None:
            return
        res_packet = Packet(paket)
        self.packet_received.emit(packet=res_packet)

    packet_received = Signal(args=['packet'])
