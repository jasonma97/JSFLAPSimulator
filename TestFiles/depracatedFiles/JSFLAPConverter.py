# Jason Ma
# Developed 6/17/16
# Hey this date is a palindrome!, kinda




def getNextTupleList(S, delim1, delim2):
    """Given a sequence that starts a tuple, reads the values inside the tuple
        Returns the tuple and the rest of the string"""
    listString = S[S.index(delim1):S[1:].index(delim2) + 2].replace(' ','')
    numEdges = listString.count('(')
    #print(numEdges)
    valueL = []
    for a0 in range(numEdges):
        newL, listString = getNextList(listString, '(', ')')
        newL = tuple(newL)
        valueL.append(newL)
    return valueL, S[S.index(delim2) + 1:]

def getNextList( S , delim1, delim2):
    """Given a string as input and delim1 and delim2 (delimiters), returns the string between the two
    delimiters"""
    listString = S[S.index(delim1):S[1:].index(delim2) + 2]
    listString = listString.replace(' ','')
    listString = listString.replace(delim1, '')
    listString = listString.replace(delim2, '')
    listString = listString.split(',')
    valueL = listString
    return valueL , S[S.index(delim2) + 1:]

def parseFile(file):
    """Reads the file file. Parses from it, lists of nodes for a state machine, the edges,
    the initial node, and the accepting nodes. Returns these lists in a 4 element tuple"""
    restOfFile = file.read()
    nodeL, edgeL, initNode, finalNodeL = 0,0,0,0
    valuesRead, restOfFile = getNextList(restOfFile, '{', '}')
    nodeL, restOfFile = getNextList(restOfFile, '{', '}')
    edgeL, restOfFile = getNextTupleList(restOfFile, '{', '}')
    initNode, restOfFile = getNextList(restOfFile, ',', ',')
    finalNodeL, restOfFile = getNextList(restOfFile, '{', '}')

    #print(valuesRead)


    return nodeL, edgeL, initNode, finalNodeL

def fileValues( file ):
    """Asks for a .jff file name, and parses it for a list of nodes, edges, the starting node, and the accepting nodes
        Then calls JFLAP creator to generate either a finite automata or turing machine to run test code.
    """
    nodeL, edgeL, initNode, finalNodeL = parseFile(file)
    return nodeL, edgeL, initNode, finalNodeL


    
def main():
    """Reads nfa.txt for testing purposes. Checks if the correct values are parsed from the file"""
    #filename = input("What is the name of the file")
    filename = 'nfa.txt'
    try:
        file = open(filename, 'r', encoding = 'utf-8')
    except IOError:
        print('File does not appear to exist. Remember to place the file in the same directory as this reader!')
    fileValues(file)

    
if __name__ == '__main__':
    main()