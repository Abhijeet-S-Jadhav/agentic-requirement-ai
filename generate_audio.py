import os
from gtts import gTTS

# Ensure the directory exists
os.makedirs("sample_audio", exist_ok=True)

# The script simulates a client from an electronics retail chain.
# It includes specific requirements mixed with professional ambiguity.
script_text = """
Hi, this is Sarah from Global Tech Retail. We want to develop an augmented reality shopping 
assistant for our customers looking at the latest iPhone 16 lineup. 
The core feature is AR visualization. A user should be able to place a virtual 3D model of 
an iPhone on their desk to see the size and colors accurately. 
We need a comparison tool where they can side-by-side the Pro and the standard models. 
Checkout must be seamless, ideally using Apple Pay, because security is a top priority for us. 
Performance is key; the AR shouldn't lag, it needs to feel very premium and smooth. 
We're expecting a huge surge of users, maybe 50,000 in the first week after launch. 
Regarding compatibility, we definitely want it on iOS. I am not sure about older iPhones, 
maybe we only support the last two years? Let me know what you think. 
Also, the 3D models should look as realistic as possible. Thanks!
"""

print("Generating iPhone Sample Audio...")

# Convert text to audio
tts = gTTS(text=script_text, lang='en', slow=False)
save_path = "sample_audio/iphone_project_call.mp3"
tts.save(save_path)

print(f"✅ iPhone Sample saved at: {save_path}")