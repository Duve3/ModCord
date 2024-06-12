# ModCord
A discord client created from the ground up.

## THIS PROJECT IS CURRENTLY ONLY THE MINIMAL VIABLE PRODUCT, MISSING HUNDREDS QOL AND DESIGN FEATURES!
### it's also missing many core features when stuff goes wrong! (whoops)

This is a pure implementation of the Official discord client, no web tricks or anything. 
Every single API/Endpoint is done through the client in pure python.

The only unfortunate feature about this client is that many discord official features will not reach
this client until weeks maybe even months after their release.

This client requires hours of work and reverse engineering to figure out how the internals of discord work.

## Development
**PLEASE** submit pull requests, issues, and anything you can do the support the development.

**PLEASE** help with the UI, I will most likely even accept pull requests to just rewrite the entire thing, 
it is awful and is terrible from a design aspect.

Please suggest any ideas on the GitHub or the [Official Discord Server](https://discord.gg/Fr8z9JnVpP)

### **CURRENT WIP AND HAS MANY BUGS**

TODO:
1. rewrite so that rendering is done in the main loop while everything has its own thread
   (this is due to a PYGAME limitation, not ours)
2. create login
3. create an interface that can switch channels and read from them
   1. add sending messages later