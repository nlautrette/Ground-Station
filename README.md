# Packet-Decode
Decode data packets streaming wirelessly into the ground station.

Data packets are of format (NNxxxxx).

NN is the integer ID of the sensor. Guaranteed to be 2 characters. For example, sensor ID 1 will be 0 padded to 01.

xxxxx is the sensor reading, in arbitary units mapped to the sensor ID. Guaranteed to be 2 characters. For example, a reading of 1 will be 0 padded to 00001.

'(' and ')' are set packet start and termination packets.
