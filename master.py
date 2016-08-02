import JFFWriterv2

def main():
    filename = input("What is the name of the JSFLAP file you want to convert? (Don't forget the file extension)\n")
    JFFWriterv2.convertFromJSFLAP2JFLAP(filename)

def test():
    main()

def fixFile(filename):
    file = open(filename, 'w+')
    string = file.read()
    string = string[:19] + 'encoding="UTF-8" standalone="no"' + string[19:]
    f = open('Fixed' + filename, 'w')
    f.write(string)

if __name__ == '__main__':
    main()