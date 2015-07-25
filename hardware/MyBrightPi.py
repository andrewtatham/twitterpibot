from ExceptionHandler import ExceptionHandler
import time

try:    
    import BrightPILed
    from BrightPILed import BrightPI
    enableBrightPi = True
except Exception as e:
    ExceptionHandler().HandleSilently(e)
    enableBrightPi = False

class MyBrightPi(object):
    def __init__(self, *args, **kwargs):
        if enableBrightPi:
            self.light = BrightPI(1)
            self.light.Reset();
            self.light.Led_1_On();
            time.sleep(0.5);
            self.light.Led_2_On();
            time.sleep(0.5);
            self.light.Led_3_On();
            time.sleep(0.5);
            self.light.Led_4_On();
            time.sleep(0.5);
            self.light.Led_4_Off();
            time.sleep(0.5);
            self.light.Led_3_Off();
            time.sleep(0.5);
            self.light.Led_2_Off();
            time.sleep(0.5);
            self.light.Led_1_Off();
            time.sleep(0.5);
            self.light.Led_All_On();
            time.sleep(0.5);
            for x in range(0, 15):
                self.light.Led_All_Brightness(x);   
                time.sleep(0.1);
            self.light.Led_All_Off();

       

    def CameraFlash(args, on):
        if enableBrightPi:
            if on:
                args.light.Led_All_On();
            else:
                args.light.Led_All_Off();
