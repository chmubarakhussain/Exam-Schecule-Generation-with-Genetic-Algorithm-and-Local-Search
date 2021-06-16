import numpy as np
import cv2
import random
import copy
import math

#global variables
TOTAL_COURSES = 0
TOTAL_STUDENTS = 0
TOTAL_REGS = 0
TOTAL_ROOMS = 0
TOTAL_DAYS = 0
TOTAL_SLOTS = 0
TOTAL_BITS_OF_CHROMOSOME = 0
TOTAL_BITS_OF_DAY = 0
TOTAL_BITS_OF_SLOT = 0
TOTAL_BITS_OF_ROOM = 0
POP_SIZE = 100
TOTAL_ROOM_CAPACITY = 0


def readDataFiles(reg, rooms, days):
    global TOTAL_COURSES
    global TOTAL_STUDENTS
    global TOTAL_REGS
    global TOTAL_ROOMS
    global TOTAL_DAYS
    global TOTAL_SLOTS

    fReg = open(reg, "r")
    fRoom = open(rooms, "r")
    fDays = open(days, "r")

    #reading registration data in 2D array
    theInts = []
    for val in fReg.read().split():
        theInts.append(int(val))
    
    TOTAL_COURSES = theInts[0]
    TOTAL_STUDENTS = theInts[1]
    iteratorForTheInts = 2
    regData2D = [[0 for x in range(TOTAL_STUDENTS)] for y in range(TOTAL_COURSES)]
    refinedRegData2D = []
    

    i = 0
    j = 0
    TOTAL_REGS = len(theInts) - 2
    maxSizeOfTheInts = TOTAL_REGS + 2
    while iteratorForTheInts < maxSizeOfTheInts:
        i = (int)((iteratorForTheInts-2)/TOTAL_STUDENTS)
        j = (iteratorForTheInts-2)%TOTAL_STUDENTS
        regData2D[i][j] = theInts[iteratorForTheInts]
        iteratorForTheInts+=1

    #reading rooms data in 2D array
    roomsData1D=[]
    for val in fRoom.read().split():
        roomsData1D.append(int(val))
    TOTAL_ROOMS = len(roomsData1D)
    #reading days and slots in global variables
    theDaysAndSlots=[]
    for val in fDays.read().split():
        theDaysAndSlots.append(int(val))

    TOTAL_DAYS = theDaysAndSlots[0]
    TOTAL_SLOTS = theDaysAndSlots[1]
    #closing file handlers
    fReg.close()
    fRoom.close()
    fDays.close()

    iu1, iu2 = 0, 0
    for iu1 in range(TOTAL_COURSES):
        temp = []
        iu2 = 0
        for iu2 in range(TOTAL_STUDENTS):
            if regData2D[iu1][iu2]==1:
                temp.append(iu2)
        refinedRegData2D.append(temp)



    return refinedRegData2D,regData2D, roomsData1D

def intersection(lst1, lst2): #u in nu
    lst3 = [value for value in lst1 if ((value in lst2) and value==1)] 
    return lst3 

def getCountStudentsWithRegInBothCourses(cid1, cid2, regData2D): #nu
    return len(intersection(regData2D[cid1-1], regData2D[cid2-1]))

def getCountStudentsWithRegInTripleCourses(cid1, cid2, cid3, regData2D): #nu
    l1 = intersection(regData2D[cid1-1], regData2D[cid2-1])
    return len(intersection(l1, regData2D[cid3-1]))

def getCountStudentsWithRegInQuadrupleCourses(cid1, cid2, cid3, cid4, regData2D): #nu
    l1 = intersection(regData2D[cid1-1], regData2D[cid2-1])
    l2 = intersection(l1, regData2D[cid3-1])
    return len(intersection(l2, regData2D[cid4-1]))

def getCountStudentsWith2ExamsInGivenSlot(s2, choromosome, refinedRegData2D):
    global TOTAL_STUDENTS
    global TOTAL_BITS_OF_SLOT

    count = 0
    strikes = 0
    courseID = 0

    dictOfStudents = dict()
    setOfSubjects = set()

    for k in range(TOTAL_STUDENTS):
        dictOfStudents[k] = 0

    i = s2
    j = 0
    for i in range(s2 + TOTAL_BITS_OF_SLOT):
        courseID = choromosome[i]
        if(courseID not in setOfSubjects):
            setOfSubjects.add(courseID)
            for j in range(len(refinedRegData2D[courseID-1])):
                dictOfStudents[refinedRegData2D[courseID-1][j]] += 1  #ExamCount of that students is increased for that particular day
                if(dictOfStudents[refinedRegData2D[courseID-1][j]]==2):
                    count += 1
   
    return count


def getCountStudentsWith2ConsecutiveExamsInGivenDay(s2, choromosome, refinedRegData2D, regData2D):
    global TOTAL_STUDENTS
    global TOTAL_BITS_OF_DAY

    count = 0
    courseID = 0
    courseIDPrevConsecutive = 0
    strikes = 0

    dictOfStudents = dict()
    listOfSubjects = list()

    for k in range(TOTAL_STUDENTS):
        dictOfStudents[k] = 0

    i = s2
    j = 0
    for i in range(s2 + TOTAL_BITS_OF_DAY):
        courseID = choromosome[i]
        if(courseID not in listOfSubjects):
            if(len(listOfSubjects) > 0):
                courseIDPrevConsecutive = listOfSubjects[-1]
            listOfSubjects.append(courseID)
            if(len(listOfSubjects) > 1):
                for j in range(len(refinedRegData2D[courseID-1])):
                    if(regData2D[courseID-1][refinedRegData2D[courseID-1][j]]==1 and regData2D[courseIDPrevConsecutive-1][refinedRegData2D[courseID-1][j]]==1): #student is registered in both courses
                        dictOfStudents[refinedRegData2D[courseID-1][j]] += 1  #ExamCount of that students is increased for that particular day
                        count += 1

    return count



def getCountStudentsWithMoreThan2ExamsInGivenSlot(s2, choromosome, refinedRegData2D):
    global TOTAL_STUDENTS
    global TOTAL_BITS_OF_SLOT

    count = 0
    courseID = 0

    dictOfStudents = dict()
    setOfSubjects = set()
    temp = []

    for k in range(TOTAL_STUDENTS):
        dictOfStudents[k] = 0

    i = s2
    j = 0
    for i in range(s2 + TOTAL_BITS_OF_SLOT):
        courseID = choromosome[i]
        if(courseID not in setOfSubjects):
            setOfSubjects.add(courseID)
            for j in range(len(refinedRegData2D[courseID-1])):
                    dictOfStudents[refinedRegData2D[courseID-1][j]] += 1  #ExamCount of that students is increased for that particular day
                    if(dictOfStudents[refinedRegData2D[courseID-1][j]] > 2):
                        if refinedRegData2D[courseID-1][j] not in temp:
                            temp.append(refinedRegData2D[courseID-1][j])
                            count += 1
   
    return count


def getCountStudentsWithMoreThan2ExamsInGivenConsecutiveSlotsInADay(s2, choromosome,refinedRegData2D, regData2D):
    global TOTAL_STUDENTS
    global TOTAL_BITS_OF_DAY

    count = 0
    courseID = 0
    courseID1stPrevConsecutive = 0
    courseID2ndPrevConsecutive = 0

    dictOfStudents = dict()
    listOfSubjects = list()

    for k in range(TOTAL_STUDENTS):
        dictOfStudents[k] = 0

    i = s2
    j = 0
    for i in range(s2 + TOTAL_BITS_OF_DAY):
        courseID = choromosome[i]
        if(courseID not in listOfSubjects):
            if(len(listOfSubjects) > 1):
                courseID1stPrevConsecutive = listOfSubjects[-1]
                courseID2ndPrevConsecutive = listOfSubjects[len(listOfSubjects)-2] #2nd last element
            listOfSubjects.append(courseID)
            if(len(listOfSubjects) > 2):
                for j in range(len(refinedRegData2D[courseID-1])):
                    if(regData2D[courseID-1][refinedRegData2D[courseID-1][j]]==1 and regData2D[courseID1stPrevConsecutive-1][refinedRegData2D[courseID-1][j]]==1 and regData2D[courseID2ndPrevConsecutive-1][refinedRegData2D[courseID-1][j]]==1): #student is registered in all 3 courses
                        dictOfStudents[refinedRegData2D[courseID-1][j]] += 1  #ExamCount of that students is increased for that particular day
                        count += 1

    return count


def getCountStudentsWithMoreThan3ExamsInADay(s2, choromosome, refinedRegData2D):
    global TOTAL_STUDENTS
    global TOTAL_BITS_OF_DAY

    count = 0
    courseID = 0

    dictOfStudents = dict()
    setOfSubjects = set()

    for k in range(TOTAL_STUDENTS):
        dictOfStudents[k] = 0

    i = s2
    j = 0
    for i in range(s2 + TOTAL_BITS_OF_DAY):
        courseID = choromosome[i]
        if(courseID not in setOfSubjects):
            setOfSubjects.add(courseID)
            for j in range(len(refinedRegData2D[courseID-1])):
                dictOfStudents[refinedRegData2D[courseID-1][j]] += 1  #ExamCount of that students is increased for that particular day
                if(dictOfStudents[refinedRegData2D[courseID-1][j]] > 3):
                    count += 1

    return count

def FitnessFunction(population, regData2D, roomsData1D, sizeOfReturnArray, refinedRegData2D):
    global TOTAL_BITS_OF_DAY
    global TOTAL_BITS_OF_SLOT
    global TOTAL_BITS_OF_ROOM
    global TOTAL_ROOM_CAPACITY

    roomPenalty, slotPenalty, dayPenalty, dateSheetPenalty = 0, 0, 0, 0
    itroom, itslot, itday = 0,0,0


    fitness = np.empty(population.shape[0])#creating 1D array of size POP_SIZE


    for s1 in range(population.shape[0]): #i.e POP_SIZE
        #reached 1 chromosome level

        courseList = list()
        courseList = [val for val in range(1, sizeOfReturnArray+1)]

        slotPenalty, dayPenalty, dateSheetPenalty = 0, 0, 0
        roomFulfillment = 0
        setOfCourseStudentsForRoomCapacity = set()

        for s2 in range(population.shape[1]): #i.e chromosome BITS (INTs)
            #reached level of each Bit

           # itday = (int)(s2/TOTAL_BITS_OF_DAY)
            #itslot = (int)((s2-((itday)*(TOTAL_BITS_OF_DAY)))/(TOTAL_BITS_OF_SLOT))
            #itroom = (int)(s2 % TOTAL_BITS_OF_SLOT)

            if (s2 % TOTAL_BITS_OF_DAY == 0):
                #reached at new day
                c3 = ((getCountStudentsWithMoreThan3ExamsInADay(s2, population[s1], refinedRegData2D)))
                dayPenalty += c3*0.02
                slotPenalty += 0.01*(getCountStudentsWith2ConsecutiveExamsInGivenDay(s2, population[s1], refinedRegData2D, regData2D))

                c2 = (getCountStudentsWithMoreThan2ExamsInGivenConsecutiveSlotsInADay(s2, population[s1], refinedRegData2D, regData2D))
                slotPenalty += c2*0.02     

            if (s2 % TOTAL_BITS_OF_SLOT == 0):
                #reached at new slot
                while(len(setOfCourseStudentsForRoomCapacity)>0):
                    roomFulfillment += len(refinedRegData2D[setOfCourseStudentsForRoomCapacity.pop()-1])
                    if(roomFulfillment > TOTAL_ROOM_CAPACITY):
                        slotPenalty += 0.02

                roomFulfillment = 0

                slotPenalty += 0.01*(getCountStudentsWith2ExamsInGivenSlot(s2, population[s1], refinedRegData2D))
                

                c1 = (getCountStudentsWithMoreThan2ExamsInGivenSlot(s2, population[s1], refinedRegData2D))
                slotPenalty += c1*0.02
                


            setOfCourseStudentsForRoomCapacity.add(population[s1][s2])
            if(population[s1][s2] in courseList):
                courseList.remove(population[s1][s2])           

            
        if(len( courseList )>0):
            dateSheetPenalty += 0.02*len(courseList)
        dateSheetPenalty += (slotPenalty) + (dayPenalty)
        fitness[s1] = 1 / (1 + dateSheetPenalty)
        if(fitness[s1]==1):
            return fitness

    return fitness

def replace(person1, person2):

    pivot = random.randrange(len(person1))
    for i in range(pivot):
        person1[i], person2[i] = person2[i], person1[i]


def localSearch(population, regData2D, roomsData1D, refinedRegData2D, finalPop):
    totalChromosomes = len(finalPop)
    e1 = 0
    e2 = 0
    for it1 in range(totalChromosomes):
        patient = finalPop[it1]
        for it2 in range(TOTAL_DAYS):
           e1 += getCountStudentsWith2ConsecutiveExamsInGivenDay(it2*TOTAL_BITS_OF_DAY, patient, refinedRegData2D, regData2D)
        if e1>0:
            while e1 > 0:
                replace(patient, patient)

    for it3 in range(totalChromosomes):
        patient = finalPop[it3]
        for it4 in range(TOTAL_SLOTS):
           e2 += getCountStudentsWith2ExamsInGivenSlot(it3*TOTAL_BITS_OF_SLOT, patient, refinedRegData2D)
        if e2>0:
            while e2 > 0:
                replace(patient, patient)

    return finalPop


def Crossover(population, newPop):
    global POP_SIZE
    for i in range(int(POP_SIZE*25/100), POP_SIZE-1):
        r1 = random.randrange(POP_SIZE-1)
        r2 = random.randrange(POP_SIZE-1)
        first = copy.deepcopy(population[r1])
        second = copy.deepcopy(population[r2])

        replace(first, second)
        newPop[i] = first
        i += 1
        newPop[i] = second

def Mutation(population):
    global POP_SIZE
    global TOTAL_COURSES
    for i in range(int(0.25*POP_SIZE)):
        if(random.randrange(1000)%4 == 0):
            randindex = random.randrange(population.shape[1])
            population[i][randindex] = random.randrange(TOTAL_COURSES+1)


def main():
    global TOTAL_BITS_OF_CHROMOSOME
    global TOTAL_BITS_OF_DAY
    global TOTAL_BITS_OF_SLOT
    global TOTAL_BITS_OF_ROOM
    global TOTAL_ROOM_CAPACITY
    global POP_SIZE
    global TOTAL_COURSES

    refinedRegData2D, regData2D, roomsData1D = readDataFiles("registration.data", "capacity.room", "general.info")
    TOTAL_ROOM_CAPACITY = np.sum(roomsData1D, axis=0)


    TOTAL_BITS_OF_ROOM = 1 #math.ceil(math.log(TOTAL_COURSES + 1, 2))
    TOTAL_BITS_OF_SLOT = TOTAL_ROOMS * TOTAL_BITS_OF_ROOM
    TOTAL_BITS_OF_DAY = TOTAL_SLOTS * TOTAL_ROOMS * TOTAL_BITS_OF_ROOM
    TOTAL_BITS_OF_CHROMOSOME =  TOTAL_DAYS * TOTAL_SLOTS * TOTAL_ROOMS * TOTAL_BITS_OF_ROOM

    #generating chromosome population
    population = np.array([np.random.randint(1,TOTAL_COURSES+1,TOTAL_BITS_OF_CHROMOSOME) for i in range(POP_SIZE)])
    population = population.astype('int32')
    
    print(population)

    #Calculating Fitness Value for population
    fitness = FitnessFunction(population, regData2D, roomsData1D, TOTAL_COURSES, refinedRegData2D)
    fitness = fitness.astype('float')
    #print(fitness)

    result = 0
    generations = 0
    output = 0
    topresults = 0
    finalPop = np.empty(5)#creating 1D array of size POP_SIZE
    while(result == 0):
        #Sorting Population on Fitness
        # Sort(population, fitness)
        arr1inds = fitness.argsort()[::-1] #in decending order
        fitness = fitness[arr1inds[::1]]
        print(fitness)
        population = population[arr1inds[::1]]

        newPop = np.empty(population.shape)
        newPop[:] = population #[:]creates copy but with different object
        newPop = newPop.astype('int32')

        if(fitness[0] >= 0.9):

            output = fitness[0]
            print("Generation # "+ str(generations) + ", Value = " + str(fitness[0]))
            topresults += 1
            finalPop[topresults-1] = (population[0]) #adding most fit chromosomes to final population
            if(topresults>4):
                break

        if(fitness[0] > 0.5 and fitness[0] < 0.9):
            finalPop = localSearch(population, regData2D, roomsData1D, refinedRegData2D, finalPop)
            fitness = FitnessFunction(finalPop, regData2D, roomsData1D, TOTAL_COURSES, refinedRegData2D)
            fitness = fitness.astype('float')
            arr1inds = fitness.argsort()[::-1] #in decending order
            fitness = fitness[arr1inds[::1]]
            print("Result found, FINAL DATESHEET")
            print(finalPop[arr1inds[0]]) #final DATESHEET
            break

        Crossover(population,newPop)
        Mutation(newPop)

        population = newPop
        population = population.astype('int32')

        fitness = FitnessFunction(population, regData2D, roomsData1D, TOTAL_COURSES, refinedRegData2D)
        fitness = fitness.astype('float')
        generations += 1


if __name__=='__main__':
    main()