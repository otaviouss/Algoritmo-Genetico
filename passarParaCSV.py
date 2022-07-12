import csv

with open('dadosMaquinasGeradoras.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(" ") for line in stripped if line)
    with open('dadosGeradoras.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('unidadeGeradora', 'Pi_min', 'pi_max', 'A', 'b', 'c', 'e', 'f'))
        writer.writerows(lines)
in_file.close()