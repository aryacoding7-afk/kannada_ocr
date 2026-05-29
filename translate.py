from deep_translator import GoogleTranslator

print("START")

text = "ಅನುಮಾ ಕಿ. ಆರ್."

translated = GoogleTranslator(
    source="kn",
    target="en"
).translate(text)

print("RESULT:")
print(translated)

print("END")