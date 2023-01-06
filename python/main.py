import serial
import matplotlib.pyplot as plt
import time
import csv

t = 0
Tp = 1
curr_temp_samples = []
curr_temp_flag = 0
set_temp_samples = []
set_temp_flag = 0
timebase = []
serialDataBuffer = bytearray()
not_exited = 1
timeFormat = "%Y%m%d-%H%M%S"


def transmit_end_handler(event):
    global not_exited
    not_exited = 0
    print("Data logging finished!")


def init_fig():
    fig = plt.figure(figsize=(10, 5))
    fig.canvas.mpl_connect('key_press_event', transmit_end_handler)
    fig.canvas.mpl_connect('close_event', transmit_end_handler)
    plt.ion()
    return fig


def start_archive(timeFormat):
    timeData = time.strftime(timeFormat)
    dataStream = open(f"data_{timeData}.csv", 'w', newline='')
    writer = csv.writer(dataStream, delimiter=',')
    header = ["Time", "Curr_temp", "Set_temp"]
    writer.writerow(header)
    return writer, dataStream


def init_uart():
    COM_PORT = int(input("Wpisz numer PORTU COM: "))
    UART = serial.Serial(f"COM{COM_PORT}", 115200, timeout=1, parity=serial.PARITY_NONE)
    set_start_temp = str(input("Ustaw temperature: "))
    UART.write(set_start_temp.encode())
    return UART


fig = init_fig()
writer, dataStream = start_archive(timeFormat)
UART = init_uart()


fig.savefig(f"Temp_plot_{timeFormat}.png")
UART.close()
dataStream.close()