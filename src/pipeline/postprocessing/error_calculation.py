import numpy

def rmse(prediction_vector, actual_vector):
        sum = 0
        for i in range(len(prediction_vector)):
            sum += pow((prediction_vector[i] - actual_vector[i]), 2)
        return numpy.sqrt(sum/len(prediction_vector))