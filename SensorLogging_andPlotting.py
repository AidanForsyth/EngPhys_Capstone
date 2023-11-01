import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

#initialize serial port
ser = serial.Serial()
ser.port = 'COM5' #Arduino serial port
ser.baudrate = 115200
# ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nSerial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters

class AnimationPlot:

    def animate(self, i, mag_x_dataList, mag_y_dataList, mag_z_dataList, mag_field_magnitude_dataList, ser):
        # Transmit the char 'g' to receive the Arduino data point
        # ser.write(b'g')                                     
        
        # Decode receive Arduino data as a formatted string
        arduinoData_string = ser.readline()
        line_as_list = arduinoData_string.split(b',')
        
        mag_field_x = line_as_list[0]
        mag_field_x_list = mag_field_x.split(b'\n')
        
        mag_field_y = line_as_list[1]
        mag_field_y_list = mag_field_y.split(b'\n')
        
        mag_field_z = line_as_list[2]
        mag_field_z_list = mag_field_z.split(b'\n')

        mag_field_magnitude = line_as_list[3]
        mag_field_magnitude_list = mag_field_magnitude.split(b'\n')
        
        try:
            # Convert to float
            mag_field_x_float = float(mag_field_x_list[0])
            mag_field_y_float = float(mag_field_y_list[0])
            mag_field_z_float = float(mag_field_z_list[0])
            mag_field_vector_float = float(mag_field_magnitude_list[0])
            # print(mag_field_vector)
            
            
            # print(mag_field_magnitude)
            
            # Add to the list holding the fixed number of points to animate
            # Converting from uTesla to Gauss
            mag_x_dataList.append(mag_field_x_float * 0.01)              
            mag_y_dataList.append(mag_field_y_float * 0.01)              
            mag_z_dataList.append(mag_field_z_float * 0.01)           
            mag_field_magnitude_dataList.append(mag_field_vector_float * 0.01)
            
        # Pass if data point is bad
        except:                                                                            
            pass

        # Fix the list size so that the animation plot 'window' is x number of points
        mag_x_dataList = mag_x_dataList[-100:]           
        mag_y_dataList = mag_y_dataList[-100:]           
        mag_z_dataList = mag_z_dataList[-100:]           
        mag_field_magnitude_dataList = mag_field_magnitude_dataList[-100:]
        # Clear last data frame
        ax.clear()                                          
        self.getPlotFormat()
        
        # plt.axis([0, 100, -1, 1]) #Use for 100 trial demo
        
        # Plot new data frame
        # ax.plot(mag_x_dataList, label = "X-axis Magnetic Field")                                   
        # ax.plot(mag_y_dataList, label = "Y-axis Magnetic Field")                                   
        ax.plot(mag_z_dataList, label = "Z-axis Magnetic Field")                                   
        # ax.plot(mag_field_magnitude_dataList, label = "Magnetic Field Magnitude")                                   
        
        plt.legend()              
    def getPlotFormat(self):
        # Set Y axis limit of plot
        ax.set_ylim([-1, 1])       
        ax.set_xlim([0, 100])                       
          
        # Set title of figure
        ax.set_title("Magnetic Field from Inside Helmholtz Coil")                        
        
        # Set title of y axis
        ax.set_ylabel("Magnetic Field [Gauss] ")  
        ax.set_xlabel("# of Data Points Continually being Displayed")              
        

# Create empty list variable for later use
mag_x_dataList = []                                           
mag_y_dataList = []                                           
mag_z_dataList = []      
mag_field_magnitude_dataList = []                                     
                                                        
# Create Matplotlib plots fig is the 'higher level' plot window
fig = plt.figure()                                      

# Add subplot to main fig window
ax = fig.add_subplot(1, 1, 1)                               

realTimePlot = AnimationPlot()

# Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
# ser = serial.Serial("COM5", 115200)                       

# Time delay for Arduino Serial initialization 
time.sleep(2)                                           

# Matplotlib Animation Fuction that takes takes care of real time plot.
# Note that 'fargs' parameter is where we pass in our dataList and Serial object. 
ani = animation.FuncAnimation(fig, realTimePlot.animate, frames=50, fargs=(mag_x_dataList, mag_y_dataList, mag_z_dataList, mag_field_magnitude_dataList, ser), interval=5) 

# Keep Matplotlib plot persistent on screen until it is closed
plt.show()                                              

# Close Serial connection when plot is closed
ser.close()                                             