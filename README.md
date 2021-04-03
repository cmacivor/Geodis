# Geodis


MessageType	Communication	Port No#
CRTIN	GEODIS --> PENDANT	31000   #this is handled by the TCP_SortMessage_Server.py, serves as a server and writes CTRIN and KEEPALIVE mess. Use Test_SortMessage_Client
CRTIN_ACK	PENDANT --> GEODIS	31001 #this is handled by the TCP_SortMessage_Client.py, serves as a client. The WMS is the server use Test_SortMessage_Server
DVTCF	PENDANT --> GEODIS	32000 TCP_DivertConfirmation_Client.py. Here the WMS is a server, so TCP_DivertConfirmation_Client is a client. use Test_DivertConfirm_Server
DVTCF_ACK	GEODIS --> PENDANT	32001 TCP_DivertConfirmation_Server -receives the ACK messages. Add a column to the table for CorrelationId, update table as Ack with that use    
     Test_DivertConfirm_Client


10/26/2020 evening TODO:


2. In the TCP_DivertConfirmation_Client.py, implement the most recent record KeepAlive message logic like in TCP_SortMessage_Client.py





