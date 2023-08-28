import csv
import os
import png #install pypng via pip for this module

snapshots = []

class snapshot:
    time = ""
    territoryAssignments = []

columnHeaders = []
             
colours = {
            "Ventrue":(145,44,238),
            "Carthian":(255,0,255),
            "Gangrel":(154,255,154),
            "Mekhet":(0,229,238),
            "Ordo":(255,128,0),
            "Nosferatu":(156,102,31),
            "Crone":(0,201,87),
            "Invictus":(238,0,0),
            "Daeva":(16,113,229),
            "Court":(40,40,40),
            "Lance":(255,246,143),   
            "Unassigned":(80,80,80),
            "Prince":(192,192,192),
            "Available":(255,255,255)
}

placementsvg = open("birminghamWardsTemplate.svg", 'r').read()

with open('territoryHistory.csv', newline='') as csvfile:
    territorycsv = csv.reader(csvfile, delimiter=',', quotechar='|')
    firstRowComplete = False
    
    for row in territorycsv:
        if not firstRowComplete: #then it's the first row, and the rest of them tell us the category headers
            for s in row:
                if not "Time" in str(s):
                    columnHeaders.append(s)
            firstRowComplete = True
        else:       
            newSnapshot = snapshot()
            newSnapshot.time = str(row[0])
            territoryAssignments = []
            for s in row:
                if not s == str(row[0]):
                    territoryAssignments.append(s)
            newSnapshot.territoryAssignments = territoryAssignments
            snapshots.append(newSnapshot)      

def colToHex(rgbTuple):
    return '#%02x%02x%02x' % rgbTuple

if not os.path.exists("./output"):
  os.mkdir("./output")

for s in snapshots:
    timeCorrected = s.time.split(" ")
    newSvgText = placementsvg.replace(">BBN<",">"+timeCorrected[2] + "/" + timeCorrected[1] +"/" + timeCorrected[0]+"<")
        
    for i in range(len(columnHeaders)):
        colAsHex = colToHex(colours[s.territoryAssignments[i]])
       
        if not ("\""+columnHeaders[i]+"\"\n   style") in newSvgText: #this is temp
            print("A shape was missing from the SVG!")
            print("\nSVG DID NOT CONTAIN A SHAPE FOR:"+columnHeaders[i]+"\n")
            print("Exiting...")
            #exit()
            
        newSvgText = newSvgText.replace("\""+columnHeaders[i]+"\"\n   style=\"fill:#00ff00","\""+columnHeaders[i]+"\"\n   style=\"fill:"+colAsHex)
    
    with open("./output/"+s.time + '.svg', 'w') as f:
        f.write(newSvgText)      

print("Done, check output folder")