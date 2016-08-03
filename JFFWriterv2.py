#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


from random import *
from time import *
import math

from StateMachine import *

lambdaChar = 'λ'

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="   ")

def addCorrectHeader(top):
    """Adds to the xml header, so that JFLAP will read it.
        This is a terrible hack because it relies on the string 
        starting the file to be a certain length
        Please don't use this code if this isn't deprecated later"""
    newTop = ''
    #encoding="UTF-8" standalone="no"
    newHeader = ''
    for char in range(len(top)):
        newTop += top[char]
        if char == 19:
            newTop += newHeader
    return newTop


def writeFA(stateMech, filename):
    if filename[-4:] != '.txt':
        print('This needs to have a .txt extension to work!')
        return
    f = open(filename[:-4] + 'jflap.jff', 'w')
    root = Element('structure')
    mechType = SubElement(root, 'type')
    mechType.text = 'fa'

    automaton = SubElement(root, 'automaton')
    automaton.append(Comment('The list of states.'))

    counter = 0
    nodeDict = {}
    for node in stateMech.nodeL:
        state = SubElement(automaton, 'state', id = str(counter), name = node.name)
        xCoor = SubElement(state, 'x')
        xCoor.text = str(math.floor(random() * 1000) * 1.0)
        yCoor = SubElement(state, 'y')
        yCoor.text = str(math.floor(random() * 1000) * 1.0)
        if node.initial:
            SubElement(state, 'initial')
        if node.accepting:
            SubElement(state, 'final')
        nodeDict[node.name] = str(counter)
        counter += 1

    for edge in stateMech.edgeL:
        transition = SubElement(automaton, 'transition')
        fromNode = SubElement(transition, 'from')
        toNode = SubElement(transition, 'to')
        read = SubElement(transition, 'read')

        fromNode.text = nodeDict[edge.fromNode.name]
        toNode.text = nodeDict[edge.intoNode.name]
        readVal = edge.readVal
        if readVal != lambdaChar:
            read.text = readVal



    prettyRoot = prettify(root)
    #print(addCorrectHeader(prettyRoot))
    f.write(addCorrectHeader(prettyRoot))
    f.close()



def writeTM(stateMech, filename):
    if filename[-4:] != '.txt':
        raise Exception('This needs to have a .txt extension to work!')
        return
    f = open(filename[:-4] + 'jflap.jff', 'w')
    root = Element('structure')
    mechType = SubElement(root, 'type')
    mechType.text = 'turing'

    automaton = SubElement(root, 'automaton')
    automaton.append(Comment('The list of states.'))

    counter = 0
    nodeDict = {}
    for node in stateMech.nodeL:
        state = SubElement(automaton, 'block', id = str(counter), name = node.name)
        tag = SubElement(state, 'tag')
        tag.text = 'Machine' + str(counter)
        xCoor = SubElement(state, 'x')
        xCoor.text = str(math.floor(random() * 1000) * 1.0)
        yCoor = SubElement(state, 'y')
        yCoor.text = str(math.floor(random() * 1000) * 1.0)
        if node.initial:
            SubElement(state, 'initial')
        if node.accepting:
            SubElement(state, 'final')
        nodeDict[node.name] = str(counter)
        counter += 1

    for edge in stateMech.edgeL:
        transition = SubElement(automaton, 'transition')
        fromNode = SubElement(transition, 'from')
        toNode = SubElement(transition, 'to')
        read = SubElement(transition, 'read')
        write = SubElement(transition, 'write')
        move = SubElement(transition, 'move')

        fromNode.text = nodeDict[edge.fromNode.name]
        toNode.text = nodeDict[edge.intoNode.name]
        readVal = edge.readVal
        writeVal = edge.writeVal
        move.text = edge.action
        if readVal != lambdaChar:
            read.text = readVal
        if writeVal != lambdaChar:
            write.text = writeVal
        


    prettyRoot = prettify(root)
    #print(addCorrectHeader(prettyRoot))
    f.write(addCorrectHeader(prettyRoot))
    f.close()

def writeJFFFile(stateMech, filename):
    seed(time)
    if stateMech.machine == 'Finite State Automata':
        writeFA(stateMech, filename)
    elif stateMech.machine == 'Turing Machine':
        writeTM(stateMech, filename)
    else:
        print("What kind of machine is this? I can't read it!")
        return

def convertFromJSFLAP2JFLAP(filename):
    seed(time)
    stateMech = parseStateMachine(filename)
    writeJFFFile(stateMech, filename)


def main():
    seed(time)
    stateMech = parseStateMachine('div7.txt')
    if stateMech.machine == 'Finite State Automata':
        writeFA(stateMech, 'div7.txt')
    elif stateMech.machine == 'Turing Machine':
        writeTM(stateMech, 'div7.txt')
    else:
        print("What kind of machine is this? I can't read it!")
        return


if __name__ == '__main__':
    main()