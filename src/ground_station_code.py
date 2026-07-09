
from cmath import sqrt
from this import d
import cv2   #BGR 
import numpy as np
np.seterr(over='ignore')
import math
from math import pi
import bluetooth
from socket import socket as Socket
from time import sleep

HOST, PORT = '192.168.4.1', 3000

socket = Socket()

def connect ():
    socket.connect((HOST, PORT))
    print("connection...")
   


def x(x):
    return x+1
#arr = np.array([1, 2, 3, 4, 5])
 
#Global variable*********************************************************************************
cap = cv2.VideoCapture(1)
error=0
squ_red_x=50      #BGR
squ_red_y=130
squ_green_x=50
squ_green_y=530
squ_blue_x=420
squ_blue_y=530
black_s_x=0
black_s_y=0  
green_x=0
green_y=0
red_x=0
red_y=0
min_way=0
dis=0
angle_robot_earth=0
order=01
count=0
#Function****************************************************************************************
def find_angle(x_1,x_2,y_1,y_2):
    c=0
    
    
    while(c==0):
        try:
            x_1=(int)(x_1)
            x_2=(int)(x_2)
            y_1=(int)(y_1)
            y_2=(int)(y_2)
            c=c+1
            x_delta =((x_2)-(x_1))
            y_delta =((y_2)-(y_1))
            angle=math.atan2(y_delta,x_delta)*180/pi
            if(angle<0):
                angle=abs(angle)
            else:
                angle=360-angle
            return angle
        except:
            c=c-1
            return "not found"

def angle_robot(frame):
    count=0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))
    detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,param2 = 30, minRadius = 10, maxRadius = 50)
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            y, x, r = pt[0], pt[1], pt[2]
            circle=frame[x,y]
            if(circle[0]<70 and circle[1]<70 and circle[2]<70):
                black_s_x=x
                black_s_y=y
                count=count+1
            # elif(circle[0]>100 and circle[1]>100 and circle[2]>100):
            #     black_e_x=x
            #     black_e_y=y
            #     count=count+1
        if(count==1):
            #ang=find_angle(black_e_x,black_s_x,black_e_y,black_s_y)
            ang=20
            if(ang=="not found"):
                return "not found"
            else:
                return [ang, black_s_x,black_s_y]
        else:
            return "not found"

def distance(x1,x2,y1,y2):
    c=0
    while(c==0):
        try:
            c=c+1
            value1=(abs(x1-x2))
            value1=value1*value1
            value2=(abs(y1-y2))
            value2=value2*value2
            
            return math.sqrt(value1+value2)
        except:
            c=c-1

def check_way():
    #*****1*****  red/green/blue
    dis=distance(black_s_x,red_x,black_s_y,red_y)+distance(red_x,squ_red_x,red_y,squ_red_y)+distance(squ_red_x,green_x,squ_red_y,green_y)+distance(green_x,squ_green_x,green_y,squ_green_y)+distance(squ_green_x,blue_x,squ_green_y,blue_y)+distance(blue_x,squ_blue_x,blue_y,squ_blue_y)
    min_way=dis
    order=[[red_x,red_y],[squ_red_x,squ_red_y],[green_x,green_y],[squ_green_x,squ_green_y],[blue_x,blue_y],[squ_blue_x,squ_blue_y]]
    #*****2*****  red/blue/green
    dis=distance(black_s_x,red_x,black_s_y,red_y)+distance(red_x,squ_red_x,red_y,squ_red_y)+distance(squ_red_x,blue_x,squ_red_y,blue_y)+distance(blue_x,squ_blue_x,blue_y,squ_blue_y)+distance(squ_blue_x,green_x,squ_blue_y,green_y)+distance(green_x,squ_green_x,green_y,squ_green_y)
    if(dis<min_way):
        min_way=dis
        order=[[red_x,red_y],[squ_red_x,squ_red_y],[blue_x,blue_y],[squ_blue_x,squ_blue_y],[green_x,green_y],[squ_green_x,squ_green_y]]
    #*****3*****  blue/red/green
    dis=distance(black_s_x,blue_x,black_s_y,blue_y)+distance(blue_x,squ_blue_x,blue_y,squ_blue_y)+distance(squ_blue_x,red_x,squ_blue_y,red_y)+distance(red_x,squ_red_x,red_y,squ_red_y)+distance(squ_red_x,green_x,squ_red_y,green_y)+distance(green_x,squ_green_x,green_y,squ_green_y)
    if(dis<min_way):
        min_way=dis
        order=[[blue_x,blue_y],[squ_blue_x,squ_blue_y],[red_x,red_y],[squ_red_x,squ_red_y],[green_x,green_y],[squ_green_x,squ_green_y]]
    #*****4*****  blue/green/red
    dis=distance(black_s_x,blue_x,black_s_y,blue_y)+distance(blue_x,squ_blue_x,blue_y,squ_blue_y)+distance(squ_blue_x,green_x,squ_blue_y,green_y)+distance(green_x,squ_green_x,green_y,squ_green_y)+distance(squ_green_x,red_x,squ_green_y,red_y)+distance(red_x,squ_red_x,red_y,squ_red_y)
    if(dis<min_way):
        min_way=dis
        order=[[blue_x,blue_y],[squ_blue_x,squ_blue_y],[green_x,green_y],[squ_green_x,squ_green_y],[red_x,red_y],[squ_red_x,squ_red_y]]
    #*****5*****  green/blue/red
    dis=distance(black_s_x,green_x,black_s_y,green_y)+distance(green_x,squ_green_x,green_y,squ_green_y)+distance(squ_green_x,blue_x,squ_green_y,blue_y)+distance(blue_x,squ_blue_x,blue_y,squ_blue_y)+distance(squ_blue_x,red_x,squ_blue_y,red_y)+distance(red_x,squ_red_x,red_y,squ_red_y)
    if(dis<min_way):
        min_way=dis
        order=[[green_x,green_y],[squ_green_x,squ_green_y],[blue_x,blue_y],[squ_blue_x,squ_blue_y],[red_x,red_y],[squ_red_x,squ_red_y]]
    #*****6*****  green/red/blue
    dis=distance(black_s_x,green_x,black_s_y,green_y)+distance(green_x,squ_green_x,green_y,squ_green_y)+distance(squ_green_x,red_x,squ_green_y,red_y)+distance(red_x,squ_red_x,red_y,squ_red_y)+distance(squ_red_x,blue_x,squ_red_y,blue_y)+distance(blue_x,squ_blue_x,blue_y,squ_blue_y)
    if(dis<min_way):
        min_way=dis
        order=[[green_x,green_y],[squ_green_x,squ_green_y],[red_x,red_y],[squ_red_x,squ_red_y],[blue_x,blue_y],[squ_blue_x,squ_blue_y]]
    
    return order

def second_processing(order):
    for i in range(3):
        # for x in range(40):
        #     print(500)
        for u in range(20):
            ret,frame = cap.read() 
            test=angle_robot(frame)
            while(test=="not found"):
                ret,frame = cap.read()
                test=angle_robot(frame)
            angle_robot_earth=test[0]
            black_s_x=test[1]
            black_s_y=test[2]
            angle2=find_angle(black_s_x,order[i*2][0],black_s_y,order[i*2][1])
            while(angle2=="not found"):
                ret,frame = cap.read()
                test=angle_robot(frame)
                while(test=="not found"):
                    ret,frame = cap.read()
                    test=angle_robot(frame)
                angle_robot_earth=test[0]
                black_s_x=test[1]
                black_s_y=test[2]       
                angle2=find_angle(black_s_x,order[i*2][0],black_s_y,order[i*2][1])
            angle3=(int)(angle2)
            angle3=angle3+180
            if(angle3>=360):
                angle3=angle3-360
            angle3=(str)(angle3)
            socket.send(angle3.encode())
            socket.send(f' '.encode())
            print(angle3)
            # while(1):
            #     print(order[i*2][0])
            #     print(order[i*2][1])
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break
            
        while((black_s_x>order[i*2][0]+35 or black_s_x<order[i*2][0]-35)and(black_s_y>order[i*2][1]+35 or black_s_y<order[i*2][1])-35):
            angle3=(int)(angle2)
            angle3=angle3+180
            if(angle3>=360):
                angle3=angle3-360
            angle3=(str)(angle3)
            socket.send(angle3.encode())
            socket.send(f' '.encode())
            print(angle3)
            ret,frame = cap.read() 
            test=angle_robot(frame)
            while(test=="not found"):
                ret,frame = cap.read()
                test=angle_robot(frame)
            angle_robot_earth=test[0]
            black_s_x=test[1]
            black_s_y=test[2]
            angle2=find_angle(black_s_x,order[i*2][0],black_s_y,order[i*2][1])
            while(angle2=="not found"):
                ret,frame = cap.read()
                test=angle_robot(frame)
                while(test=="not found"):
                    ret,frame = cap.read()
                    test=angle_robot(frame)
                angle_robot_earth=test[0]
                black_s_x=test[1]
                black_s_y=test[2]       
                angle2=find_angle(black_s_x,order[i*2][0],black_s_y,order[i*2][1])
            #************************************************************************************
        #print((str)(angle3))
        for j in range(5):
            print(600)
            socket.send(f'600 '.encode())
        # while(1):
        #     print(i)
        #     print((i*2)+1)
        #     print(order[(i*2)+1][0])
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        message="u"
        while(message!=b'g'):
            print(message)
            #message=sock.recv(1)
        # while(1):
        #     print("uuuuuuuu")
        # #     print((i*2)+1)
        # #     print(order[(i*2)+1][0])
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        ret,frame = cap.read() 
        test=angle_robot(frame)
        while(test=="not found"):
            ret,frame = cap.read()
            test=angle_robot(frame)
        angle_robot_earth=test[0]
        black_s_x=test[1]
        black_s_y=test[2]
        angle2=find_angle(black_s_x,order[(i*2)+1][0],black_s_y,order[(i*2)+1][1])
        while(angle2=="not found"):
            ret,frame = cap.read()
            test=angle_robot(frame)
            while(test=="not found"):
                ret,frame = cap.read()
                test=angle_robot(frame)
            angle_robot_earth=test[0]
            black_s_x=test[1]
            black_s_y=test[2]       
            angle2=find_angle(black_s_x,order[(i*2)+1][0],black_s_y,order[(i*2)+1][1])
        while((black_s_x>order[(i*2)+1][0]+10 or black_s_x<order[(i*2)+1][0]-10)and(black_s_y>order[(i*2)+1][1]+10 or black_s_y<order[(i*2)+1][1])-10):
            angle3=(int)(angle2)
            angle3=angle3+180
            if(angle3>=360):
                angle3=angle3-360
            angle3=(str)(angle3)
            socket.send(angle3.encode())
            socket.send(f' '.encode())
            print(angle3)
            ret,frame = cap.read() 
            test=angle_robot(frame)
            while(test=="not found"):
                ret,frame = cap.read()
                test=angle_robot(frame)
            angle_robot_earth=test[0]
            black_s_x=test[1]
            black_s_y=test[2]
            angle2=find_angle(black_s_x,order[(i*2)+1][0],black_s_y,order[(i*2)+1][1])
            while(angle2=="not found"):
                ret,frame = cap.read()
                test=angle_robot(frame)
                while(test=="not found"):
                    ret,frame = cap.read()
                    test=angle_robot(frame)
                angle_robot_earth=test[0]
                black_s_x=test[1]
                black_s_y=test[2]       
                angle2=find_angle(black_s_x,order[(i*2)+1][0],black_s_y,order[(i*2)+1][1])
        for x in range(5):
            print(500)
            socket.send(f'500 '.encode())
        message2="u"
        while(message2!=b'd'):
            print(message2)
            #message2=sock.recv(1)
            
        
    
#main********************************************************************************************
#first processing********************************************************************************
ret,frame = cap.read()
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
gray_blurred = cv2.blur(gray, (3, 3))
detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,param2 = 30, minRadius = 10, maxRadius = 50)
if detected_circles is not None:
    detected_circles = np.uint16(np.around(detected_circles))
    for pt in detected_circles[0, :]:
        y, x, r = pt[0], pt[1], pt[2]
        circle=frame[x,y]
        print(circle,"rrr")
        if(circle[0]<50 and circle[1]<50 and circle[2]<50):
            black_s_x=x
            black_s_y=y
            cv2.circle(frame, (y, x), r, (0, 255, 255), 2)
            print("a",circle)
        # elif(circle[0]>90 and circle[1]>90 and circle[2]>90):
        #     black_e_x=x
        #     black_e_y=y
        #     cv2.circle(frame, (y, x), r, (0, 255, 255), 2)
        #     print("b",circle)
        elif(circle[0]>circle[1] and circle[0]>circle[2] and circle[2]<70 and circle[0]>80):
            blue_x=x
            blue_y=y
            cv2.circle(frame, (y, x), r, (0, 255, 255), 2)
            print("c",circle)
        elif(circle[1]>circle[0] and circle[1]>circle[2]and circle[1]>80):
            green_x=x
            green_y=y
            cv2.circle(frame, (y, x), r, (0, 255, 255), 2)
            print("e",circle)
        else:
            red_x=x
            red_y=y
            cv2.circle(frame, (y, x), r, (0, 255, 255), 2)
            print("z",circle)
        
    while(1):
        cv2.imshow("Detected Circle", frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
order=check_way()
#order=[[green_x,green_y],[squ_green_x,squ_green_y],[blue_x,blue_y],[squ_blue_x,squ_blue_y],[red_x,red_y],[squ_red_x,squ_red_y]]
order=[[green_x,green_y],[squ_green_x,squ_green_y],[red_x,red_y],[squ_red_x,squ_red_y],[blue_x,blue_y],[squ_blue_x,squ_blue_y]]
cv2.line(frame, (black_s_y,black_s_x), (order[0][1], order[0][0]), (255, 0, 0), thickness=4, lineType=cv2.LINE_AA)
cv2.line(frame, (order[0][1], order[0][0]), (order[1][1], order[1][0]), (255, 255, 0), thickness=4, lineType=cv2.LINE_AA)

cv2.line(frame, (order[1][1], order[1][0]), (order[2][1], order[2][0]), (255, 255, 255), thickness=4, lineType=cv2.LINE_AA)
cv2.line(frame, (order[2][1], order[2][0]), (order[3][1], order[3][0]), (0, 0, 0), thickness=4, lineType=cv2.LINE_AA)
cv2.line(frame, (order[3][1], order[3][0]), (order[4][1], order[4][0]), (0, 255, 0), thickness=4, lineType=cv2.LINE_AA)
cv2.line(frame, (order[4][1], order[4][0]), (order[5][1], order[5][0]), (255, 0, 0), thickness=4, lineType=cv2.LINE_AA)
while(1):
    cv2.imshow("Detected Circle", frame) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print("Wait for the connection...")
connect ()
while(1):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
second_processing(order)




        
cap.release()
cv2.destroyAllWindows()




