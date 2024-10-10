import fluidsynth
import mido
import time
import rtmidi

###################################
#
#       Getting MIDI data part
#
###################################
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
    msg = midi_in.get_message() #Example for middle C : [144, 60, 127] ([channel, note, velocity]), 0.001413 (Timestamp) 
    if msg:
        data, timestamp = msg #splits the tuple
        print(f"Msg: {data}, Timestamp: {timestamp}") #Debug
        return msg
    return None



###########################################
#
#   Converting the MIDI data into sound
#
###########################################

#initalize Fludisynth
fs = fluidsynth.Synth()
fs.start()
#loading soundfont (this case it's the steinway one)
sfid = fs.sfload("C:\\Users\\Priva\\Desktop\\PROJECTS\\GIthub Repos\\MidiToSound\\Soundfonts\\StudioOne_Steinway_B.sf2")
fs.program_select(0,sfid,0,0) # channel,soundfont, bank, preset -> outputs the default font preset into midi channel one
while(True):
    if(input("type 'start' or 's' to start the programm: ") == "s" or "start" ):
        break

active_notes = set()  # Keeps track of notes currently being played
sustained_notes = set()  # Keeps track of notes that should remain on due to pedal
pedal_pressed = False  # Boolean to track if the pedal is pressed

while (True):
    msg = msgHandler()
    if msg:                                 #This is important to not accidentily unpack nothing when msgHandler returns None
        data, timestamp = msg
        if(data[0] == 144):                 #This equals a note being turned on (TESTED ONLY ON YAMAHA P-125)
            fs.noteon(0,data[1],data[2]) 
        elif(data[0] == 128):               #This equals a note being turned on (TESTED ONLY ON YAMAHA P-125)
            if pedal_pressed:
                sustained_notes.add(data[1])
            else:
                fs.noteoff(0,data[1])
                active_notes.discard(data[1])
        elif(data[0] == 176):               #This equals a note being turned on (TESTED ONLY ON YAMAHA P-125)
            if(data[2] >= 54):
                print("Pedal pressed")
                pedal_pressed = True 
            else:
                print("Pedal releasd")
                pedal_pressed = False
                
                #Handle sustained notes after release
                for note in sustained_notes:
                    fs.noteoff(0,note)
                sustained_notes.clear()
        else:
            time.sleep(0.0001)

  