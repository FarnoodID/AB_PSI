import time
dir = "" # CWD 

print("Avg time to wait: 0.01 s")

start = time.time()

ignored = 0
# enter = 0 # CodeBy FarnoodID
f = open(dir+"sequenced.txt", "w")
with open(dir+"Raw.txt","r") as openfileobject:
    counter = -1
    for line in openfileobject:
        newLine = ""
        for nucleotide in line:
            if nucleotide == "\n":
                # newLine += "\n"
                # enter +=1
                break
            counter +=1
            if nucleotide != "A" and nucleotide != "T" and nucleotide != "C" and nucleotide != "G":
                ignored +=1
                continue
            newLine += (nucleotide + str(counter))
            
        f.write(newLine)
        # print(newLine)
    # f.write(newLine)
f.close()        

end = time.time()

print("Time spent:", "{0:.2f}".format(end-start) , "s")
print("Number of ignored nucleotides is:",ignored)
# print("Number of entered is:",enter)