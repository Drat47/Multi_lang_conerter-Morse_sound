import pyttsx3
import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import numpy as np
import simpleaudio as sa
import winsound
winsound.Beep(700, 150)  # frequency, duration in ms

# ---------------------------
# Braille Mapping
# ---------------------------
LETTER_TO_BRAILLE = {
    'a': '⠁','b':'⠃','c':'⠉','d':'⠙','e':'⠑',
    'f':'⠋','g':'⠛','h':'⠓','i':'⠊','j':'⠚',
    'k':'⠅','l':'⠇','m':'⠍','n':'⠝','o':'⠕',
    'p':'⠏','q':'⠟','r':'⠗','s':'⠎','t':'⠞',
    'u':'⠥','v':'⠧','w':'⠺','x':'⠭','y':'⠽','z':'⠵'
}
NUMBER_SIGN = '⠼'
A_J = ['⠁','⠃','⠉','⠙','⠑','⠋','⠛','⠓','⠊','⠚']
DIGIT_TO_BRAILLE = {str(i):A_J[i-1] if i!=0 else A_J[9] for i in range(10)}
PUNCT_TO_BRAILLE = {'.':'⠲',',':'⠂','?':'⠦','!':'⠖',';':'⠆',':':'⠒',"'":'⠄','"':'⠶','-':'⠤'}

BRAILLE_TO_LETTER = {v:k for k,v in LETTER_TO_BRAILLE.items()}
BRAILLE_TO_DIGIT = {v:k for k,v in DIGIT_TO_BRAILLE.items()}
BRAILLE_TO_PUNCT = {v:k for k,v in PUNCT_TO_BRAILLE.items()}

# ---------------------------
# Morse Mapping
# ---------------------------
MORSE_CODE_DICT = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.',
    'G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..',
    'M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.',
    'S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-',
    'Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---',
    '3':'...--','4':'....-','5':'.....','6':'-....','7':'--...',
    '8':'---..','9':'----.','.':'.-.-.-',',':'--..--','?':'..--..',
    '!':'-.-.--','-':'-....-','/':'-..-.','@':'.--.-.','(':'-.--.',
    ')':'-.--.-'
}
MORSE_TO_LETTER = {v:k for k,v in MORSE_CODE_DICT.items()}

# ---------------------------
# Conversion Functions
# ---------------------------
def english_to_braille(text):
    out = []
    i=0
    while i<len(text):
        ch = text[i]
        if ch.isalpha(): out.append(LETTER_TO_BRAILLE.get(ch.lower(),'?')); i+=1
        elif ch.isdigit():
            out.append(NUMBER_SIGN)
            while i<len(text) and text[i].isdigit(): out.append(DIGIT_TO_BRAILLE.get(text[i],'?')); i+=1
        elif ch.isspace(): out.append(' '); i+=1
        else: out.append(PUNCT_TO_BRAILLE.get(ch,'?')); i+=1
    return ''.join(out)

def braille_to_english(text):
    out=[]; in_number=False
    for c in text:
        if c==' ': out.append(' '); in_number=False
        elif c==NUMBER_SIGN: in_number=True
        elif in_number: out.append(BRAILLE_TO_DIGIT.get(c,'?'))
        elif c in BRAILLE_TO_LETTER: out.append(BRAILLE_TO_LETTER[c])
        elif c in BRAILLE_TO_PUNCT: out.append(BRAILLE_TO_PUNCT[c])
        else: out.append('?')
    return ''.join(out)

def english_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(ch.upper(),'?') if ch!=' ' else '/' for ch in text)

def morse_to_english(text):
    words=text.split('/')
    decoded=[]
    for w in words:
        letters=w.strip().split()
        decoded.append(''.join(MORSE_TO_LETTER.get(l,'?') for l in letters))
    return ' '.join(decoded)

# ---------------------------
# TTS & Morse Audio
# ---------------------------
engine = pyttsx3.init()
def speak_text(text): engine.say(text); engine.runAndWait()

def play_beep(frequency=700, duration_ms=150):
    fs=44100
    t=np.linspace(0,duration_ms/1000,int(fs*duration_ms/1000),False)
    note=np.sin(frequency*t*2*np.pi)
    audio=(note*32767).astype(np.int16)
    sa.play_buffer(audio,1,2,fs).wait_done()

def speak_morse_audio(morse_code):
    for ch in morse_code:
        if ch=='.': play_beep(700,150)
        elif ch=='-': play_beep(700,400)
        elif ch==' ': time.sleep(0.2) # between letters
        elif ch=='/': time.sleep(0.6) # between words
        time.sleep(0.1)  # small gap

# ---------------------------
# Braille Dot Visualization
# ---------------------------
def braille_unicode_to_dots(ch):
    code = ord(ch) - 0x2800
    return [(code >> i) & 1 for i in range(6)]

def draw_braille_cell(canvas, x, y, dots, radius=8, cell_padding=20):
    positions = [
        (x, y),
        (x, y+cell_padding),
        (x, y+2*cell_padding),
        (x+cell_padding, y),
        (x+cell_padding, y+cell_padding),
        (x+cell_padding, y+2*cell_padding)
    ]
    for i, (dx, dy) in enumerate(positions):
        fill = 'black' if dots[i] else 'white'
        canvas.create_oval(dx-radius, dy-radius, dx+radius, dy+radius, fill=fill, outline='black')

def draw_braille_string(canvas, braille_text, start_x=20, start_y=20, cell_spacing=40):
    canvas.delete('all')
    x = start_x
    for ch in braille_text:
        if ch == ' ':
            x += cell_spacing  # Extra space for word gap
            continue
        dots = braille_unicode_to_dots(ch)
        draw_braille_cell(canvas, x, start_y, dots)
        x += cell_spacing

# ---------------------------
# GUI
# ---------------------------
def build_ui():
    root=tk.Tk()
    root.title("Multi-language Converter + Morse Audio")

    tk.Label(root,text="English Text").grid(row=0,column=0)
    tk.Label(root,text="Braille / Morse").grid(row=0,column=1)

    txt_eng=scrolledtext.ScrolledText(root,width=40,height=12)
    txt_other=scrolledtext.ScrolledText(root,width=40,height=12)
    txt_eng.grid(row=1,column=0,padx=6,pady=6)
    txt_other.grid(row=1,column=1,padx=6,pady=6)

    # Braille visualization canvas
    canvas_braille = tk.Canvas(root, width=600, height=60, bg='white')
    canvas_braille.grid(row=3, column=0, columnspan=2, pady=6)

    def eng_to_braille():
        txt_other.delete('1.0', tk.END)
        braille = english_to_braille(txt_eng.get('1.0', tk.END).strip())
        txt_other.insert(tk.END, braille)
        draw_braille_string(canvas_braille, braille)

    def braille_to_eng():
        txt_eng.delete('1.0', tk.END)
        txt_eng.insert(tk.END, braille_to_english(txt_other.get('1.0', tk.END).strip()))
        canvas_braille.delete('all')

    def eng_to_morse():
        txt_other.delete('1.0', tk.END)
        morse = english_to_morse(txt_eng.get('1.0', tk.END).strip())
        txt_other.insert(tk.END, morse)
        canvas_braille.delete('all')

    def morse_to_eng():
        txt_eng.delete('1.0', tk.END)
        txt_eng.insert(tk.END, morse_to_english(txt_other.get('1.0', tk.END).strip()))
        canvas_braille.delete('all')

    def speak_eng():
        speak_text(txt_eng.get('1.0', tk.END).strip())

    def speak_other():
        s=txt_other.get('1.0', tk.END).strip()
        if any(c in LETTER_TO_BRAILLE.values() or c==NUMBER_SIGN for c in s):
            speak_text(braille_to_english(s))
        else:
            speak_text(morse_to_english(s))
            speak_morse_audio(s)

    btn_frame=tk.Frame(root); btn_frame.grid(row=2,column=0,columnspan=2,pady=6)
    tk.Button(btn_frame,text="English → Braille",command=eng_to_braille).grid(row=0,column=0,padx=6)
    tk.Button(btn_frame,text="Braille → English",command=braille_to_eng).grid(row=0,column=1,padx=6)
    tk.Button(btn_frame,text="English → Morse",command=eng_to_morse).grid(row=0,column=2,padx=6)
    tk.Button(btn_frame,text="Morse → English",command=morse_to_eng).grid(row=0,column=3,padx=6)
    tk.Button(btn_frame,text="Speak English",command=speak_eng).grid(row=1,column=0,padx=6,pady=6)
    tk.Button(btn_frame,text="Speak Braille/Morse + Audio",command=speak_other).grid(row=1,column=1,padx=6,pady=6)

    root.mainloop()

if __name__=="__main__":
    build_ui()
