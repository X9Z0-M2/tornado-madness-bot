import keyboard



def main():


    def keyboard_quit_cb(KeyboardEvent):
        nonlocal quit
        quit = True
        # print(KeyboardEvent.name, KeyboardEvent.scan_code, KeyboardEvent.time)

    quit = False
    keyboard.on_press_key("q",keyboard_quit_cb )
    
    while not quit:
        # Wait for the next event.
        event = keyboard.read_event()

    print("Ended.")


if __name__ == "__main__":
    main()

