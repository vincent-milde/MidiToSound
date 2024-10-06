import fluidsynth
import mido
import time
import rtmidi

# Initialize MIDI input
mido.get_input_names()
midi_in = rtmidi.MidiIn()
available_ports = midi_in.get_ports()
if available_ports:
    # Open the first available MIDI input port
    try:
        midi_in.open_port(0)
        print("Using MIDI input port:", available_ports[0])
    except rtmidi._rtmidi.SystemError as e:
        print("Failed to open MIDI input port:", available_ports[0])
        print("Error:", e)
else:
    print("No MIDI input ports available. Make sure your MIDI device is connected.")

if not available_ports:
    exit()

def msgHandler ():
    msg = midi_in.getMesssage() #Example for middle C : [144, 60, 127] ([channel, note, velocity]), 0.001413 (Timestamp) 
    if msg:
        data, timestamp = msg #splits the tuple
        print(f"Msg: {data}, Timestamp: {timestamp}") #Debug
        
        