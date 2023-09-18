import os
import pandas as pd
import png #install pypng via pip for this module

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

def colToHex(rgbTuple):
    return '#%02x%02x%02x' % rgbTuple

if not os.path.exists("./output"):
  os.mkdir("./output")

placementsvg = open("birminghamWardsTemplate.svg", 'r').read()

df = pd.read_csv('wardmap.csv', index_col=0)

for r in range(0, len(df.index)):   #Go through each row in the dataframe (representing each session)
    t = df.index[r]
    timeCorrected = t.split(" ")

    row = df.iloc[r]    
    newSvgText = placementsvg.replace(">BBN<",">"+timeCorrected[2] + "/" + timeCorrected[1] +"/" + timeCorrected[0]+"<")    #format the date string for this row

    for i in range(0,len(df.columns)):      #For each territory (column) on that date (row)
        territoryName = df.columns[i]                      #Get its name
        territoryAlignment = df.at[t,territoryName]        #Get its value (alignment)
        colAsHex = colToHex(colours[row.iloc[i]])          #Convert that alignment into a colour for the map

        if not ("\""+territoryName+"\"\n   style") in newSvgText:
            print("A shape was missing from the SVG!")
            print("\nSVG DID NOT CONTAIN A SHAPE FOR:"+territoryName+"\n")
            print("Exiting...")
            exit()
            
        newSvgText = newSvgText.replace("\""+territoryName+"\"\n   style=\"fill:#00ff00","\""+territoryName+"\"\n   style=\"fill:"+colAsHex)
    
    with open("./output/"+ t.replace(" ","_") + '.svg', 'w') as f:
        f.write(newSvgText)

print("Done, check output folder")