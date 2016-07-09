import JSFLAPConverter


lamb = '☐'

class Node:
    def __init__(self, name, edgeL ,initial, accepting):
        """ Initializes an object of the Node class to represent a state for finite/infinite state machines
            Accepts a string name - name of the node
            list edgeL - list of edges that the node is attached to
            initial - a boolean, true if the node is an initial node, false otherwise
            accepting - a boolean, true if the node is an accepting node, false otherwise """
        self.name = name
        self.intoNode, self.fromNode = self.separateEdges(edgeL)
        self.initial = initial
        self.accepting = accepting

    def canContinue( self, I ):
        """Given an input I, canContinue checks to see if the node is connected to
        another node through an edge, and if the edge has the correct read value to continue
        If so, return true, otherwise return false"""
        goToNodeL = []
        for edge in self.fromNode:
            if edge.readVal == I:
                goToNodeL.append(edge)  
        if len(goToNodeL) > 0:
            return True, goToNodeL
        return False, None

    def addEdge( self,  edge ):
        """Accepts an edge, checks if the node is in the edge, if it is,
        it adds the edge to the relevant storer, either it is added to the fromNode or intoNode
        Otherwise, it just returns and doesn't change the ndoe"""
        if self.name == edge.fromNode:
            self.fromNode.append(edge)
        elif self.name == edge.toNode:
            self.intoNode.append(edge)
        else:
            return None

    def hasLambda( self ):
        """ Determines if the node is attached to an edge that reads a lambda, if so, 
        return True and the node the lambda edge leads to"""
        for edge in self.fromNode:
            if edge[2] == lamb:
                return True

    def separateEdges( self, edgeL ):
        """Filters the edges depending on which edges go into the node and which edges
        come from the node"""
        intoNode = []
        fromNode = []
        for edge in edgeL:
            if self.name ==  edge[0]:
                fromNode.append(edge)
            elif self.name == edge[1]:
                intoNode.append(edge)
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
    def __init__(self, toNode, fromNode, readWriteTrigger):
        self.fromNode = fromNode
        self.toNode = toNode
        self.readVal, self.writeVal, self.action = self.actionEval(readWriteTrigger)

    def actionEval( self, readWriteTrigger ):
        """Reads in the action trigger, the 3rd element in the tuple for edges. This function
        Determines if the edge signifieas any actions (ie write or move right/left)
        Determines what needs to be read in order to traverse the edge"""
        if '/' not in readWriteTrigger and ';' not in readWriteTrigger:
            return readWriteTrigger, None, None
        else:
            return readWriteTrigger[0], readWriteTrigger[2], readWriteTrigger[-1]

    def __repr__(self):
        """Basic printout representation of an edge as a tuple"""
        if self.writeVal == None:
            return str((self.fromNode, self.toNode, self.readVal))
        else:
            return str((self.fromNode, self.toNode, self.readVal, self.writeVal, self.action))


class StateMachine:
    def __init__(self, nodeL, edgeL, initial, accepting, typeOfMachine, deterministic):
        self.nodeL = nodeL
        self.edgeL = edgeL
        self.initial = initial
        self.accepting = accepting
        self.machine, self.deterministic = self.whatAmI( typeOfMachine, deterministic)


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
        if not currentNode:
            currentNode = self.initial
        if S == '':
            if currentNode in self.accepting:
                return True
            else:
                return False
        canGo, nextNodeL = currentNode.canContinue(S[0])
        print(nextNodeL)
        hasLamb, nextNodeLamb = currentNode.canContinue(lamb)
        if canGo and hasLamb:
            f = lambda x: runFSM(S[1:], x)
            return max(map(f, nextNodeL)) or runFSM( S, nextNodeLamb)

        elif canGo :
            return runFSM( s[1:], nextNode)

        elif hasLamb:
            return runFSM( S, nextNodeLamb)

        else:
            return False



    def runTM ( self, S ):
        """Accepts a string of input S. Runs through the instance described by the class StateMachine
        as if it were a turing machine. Returns True if it ends in an accepting state.
        False otherwise """
        pass

def findNode( name, nodeL ):
    for node in nodeL:
        if node.name == name:
            return node
    return None

def main():
    """Designed to read a JSFLAP file and generate a state machine from it
    Then tests the state machine with input to see if behavior is consistent with what
    is expected. Returns True if all tests pass, false otherwise"""
    #filename = input("What is the name of the file")
    filename = 'nfa.txt'
    try:
        file = open(filename, 'r', encoding = 'utf-8')
    except IOError:
        print('File does not appear to exist. Remember to place the file in the same directory as this reader!')
    deterministic = file.read(1).lower()
    automata = file.read(2).lower()
    tempNodeL, tempEdgeL, tempInitNode, tempFinalNodeL = JSFLAPConverter.fileValues(file)
    #print(deterministic, automata)
    #print(tempNodeL)
    #print(tempEdgeL)
    #print(tempInitNode)
    #print(tempFinalNodeL)
    nodeL = [Node(node, [], node in tempInitNode, node in tempFinalNodeL) for node in tempNodeL]
    edgeL = [Edge( findNode(edge[0], nodeL), findNode(edge[1], nodeL), edge[2]) for edge in tempEdgeL]
    for edge in edgeL:
        edge.toNode.addEdge(edge)
        edge.fromNode.addEdge(edge)
    initNode = findNode( tempInitNode[0], nodeL )
    finalNodeL = [findNode( name, nodeL) for name in tempFinalNodeL]
    #print(nodeL)
    #print(list(edgeL))
    #print(initNode)
    #print(finalNodeL)

    print(nodeL[0].fromNode)
    stateMech = StateMachine( nodeL, edgeL, initNode, finalNodeL, automata,  deterministic )
    #print(automata)
    #print(stateMech.machine)
    #print(stateMech.deterministic)
    print(stateMech.runInput('0'))

if __name__ == '__main__':
    main()


