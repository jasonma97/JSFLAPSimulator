header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 6.4.--><structure>\n'
tab = '    '
stateHeader = ['<state id="', '" name="', '">']

def writeState(idOfState, name, xCoor, yCoor, isInitial, isFinal):
    stateString = [stateHeader[0] + idOfState + stateHeader[1] + name + stateHeader[2] ]
    stateString += ['    <x>' + xCoor + '</x>']
    stateString += ['    <y>' + xCoor + '</y>']
    if isInitial:
        stateString += ['    <initial/>']
    if isFinal:
        stateString += ['    <final/>']
    stateString += ['</state>']    
    return stateString


def writeTransition( fromNode, toNode , read):
    transString = ['<transition']
    transString += ['    <from>' + fromNode + '</from>']
    transString += ['    <to>' + toNode + '</to>']
    transString += ['    <read>' + read + '</read>']
    transString += ['</transition']
    return transString

def main():
    f = open('output.jff', 'w')
    f.write(header)
    f.write(string + '\n')
    nextNode = writeState('7', "q7", '215', '123', False, True)
    for thing in nextNode:
        f.write('        ' + thing + '\n')
    f.close()

string = """    <type>fa</type>
    <automaton>
        <!--The list of states.-->
        <state id="0" name="q0">
            <x>174.0</x>
            <y>213.0</y>
            <initial/>
        </state>
        <state id="1" name="q1">
            <x>292.0</x>
            <y>120.0</y>
        </state>
        <state id="2" name="q2">
            <x>448.0</x>
            <y>120.0</y>
            <final/>
        </state>
        <state id="3" name="q3">
            <x>599.0</x>
            <y>142.0</y>
            <final/>
        </state>
        <state id="4" name="q4">
            <x>284.0</x>
            <y>363.0</y>
        </state>
        <state id="5" name="q5">
            <x>446.0</x>
            <y>365.0</y>
        </state>
        <state id="6" name="q6">
            <x>358.0</x>
            <y>234.0</y>
        </state>
        <!--The list of transitions.-->
        <transition>
            <from>1</from>
            <to>6</to>
            <read>1</read>
        </transition>
        <transition>
            <from>0</from>
            <to>1</to>
            <read>0</read>
        </transition>
        <transition>
            <from>3</from>
            <to>3</to>
            <read>0</read>
        </transition>
        <transition>
            <from>2</from>
            <to>2</to>
            <read>0</read>
        </transition>
        <transition>
            <from>6</from>
            <to>3</to>
            <read>0</read>
        </transition>
        <transition>
            <from>4</from>
            <to>6</to>
            <read>0</read>
        </transition>
        <transition>
            <from>0</from>
            <to>4</to>
            <read>1</read>
        </transition>
        <transition>
            <from>2</from>
            <to>3</to>
            <read>1</read>
        </transition>
        <transition>
            <from>6</from>
            <to>5</to>
            <read>1</read>
        </transition>
        <transition>
            <from>4</from>
            <to>5</to>
            <read>1</read>
        </transition>
        <transition>
            <from>1</from>
            <to>2</to>
            <read>0</read>
        </transition>
    </automaton>
</structure>"""
if __name__ == '__main__':
    main()

