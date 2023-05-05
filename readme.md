1) funcao p mandar a msg sem precisar digitar no pywhatkit

def send_message(message: str, receiver: str, wait_time: int) -> None:
    """Parses and Sends the Message"""
    _web(receiver=receiver, message=message)
    time.sleep(7)
    # click(WIDTH / 2, HEIGHT / 2)
    time.sleep(wait_time - 7)
    if not check_number(number=receiver):
        pyperclip.copy(message)
        time.sleep(5)
        hotkey('ctrl', 'v')
        # for char in message:
        #     if char == "\n":
        #         hotkey("shift", "enter")
        #     else:
        #         typewrite(char)  
    press("enter")