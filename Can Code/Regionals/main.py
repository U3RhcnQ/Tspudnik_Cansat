recovery = False 
send_enabled = False
music.set_built_in_speaker_enabled (False)
music.set_volume(255) 
Radio_recieve=""
serial.redirect(SerialPin.P16, SerialPin.P1, BaudRate.BAUD_RATE9600) 
text_list: List[str] = []

def on_forever():
    global Radio_recieve, send_enabled, recovery 
    music.play_tone(262, music.beat (BeatFraction.WHOLE))
    Radio_recieve = serial.read_string()
    if Radio_recieve != "":
        if Radio_recieve == "loging":
            if send_enabled:
                send_enabled = False
            else:
                send_enabled = True
        if Radio_recieve == "ping":
            serial.write_line("pong") 
            basic.show_icon(IconNames.SQUARE)
        if Radio_recieve == "recovery":
            if recovery:
                recovery = False
                send_enabled = False
            else:          
                recovery = True
        Radio_recieve=""
    if recovery:
        music.set_built_in_speaker_enabled(True)
    else:
        music.set_built_in_speaker_enabled(False)
    if send_enabled:
        text_list.append("ID1234" + "," + str(envirobit.get_pressure_decimal(basic.forever(on_forever))))

def on_every_interval():
    global text_list
    basic.show_icon (IconNames.SMALL_SQUARE)
    for value in text_list:
        serial.write_line("" + (value))
    text_list = []
    basic.show_icon (IconNames.SQUARE)
loops.every_interval(3000, on_every_interval)