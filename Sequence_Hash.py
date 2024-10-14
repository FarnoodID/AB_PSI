import time,hashlib
dir = "" #CWD

print("Avg time to wait: 0.04 s")

start = time.time()

ignored = 0
# enter = 0
f = open(dir+"sequenced_Hashed.txt", "w")
with open(dir+"Raw.txt","r") as openfileobject:
    counter = -1
    for line in openfileobject:
        for nucleotide in line:
            newLine = ""
            if nucleotide == "\n":
                # newLine += "\n"
                # enter +=1
                break
            counter +=1
            if nucleotide != "A" and nucleotide != "T" and nucleotide != "C" and nucleotide != "G":
                ignored +=1
                continue
            newLine += (hashlib.sha256((nucleotide + str(counter)).encode()).hexdigest())
            newLine +="\n"
            f.write(newLine)
        # print(newLine)
    # f.write(newLine)
f.close()        

end = time.time()

print("Time spent:", "{0:.2f}".format(end-start) , "s")
print("Number of ignored nucleotides is:",ignored) 
# print("Number of entered is:",enter) # CodeBy FarnoodID