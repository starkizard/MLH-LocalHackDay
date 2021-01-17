#if 0
import cv2
import numpy as np
import torch
import torch.nn as nn 
import torch.nn.functional as F 
import random
import time 
import os

from LDR import *
from tone import *
from genStroke_origin import *
from drawpatch import rotate
from tools import *
from ETF.edge_tangent_flow import *
from deblue import deblue
from quicksort import *


def TextPrint(str):
    print("\r",end="",flush=True)
    for i in str:
        print(i,end="",flush=True)
        time.sleep([0.07,0.15][i==" "])
    time.sleep(1.3)
    print("\r"+" "*len(str),end="",flush=True)


input_path = './input/CarolMusk.png'
output_path = './output' 

np.random.seed(1)
n =  10                
period = 4             
direction =  10        
Freq = 100             
deepen =  1            
transTone = False      
kernel_radius = 3       
iter_time = 15          
background_dir = None    
CLAHE = True
edge_CLAHE = True
draw_new = True
random_order = False
ETF_order = True
process_visible = True

if __name__ == '__main__': 
  
    file_name = os.path.basename(input_path)
    file_name = file_name.split('.')[0]
    os.system('clear')
    TP = TextPrint
    TP(" Idk if this impresses you or not , but it's kind of the only thing i can give you")
    TP(" 2020 wasn't a good year for you, and neither it was for me. but i guess we can only hope for the better future right")
    TP(" We weren't talking on your actual birthday lol")
    TP(" I hope this makes up for it.")
    TP(" Merry Christmas, Happy Pseudo- Bday, And A Happy new year to you too, Enjoy")
    TP(" - With love, from starkizard")
    output_path = output_path+"/"+file_name
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        os.makedirs(output_path+"/mask")
        os.makedirs(output_path+"/process")

    time_start=time.time()
    ETF_filter = ETF(input_path=input_path, output_path=output_path+'/mask',\
         dir_num=direction, kernel_radius=kernel_radius, iter_time=iter_time, background_dir=background_dir)
    ETF_filter.forward()


    input_img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    (h0,w0) = input_img.shape
    cv2.imwrite(output_path + "/input_gray.jpg", input_img)

    if transTone == True:
        input_img = transferTone(input_img)
    
    now_ = np.uint8(np.ones((h0,w0)))*255
    step = 0
    if draw_new==True:
        time_start=time.time()
        stroke_sequence=[]
        stroke_temp={'angle':None, 'grayscale':None, 'row':None, 'begin':None, 'end':None}
        for dirs in range(direction):
            angle = -90+dirs*180/direction
            stroke_temp['angle'] = angle
            img,_ = rotate(input_img, -angle)

            if CLAHE==True:
                img = HistogramEqualization(img)

            img_pad = cv2.copyMakeBorder(img, 2*period, 2*period, 2*period, 2*period, cv2.BORDER_REPLICATE)
            img_normal = cv2.normalize(img_pad.astype("float32"), None, 0.0, 1.0, cv2.NORM_MINMAX)

            x_der = cv2.Sobel(img_normal, cv2.CV_32FC1, 1, 0, ksize=5) 
            y_der = cv2.Sobel(img_normal, cv2.CV_32FC1, 0, 1, ksize=5) 

            x_der = torch.from_numpy(x_der) + 1e-12
            y_der = torch.from_numpy(y_der) + 1e-12

            gradient_magnitude = torch.sqrt(x_der**2.0 + y_der**2.0)
            gradient_norm = gradient_magnitude/gradient_magnitude.max()

            ldr = LDR(img, n)

            cv2.imwrite(output_path + "/Quantization.png", ldr)
            LDR_single_add(ldr,n,output_path)
            
            (h,w) = ldr.shape
            canvas = Gassian((h+4*period,w+4*period), mean=250, var = 3)


            for j in range(n):

                stroke_temp['grayscale'] = j*256/n
                mask = cv2.imread(output_path + '/mask/mask{}.png'.format(j),cv2.IMREAD_GRAYSCALE)/255
                dir_mask = cv2.imread(output_path + '/mask/dir_mask{}.png'.format(dirs),cv2.IMREAD_GRAYSCALE)
                dir_mask,_ = rotate(dir_mask, -angle, pad_color=0)
                dir_mask[dir_mask<128]=0
                dir_mask[dir_mask>127]=1

                distensce = Gassian((1,int(h/period)+4), mean = period, var = 1)
                distensce = np.uint8(np.round(np.clip(distensce, period*0.8, period*1.25)))
                raw = -int(period/2)

                for i in np.squeeze(distensce).tolist():
                    if raw < h:    
                        y = raw + 2*period 
                        raw += i        
                        for interval in get_start_end(mask[y-2*period]*dir_mask[y-2*period]):

                            begin = interval[0]
                            end = interval[1]
                            
                            begin -= 2*period
                            end += 2*period

                            length = end - begin
                            stroke_temp['begin'] = begin
                            stroke_temp['end'] = end
                            stroke_temp['row'] = y-int(period/2)
                            stroke_temp['importance'] = (255-stroke_temp['grayscale'])*torch.sum(gradient_norm[y:y+period,interval[0]+2*period:interval[1]+2*period]).numpy()

                            stroke_sequence.append(stroke_temp.copy())

        time_end=time.time()
        print('total time',time_end-time_start)
        print('stoke number',len(stroke_sequence))

        if random_order == True:
            random.shuffle(stroke_sequence)   

    
        if ETF_order == True:
            random.shuffle(stroke_sequence)   
            quickSort(stroke_sequence,0,len(stroke_sequence)-1)
        result = Gassian((h0,w0), mean=250, var = 3)
        canvases = []
    

        for dirs in range(direction):
            angle = -90+dirs*180/direction
            canvas,_ = rotate(result, -angle)
            canvas = np.pad(canvas, pad_width=2*period, mode='constant', constant_values=(255,255))
            canvases.append(canvas)
            

        
        for stroke_temp in stroke_sequence:
            angle = stroke_temp['angle']
            dirs = int((angle+90)*direction/180)
            grayscale = stroke_temp['grayscale']
            distribution = ChooseDistribution(period=period,Grayscale=grayscale)
            row = stroke_temp['row']
            begin = stroke_temp['begin']
            end = stroke_temp['end']
            length = end - begin

            newline = Getline(distribution=distribution, length=length)

            canvas = canvases[dirs]

            if length<1000 or begin == -2*period or end == w-1+2*period:
                temp = canvas[row:row+2*period,2*period+begin:2*period+end]
                m = np.minimum(temp, newline[:,:temp.shape[1]])
                canvas[row:row+2*period,2*period+begin:2*period+end] = m
            
            now,_ = rotate(canvas[2*period:-2*period,2*period:-2*period], angle)
            (H,W) = now.shape
            now = now[int((H-h0)/2):int((H-h0)/2)+h0, int((W-w0)/2):int((W-w0)/2)+w0]       
            result = np.minimum(now,result)           
            if process_visible == True:
                cv2.imshow('step', result)
                cv2.waitKey(1)   

            step += 1
            if step % Freq == 0:
                cv2.imwrite(output_path + "/process/{0:04d}.jpg".format(int(step/Freq)), result)
        if step % Freq != 0:
            step = int(step/Freq)+1
            cv2.imwrite(output_path + "/process/{0:04d}.jpg".format(step), result)     

        cv2.destroyAllWindows()
        time_end=time.time()
        print('total time',time_end-time_start)
        print('stoke number',len(stroke_sequence))
        cv2.imwrite(output_path + '/draw.jpg', result)

    edge = genStroke(input_img,18)
    edge = np.power(edge, deepen)
    edge = np.uint8(edge*255)
    if edge_CLAHE==True:
        edge = HistogramEqualization(edge)

    cv2.imwrite(output_path + '/edge.jpg', edge)
    cv2.imshow("edge",edge)

    edge = np.float32(edge)
    now_ = cv2.imread(output_path + "/draw.jpg", cv2.IMREAD_GRAYSCALE)
    result = res_cross= np.float32(now_)

    result[1:,1:] = np.uint8(edge[:-1,:-1] * res_cross[1:,1:]/255)
    result[0] = np.uint8(edge[0] * res_cross[0]/255)
    result[:,0] = np.uint8(edge[:,0] * res_cross[:,0]/255)
    result = edge*res_cross/255
    result=np.uint8(result)  

    cv2.imwrite(output_path + '/result.jpg', result)
    cv2.imshow("result",result)

    deblue(result, output_path)

    img_rgb_original = cv2.imread(input_path, cv2.IMREAD_COLOR)
    cv2.imwrite(output_path + "/input.jpg", img_rgb_original)
    img_yuv = cv2.cvtColor(img_rgb_original, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = result
    img_rgb = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR) 

    cv2.imshow("RGB",img_rgb)
    cv2.waitKey(0)
    cv2.imwrite(output_path + "/result_RGB.jpg",img_rgb)

    
#endif
#if 0
""" "
#endif
#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif
#include<bits/stdc++.h>
using namespace std;

int main(){
    
    cout << "Hello";
    cout.flush();
    sleep(2);
    cout << " Soldier!\n";

    cout.flush();
    sleep(2);
    cout << "Please don't mind this crappy program because I kinda am running out of time... \n";

    cout.flush();
    sleep(2);
    cout << "But the point being that all of this leads to something impressive\n";
    cout << " Or that's what I think of it....\n";

    cout.flush();
    sleep(4);
    cout << " But getting to the real thing won't be easy, you'll have to answer 10 questions correctly...";
    cout << " All input in lowercase\n";
    cout << " Without wasting time in this anymore , LETS GOOOOOOOOOOOOOOOOOOO\n";


    string ans= "happybday";
    vector<string> questions = {"Which is the best character in the MCU?\n",
    "Which is the best game in existence?\n",
    "How is my drawing ability?\n",
    "Do you remember you promised to have a chess game with me and BetaZero?\n",
    "What's the single most asked question in all of mankind? (Options arent missing) \n",
    "Minecraft 1.15 update was about :\n",
    "Which is the best pizzeria?\n",
    "What do gold and sliver have in common? \n",
    "The answer of the next question is: \n",

    };
    vector<string> options = {"g) Donald Duck \nh) Tony Stark \ni) Mickey Mouse\n",
    "a) Minecraft \n b) PUBG \n c) Candy Crush (why tf would you think about selecting this)\n",
    "p) Shit \nq) Decent \nr) Good (Who are we kidding)\n",
    "p) Yes \nq) Shit i forgot (but now you do, so select p) \n r) Idk what to write here\n",
    "x)\ny)\nz)\n",
    "a)\nb)\nc)\n",
    "b) Dominos\nc) Papa Johns\n d) Pizza hut (No one can outpizza the hut)\n",
    "a)\nb)\nc)\n",
    "x) False\n y) 100% correct\n z) Just a joke\n"
    };

    cout.flush();
    cout << "Press y to start\n"; 
    char x;
    cin >> x;

    


    for(int i=0;i<9;++i){
        char choice='q';
        while(choice!=ans[i]){
            cout << "QUESTION " << i+1 << "\n\n" << questions[i] << options[i];
            cout << "\nEnter your choice:   ";
            cin >> choice;
            if(choice == ans[i]) cout << "\n Correct!! Proceeding to next q\n\n";
            else cout << "\n Incorrect, Retrying the same question\n\n";
            sleep(2);            
            cout.flush();
            
        }
    }

    string response;
    cout << " So the last question, who is the most beautiful , awesome, intelligent girl on the planet? \n";
    cout << " You don't have options this time, type in your firstname:\t";
    cin >> response;
    while (response!="thename"){
        cout << "\nRetry :  ";
        cin >> response;
    }

    cout << "Yipee! You successfully completed the quiz, the answers were , 'h','a','p','p','y','b','d','a','y', Muskan \n";

    cout << " All of this was pretty useless lol, i just wanted to incorporate some time. change the file extension of this file to .py and run it.\n";
}
#if 0
" """
#endif
