with open('dadosMaquinasGeradoras.txt', 'r') as in_file :
    stripped = (line.strip() for line in in_file)
    lines = (line.split(" ") for line in stripped if line)

    for line in lines:
        print(line)


in_file.close()


#print(filedata)