import JFFWriterv2

def main():
    while(True):
        print("Hello, this is a JSFLAP to JFLAP converter that converts JSFLAP Automaton definition files to JFLAP files, which are in .jff format")
        print("1. Convert JSFLAP File to .jff Format")
        print("2. Create a state machine from command line")
        print("3. Quit")
        decision = input("What do you want to do? (Pick a number)")
        if str(decision) == '1':
            convertJSFLAPToJFLAP()
        elif str(decision) == '2':
            createStateMachine()
        elif str(decision) == '3':
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
        if typeOfMachine != 'Finite State Automata' and typeOfMachine != 'Turing Machine':
            print("Invalid input, try again.")
        else:
            break
    while(True):
        print('Is your machine deterministic (Does it accept lambda/empty transitions)?')
        deterministic = input("Enter 'd' if yes, and 'n' if not")
        if deterministic != 'd' and deterministic != 'n':
            print('Invalid input, please try again.\n')
        else:
            break

    while(True):
        break
def convertJSFLAPToJFLAP():
    filename = input("What is the name of the JSFLAP file you want to convert? (Don't forget the file extension)\n")
    JFFWriterv2.convertFromJSFLAP2JFLAP(filename)

def fixFile(filename):
    file = open(filename, 'w+')
    string = file.read()
    string = string[:19] + 'encoding="UTF-8" standalone="no"' + string[19:]
    f = open('Fixed' + filename, 'w')
    f.write(string)

if __name__ == '__main__':
    main()