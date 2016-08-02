#Developed by Jason Ma
#Date:07/08/2016
#Designed to mimic finite state automata and run them to see if inputs are accepted or not


import JSFLAPReader

lamb = '☐'
lambdaChar = 'λ'
class Node:
    #This is an object representing the nodes in state automata
    def __init__(self, name, edgeL ,initial, accepting):
        """ Initializes an object of the Node class to represent a state for finite/infinite state machines
            Accepts a string name - name of the node
            list edgeL - list of edges that the node is attached to
            initial - a boolean, true if the node is an initial node, false otherwise
            accepting - a boolean, true if the node is an accepting node, false otherwise """
        self.name = name
        #print(edgeL)
        self.intoNode, self.fromNode = self.separateEdges(edgeL)
        self.initial = initial
        self.accepting = accepting

    def canContinue( self, I ):
        """Given an input I, canContinue checks to see if the node is connected to
        another node through an edge, and if the edge has the correct read value to continue
        If so, return true, otherwise return false"""
        #initializes the list of nodes the current node, whatever node is calling this method, can go to
        goToNodeL = []
        #Checks in the list of edges that start from the node
        #if their readValues match whatever the current input is,
        #add it to the list of nodes the machine can go to
        #also checks for if we can shift due to lambdas
        for edge in self.fromNode:
            if edge.readVal == I or edge.readVal == lambdaChar:
                goToNodeL.append(edge.intoNode)  
        #if the goToNodeL is populated, return a tuple of True and the list
        if len(goToNodeL) > 0:
            return True, goToNodeL
        #Else return false and empty list
        return False, []

    def addEdge( self,  edgeL ):
        """Accepts an edge list edgeL, checks if the node is in any edges in the list.
            If so, add the edge to the corresponding list of the node
            else does nothing """
        self.intoNode, self.fromNode = self.separateEdges(edgeL)
        #print(self.intoNode, self.fromNode)

    def hasLambda( self ):
        """ Determines if the node is attached to an edge that reads a lambda, if so, 
        return True if any edge accepts lambda"""
        for edge in self.fromNode:
            if edge.readVal == lamb or edge.readVal == lambdaChar:
                return True

    def separateEdges( self, edgeL ):
        """Filters the edge list depending on which edges go into the node and which edges
        come from the node"""
        #intoNode is a list of edges that go into the node
        intoNode = []
        #List of edges that leave from this node
        fromNode = []
        #For every edge in the edge list
        #Compare to see if the names of any nodes that the edges leaves or go into
        #match the name of the current node
        #Adds these edges to corresponding lists
        for edge in edgeL:
            if self.name ==  edge.fromNode.name:
                fromNode.append(edge)
            if self.name == edge.intoNode.name:
                intoNode.append(edge)
        #print(intoNode, fromNode)
        return intoNode, fromNode

    def __repr__( self ):
        """Print the node's name"""
        return self.name

    def nodeType( self ):
        """Gives a basic description of the node's name, and if it accepts or is the initial node"""
        s = self.name
        if self.initial:
            s += ' is an initial node'
        if self.initial and self.accepting:
            s += ' and an accepting node'
        elif self.accepting:
            s += ' is an accepting node'
        else:
            s += ' is a node'
        return s

class Edge:
    #This is an Edge object designed to represent the edges between nodes in state automata
    def __init__(self, fromNode, intoNode, readWriteTrigger):
        self.intoNode = intoNode
        self.fromNode = fromNode
        self.readVal, self.writeVal, self.action = self.actionEval(readWriteTrigger)

    def actionEval( self, readWriteTrigger ):
        """Reads in the action trigger, the 3rd element in the tuple for edges. This function
        Determines if the edge signifieas any actions (ie write or move right/left)
        Determines what needs to be read in order to traverse the edge"""
        if '/' not in readWriteTrigger and ';' not in readWriteTrigger:
            return self.replaceEmptyChar(readWriteTrigger), None, None
        else:
            return self.replaceEmptyChar(readWriteTrigger[0]), self.replaceEmptyChar(readWriteTrigger[2]), readWriteTrigger[-1]

    def __repr__(self):
        """Basic printout representation of an edge as a tuple"""
        if self.writeVal == None:
            return str((self.fromNode, self.intoNode, self.readVal))
        else:
            return str((self.fromNode, self.intoNode, self.readVal, self.writeVal, self.action))

    def replaceEmptyChar(self, val):
        """Given a character val. If val is a ☐ character, return a lambda character
            Else return the character.
            This function is needed because the ☐ is used in JSFLAP to represent an empty space with no values in it"""
        if val == lamb:
            return lambdaChar
        else:
            return val

class StateMachine:
    def __init__(self, nodeL, edgeL, initial, accepting, typeOfMachine, deterministic):
        self.nodeL = nodeL
        self.edgeL = edgeL
        self.initial = initial
        self.accepting = accepting
        self.machine, self.deterministic = self.whatAmI( typeOfMachine, deterministic)
        self.isDeterministic(edgeL, deterministic)

    def isDeterministic(self, edgeL, deterministic):
        """Used in the state machine creators to test to see if the machine has the attribute determinstic that the
        transitions follow this rule. Accepts a list of edges and the deterministic attribute(a string) and returns a boolean
        True if the determinstic nature matches the values on the edges, false otherwise"""
        for edge in edgeL:
            if edge.readVal == lambdaChar and deterministic == 'd':
                raise ValueError("You cannot have lambda transitions in a deterministic state machine!")
        return

    def whatAmI( self, typeOfMachine, deterministic ):
        """Determines what type of machine (finite state automata or turing) 
        and if it's deterministic or not. returns its settings"""
        if typeOfMachine == 'fa':
            mech = 'Finite State Automata'
        elif typeOfMachine == 'tm':
            mech = 'Turing Machine'
        else:
            mech = None
        if deterministic == 'd':
            det = 'Deterministic'
        elif deterministic == 'n':
            det = 'Nondeterministic'
        else:
            det = 'boi'
        return mech, det

    def runInput( self, S ):
        """Accepts a string as input. Runs the machine to determine if the input
        is accepted by the machine. Returns True if accepted, false otherwise"""
        if self.machine == 'Finite State Automata':
            return self.runFSM( S )
        elif self.machine == 'Turing Machine':
            return self.runTM( S )
        else:
            print("What kind of machine am I? I'm not one that just passes butter!")
            print("I can't run this input because I don't know what I am.")
            return None

    def runFSM( self,  S , currentNode = None):
        """Runs a string S through a Finite statemachine described by the class StateMachine
        Returns True if the input S ends in an accepting state
        False otherwise"""
        #If currentNode is None, replace it with the initial node of the state machine
        if not currentNode:
            currentNode = self.initial
        #print(currentNode)
        #When the input string S is empty, checks to see if we are in an accepting state
        #or not, returns corresponding result
        if S == '':
            if currentNode in self.accepting:
                return True
            else:
                return False


        #Checks to see if we can move to another edge given the current input from S
        #Also gets the list of nodes it can go to
        canGo, nextNodeL = currentNode.canContinue(S[0])

        #checks to see if there is a lambda attached to an edge with lambda
        #Also gets a list of those nodes
        hasLamb, nextNodeLamb = currentNode.canContinue(lambdaChar)
        f = lambda x: self.runFSM(S[1:], x)
        fLamb = lambda x: self.runFSM(S, x)



        #Map function calls to their corresponding lists. Returns the maximum
        #If any are true, the max functions returns that result
        #Else false is returned
        #Makes appropriate calls based on if there are lambdas or if an edge accepts the input
        if canGo and hasLamb:
            return max(map(f, nextNodeL)) or max(map(fLamb, nextNodeLamb))
        elif canGo :
            #print(nextNodeL)
            return max(map(f, nextNodeL))
        elif hasLamb:
            return max(map(fLamb, nextNodeLamb))
        #return false
        else:
            return False

    def writeValueAtIndex( self, S, val, index):
        """Reveives a string S and an int index which is the index of S to write to.
        Writes the string val to that location"""
        newString = ''
        for ind in range(len(S)):
            if ind == index:
                newString += val
            else:
                newString += S[ind]
        return newString

    def shiftAmount( self, direction):
        """Determines which direction to shift in. If a R is given, gives a plus 1 (signals index being incremented by 1)
        if L is given, gives a -1 (signals index being shifted left). All other values returmn None"""
        if direction == 'R':
            return 1
        elif direction == 'L':
            return -1
        elif direction == 'S':
            return 0
        else:
            return None

    def runTM ( self, S , currentNode = None, index = 0):
        """Accepts a string of input S. Runs through the instance described by the class StateMachine
        as if it were a turing machine. Returns True if it ends in an accepting state.
        False otherwise """

        #Basic checking to make sure the tape doesn't become extremely large when running their machine
        if len(S) > 1023:
            print("Error: Exceeded maximum tape size. Reconsider your algorithm because you're constructing an abnormally size")

        #Uses new variables to hold values
        ind = index
        #If the index is currently outside whatever tapelength we have, extend it with a 
        if ind == len(S):
            string = S + lambdaChar
        elif ind < 0:
            string = lambdaChar + S
            ind += 1
        else:
            string = S

        #If the currentNode is None, initialize it to be the initial node
        if not currentNode:
            currentNode = self.initial
        #List of actions that are possible at the current index/node
        actions = []

        #print(string)
        #print(string[ind])

        #For every edge leaving the current Node
        #If they read the value at our current index of the tape, save their write values, the node they go to, and the direction they move in
        for leavingEdge in currentNode.fromNode:
            #print(leavingEdge.readVal)
            #print(leavingEdge)
            if leavingEdge.readVal == string[ind]:
                actions.append((leavingEdge.writeVal, leavingEdge.intoNode, leavingEdge.action ))
        #If the actions list is populated, 
        #Run all possible calls
        if len(actions) > 0:
            f = lambda x: self.runTM( self.writeValueAtIndex( string, x[0], ind), x[1], ind + self.shiftAmount(x[2]))
            return max(map(f, actions))
        #If actions list is empty and our current node is accepting, return True
        #Else return false
        elif currentNode.accepting:
            return True
        else:
            return False


def findNode( name, nodeL ):
    for node in nodeL:
        if node.name == name:
            return node
    return None



def parseStateMachine(filename):
    """Accepts a string filename. Looks for a file named filename and tries to open it and parse for a statemachine to run frmo it"""
    try:
        file = open(filename, 'r', encoding = 'utf-8')
    except IOError:
        print('File does not appear to exist. Remember to place the file in the same directory as this reader!')
        file = None
    if not file:
        return
    deterministic = file.read(1).lower()
    automata = file.read(2).lower()
    tempNodeL, tempEdgeL, tempInitNode, tempFinalNodeL = JSFLAPReader.fileValues(file)  
    nodeL = [Node(node, [], node in tempInitNode, node in tempFinalNodeL) for node in tempNodeL]
    edgeL = [Edge( findNode(edge[0], nodeL), findNode(edge[1], nodeL), edge[2]) for edge in tempEdgeL]
    for node in nodeL:
        node.addEdge(edgeL)
    initNode = findNode( tempInitNode[0], nodeL )
    finalNodeL = [findNode( name, nodeL) for name in tempFinalNodeL]
    stateMech = StateMachine( nodeL, edgeL, initNode, finalNodeL, automata,  deterministic )
    return stateMech

def testFile(filename, inputL):
    """Accepts a string filename and a list of strings inputL
        Uses filename to read a .txt file exported from JSFLAP and creates a finite state automata
        Then runs the state automata for every input in inputL
        Returns a list of results of running each input. Each element of the returned list
        Corresponds to running the input from inputL at the same index"""
    try:
        file = open(filename, 'r', encoding = 'utf-8')
    except IOError:
        print('File does not appear to exist. Remember to place the file in the same directory as this reader!')
        file = None
    if not file:
        return

    
    #Reads first 3 characters. First one determines if it is deterministic or not
    #Final two determine if it's a state automata or turing machine
    deterministic = file.read(1).lower()
    automata = file.read(2).lower()

    #Parses the nodes and edges from the file using JSFLAP converter
    tempNodeL, tempEdgeL, tempInitNode, tempFinalNodeL = JSFLAPReader.fileValues(file)  

    #Convert the list of strings tempNodeL to Node objects. No associated edges yet
    #Converts the list of tuples to Edge objects
    #Just pass an empty list for the edgeL for the nodes because we don't have a list of Edge objects yet
    nodeL = [Node(node, [], node in tempInitNode, node in tempFinalNodeL) for node in tempNodeL]
    edgeL = [Edge( findNode(edge[0], nodeL), findNode(edge[1], nodeL), edge[2]) for edge in tempEdgeL]

    #Since we now have a list of Edge objects, 
    #Associate nodes with their edges now.
    for node in nodeL:
        node.addEdge(edgeL)

    #Find the initial node and final (ie accepting) nodes
    initNode = findNode( tempInitNode[0], nodeL )
    finalNodeL = [findNode( name, nodeL) for name in tempFinalNodeL]


    stateMech = StateMachine( nodeL, edgeL, initNode, finalNodeL, automata,  deterministic )
    resultList = [stateMech.runInput(inputString) for inputString in inputL]
    return resultList


def main():
    """Designed to read a JSFLAP file and generate a state machine from it
    Then tests the state machine with input to see if behavior is consistent with what
    is expected. Returns True if all tests pass, false otherwise"""
    #filename = input("What is the name of the file")

    #Opens the specfied file
    filename = 'div7.txt'
    try:
        file = open(filename, 'r', encoding = 'utf-8')
    except IOError:
        print('File does not appear to exist. Remember to place the file in the same directory as this reader!')
        file = None
    if not file:
        return
    #Reads first 3 characters. First one determines if it is deterministic or not
    #Final two determine if it's a state automata or turing machine
    deterministic = file.read(1).lower()
    automata = file.read(2).lower()
    #Parses the nodes and edges from the file using JSFLAP converter
    tempNodeL, tempEdgeL, tempInitNode, tempFinalNodeL = JSFLAPReader.fileValues(file)

    #Convert the list of strings tempNodeL to Node objects
    #Converts the list of tuples to Edge objects
    #Just pass an empty list for the edgeL for the nodes because we don't have a list of Edge objects yet
    nodeL = [Node(node, [], node in tempInitNode, node in tempFinalNodeL) for node in tempNodeL]
    edgeL = [Edge( findNode(edge[0], nodeL), findNode(edge[1], nodeL), edge[2]) for edge in tempEdgeL]

    #Since we now have a list of Edge objects, pass each node0 the list of Edges, so they can
    #determine which edges are related to them
    for node in nodeL:
        node.addEdge(edgeL)

    #Find the initial node and final (ie accepting) nodes
    initNode = findNode( tempInitNode[0], nodeL )
    finalNodeL = [findNode( name, nodeL) for name in tempFinalNodeL]

    #Initialize the state machine with the given node list, edge list, list of initial nodes, list of accepting nodes
    #and the type of automata and whether it is deterministic or not
    stateMech = StateMachine( nodeL, edgeL, initNode, finalNodeL, automata,  deterministic )
    #Testing for divisibility by 7
    #strings = ['00', '0000', '0', '1', '10', '11', '100', '101', '110', '111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111', '10000', '10001', '10010','10011', '10100', '10101', '10110', '10111', '11000', '11001', '11010', '11011', '11100', '11101', '11110', '11111', '100000' ,'100001' ,'100010' ,'100011' ,'100100']
    #for string in strings:
        #print(string + ':' + str(stateMech.runInput(string)))
    #print(sys.getsizeof(stateMech))

    #Testing for if the first two bits match the last two bits
    #strings = ['00', '0000', '0', '1', '10', '11', '01', '000', '001', '010', '011', '100', '101', '110', '111', '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111', '0111010100', '1001010011', '0110100001', '1110010111']
    #for string in strings:
        #print(string + ':' + str(stateMech.runInput(string)))
    #print(stateMech.runInput('1010'))

    #Testing for divisbility by 3
    #strings = ['00000', '000100', '00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001', '01010' , '01011', '01100', '0']
    #stringsTest = ['0', '1', '10', '11', '100', '101', '110', '111', '1000', '1001', '1010', '1011', '1100', '1101', '1110' ,'1111', '10000', '10001', '10010', '10011' , '10100', '10101', '10110', '10111', '11000', '11001', '11010' ,'11011', '11100', '11101', '11110', '11111', '100000', '100001', '100010', '100011', '100100']
    #for string in stringsTest:
        #print(string + ':' + str(stateMech.runInput(string)))

    #Testing for palindromes. TM
    #strings = ['0', '1', '00', '01', '10', '11', '000', '001', '010', '011', '100', '101', '110', '111', '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111',  '0111010100', '1001010011', '0110100001', '1110010111', '1110000111', '0110000110', '11100100111', '01100100110']
    #for string in strings:
        #print(string + ' : ' + str(stateMech.runInput(string)))

    #Testing for same number of 1's and 0's. TM
    #strings =  ['', '0', '1', '00', '01', '10', '11', '000', '001', '010', '011', '100', '101', '110', '111', '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111', '0111010100', '1001010011', '0110100001', '1110010111', '1110000111', '0110000110', '11100100111', '01100100110']
    #for string in strings:
        #print(string + ' : ' + str(stateMech.runInput(string)))

    #Testing for part 1
    #strings = ['', '0', '1','00', '01', '10', '11', '000', '001', '010', '011', '100', '101', '110', '111', '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']
    #for string in strings:
        #print(string + ' : ' + str(stateMech.runInput(string)))

    #Testing if the first and last bit are the same
    #strings = [ '0', '1','00', '01', '10', '11', '000', '001', '010', '011', '100', '101', '110', '111', '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111', '0111010100', '1001010111', '0110100101', '1110010110']
    #for string in strings:
        #print(string + ' : ' + str(stateMech.runInput(string)))

    #Testing if the number of 0's is a multiple of 2 and/or 3
    #strings = ['', '0', '1','00', '01', '10', '11', '000', '001', '010', '011', '100', '101', '110', '111', '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111', '0101010101', '000000', '0100000', '111000000', '1010101010', '00000', '00111111000']
    #for string in strings:
        #print(string + ' : ' + str(stateMech.runInput(string)))

    #Testing if third to last bit is 1
    #strings = ['', '0', '1','00', '01', '10', '11', '000', '001', '010', '011', '100', '101', '110', '111', '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111', '0111010100', '1001010011', '0110100001', '0110100001', '1110010110', '100101101101']
    #for string in strings:
        #print(string + ' : ' + str(stateMech.runInput(string)))    

    print(stateMech.edgeL)
if __name__ == '__main__':
    main()


