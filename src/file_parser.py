# system imports
import re
import gzip
# third party imports
import numpy
# application imports
import custom_logger as Log

class FileParser(object):

    # imports a timeseries from csv to a 1-dimensional numpy array with the timeseries values
    def arff_to_numpy(self, filename):
        fin = open(filename, "r")
        data = []
        number_of_classes = 0
        dimension = 0
        class_values = []

        # get the different section of ARFF-File
        for line in fin:
            sline = line.strip().lower()
            sline = sline.strip(',')
            if sline.startswith("%") or len(sline) == 0:
                continue

            if sline.startswith("@data"):
                break

            if sline.startswith("@attribute"):
                value = sline.split()
                if value[1].startswith("class"):
                    number_of_classes += 1
                else:
                    dimension += 1
                    data.append([])

        # read in the data stored in the ARFF file
        for line in fin:
            sline = line.strip()
            sline = sline.strip(',')
            if sline.startswith("%") or len(sline) == 0:
                continue

            values = sline.split(",")
            for i in xrange(number_of_classes):
                class_values.append(float(values[-i]))
            values = values[:-number_of_classes]
            for i in xrange(len(data)):
                data[i].append(float(values[i]))

        tmp_array = numpy.ndarray(shape=(len(class_values), dimension))
        for i in xrange(dimension):
            for j in xrange(len(class_values)):
                tmp_array[j][i] = data[i][j]

        # cleaning up and return
        fin.close()
        return(tmp_array, class_values)
