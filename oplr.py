import tkinter as tk
import pickle
from tkinter import filedialog
from tkinter import font
from tkinter import *
import webbrowser
import csv
import operator

mydict={}
orderedpubs=[]
currentpub=0
currentpos=0
filename=""
buttonpress=0

# this function opens a dialog box to select a pickle file to open
# that pickle file (currently generated by labtree_construct) is a dictionary with two main
# keys : "pubs" (which is a google scholar list of pubs objects) and "labels" which is the
# corresponding list of labels.
# labels[1] will include all the labels of pub #1 as keys, for example :
# labels[1] = {"labelled":True, "robotic":1, "architecture":1}
# labels["list"] includes the list of all existing labels in the file.
# labels["list"] = {"robotic":0, "architecture":0}
# the associated number will indicate (in the future) the number of time each label has been
# used
def openpickle():
    global mydict
    global filename
    global currentpub
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pickle files","*.pickle"),("all files","*.*")))
    # we only do something if a filename was selected 
    if filename != '':
        with open(filename, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
            mydict = pickle.load(f)
        # we check very quickly that the file has at least a "labels" key
        # it is not sufficient to be sure the format is OK but it is likely the
        # format is ok if "labels" is here, unless the pickle was constructed by
        # a totally new script
        if "labels" not in mydict:
            print("error: this pickle file doesn't have labels in structure")
        else:
            repairpickle()
            # we display a new pub
            ordering()
            nextpub()
            # we display the labels
            definelabels()
            # we add buttons to deal with the pubs
            pubbuttonscreate()

# add all buttons relative to publications
def pubbuttonscreate():
    global buttonpress
    if buttonpress == 0:
        # ordering buttons
        btn_c3 = tk.Radiobutton(master=frm_menu, text='Cited',variable=order, value=3, command=ordering)
        btn_c3.pack(side=tk.RIGHT)
        btn_c2 = tk.Radiobutton(master=frm_menu, text='Year',variable=order, value=2, command=ordering)
        btn_c2.pack(side=tk.RIGHT)
        btn_c1 = tk.Radiobutton(master=frm_menu, text='ID',variable=order, value=1, command=ordering)
        btn_c1.pack(side=tk.RIGHT)

        btn_c1.select()

        lbl_ordering = tk.Label(master=frm_menu,text="Order by: ")
        lbl_ordering.pack(side=tk.RIGHT)
        
        # X and Next Pub buttons
        btn_del = tk.Button(master=frm_buttons, text="X", width=3, height=1, fg='red', command=delbuttonpress)
        btn_del.pack(side=tk.LEFT, padx=10, pady=10)
        btn_next = tk.Button(master=frm_buttons, text="Mark as Labelled", width=16, height=1, command=nextbuttonpress)
        btn_next.pack(side=tk.LEFT, padx=10, pady=10)

        # Nav buttons
        btn_navprev = tk.Button(master=frm_nav2, text="<", width=3, height=1, command=navprev)
        btn_navprev.pack(side=tk.LEFT, padx=10, pady=10)
       
        btn_navnext = tk.Button(master=frm_nav, text=">", width=3, height=1, command=navnext)
        btn_navnext.pack(side=tk.LEFT, padx=10, pady=10)

        buttonpress=1

# this function set the current pub as "labelled" and go to next pub
# but doesn't save ! only adding a new label actually saves
# this is to avoid the "oops double clicked on next !" problem
# (you can just close the app to reset)
def nextbuttonpress():
    global mydict
    global currentpub
    mydict["labels"][currentpub]["labelled"] = True
    nextpub()    

# this function ask for confirmation, then delete the publication from the pickle
def delbuttonpress():
    global mydict
    global currentpub
    global window
    window_popup = Toplevel()

    def cancelbuttonpress():
        window_popup.destroy()
        window_popup.update()
    
    def confirmbuttonpress():
        window_popup.destroy()
        window_popup.update()
        mydict["pubs"].pop(currentpub, None)
        mydict["labels"].pop(currentpub, None)
        ordering()
        nextpub()
        
    x = window.winfo_x()
    y = window.winfo_y()
    window_popup.geometry("%dx%d+%d+%d" % (400, 200, x + 300, y + 300))
   
    lbl_confirm = tk.Message(master=window_popup, text="Are you sure you want to delete this publication from the list ? It will delete it from the pickle irremediably.")
    lbl_confirm.pack(side=tk.TOP, fill = tk.BOTH, padx=10, pady=10)
    # frame for the buttons.
    frm_delbuttons = tk.Frame(master=window_popup)
    frm_delbuttons.pack(side=tk.TOP, padx=10, pady=10)
    # button cancel
    btn_cancel = tk.Button(master=frm_delbuttons, text="Cancel", width=6, height=1, command=cancelbuttonpress)
    btn_cancel.pack(side=tk.LEFT, padx=10, pady=10)
    # button confirm
    btn_confirm = tk.Button(master=frm_delbuttons, text="Delete", width=6, height=1, fg='red', command=confirmbuttonpress)
    btn_confirm.pack(side=tk.LEFT, padx=10, pady=10)

    window_popup.mainloop()



# this function displays a new publication
def nextpub():
    global mydict
    global currentpub
    global currentpos
    # For every publication, we check :
    for n in range(len(orderedpubs)):
        pub = orderedpubs[n]
        # if the publication has never been labelled, we display it and we stop there
        if mydict["labels"][pub]["labelled"] == False:
            changepub(n)
            break

# go to the previous pub in navigation
def navprev():
    global currentpos
    changepub(currentpos-1)
    
# go to the next pub in navigation
def navnext():
    global currentpos
    changepub(currentpos+1)
    
# change the pub to position "pos"
def changepub(n):
    global mydict
    global currentpub
    global currentpos
    
    if n > len(orderedpubs):
        return
    if n < 0:
        return
    
    pub = orderedpubs[n]
    currentpub=pub
    currentpos=n
    lbl_abstract["text"] = mydict["pubs"][pub]['bib']['abstract']
    lbl_title["text"] = mydict["pubs"][pub]['bib']['title']
    subtitle = ""
    for a in mydict["pubs"][pub]['bib']['author']:
        if subtitle == "":
            subtitle = a
        else:
            subtitle = subtitle + ", " + a
    subtitle = subtitle + " (" + mydict["pubs"][pub]['bib']['pub_year'] + ")"
    subtitle = subtitle + " [" + str(mydict["pubs"][pub]['num_citations']) + "]"
    lbl_subtitle["text"] = subtitle
    lbl_link["text"] = mydict["pubs"][pub]['pub_url']
    # we bind a new callback for the url link of the pub
    lbl_link.bind("<Button-1>", lambda e: callback(mydict["pubs"][pub]['pub_url']))
    updatelabels()

# this function open the "url" into the browser
def callback(url):
    webbrowser.open_new(url)

# this function updates the display of the labels of the publication
def updatelabels():
    global mydict
    global currentpub
    global currentpos
    
    # we remove the labels
    for child in frm_currentlabels2.winfo_children():
        child.destroy()
        
    font3 = font.Font(window, ('Arial', 10, 'bold'))
    
    mylabels={}
    mylabelsdel={}
    mylabelsend={}
    for label in mydict['labels'][currentpub]:
        if label != "labelled":
            text = "["+label
            mylabels[label] = tk.Label(master=frm_currentlabels2,text=text,font=font3, bg="#DDDDDD")
            mylabels[label].pack(side=tk.LEFT, fill = tk.BOTH)
            mylabelsdel[label] = tk.Label(master=frm_currentlabels2,text="x",font=font3, fg="red", bg="#DDDDDD")
            mylabelsdel[label].pack(side=tk.LEFT, fill = tk.BOTH)
            mylabelsend[label] = tk.Label(master=frm_currentlabels2,text="]  ",font=font3, bg="#DDDDDD")
            mylabelsend[label].pack(side=tk.LEFT, fill = tk.BOTH)
            mylabelsdel[label].bind("<Button-1>", lambda event,name=label: removelabel(event,name))

    try:
        lbl_nav["text"] = str(currentpos+1)+"/"+str(len(orderedpubs))
    except NameError:
       print("lbl_nav doesn't exist")

    

# this function removes a label "label" from the current publication "currentpub"
# it also saves !
def removelabel(event,num):
    global mydict
    global currentpub
    mydict['labels'][currentpub].pop(num, None)
    updatelabels()
    savepickle()   


# this function add a label "id" to the current publication "currentpub"
# it also saves !
def addlabel(num):
    global mydict
    global currentpub
    mydict['labels'][currentpub][num] = 1
    updatelabels()
    savepickle()

# this function checks that main fields exist and create them if they dont
def repairpickle():
    global mydict
    
    if "labels" not in mydict:
        mydict = {"pubs":mydict,"labels":{"list":{}}}
        
    for pub in mydict['pubs']:
        # if no labels exist for this pub, we create the pub in labels
        if pub not in mydict["labels"]:
            mydict["labels"][pub] = {"labelled":False}
        # if the pub is missing a field, we create it
        if "title" not in mydict["pubs"][pub]['bib']:
            mydict["pubs"][pub]['bib']['title'] = "<NO TITLE>"
        if "pub_year" not in mydict["pubs"][pub]['bib']:
            mydict["pubs"][pub]['bib']['pub_year'] = "<NO YEAR>"
        if "author" not in mydict["pubs"][pub]['bib']:
            mydict["pubs"][pub]['bib']['author'] = "<NO AUTHOR>"
        if "abstract" not in mydict["pubs"][pub]['bib']:
            mydict["pubs"][pub]['bib']['abstract'] = "<NO ABSTRACT>"
        if "pub_url" not in mydict["pubs"][pub]:
            mydict["pubs"][pub]['pub_url'] = "<NO URL>"
        if "num_citations" not in mydict["pubs"][pub]:
            mydict["pubs"][pub]['num_citations'] = "??"
            
    savepickle()
    
# this function save the pickle 
def savepickle():
    global mydict
    global filename
    with open(filename, 'wb') as f:
        pickle.dump(mydict, f, pickle.HIGHEST_PROTOCOL)

# this function creates a whole new label, add it to the menu, and add it to the publication
def newlabel():
    global mydict
    global currentpub
    global filename
    if filename != "":
        toadd = ent_newlabel.get()
        if toadd not in mydict["labels"]["list"]:
            mydict["labels"]["list"][toadd]=0
            newbutton = tk.Button(master=frm_labels,
                             text=toadd,
                             command=lambda toadd=toadd: addlabel(toadd))
            newbutton.pack(side=tk.TOP)
        addlabel(toadd)
    else:
        print("Open a pickle first !")

# this function creates all the "labels" buttons for the first time when the pub is opened    
def definelabels():
    if "labels" in mydict:
        for label in mydict["labels"]["list"]:
            newbutton = tk.Button(master=frm_labels,
                                 text=label,
                                 command=lambda label=label: addlabel(label))
            newbutton.pack(side=tk.TOP, padx=3, pady=3)

# this function exports the pickled dictionary as a CSV
def csvexport():
    global mydict
    directory = filedialog.asksaveasfilename(defaultextension='.csv',
                                             filetypes=[("csv files", '*.csv')],
                                             title="Choose filename")

    if directory != "":
        with open(directory, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['','title','year','authors','abstract']
            for label in mydict['labels']['list']:
                fieldnames.append(label)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for pub in mydict['pubs']:
                authors = ""
                for author in mydict["pubs"][pub]['bib']['author']:
                    if authors == "" or authors == " ":
                        authors=author
                    else:
                        authors=authors+" and "+author
                        
                pubdict = {'':pub,
                           'title':mydict["pubs"][pub]['bib']['title'],
                           'year':mydict["pubs"][pub]['bib']['pub_year'],
                           'authors':authors,
                           'abstract':mydict["pubs"][pub]['bib']['abstract']}
                
                for ilabel in mydict['labels']['list']:
                    if pub not in mydict["labels"]:
                        pubdict[ilabel]=""
                    elif ilabel in mydict["labels"][pub]:
                        pubdict[ilabel]=1
                    else:
                        pubdict[ilabel]=""
                        
                writer.writerow(pubdict)

# creates the ordered list of publications depending on ID, year, or citations
def ordering():
    global mydict
    global orderedpubs
    if order.get() == 1: #id
        # first we create a list
        ordered = []
        for i in mydict["pubs"]:
            # we convert the key into an integer
            j = -1
            try:
                j = int(i)
            except ValueError:
                pass
            # if that worked, we add that integer to the list
            if j != -1:
                ordered.append(j)
        # we now have a list of IDs, we sort it
        sorted(ordered)
        orderedpubs=ordered
        
    if order.get() == 2: #year
        # first we create a dictionary with the IDs as key and the year as value
        newdict = {}
        for i in mydict["pubs"]:
            newdict[i] = mydict["pubs"][i]["bib"]["pub_year"]
        # then we sort it, which will give us a list of tuples
        sorted_dict = sorted(newdict.items(), key=operator.itemgetter(1))
        # we convert that list of tupples into a list of ids
        ordered = []
        for i in sorted_dict:
            ordered.append(i[0])
        orderedpubs=ordered
        
    if order.get() == 3: #cited
        # first we create a dictionary with the IDs as key and the citations as value
        newdict = {}
        for i in mydict["pubs"]:
            newdict[i] = mydict["pubs"][i]['num_citations']
        # then we sort it by desceding order, which will give us a list of tuples
        sorted_dict = sorted(newdict.items(), key=operator.itemgetter(1), reverse = True)
        # we convert that list of tupples into a list of ids
        ordered = []
        for i in sorted_dict:
            ordered.append(i[0])
        orderedpubs=ordered
    nextpub()
    
#creation of the Tk window
window = tk.Tk()

# ordering checkbox
order=IntVar(master=window)
order.set(1)

# menu frame
frm_menu = tk.Frame(master=window, width=200)#, bg="red")
frm_menu.pack(fill=tk.X, side=tk.TOP, padx=20, pady=20)

# "open pickle" button of the menu frame
btn_open = tk.Button(master=frm_menu, text="Open Pickle", width=11, height=1, command=openpickle)
btn_open.pack(side=tk.LEFT, padx=10)

# "export as csv" button of the menu frame
btn_exportcsv = tk.Button(master=frm_menu, text="Export as CSV", width=13, height=1, command=csvexport)
btn_exportcsv.pack(side=tk.LEFT, padx=10)

# publication frame with the abstract etc.
frm_abstract = tk.Frame(master=window, width=800, height=800)
frm_abstract.pack(fill=tk.BOTH, side=tk.LEFT, padx=20, pady=20, expand=True)
frm_abstract.pack_propagate(0) #this is to avoid being resized by content

# navigation frame
frm_nav = tk.Frame(master=frm_abstract)
frm_nav.pack(side=tk.TOP)
frm_nav2 = tk.Frame(master=frm_nav)
frm_nav2.pack(side=tk.LEFT)
lbl_nav = tk.Label(master=frm_nav,text="")
lbl_nav.pack(side=tk.LEFT) 

# this is the title of the publications (default: "Instructions")
font1 = font.Font(window, ('Arial', 12, 'bold'))
lbl_title = tk.Message(master=frm_abstract, text="Instructions", width=750, font=font1, bg="#DDDDDD")
lbl_title.pack(side=tk.TOP, fill = tk.BOTH)

# this is the list of authors and the year of the publications
font2 = font.Font(window, ('Arial', 10, 'italic'))
lbl_subtitle = tk.Message(master=frm_abstract, text="", width=750, font=font2, bg="#DDDDDD")
lbl_subtitle.pack(side=tk.TOP, fill = tk.BOTH)

# this is the text of the abstract (default: explanations about the software)
lbl_abstract = tk.Message(master=frm_abstract, text="Click 'Open Pickle' to open the dictionary created by the labtree_construct script. You can then add new labels or existing ones dynamically for each publications. Your work is saved WHEN YOU ADD A LABEL. So if you click 'next pub' by mistake, just close the program and start it again. Written by Clara Lehenaff for research purpose, feel free to modify whatever needed. Any question ? clara.lehenaff@cri-paris.org", width=750, bg="#DDDDDD")
lbl_abstract.pack(side=tk.TOP, fill = tk.BOTH)

# this is the link to the publication (thus the abstract)
lbl_link = tk.Message(master=frm_abstract, text="", width=750, bg="#DDDDDD", fg='blue')
lbl_link.pack(side=tk.TOP, fill = tk.BOTH)

# this is the frame in which we put the labels associated with the publication
frm_currentlabels = tk.Frame(master=frm_abstract, width=750, bg="#DDDDDD")
frm_currentlabels.pack(side=tk.TOP, fill = tk.BOTH)
# this is a frame in the frame for beauty purpose
frm_currentlabels2 = tk.Frame(master=frm_currentlabels, bg="#DDDDDD")
frm_currentlabels2.pack(side=tk.TOP)

# frame for the buttons.
frm_buttons = tk.Frame(master=frm_abstract)#, bg="yellow")
frm_buttons.pack(side=tk.TOP)

# this is the LABELS frame including all labels that can be added
frm_labels = tk.Frame(master=window, width=200,height=800)#, bg="blue")
frm_labels.pack(fill=tk.BOTH, side=tk.LEFT, padx=20, pady=20, expand=True)

# this is the "new label" text, entry box, and button to validate
lbl_newlabel = tk.Label(master=frm_labels,text="New Label :")
lbl_newlabel.pack(side=tk.TOP, fill = tk.BOTH)

ent_newlabel = tk.Entry(master=frm_labels)
ent_newlabel.pack(side=tk.TOP, fill = tk.BOTH)

btn_newlabel = tk.Button(master=frm_labels, text="Create", width=6, height=1, command=newlabel)
btn_newlabel.pack(side=tk.TOP, fill = tk.BOTH)

# this is a separator
lbl_separat = tk.Label(master=frm_labels,text="---")
lbl_separat.pack(side=tk.TOP, fill = tk.BOTH, padx=10, pady=10)

# title of the software
window.title("Open Paper Labelling for Research (OPLR 1.1)")

# main loop
window.mainloop()