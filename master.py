#!/usr/bin/env python
# -*- coding: utf-8 -*- 
lamb = '☐'
import JFFWriterv2
import StateMachine
import time
import sys
if sys.version_info < (3,0):
    input = raw_input
DEBUG = True
def main():
    while(True):
        print("Hello, this is a JSFLAP to JFLAP converter that converts JSFLAP Automaton definition files to JFLAP files, which are in .jff format")
        print("1. Convert JSFLAP File to .jff Format")
        print("2. Create a state machine from command line")
        print("3. Quit")
        decision = input("What do you want to do? (Pick a number)\n")
        if str(decision) == '1':
            convertJSFLAPToJFLAP()
        elif str(decision) == '2':
            createStateMachine()
        elif str(decision) == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid input, please select a valid command(1-3)")
    return



def test():
    main()

def createStateMachine():
    print("Hello, welcome to Jason's CLI for state machine")
    typeOfMachine = ''
    deterministic = ''
    print()
    while(True):
        print("What type of machine are you making?")
        print("Enter 'fa' for Finite Automata's (Read string and determines if it's in the language")
        print("Enter 'tm' to create a Turing Machine")
        typeOfMachine = input()
        if typeOfMachine != 'fa' and typeOfMachine != 'tm':
            print("Invalid input, try again.")
        else:
            break
    while(True):
        print('Is your machine deterministic (Does it accept lambda/empty transitions)?')
        deterministic = str(input("Enter 'd' if yes, and 'n' if not:\n"))
        if deterministic != 'd' and deterministic != 'n':
            print('Invalid input, please try again.\n')
        else:
            break

    # stateMech = StateMachine.StateMachine([], [], [], [], typeOfMachine, deterministic)
    nodeL = []
    edgeL = []
    initial = None
    accepting = []
    while(True):
        print("What do you want to do with your state machine?")
        print("1. Add Node")
        print("2. Add Edge")
        print("3. Declare Initial Node (Will rewrite previous initial node")
        print("4. Add Accepting/Final Node")
        print("5. Remove Accepting/Final Node (Makes it a nonaccepting node)")
        print("6. Remove a node")
        print("7. Remove an edge")
        print("8. Generate JFLAP file (.jff format)")
        print("9. Quit")
        decision = str(input())
        if decision == '1':
            nodeL = addNode(nodeL)
        elif decision =='2':
            edgeL = addEdge(nodeL, edgeL, typeOfMachine, deterministic)
        elif decision == '3':
            initial = declareStartNode(nodeL)
        elif decision == '4':
            accepting = declareAcceptingNode(nodeL, accepting)
        elif decision == '5':
            accepting = removeAcceptingNode(accepting)
        elif decision == '6':
            nodeL, initial, accepting, edgeL = deleteNode(nodeL, initial, accepting, edgeL)
        elif decision == '7':
            edgeL = removeEdge(edgeL, typeOfMachine)
        elif decision == '8':
            try:
                generateJFLAPFile(deterministic, typeOfMachine, nodeL, edgeL, initial, accepting)
            except NameError:
                print("Try entering a better filename next time")
            #print("Goodbye! Thanks for using my program!")
            #break
        elif decision == '9':
            print("Goodbye!")
            break
        elif DEBUG and '-1':
            print(nodeL)
            print(edgeL)
            print(initial)
            print(accepting)
        else:
            print("Invalid input, Try again.")
        time.sleep(0.1)
        print("")

def addNode(nodeL):
    print("Entering a new node. Enter q at anytime to quit.")
    while(True):
        nodeName = input("Enter the name of the node:\n")
        if nodeName == 'q':
            return nodeL
        validNode = True
        for node in nodeL:
            if node == nodeName:
                print("This name has been used before! Try again with a new name")
                validNode = False
        if validNode:                  
            nodeL.append(nodeName)
            break
    return nodeL

def addEdge(nodeL, edgeL, typeOfMachine, deterministic):
    print("Entering a new edge. Enter q at anytime to quit.")
    startNode = None
    while(True):
        startNode = input("From which node does the edge start?:\n")
        validNode = False
        if startNode == 'q':
            return nodeL, edgeL
        for node in nodeL:
            if node == startNode:
                validNode = True
        if not validNode:
            print("This is not a valid start node, enter a new one!")
            continue
        else:
            break

    while(True):
        endNode = input("At which node does the edge end?:\n")
        validNode = False
        if endNode == 'q':
            return nodeL, edgeL
        for node in nodeL:
            if node == endNode:
                validNode = True
        if not validNode:
            print("This is not a valid ending node, enter a new one.")
            continue
        else:
            break

    if typeOfMachine == 'fa':
        readVal = getReadVal(deterministic)

    elif typeOfMachine == 'tm':
        readVal = getReadWriteVal(deterministic)
    if readVal == 'q':
        return edgeL

    edgeL.append([startNode, endNode, readVal])
    return edgeL

def getReadVal(deterministic):
    while(True):
        if deterministic == 'd':
            readVal = input('What value does this edge read?:\n')
        else:
            readVal = input('What value does this edge read? (Enter lambda for lambda transitions):\n')
        if readVal == 'q':
            return 'q'
        if readVal == 'lambda' and deterministic == 'd':
            print("You can't have lambda transitions on deterministic machines.")
            print("Enter a new read value, please!")
        if len(readVal) > 1:
            print("Edges only read one character at a time! Enter in one character next time.")
        else:
            return readVal

def getReadWriteVal(deterministic):
    while(True):
        if deterministic == 'd':
            readVal = input('What value does this edge read?:\n')
        else:
            readVal = input('What value does this edge read? (Enter lambda for lambda transitions):\n')
        if readVal == 'q':
            return 'q'
        if readVal == 'lambda' and deterministic == 'd':
            print("You can't have lambda transitions on deterministic machines.")
            print("Enter a new read value, please!")
        if readVal == 'lambda':
            readVal = lamb
        if len(readVal) > 1:
            print("Edges only read one character at a time! Enter in one character next time.")
        else:
            break

    while(True):
        if deterministic == 'd':
            writeVal = input('What value does this edge write?:\n')
        else:
            writeVal = input('What value does this edge read? (Enter lambda for lambda transitions):')
        if writeVal == 'q':
            return 'q'
        if writeVal == 'lambda' and deterministic == 'd':
            print("You can't have lambda transitions on deterministic machines.")
            print("Enter a new read value, please!")
        if len(writeVal) > 1:
            print("Edges only read one character at a time! Enter in one character next time.")
        else:
            break
    while(True):
        direction = input("Where does the turing machine move to next? (l/s/r):\n")
        if direction == 'q':
            return 'q'
        elif direction == 's' or direction =='r' or direction =='l':
            break
        else:
            print("Not a valid direction")
    return [readVal, writeVal, direction]

def declareStartNode(nodeL):
    while(True):
        for a0 in range(len(nodeL)):
            print(str(a0) + ". " + nodeL[a0])
        start = input("Enter the Index of the node to make initial. 0 - " + str(len(nodeL) - 1) + ".\n")
        if start == 'q':
            return None
        if int(start) >= len(nodeL):
            print("Node specified not in range. Try again.")
        else:
            return nodeL[int(start)]

def declareAcceptingNode(nodeL, acceptingL):
    while(True):
        for a0 in range(len(nodeL)):
            print(str(a0) + ". " + nodeL[a0])
        acc = input("Enter the index of the node you want to make accepting. 0 - " + str(len(nodeL) - 1) + ".\n")
        if acc == 'q':
            return acceptingL
        elif int(acc) >= len(nodeL):
            print("Node specified not in range. Try again.")
        else:
            acceptingL.append(nodeL[int(acc)])
            return acceptingL

def removeAcceptingNode(acceptingL):
    for a0 in range(len(acceptingL)):
        print(str(a0) + ". " + acceptingL[a0])
    delete = input("Enter the index of the node to remove from accepting nodes. 0 - " + str(len(acceptingL) - 1) + ".\n") 
    if delete == 'q':
        return acceptingL
    elif int(delete) >= len(acceptingL):
        print("Node specified not in range. Try again.")
    else:
        return [acceptNode for acceptNode in acceptingL if acceptNode != acceptingL[int(delete)]]

def deleteNode(nodeL, initial, acceptingL, edgeL):
    while(True):
        for a0 in range(len(nodeL)):
            print(str(a0) + ". " + nodeL[a0])
        delete = input("Enter the index of the node to remove from accepting nodes. 0 - " + str(len(nodeL) - 1) + ".\n")
        if delete == 'q':
            return nodeL, initial, acceptingL
        elif int(delete) >= len(nodeL):
            print("Node specified not in range. Try again.")
        else:
            if initial == nodeL[int(delete)]:
                initial = None
            if nodeL[int(delete)] in acceptingL:
                acceptingL = [accept for accept in acceptingL if accept != nodeL[int(delete)]]
            edgeL = [edge for edge in edgeL if edge[0] != nodeL[int(delete)]] and edge[1] != nodeL[(int(delete))]
            nodeL = [nodeL[a0] for a0 in range(len(nodeL)) if a0 != int(delete)]
            return nodeL, initial, acceptingL, edgeL

def removeEdge(edgeL, typeOfMachine):
    while(True):
        print("The edges will be listed in the following format:")
        print("starting state / ending state / read value")
        if typeOfMachine == 'tm':
            for a0 in range(len(edgeL)):
                print(str(a0) + ". " + edgeL[a0][0] + "/" + edgeL[a0][1] + "/ (" + edgeL[a0][2][0] + "/" + edgeL[a0][2][1] + "/" + edgeL[a0][2][2] + ")")
        else:
            for a0 in range(len(edgeL)):
                print(str(a0) + ". " + edgeL[a0][0] + "/" + edgeL[a0][1] + "/" + edgeL[a0][2])
        delete = input("Enter the index of the edge to delete. 0 - " + str(len(edgeL) - 1) + '.\n')
        if delete == 'q':
            return edgeL
        elif int(delete) >= len(edgeL):
            print("Edge specified not in range. Try again.")
        else:
            return [edge for edge in edgeL if edge != edgeL[int(delete)]]

def generateJFLAPFile(deterministic, typeOfMachine, nodeL, edgeL, initial, accepting):
    newNodeL = [StateMachine.Node(node, [], node == initial, node in accepting) for node in nodeL]
    if DEBUG:
        print(newNodeL)
    newEdgeL = [StateMachine.Edge( StateMachine.findNode(edge[0], newNodeL), StateMachine.findNode(edge[1], newNodeL), edge[2]) for edge in edgeL]
    if DEBUG:
        print(newEdgeL)
    for node in newNodeL:
        node.addEdge(newEdgeL)
    if DEBUG:
        print(newNodeL)
    initNode = StateMachine.findNode( initial, newNodeL )
    if DEBUG:
        print(initNode)
    finalNodeL = [StateMachine.findNode( name, newNodeL) for name in accepting]
    if DEBUG:
        print(finalNodeL)
    stateMech = StateMachine.StateMachine( newNodeL, newEdgeL, initNode, finalNodeL, typeOfMachine, deterministic)
    filename = input("What do you want the output to be named?\n")
    filename+='.txt'   
    JFFWriterv2.writeJFFFile(stateMech, filename)
    

def convertJSFLAPToJFLAP():
    filename = input("What is the name of the JSFLAP file you want to convert? (Don't forget the file extension)\n")
    if filename == 'q':
        return
    JFFWriterv2.convertFromJSFLAP2JFLAP(filename)

def fixFile(filename):
    file = open(filename, 'w+')
    string = file.read()
    string = string[:19] + 'encoding="UTF-8" standalone="no"' + string[19:]
    f = open('Fixed' + filename, 'w')
    f.write(string)

if __name__ == '__main__':
    main()