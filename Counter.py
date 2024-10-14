import time
dir = "" # CWD

print("Avg time to wait: 0.04 s")

start = time.time()
goal = 16777216
ignored = 0
# enter = 0
f = open(dir+"output.txt", "w")
with open(dir+"raw.txt","r") as openfileobject:
    counter = 0
    for line in openfileobject:
        newLine = ""
        for nucleotide in line:
            if counter >= goal:
                newLine+="\n"
                f.write(newLine)
                break
            if nucleotide == "\n":
                # newLine += "\n"
                # enter +=1
                newLine +="\n"
                f.write(newLine)
                break
            if nucleotide != "A" and nucleotide != "T" and nucleotide != "C" and nucleotide != "G":
                ignored +=1
                # CodeBy FarnoodID
                continue
            counter +=1
            newLine += nucleotide
            
        if counter >= goal:
            break
            
        # print(newLine)
    # f.write(newLine)
f.close()        

end = time.time()

print("Time spent:", "{0:.2f}".format(end-start) , "s")
print("Number of ignored nucleotides is:",ignored)
# print("Number of entered is:",enter)