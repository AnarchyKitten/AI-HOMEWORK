import numpy as np
import pandas as pd

#Returns true if input is Iris-setosa
def encodersetosa(Class):
    if Class == "Iris-setosa":
        return 1
    else:
        return 0

#Returns true if input is Iris-veriscolor
def encoderversicolor(Class):
    if Class == "Iris-versicolor":
        return 1
    else:
        return 0

#Returns true if input is Iris-virginica
def encodervirginica(Class):
    if Class == "Iris-virginica":
        return 1
    else:
        return 0

#sigmoid function on input x
def sig(x):
    return (1 / (1 + np.exp(-x)))

#derivative of sigmoid function on input y
def derisig(y):
    return y * (1 - y)

#declare class NeuralNetwork
class NerualNetwork:
    Input_Size = 0
    Hidden_Size = 0
    Output_Size = 0
    w0 = None
    w1 = None
    b0 = None
    b1 = None
    lr = None

    #init function
    def __init__(self, input_layer_size, hidden_layer_size, output_layer_size, learning_rate):
        self.Input_Size = input_layer_size
        self.Hidden_Size = hidden_layer_size
        self.Output_Size = output_layer_size
        self.w0 = 2 * np.random.random((input_layer_size, hidden_layer_size)) - 1
        self.w1 = 2 * np.random.random((hidden_layer_size, output_layer_size)) - 1
        self.b0 = 1
        self.b1 = 1
        self.lr = learning_rate
        pass

    #member function train takes inputs self, X, Y, iter_turns
    def train(self, X, y, iter_turns):
        for iter in range(iter_turns):
            for i in range(len(X)):

                # forward propagation
                self.l0 = X[i]
                y_one = y[i]
                self.l1 = sig(np.dot(self.l0, self.w0) + self.b0)
                self.l2 = sig(np.dot(self.l1, self.w1) + self.b1)
                Delta2 = derisig(self.l2) * (y_one - self.l2)

                # backword propagation
                Delta1 = derisig(self.l1) * np.dot(self.w1, Delta2)
                self.w1 += np.dot(self.l1.reshape(self.Hidden_Size, 1), Delta2.reshape(1, self.Output_Size)) * self.lr
                self.b1 += Delta2 * 1 * self.lr
                self.w0 += np.dot(self.l0.reshape(self.Input_Size, 1), Delta1.reshape(1, self.Hidden_Size)) * self.lr
                self.b0 += Delta1 * 1 * self.lr

    #predict function takes inputs self and X
    def predict(self, X):
        l0 = X
        l1 = sig(np.dot(l0, self.w0) + self.b0)
        l2 = sig(np.dot(l1, self.w1) + self.b1)
        Result = l2.tolist()
        result = []
        for i in Result:
            if (i[0] >= i[1]) & (i[0] >= i[2]):
                result.append([1, 0, 0])
            elif (i[1] >= i[0]) & (i[1] >= i[2]):
                result.append([0, 1, 0])
            elif (i[2] >= i[0]) & (i[2] >= i[1]):
                result.append([0, 0, 1])
        return np.array(result)

    #predict_and_calculate_accuracy takes inputs self, X and y
    def predict_and_calculate_accuracy(self, X, y):
        result = self.predict(X).tolist()
        count = 0
        for i in range(len(result)):
            if result[i] != y.tolist()[i]:
                count += 1
        return 1 - (count / len(result))

    #predict_one takes inputs self and X, for use on single inputs
    def predict_one(self, X):
        result = ""
        l0 = [X]
        l1 = sig(np.dot(l0, self.w0) + self.b0)
        l2 = sig(np.dot(l1, self.w1) + self.b1)
        Result = l2.tolist()
        for i in Result:
            if (i[0] >= i[1]) & (i[0] >= i[2]):
                result = "Iris-setosa"
            elif (i[1] >= i[0]) & (i[1] >= i[2]):
                result = "Iris-versicolor"
            elif (i[2] >= i[0]) & (i[2] >= i[1]):
                result = "Iris-virginica"
        return result

    #outputs value of Nerual Network
    def output(self):
        return self.w0, self.w1, self.b0, self.b1

#main function
if __name__ == "__main__":
    #read data from input file
    df = pd.read_csv("ANN - Iris data.txt", header=None)
    df = df.rename(columns={0: "Sepal-Length", 1: "Sepal-Width", 2: "Petal-Length", 3: "Petal-Width", 4: "Class"})

    #pass data from fie to encoder functiosn to determine plant type
    df["Iris-setosa"] = df["Class"].apply(encodersetosa)
    df["Iris-versicolor"] = df["Class"].apply(encoderversicolor)
    df["Iris-virginica"] = df["Class"].apply(encodervirginica)


    #strings results of encoder function together to result in a unique code for each plant type
    # 1 0 0 = Iris-setosa, 0 1 0 = Iris-veriscolor, 0 0 1 = Iris-virginica
    full_list = df.drop(["Class"], axis=1).values

    np.random.shuffle(full_list)
    train_list=full_list[:100]
    test_list=full_list[100:]
    X_train = train_list[:, :4]
    y_train = train_list[:, 4:]
    X_test = test_list[:, :4]
    y_test = test_list[:, 4:]


    #Initialize Neural Network with the following properties
    nn = NerualNetwork(input_layer_size=4, hidden_layer_size=6, output_layer_size=3, learning_rate=0.1)

    #Train NN with data from dataset
    nn.train(X_train, y_train, 1000)

    #Print accuracy
    print("Accuracy on trainset is : " + str(nn.predict_and_calculate_accuracy(X_train, y_train)))
    print("Accuracy on test is : " + str(nn.predict_and_calculate_accuracy(X_test, y_test)))

    #Arr with data to be passed to predict function
    predict_data=[4.8, 3.4, 1.6, 0.2]
    print("If an iris flower have X = {} , It is an {}".format(str(predict_data),nn.predict_one(predict_data)))
