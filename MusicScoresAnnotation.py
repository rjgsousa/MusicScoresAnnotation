#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
# Coded by Ricardo Sousa, 2007
# rsousa at rsousa dot org
# Check License with this code

from Tkinter import *
from PIL import Image, ImageTk
import sys, copy

# global variables
line = 1
data = {}
listposition = []

# stack for undo operations
stackundo = []
# stack for o undo operations on new lines
stackundo2 = []

# hack for zoom
scaleFactor = 1

# radius for the circle which will be drawn
pointerradius = 5

#
canvasposx = 0
canvasposy = 0

#
flag = 0
not_newline = 1

# Novo
dot_num = 1

def mouseMove(event):
    print canvas.canvasx(event.x), canvas.canvasy(event.y)


def keypressed(event):
    global outfile, stackundo, stackundo2, data,flag,listposition,line,canvasposx, canvasposy, not_newline, dot_num
    if event.keysym == "q":
        if flag == 0:
            data[line] = copy.deepcopy(listposition)
        for i,v in data.iteritems():
            xpto = v
            for x,y in xpto:
                string = str(x)+";"+str(y)+";"
                outfile.write(string)
            outfile.write("\n")

        outfile.close()
        sys.exit(0)
        
    elif event.keysym == "u":

        if len(stackundo) != 0:
            identification = stackundo.pop()
            canvas.delete(identification)

            if (len(listposition) > 0):
                canvasposx, canvasposy = listposition[-1]
                listposition = listposition[0:-1]
                dot_num -= 1
                
            else:
                dot_num -= 1
                if len(stackundo2) != 0:
                    identification = stackundo2.pop()
                    canvas.delete(identification)
					
					
                    if (data.has_key(line-1)):
                        listposition = copy.deepcopy(data[line-1])
                        listposition = listposition[0:-1]
                        del data[line-1]
                        line = line - 1
                        dot_num = 1

            if (len(listposition) == 0):
                not_newline = 1
            
            canvasposx = (canvasposx-1)*scaleFactor
            canvasposy = (canvasposy-1)*scaleFactor

        else:
            print "No elements to undo"

    #print data

# newline print
def printnewline(event):
    global outfile, line, data, listposition, flag, stackundo, canvasposx, canvasposy, not_newline, dot_num
    pos = 10
    if not_newline == 0:
        identification = canvas.create_oval((canvasposx + pos), (canvasposy - pointerradius),
                                            (canvasposx + pos+pos), (canvasposy + pointerradius),
                                            fill="red")

        stackundo2.append(identification)
        not_newline = 1
        dot_num = 1
    else:
        return
        
    data[line] = copy.deepcopy(listposition)

    line = line + 1
    del listposition[:]
    flag = 1

# if you click with the left button of our mouse, it prints the coordinates divided
# by a given scale factor
def leftclick(event):
    global i, outfile,stackundo, listposition, flag, canvasposx, canvasposy, not_newline, dot_num
    canvasposx = canvas.canvasx(event.x)
    canvasposy = canvas.canvasy(event.y)
    
    identification = canvas.create_oval((canvasposx - pointerradius), (canvasposy - pointerradius),
                                        (canvasposx + pointerradius), (canvasposy + pointerradius),
                                        fill="green")
    stackundo.append(identification)
    
    listposition.append( (int(canvasposx/scaleFactor+1), int(canvasposy/scaleFactor+1)) )
    flag = 0
    not_newline = 0
	
    if dot_num == 1:
        print "===> New line <==="
        print dot_num.__str__() + " dots marked"
    else:
        print dot_num.__str__() + " dots marked"
    dot_num += 1


# input filename
infile = sys.argv[1]

# output filename
outfile = open(infile+".csv","w")
	
# root window
root = Tk()

# opens the image
image = Image.open(infile)

# largura e altura da imagem
width, height = image.size

# faz um zoom de scaleFactor à imagem
image = image.resize((width*scaleFactor,height*scaleFactor))

# transforma a imagem que se encontra em PIL para Tkinter
photo = ImageTk.PhotoImage(image)

# cria um canvas
canvas = Canvas(root, width=photo.width(),height=photo.height(),
                scrollregion = (0,0, photo.width(), photo.height()) )

# cria uma imagem no canvas
item = canvas.create_image(0, 0, anchor=NW, image=photo)

# adiciona as scrollbars
canvas.scrollX = Scrollbar(canvas, orient=HORIZONTAL)
canvas.scrollY = Scrollbar(canvas, orient=VERTICAL)

# eventos para as scrollbars
canvas['xscrollcommand'] = canvas.scrollX.set
canvas['yscrollcommand'] = canvas.scrollY.set
canvas.scrollX['command'] = canvas.xview
canvas.scrollY['command'] = canvas.yview

# quero que as scrollbars estejam preenchidas em todo o canvas
canvas.scrollX.pack(side=BOTTOM, fill=X)
canvas.scrollY.pack(side=RIGHT, fill=Y)

# o mesmo para o canvas
canvas.pack(fill=BOTH,expand=1)

# eventos para o rato
#canvas.bind('<Motion>',mouseMove)
canvas.bind('<Button-1>',leftclick)
canvas.bind('<Button-3>',printnewline)
root.bind('<KeyPress>',keypressed)

# mantem o janela activa
root.mainloop()
