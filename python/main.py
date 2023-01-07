import serial
import matplotlib.pyplot as plt
import time
import csv

t = 0
Tp = 1
measured_temps = []
measured_temp_changed = 0
destined_temps = []
destined_temp_changed = 0
timeaxis = []
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
    beginning_temperature = str(input("Ustaw temperature: "))
    UART.write(beginning_temperature.encode())
    return UART


fig = init_fig()
writer, dataStream = start_archive(timeFormat)
UART = init_uart()


def handle_uart(serialDataBuffer, t):
    global measured_temp_changed, destined_temp_changed
    set_temp = read_data(serialDataBuffer)



def read_data(serialDataBuffer):
    global measured_temp_changed, destined_temp_changed
    if UART.inWaiting() >= 0:
        serialDataBuffer += UART.read(1)
        if b"Current temperature: " in serialDataBuffer:
            measured_temperature = UART.read(5)
            measured_temperature = measured_temperature.decode()
            measured_temperature = float(measured_temperature)
            measured_temps.append(measured_temperature)
            serialDataBuffer[::] = b""
            measured_temp_changed = 1
            print("Current temperature:", measured_temperature)
        elif b"Set temperature: " in serialDataBuffer:
            destined_temperature = UART.read(5)
            destined_temperature = destined_temperature.decode()
            destined_temperature = float(destined_temperature)
            destined_temps.append(destined_temperature)
            serialDataBuffer[::] = b""
            destined_temp_changed = 1
            print("Set temperature:", destined_temperature)
    return destined_temperature


while not_exited:
    handle_uart(serialDataBuffer)

fig.savefig(f"Temp_plot_{timeFormat}.png")
UART.close()
dataStream.close()