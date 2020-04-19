from PIL import Image, ImageDraw,ImageFont
import math

def make_graph(data,healthy):
    width = 1000
    height = 500

    final = []
    temp = [0,0,0,healthy]

    for x in range(len(data)):
        if x % 4 == 0:
            final.append(temp)
            temp = [0,0,0,healthy]

        frame = data[x]

        cam_inf = 0
        cam_rec = 0
        cam_ded = 0
        cam_gud = 0
        for node in frame:
            if node[0]:
                cam_inf += 1
            elif node[1]:
                cam_rec += 1
            elif node[2]:
                cam_ded += 1

        cam_inf = cam_inf-temp[0] if cam_inf-temp[0] >= 0 else 0
        cam_rec = cam_rec-temp[1] if cam_rec-temp[1] >= 0 else 0
        cam_ded = cam_ded-temp[2] if cam_ded-temp[2] >= 0 else 0
        cam_gud = temp[3] - (healthy - (cam_inf+cam_ded+cam_rec)) if temp[3] - (healthy - (cam_inf+cam_ded+cam_rec)) >= 0 else 0

        temp[0] += cam_inf
        temp[1] += cam_rec
        temp[2] += cam_ded
        temp[3] -= cam_gud

    return final

def base_graph(nums,max_v):
    #setup
    font = ImageFont.truetype("arial.ttf",size=15)
    width = 0
    height = 500

    start = [70,height-50]

    graph_y = height-(height-start[1])
    graph_x = start[0]

    amount = len(nums)
    width = 500 + int( math.floor(amount/10)*400 )
    lines_x = int((width-int(start[0]/2))/(amount+1))

    heighest = 0
    for x in nums:
        if heighest < x[0] or heighest < x[1] or heighest < x[2]:
            heighest = max(x)
 
    lines_y = int(height-int((height-start[1])/2))/11

    #define image variables
    im = Image.new("RGB",[width,height],"Black")
    draw = ImageDraw.Draw(im) 

    #draw graph
    draw.text([start[0]-5,(start[1])],"0",fill=(255,255,255),font=font)

    draw.line((graph_x,graph_y,   graph_x,0), fill=(255,255,255),width=2)
    draw.line((graph_x,graph_y,   width,graph_y),fill=(255,255,255),width=2)

    top = 0
    bottom = start[1]
    #draw y
    y_values = []
    for x in range(10):
        if x == 0:
            top = int(lines_y*(x+1)-20)
        
        pix_y = int(lines_y*(x+1)-20)
        pers = ((bottom-top)-(pix_y+graph_y))/(bottom-top)*100
        val = int((heighest/100*pers) * -1)
        if val > max_v:
            val = max_v
        y_values.append([pix_y,val])

    y_values.reverse()
    for x in range(len(y_values)):
        var = y_values[x]
        pix_y = var[0]
        val = var[1]

        draw.line(  (graph_x,pix_y,  graph_x-5,pix_y), fill=(255,255,255), width=2  )
        off = (len(str(val))-1) * 10
        draw.text( (graph_x-20 - off,lines_y*(x+1)-30),text=str(val), fill=(255,255,255), font=font )

    #draw x
    for x in range(amount):
        draw.line( ( (lines_x*(x+1))+start[0],graph_y, (lines_x*(x+1))+start[0],graph_y+5), fill=(255,255,255), width=2)
        draw.text( (lines_x*(x+1)+start[0]-5,graph_y+10), text=str(x+1), fill=(255,255,255), font = font )

    #draw actual graph



    #Draw lines
    def draw_graph(nums,ind,col):
        y_list = []
        for x in range(len(nums)):
            val = nums[x][ind]
            pers = val/heighest*100
            if pers > 100:
                pers = 100

            ypos = int(start[1] - ((bottom-top) / 100 * pers))

            xpos = (lines_x*(x+1))+start[0]
            y_list.append([xpos,ypos])
            draw.ellipse([xpos-2,ypos-2,xpos+2,ypos+2],fill=col,width=2)
        
        for x in range(len(y_list)-1):
            v = y_list[x]
            v1 = y_list[x+1]

            draw.line([v[0],v[1],  v1[0],v1[1]],fill=col,width=1)

    draw_graph(nums,0,(255,0,0))
    draw_graph(nums,1,(100,100,100))
    draw_graph(nums,2,(0,0,255))
    draw_graph(nums,3,(255,255,255))

    im.show()