import mido
import pygame
import pygame.midi
import mido
import pygame
import pygame.midi

    """
    NOT MY CODE ---- EXAMPLE ONLY
    """
def midi_to_sound():
    # Initialize Pygame mixer
    pygame.mixer.init()

    # Initialize Pygame MIDI
    pygame.midi.init()

    # Open the default MIDI input device
    midi_input = mido.open_input()

    # Create a Pygame MIDI input stream
    midi_stream = pygame.midi.Input(1)

    # Initialize a list to hold MIDI events
    events = []

    # Start capturing MIDI input
    print("Capturing MIDI input... Press Ctrl+C to stop.")
    try:
        while True:
            # Check for MIDI events
            if midi_stream.poll():
                # Get MIDI event
                midi_data = midi_stream.read(1)[0][0]
                
                # Append MIDI event to the list
                events.append(midi_data)
                
                # Convert MIDI event into sound
                # Example: Play MIDI note as piano sound
                note, velocity, _ = midi_data
                sound = pygame.mixer.Sound(pygame.midi.SoundFont().get_patch(0), attacktime=100)
                sound.set_volume(velocity / 127)  # Set volume based on velocity
                sound.play(-1)  # Play sound indefinitely
                
    except KeyboardInterrupt:
        print("\nStopping MIDI input capture.")
        
    finally:
        # Close MIDI input and stream
        midi_input.close()
        midi_stream.close()

        # Clean up Pygame
        pygame.midi.quit()
        pygame.mixer.quit()

# Example usage:
midi_to_sound()