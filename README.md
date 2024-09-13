# ModCord
A discord client created from the ground up.

This is the CLI-rewrite branch. This branch is a CLI version of ModCord, as the GUI is too challenging!

## READ THIS:
(technical jargon, tl;dr at the end)

Due to how discord works with the `resume` OP code, I can't find a way to call it if someone has previously used
the official client.
(How would we know the last sequence value??? or last session!) This is a bold assumption and untested
in the future I will see if there is any possible way around it or if it will accept outdated values.
Without this
method, we can't get a replay of many previous events. 

Based on research conducted by me I was unable to get the resume method working.

^ we are currently testing the `resume` method and seeing if we can get to replay without proper values.

TL;DR:
You won't get previous notifications if you close ModCord, go to the official client, then reopen ModCord

## THIS PROJECT IS CURRENTLY ONLY THE MINIMAL VIABLE PRODUCT, MISSING HUNDREDS QOL AND DESIGN FEATURES!
### it's also missing many core features when stuff goes wrong! (whoops)

This is a pure implementation of the Official discord client, no web tricks or anything. 
Every single API/Endpoint is done through the client in pure python.

The only unfortunate feature about this client is that many discord official features will not reach
this client until weeks maybe even months after their release.

This client requires hours of work and reverse engineering to figure out how the internals of discord work.

## Development
**PLEASE** submit pull requests, issues, and anything you can do the support the development.

**PLEASE** help with the CLI, I will most likely even accept pull requests to just rewrite the entire thing, 
it is awful and is terrible from a design aspect.

Please suggest any ideas on the GitHub or the ~~Official Discord Server~~ (no longer exists)

### **CURRENT WIP AND HAS MANY BUGS**
(check the bug tracker!)