# ModCord
A discord client created from the ground up.

This is the CLI-rewrite branch. This branch is a CLI version of ModCord, as the GUI is too hard!

### **DISCLAIMER**

This client is based heavily on discord.py and even takes some code from it (like types).
If you're Rapptz (or are of similar level) and want me to remove this code, 
please contact me via GitHub Issues or discord (user: duve3)

## READ THIS:
(technical jargon, tl;dr at the end)

Sometimes we can get resume working but sometimes we aren't able to. 
Resulting in old events not replaying.
If the normal client is open at the same time, we fail to `resume` resulting in instant disconnection from the API.


TL;DR:
You won't get previous events if at the same time you have the official discord client open

## THIS PROJECT DOES NOT WORK CURRENTLY!!!
### it is missing many core features when stuff goes wrong! (whoops)

This is a pure implementation of the Official discord client, no web tricks or anything. 
Every single API/Endpoint is done through the client in pure python.

The only unfortunate feature about this client is that many discord official features will not reach
this client until weeks maybe even months after their release.

This client requires hours of work and reverse engineering to figure out how the internals of discord work.

## Trust
We're committed to security and will never store anything private anywhere.
(we're open source for a reason!)

The most private information we store is a HASH of your token, not the token 
but a secure hash (SHA-256 hashed!). 
This is just to check if you logged in with the same token again!
(for the session resuming feature!)

## Development
**PLEASE** submit pull requests, issues, and anything you can do the support the development.

**PLEASE** help with the CLI, I will most likely even accept pull requests to just rewrite the entire thing, 
it is awful and is terrible from a design aspect.

Please suggest any ideas on the GitHub or the [Official Discord Server](https://discord.gg/R5e6Gc4SDp)

### **CURRENT WIP AND HAS MANY BUGS**
(check the bug tracker!)

(most of the future stuff after this point is for me to remember what to work on)
### Planned/TODO:
- Some form of CLI (currently deciding but [AsciiMatics](https://github.com/peterbrittain/asciimatics?tab=readme-ov-file) looks promising)
- Implementing the entire Message event (this will take a LONG time as it is a MASSIVE event)

I plan to make this client a "read-only" client first.
Once this client allows you to actually read everything, then I will work on actually interacting (sending messages, etc)