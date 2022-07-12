# Read in the file
with open('dadosMaquinasGeradoras.txt', 'r') as file :
  filedata = file.read()
file.close()

# Replace the target string
filedata = filedata.replace(',', '.')

# Write the file out again
with open('teste.txt', 'w') as file:
  file.write(filedata)
file.close()