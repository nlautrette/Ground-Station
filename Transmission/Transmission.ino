void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}

int createTransmissionMatrix(int numVariables) {
  int numRows = numVariables
  int rowCounter = numVariables - 1
  while (rowCounter > 0) {
    numRows += rowCounter;
    rowCounter--;
  }
  int transmissionMatrix[numRows][numVariables];
  for (int i = 0; i < numRows; i++) {
    for (int j = 0; j < numVariables; j++) {
      if (i < numVariables) {
        // The first i rows that are smaller than the numVariables are
        // your identity rows
        if (i == j) {
          transmissionMatrix[i][j] = 1;
        } else {
          transmissionMatrix[i][j] = 0;
        }
      }
    }
  }
}
