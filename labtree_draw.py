from PIL import Image, ImageDraw
import collections
import csv
import random
import math
import operator
from tqdm import tqdm

############ VARIABLES YOU NEED TO CHANGE ######################
filecsv = 'Labtree_ClaraThea.csv'
imgoutput = 'labtree.jpg'
periodsize = 1 # number of years per period of time
###############################################################


# after you clean the CSV, export CSV as dict
with open(filecsv, newline='',encoding='utf-8') as csvfile:
    labreader = csv.reader(csvfile, delimiter=',')
    years = [] #let's just look at all the years first
    header = [] #this is the header
    copy = []
    for row in labreader:
        if row[2] == "year":
            header = row
        else:
            years.append(int(row[2]))
        copy.append(row)
    years.sort()
    
    tree = collections.OrderedDict() #our future tree, ordered
    year = years[0] #first year
    tree[year]={} #creation of the first period, for exemple "2010" for 2010-2014
    
    for y in years:
        if y < year+periodsize: #if y is still in the x year period
            pass
        else: #y is no longer in the x year period, looking for another period...
            while y >= year+periodsize: #as long as y is not in the right x years period
                year = year+periodsize #we add a five years period
                tree[year]={}
    #we now have all our periods in tree, we can now begin to fill tree
    maxpapers = 0
    maxlinks = 0
    for period in tqdm(tree):
        for i in range(5,len(header)):
            tree[period][header[i]] = 0 #we set the number of paper per label to 0
            for j in range(5,len(header)):
                if j>i:
                    tree[period][header[i]+"+"+header[j]] = 0 #we set the links to 0
        for row in copy:
            if row[2] != "year":
                if int(row[2]) >= period and int(row[2]) < period+periodsize: # we are in the period
                    for i in range(5,len(row)): #we iter through labels (row[5] and more)
                        if row[i] == "":
                            row[i] = 0
                        if int(row[i]) == 1: #if the label is true
                            tree[period][header[i]]+=1 #we increase the number of this label in that period
                            if tree[period][header[i]]>maxpapers:
                                maxpapers = tree[period][header[i]]
                            for j in range(5,len(row)): #we iter again through the labels
                                if row[j] == "":
                                    row[j] = 0
                                if j>i and int(row[j])>0: #we construct the link for every label that is also true
                                    tree[period][header[i]+"+"+header[j]]+=1
                                    if tree[period][header[i]+"+"+header[j]]>maxlinks:
                                        maxlinks = tree[period][header[i]+"+"+header[j]]
    
    #let's position each period
    positions = {}
    previous = 0
    first = True
    for period in tqdm(tree):
        # the first time, we have nothing to build on so we start from 0
        if first:
            positions[period] = [] #we will use a simple list to save the positions using the list flexibility
            # we first construct a dict of links
            # and a dict of label
            links = {}
            labels = {}
            for label in tree[period]:
                if "+" in label and tree[period][label]>0:
                    links[label]=tree[period][label]
                if "+" not in label and tree[period][label]>0:
                    labels[label]=tree[period][label]
            #empty dictionaries evaluate to False in python
            if links:
                #we take the bigger one
                bigger = max(links.items(), key=operator.itemgetter(1))[0]
                #we split it to get the two labels
                biglabels = bigger.split("+")
                positions[period].append(biglabels[0])
                positions[period].append(biglabels[1])
                links.pop(bigger, None)
                #now that we have a start, we will build on it
                while links:
                    bigger = max(links.items(), key=operator.itemgetter(1))[0]
                    biglabels = bigger.split("+")
                    if biglabels[0] not in positions[period] and biglabels[1] not in positions[period]:
                        # if none of them is here, we want to first build weaker links until one of them is
                        # this is the only case where we don't build the stronger links first : when the stronger
                        # links are unrelated. 
                        # so we will decrease the strength of the link until it's no longer the best one
                        links[bigger]-=1
                        if links[bigger]<0:
                            links.pop(bigger, None)
                    if biglabels[0] in positions[period] and biglabels[1] not in positions[period]:
                        #only [0] is here, so we plug [1] where [0] is, only if [0] is at beginning or at end
                        # if [0] is in the middle then it already has stronger links ! We do nothing.
                        if biglabels[0] == positions[period][0]:
                            positions[period].insert(0, biglabels[1])
                        if biglabels[0] == positions[period][-1]:
                            positions[period].append(biglabels[1])
                        links.pop(bigger, None)
                    if biglabels[0] not in positions[period] and biglabels[1] in positions[period]:
                        #here it's just the inverse
                        if biglabels[1] == positions[period][0]:
                            positions[period].insert(0, biglabels[0])
                        if biglabels[1] == positions[period][-1]:
                            positions[period].append(biglabels[0])
                        links.pop(bigger, None)
                    # finally, if both of them are already in the table, we also do nothing. (bigger links win)
                    if biglabels[0] in positions[period] and biglabels[1] in positions[period]:
                        links.pop(bigger, None)
            # there is no link, so we just copy the remaining labels one by one
            else:
                print(labels)
                print(period)
                for label in list(labels):
                    if label not in positions[period] and labels[label]>0:
                        positions[period].append(label)
                    labels.pop(label, None)
            #we have finished constructing the first period !
        #now the next periods will inherit the positions of the previous ones
        #however new labels can now be INSERTED, if they validate two conditions :
        # - they need to be new labels (never present before)
        # - their bigger link is bigger than the one they insert
        # - OR a weaker of their links is bigger than the one they insert
        #     if they have no link bigger than a link already in place, they are inserted at the end
        else:
            positions[period] = positions[previous][:] # we copy the previous positionning
            # we first construct a dict of links
            # and a dict of label
            links = {}
            labels = {}
            for label in tree[period]:
                if "+" in label and tree[period][label]>0:
                    links[label]=tree[period][label]
                if "+" not in label and tree[period][label]>0:
                    labels[label]=tree[period][label]
            #empty dictionaries evaluate to False in python
            while links:
                bigger = max(links.items(), key=operator.itemgetter(1))[0]
                biglabels = bigger.split("+")
                if biglabels[0] not in positions[period] and biglabels[1] not in positions[period]:
                    # if none of them is here, we want to first build weaker links until one of them is
                    # this is the only case where we don't build the stronger links first : when the stronger
                    # links are unrelated. 
                    # so we will decrease the strength of the link until it's no longer the best one
                    links[bigger]-=1
                    if(links[bigger]<0):
                        links.pop(bigger, None)
                if biglabels[0] in positions[period] and biglabels[1] not in positions[period]:
                    #only [0] is here, so we plug [1] where [0] is, only if the existing links are not stronger
                    index = positions[period].index(biglabels[0])
                    beforelinkA = positions[period][index]+"+"+positions[period][index-1]
                    if beforelinkA in tree[period]:
                        beforepower = tree[period][beforelinkA]
                    beforelinkB = positions[period][index-1]+"+"+positions[period][index]
                    if beforelinkB in tree[period]:
                        beforepower = tree[period][beforelinkB]
                    afterlinkA = positions[period][index]+"+"+positions[period][index+1]
                    if afterlinkA in tree[period]:
                        afterpower = tree[period][afterlinkA]
                    afterlinkB = positions[period][index+1]+"+"+positions[period][index]
                    if afterlinkB in tree[period]:
                        afterpower = tree[period][afterlinkB]
                    # we just reconstructed the power of this period links around the index we are looking at.
                    # we now compare those powers
                    if beforepower>afterpower and links[bigger]>afterpower:
                        #afterpower is inferior to both, it can be replaced
                        # since it's AFTER, we put the new label between the index and its +1
                        positions[period].insert(index+1, biglabels[1])
                    if afterpower>=beforepower and links[bigger]>beforepower:
                        #beforepower is inferior or equal to afterpower, and inferior to links, it can be replaced
                        # since it's BEFORE, we put the new label between the index and its -1
                        positions[period].insert(index, biglabels[1])
                    # if our new link is weaker than the existing, we do nothing
                    links.pop(bigger, None)
                if biglabels[0] not in positions[period] and biglabels[1] in positions[period]:
                    #only [1] is here, so we plug [0] where [1] is, only if the existing links are not stronger
                    index = positions[period].index(biglabels[1])
                    beforelinkA = positions[period][index]+"+"+positions[period][index-1]
                    if beforelinkA in tree[period]:
                        beforepower = tree[period][beforelinkA]
                    beforelinkB = positions[period][index-1]+"+"+positions[period][index]
                    if beforelinkB in tree[period]:
                        beforepower = tree[period][beforelinkB]
                    afterlinkA = positions[period][index]+"+"+positions[period][index+1]
                    if afterlinkA in tree[period]:
                        afterpower = tree[period][afterlinkA]
                    afterlinkB = positions[period][index+1]+"+"+positions[period][index]
                    if afterlinkB in tree[period]:
                        afterpower = tree[period][afterlinkB]
                    # we just reconstructed the power of this period links around the index we are looking at.
                    # we now compare those powers
                    if beforepower>afterpower and links[bigger]>afterpower:
                        #afterpower is inferior to both, it can be replaced
                        # since it's AFTER, we put the new label between the index and its +1
                        positions[period].insert(index+1, biglabels[0])
                    if afterpower>=beforepower and links[bigger]>beforepower:
                        #beforepower is inferior or equal to afterpower, and inferior to links, it can be replaced
                        # since it's BEFORE, we put the new label between the index and its -1
                        positions[period].insert(index, biglabels[0])
                    # if our new link is weaker than the existing, we do nothing
                    links.pop(bigger, None)
                if biglabels[0] in positions[period] and biglabels[1] in positions[period]:
                    # finally, if both of them are already in the table, we also do nothing.
                    links.pop(bigger, None)
                # !!!!!!!!!!!
                # !!!!! It means we don't reorganize by link size : this is a choice ! might be a wrong one dunno. 
                # !!!!!!!!!!!
            # we just copy the remaining labels one by one
            for label in list(labels):
                if label not in positions[period] and labels[label]>0:
                    positions[period].append(label)
                labels.pop(label, None)
            #we have finished constructing the other periods !          
        # we have constructed the periods
        first = False
        previous = period



    # Our tree is now in a dictionary format. We can start drawing it !
    # Each period should be 1 to 5 years and we don't expect more than 10, max 20 periods (else we're doing it wrong)
    # So let's say a period will be 100 pixels wide
    imgwidth = len(tree)*100
    # We also want labels to display, and expect something like max 20 labels, so 50 px per label sounds about right
    numlabels = len(header)-5
    imgheight = numlabels*50
    
    im = Image.new('RGB', (imgwidth, imgheight), (256, 256, 256))
    draw = ImageDraw.Draw(im)

    #let's first draw the periods
    for i in range(len(tree)):
        draw.line(((i+1)*100, 0, (i+1)*100, imgheight), fill=(210, 210, 210), width=1)
    
    #let's define (random) colors for the labels
    #colors will be between 100 (dark) and 250 (light)
    colors = {}
    random.seed(10) # change the seed if you don't like the colors hahaha
    for i in range(len(header)):
        col1 = 100+int(random.random()*150)
        col2 = 100+int(random.random()*150)
        col3 = 100+int(random.random()*150)
        colors[header[i]]=(col1,col2,col3)    
    # we have the positions, let's draw them
    x=0
    first=True
    for period in tree:
        margin = 50*(math.floor((len(header)-len(positions[period]))/2)-2) # half the empty squares, floored
        if not first:
            for i in range(len(positions[period])):
                if positions[period][i] in positions[previous] and tree[period][positions[period][i]]>0:
                    index = positions[previous].index(positions[period][i])
                    draw.line((x+50, margin+i*50+25, x-50,previousmargin+index*50+25), fill=colors[positions[period][i]], width=1)
        for i in range(len(positions[period])):
            #we draw positions[period][i] which is a label
            size=75*tree[period][positions[period][i]]/maxpapers #this will give something between 0 and 75
            half = (50-size)/2
            draw.chord((x+25+half, margin+i*50+half, x+25+half+size, margin+i*50+half+size), start=0, end=360, fill=colors[positions[period][i]], outline=(0, 0, 0))
                
        first=False
        previous=period
        previousmargin=margin
        x+=100 #next period will be drawn 100 pixels further
    im.save(imgoutput, quality=95)


# order by link strenght (bigger link first, then bigger link of each of the two on each side, etc.
# when this is done, if there is still a bubble left, we place it on the left, and we do it all over again on it
# until no bubble is left.

# then we draw each bubble for every 5 year period