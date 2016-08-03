JSFLAP Simulator
Reads the Automata Definition output from JSFLAP.com (developed by Ben Grawi), and creates a Pythonic representation. Creates a Python representation of Formal Language and Automata Theory through the command line. 

Instructions:
1. Run the master.py in your command line
2. Follow it's instructions to either convert a JSFLAP file* or to create a new state machine from your command line.
3. Both features can output a .jff file which JFLAP can then read and render itself.

Files and Their Purposes:
master - combines all the files to create a command line interface for converting JSFLAP files and creating new JFLAP files from scratch.

JFFWriterv2 - Imports relevant libraries to output .jff files in XML format that JFLAP can read

StateMachine - Contains the Python classes for representing finite automata and turing machines. Note the reason why this file is called StateMachine instead of finite automata is to avoid confusion between finite automata and turing machines, though students should know that these are all equivalent as any FA can be represented as a TM and vice versa. Also houses functions to parse a state machine from a given filename.

JSFLAPReader - Reads the automaton definition output file from 

Future Features:
*Possibly add an option to save a JSFLAP file and create a new JSFLAP page with the same states/edges. Due to how the automaton output option is structured from the JSFLAP site, the relative locations of each state is not saved, so when creating a JFLAP file, their locations are randomized.