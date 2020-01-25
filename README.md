# Ground-Station
## Setup:
We're likely to be using the Teensy 4.0 board for the ground station. Setup the environment according to the instructions here:
https://www.pjrc.com/teensy/td_download.html

## Decode:
Decode data packets streaming wirelessly into the ground station.

Data packets are of format **(NNxxxxx)**.

NN is the integer ID of the sensor. Guaranteed to be 2 characters. For example, sensor ID 1 will be 0 padded to 01.

xxxxx is the sensor reading, in arbitary units mapped to the sensor ID. Guaranteed to be 2 characters. For example, a reading of 1 will be 0 padded to 00001.

'(' and ')' are determined packet start and termination packets.

## TO-DO: Command send from ground station.
## TO-DO: Read switch states.
## TO-DO: Send data to computer.
