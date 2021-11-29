# -*- coding: utf-8 -*-
import threading


class TimerClass(threading.Thread):
    
    def __init__(self,Tthread = threading.Thread,i=0.1,target =None):
        threading.Thread.__init__(self)
        self.i = i
        self.target = target
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            self.target()
            self.event.wait(self.i)

    def stop(self):
        self.event.set()