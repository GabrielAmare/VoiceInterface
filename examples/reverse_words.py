from vi37 import VoiceInterface

QUIT_KW = "quit"

if __name__ == '__main__':
    vi = VoiceInterface(lang_IETF="en-US")

    while True:
        text = vi.listen()

        if text == QUIT_KW:
            break

        words = text.split(" ")

        print(words)

        vi.speak(" ".join(reversed(words)))
