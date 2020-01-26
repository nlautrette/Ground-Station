# Ground-Station
## Setup:
We're using the Teensy 4.0 board. Setup the environment according to the instructions here:
https://www.pjrc.com/teensy/td_download.html

### Windows users:
1. Make sure git is installed with symlink support

During the install of git on Windows, enable symbolic links:

<img src="https://i.stack.imgur.com/rQF1w.png" width="300"/>

2. Tell Bash to create hardlinks instead of symlinks

Edit: `(git folder)/etc/bash.bashrc` and add to bottom: `MSYS=winsymlinks:nativestrict`

3. Set git config to use symlinks
```bash
git config core.symlinks true
```
or

```bash
git clone -c core.symlinks=true <URL>
```
NOTE: I have tried adding this to the global git config and at the moment it is not working for me so I recommend adding this to each repo...

4. Pull the repo

NOTE: Unless you have enabled developer mode in the latest version of Windows 10, you need to run bash as **administrator** to create symlinks.

5. Reset all Symlinks (optional) If you have an existing repo, or are using submodules you may find that the symlinks are not being created correctly so to refresh all the symlinks in the repo you can run these commands.

```bash
find -type l -delete
git reset --hard
```
NOTE: This will reset any changes since last commit so make sure you have committed first.

## Decode:
Decode data packets streaming wirelessly into the ground station.

Data packets are of format **(NNxxxxx)**.

NN is the integer ID of the sensor. Guaranteed to be 2 characters. For example, sensor ID 1 will be 0 padded to 01.

xxxxx is the sensor reading, in arbitary units mapped to the sensor ID. Guaranteed to be 2 characters. For example, a reading of 1 will be 0 padded to 00001.

'(' and ')' are determined packet start and termination packets.

## TO-DO: Command send from ground station.
## TO-DO: Read switch states.
## TO-DO: Send data to computer.
