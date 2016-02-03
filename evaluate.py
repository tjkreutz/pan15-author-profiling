import sys

path1 = sys.argv[1]
path2 = sys.argv[2]
languages = ['dutch', 'english', 'spanish', 'italian']

for language in languages:
    file1 = open(path1 + '/' + language + '/truth.txt', 'r')
    file2 = open(path2 + '/' + language + '/truth.txt', 'r') 
    truthdict = {}
    gendercorrect, agecorrect, total = 0,0,0

    for line in file1:
        values = line.split(':::')
        truthdict[values[0]]=(values[1],values[2])

    for line in file2:
        values = line.split(':::')
        if values[0] in truthdict:
            total+=1
            if truthdict[values[0]][0]==values[1]:
                gendercorrect+=1
            if truthdict[values[0]][1]==values[2]:
                agecorrect+=1
    print(language + ':')
    print("{0} correct out of {1}".format(gendercorrect, total))
    print("gender accuracy: {0}".format(gendercorrect/total))
    print("{0} correct out of {1}".format(agecorrect, total))
    print("age accuracy: {0}".format(agecorrect/total))
    print()
        

