HEADER = '<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 6.4.--><structure>\n'
TAB = '    '
STATEHEADER = ['<state id="', '" name="', '">']
BLOCKHEADER = ['<block id="', '" name="', '">']
CARRETURN = '&#13;'
rangeOfNumbers = range(1,500)

from random import *
from time import *
from StateMachine import *
import math
from xml.etree.ElementTree import Element, SubElement, Comment


def writeState(idOfState, name, xCoor, yCoor, isInitial, isFinal,  machineNumber = None):
    if machineNumber == None:
        stateString = [STATEHEADER[0] + idOfState + STATEHEADER[1] + name + STATEHEADER[2]]
    else:
        stateString = [BLOCKHEADER[0] + idOfState + BLOCKHEADER[1] + name + BLOCKHEADER[2]]
    if machineNumber != None:
        stateString += [TAB + '<tag>' + 'Machine' + machineNumber + '</tag>']
    stateString += ['    <x>' + xCoor + '</x>']
    stateString += ['    <y>' + yCoor + '</y>']
    if isInitial:
        stateString += ['    <initial/>']
    if isFinal:
        stateString += ['    <final/>']
    if machineNumber == None:
        stateString += ['</state>']
    else:
        stateString += ['</block>']
    return stateString


def writeTransition( fromNode, toNode , read, writeVal = None, move = None):
    transString = ['<transition>']
    transString += [TAB + '<from>' + fromNode + '</from>']
    transString += [TAB + '<to>' + toNode + '</to>']

    if read == '':
        transString += [TAB + '<read/>']
    else:
        transString += [TAB + '<read>' + read + '</read>']
    if writeVal != None and move != None:
        if writeVal == '':
            transString += [TAB + '<write/>']
        else:
            transString += [TAB + '<write>' + writeVal + '</write>']
        transString += [TAB + '<move>' + move + '</move>']
    transString += ['</transition>']
    return transString

def replaceLambda(string):
    if string == 'λ':
        return ''
    else:
        return string
def writeFile(stateMech, mechType):
    f = open('output.jff', 'w')
    seed(time())

    f.write(HEADER)
    f.write(TAB + '<type>' + mechType + '</type>' + CARRETURN 
        + '\n')
    f.write(TAB + '<automaton>' + CARRETURN + '\n')
    f.write(TAB + TAB + '<!--The list of states.-->' + CARRETURN + '\n')

    nodeDict = {}
    nodeID = 0
    for node in stateMech.nodeL:
        xCoor = choice(rangeOfNumbers) * 1.0
        yCoor = (choice(rangeOfNumbers) * 1.0)
        if mechType == 'turing':
            nodeFormatted = writeState(str(nodeID), node.name, str(xCoor), str(yCoor), node.initial, node.accepting, str(nodeID))
        else:
            nodeFormatted = writeState(str(nodeID), node.name, str(xCoor), str(yCoor), node.initial, node.accepting)
        for string in nodeFormatted:
            f.write(TAB + TAB + string + CARRETURN + '\n')
        nodeDict[node.name] = nodeID
        nodeID += 1

    f.write(TAB + TAB + '<!--The list of transitions.-->\n')
    for transition in stateMech.edgeL:
        if mechType == 'fa':
            fromNodeName = str(nodeDict[transition.fromNode.name])
            intoNodeName = str(nodeDict[transition.intoNode.name])
            readVal = str(transition.readVal)
            transitionFormatted = writeTransition(fromNodeName, intoNodeName, readVal)
        elif mechType == 'turing':
            fromNodeName = str(nodeDict[transition.fromNode.name])
            intoNodeName = str(nodeDict[transition.intoNode.name])
            readVal = replaceLambda(transition.readVal)
            writeVal = replaceLambda(transition.writeVal)
            transitionFormatted = writeTransition(fromNodeName, intoNodeName, readVal, writeVal, transition.action)
        for string in transitionFormatted:
            f.write(TAB + TAB + string + CARRETURN + '\n')
    if mechType == 'turing':
        f.write(TAB + TAB + '<!--The list of automata-->' + CARRETURN + '\n')
        for machineNumber in range(nodeID):
            f.write(TAB + TAB + '<Machine' + str(machineNumber) + '/>' + CARRETURN + '\n')
    f.write(TAB + '</automaton>' + CARRETURN + '\n')
    f.write('</structure>')
    f.close()



def main():
    stateMech = parseStateMachine('Palindrome.txt')
    if stateMech.machine == 'Finite State Automata':
        writeFile(stateMech, 'fa')
    elif stateMech.machine == 'Turing Machine':
        writeFile(stateMech, 'turing')
    else:
        print("What kind of machine is this? I can't read it!")
        return


if __name__ == '__main__':
    main()

