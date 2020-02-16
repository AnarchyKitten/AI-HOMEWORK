# artificial neural networks
###### COMP 131: Artificial Intelligence
###### Homework 5: Artificial Neural Networks
###### Tufts University

### Author(s): Brandon Bell and Yuchen Yang


### CODE DETAILS

  #### IMPLEMENTATION:

  We expect that our solution has been completely and correctly implemented. The code was written in Python 3.

  #### ARCHITECTURE:

  Our solution makes use of an Artificial Neural Network in order to classify plants according to values corresponding to the length and width of both their petals and sepals.

  According to standard procedure, our Neural Network trains on the dataset ANN -- Iris data.txt using forward propogation followed by backward propogation to generalize attributes for each type of plant so as to predict type on attribute input.

  We use various helper functions in addition to a Neural Network class complete with its own member functions to implement the solution.

  Our Neural Network randomly selects 100/150 data entries in order to train itself, and then tests the validity of the training process on the remaining 50 individuals. It prints the accuracy score of the prediction on both trainset and testset. And the average accuracy score reachs a 0.97.

  Helper functions include boolean return functions for each of the three types of plant, and a sigmoid function that serves as the activation function for this artificial neural net.

  We also make use of python libraries numpy and pandas for mathematical operations.

  #### USAGE:

  Put the ANN - Iris data.txt and ANN - Iris description.txt in the same folder with ANN.py. Run the .py file in any Python IDE.

  #### FUNCTION(S) IMPLEMENTED INCLUDE:

  Class Member Functions:

      train
      - trains the neural net with 100 individuals randomly selected
        from data set using forward propogation and backward propogation

      predict_one
      predict
      - uses training data to predict plant type based on length and width of
        petals and sepals

      predict_and_calculate_accuracy
      - uses training data to predict plant type and calculates accuracy



      encodersetosa(Class)
      - Returns true if input is Iris-setosa

      encoderversicolor(Class)
      - Returns true if input is Iris-veriscolor

      encodervirginica(Class)
      - Returns true if input is Iris-virginica

      sig(x)
        - Sigmoid activation function

      derisig(y)
        - Derivative of sigmoid function on input y

  #### METHODOLOGY:
  
    Our program is implemented according to the ANN guidelines
    in the homework specification found at https://canvas.tufts.edu/courses/9172/assignments/63634
