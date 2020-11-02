import numpy as np
import cv2 as cv2
import time
import math
import time
from tqdm import tqdm

class temporal_fx:
    def __init__(self):
        self.buffer = []
        self.buffer2 = []
        self.video  = []
        self.filter = np.array(0)
        self.height = 0
        self.width  = 0
        self.length = 0
        self.max_temporal_diff =0
        self.output = []
        
    def load(self, title):
        self.video = cv2. VideoCapture(title)
        a, b = self.video.read(); 
        self.height, self.width = b.shape[:2]
        self.generate_filter()
        self.length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

            
    def apply_filter(self):
        out = cv2.VideoWriter('outvide.avi', cv2.VideoWriter_fourcc(*'MJPG'),24, (self.width,self.height) )

        frame_start = self.max_temporal_diff+1
        
        new_frame = np.ones([self.height,self.width,3], dtype=np.uint8)*0

        for frame_num in tqdm(range( frame_start, self.length)):
            
            self.__save_to_buffer( frame_num )
            
            for t in range(0, self.max_temporal_diff-1):
                buffer_frame = self.buffer[t]

                if buffer_frame is None:
                    break
                
                new_frame[ (self.filter == t) ] = buffer_frame[ ( self.filter == t) ]
            
            out.write(new_frame)

    def generate_filter(self):
        self.filter  = np.ones([self.height,self.width,3], dtype=np.uint8)*0
        x2 =0
        y2 =0
        for y1 in self.filter:
            #print(y1)
            for x1 in y1:
                self.filter[y2][x2][0]=  int ( abs(math.sqrt(abs(  abs(x2 - self.width/2) **2  +  abs(y2 - self.height/2) **2 )))/4 )
                self.filter[y2][x2][1]=  int ( abs(math.sqrt(abs(  abs(x2 - self.width/2) **2  +  abs(y2 - self.height/2) **2 )))/4 )
                self.filter[y2][x2][2]=  int ( abs(math.sqrt(abs(  abs(x2 - self.width/2) **2  +  abs(y2 - self.height/2) **2 )))/4 )
                x2+=1
            y2+=1
            x2=0
        self.max_temporal_diff = np.max(self.filter);
        
    def play(self):
        self.__apply_filter()
        a = True
        a, b = self.video.read(); 
        while a:
            # Write the frame into the file 'output.avi'
            # Display the resulting frame   
            
            cv2.imshow('frame',b)
            if cv2.waitKey(1) & 0xFF == ord('s'): 
                break
            a, b = self.video.read(); 
            
    def __save_to_buffer(self, frame_num):
        self.buffer.clear()
        self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_num - self.max_temporal_diff)
        for t in range (frame_num - self.max_temporal_diff, frame_num+1):
            c, d = self.video.read();
            self.buffer.append(d)
            
vid = temporal_fx()

vid.load('stationary.mp4')
vid.apply_filter()
