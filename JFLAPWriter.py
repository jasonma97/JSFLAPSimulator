# Jason Ma
# Developed 6/17/16

def writeJFLAPFile(automata, nodeL, edgeL, initNode, finalNodeL):
    f = open('output.jff', 'w')
    f.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 6.4.--><structure>&#13;
    <type>""" + automata.lower() + """</type>&#13;
    <automaton>&#13;
        <!--The list of states.-->&#13;""")
    f.close()