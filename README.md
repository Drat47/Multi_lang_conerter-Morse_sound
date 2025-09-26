
# Multi-language Converter with Braille, Morse, TTS & Audio Beeps

This is a Python desktop application that converts text between English, Braille, and Morse code, with additional features for accessibility including text-to-speech and Morse code audio beeps. The project also visually simulates Braille dots for enhanced interactive learning.

## Features

- **English ↔ Braille Conversion:**  
  Converts English text to Unicode Braille and back, supporting alphabets, digits, and punctuation.

- **English ↔ Morse Conversion:**  
  Converts English text to international Morse code and back.

- **Text-to-Speech (TTS):**  
  Reads English or converted text aloud using the `pyttsx3` engine.

- **Morse Code Audio Beeps:**  
  Plays short (dot) and long (dash) beeps with spacing reflecting Morse code timing, implemented cross-platform.

- **Braille Dot Visualization:**  
  Graphical 2x3 dot grid display simulating Braille cells for visual recognition and learning.

- **User-Friendly GUI:**  
  Built with Tkinter, providing text input, conversion buttons, speech controls, and Braille dot visualization.

## Installation

1. Clone this repository.
2. Install required Python packages:
   ```
   pip install pyttsx3 simpleaudio numpy
   ```
3. On Windows, ensure Microsoft Visual C++ Build Tools are installed for `simpleaudio`.

## Usage

Run the main script:
```
python multi_lang_converter_morse_sound.py
```

- Enter English text in the left box.
- Use the buttons to convert between English, Braille, and Morse.
- Visual Braille dots display below.
- Use Speak buttons for TTS and Morse audio playback.

## Notes

- For best audio beep performance on Windows, this project uses the built-in `winsound` module.
- Audio playback and speech run in background threads to keep the interface responsive.

## License

This project is open source and free to use.

---

Feel free to customize the README with your contact info or additional instructions!

Would you like me to generate the `.md` file content directly or help with GitHub repository setup next?
