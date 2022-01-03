# Networking Instructions

Open Source Car Watchman (OSCW) requires networking features for sending data to a self-hosted server.
This data at the moment includes: 
- Messages about events near your car for push notification purposes

Plan to include in the future:
- Snippets of footage sent to the server to be relayed to phone app 

The server is self-hosted and can be hosted anywhere as long as a static IP and port forwarding is available.

An active internet connection is required for the network features to work. The server software will automatically
determine the external and internal IP of the device it is running on and will expect data on a specific port which 
is defined in **NetworkManager.py**

```
COMM_PORT = 52345  
```

Feel free to use the value already defined or change it to a different port number. Please make sure that appropriate
port forwarding is set up in your router's settings for this to work. 

The processor unit in the car and the mobile app will require the IP of your server and the port number that your server
is receiving data on. 

TODO: 
- Make mobile app :)
- Add this stuff to a settings page in the GUI frontend at some point.

