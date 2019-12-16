
csv = open("movie_metadata.csv", "r")
final = open("movie_metadata_final.csv", "w")

# discard first line
line = csv.readline()

while True:
    line = csv.readline().replace("&", "and")
    elements = line.split(",")
    if not line:
        break
    if "None" in elements or "" in elements:
        continue
    final.write(line)

final.close()
csv.close()
