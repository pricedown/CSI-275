# Final CSI-275

### The Server
Execute this to start the server:
```commandline
python server.py
```
It will open the server on ports 5000 (sending clients) and 5001 (receiving clients)

#### Logs
- Joining chatters
- Leaving chatters 
- All messages sent between chatters
### The Client
Execute this to start the client:
```commandline
python client.py
```
This will first prompt you for a username, 
and then attempt to connect to the server.

You can run this in parallel terminals for connecting more clients. 

Note that if you give a client the same name as another, the previous client 
will no longer be able to receive messages.

#### Inputs
- Exit: Type !exit to disconnect and exit
- Private messages: Begin messages with @[username]
- Broadcast: Type normally

#### Outputs
* Global messages
* Private messages to you

