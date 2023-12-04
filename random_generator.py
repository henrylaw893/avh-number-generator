from random import randrange
from queue_adt import CircularQueue
#Get list of numbers to exclude

class RandomGenerator:

    #intialise all the variables
    def __init__(self, min, max, blacklist):
        """Initialise the random generator

        :min: minimum number to generate from (inclusive)
        :max: maximum number to generate up to (inclusive)
        :blacklist: python list containing all the numbers not to be drawn -- needs to be something with contains
        """
        self.number_list = []
        for number in range(min,max+1):
            if number not in blacklist:
                if number < 100:
                    number = "00" + str(number)
                elif number < 1000:
                    number = "0" + str(number)
                else:
                    number = str(number)
                self.number_list.append(number)
        
        #ADT needs to be able to index to get a value, and needs to have contains. thats all
    
    def generate_number(self) -> str:
        """
        array set method:
        generate a set from min to max numbers
        generate a set of blacklisted numbers
        difference set1 to set2
        generate an int from the range(len(set1))
        number = set1.array[int]
        """
        index = randrange(0,len(self.number_list),1)
        return self.number_list[index]

