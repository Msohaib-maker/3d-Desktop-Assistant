from elevenlabs import VoiceSettings, play, Voice
from elevenlabs.client import ElevenLabs
from playsound import playsound
# from pydub import AudioSegment
# from pydub.playback import play

audio = None
client = None

# "sk_8f4ad889c982327650bfcface1c4f0e1e672576df3a0e252"
def Set_Eleven_API_KEY(key):

    global audio
    global client
    print(f"Eleven Labs init {key} . . .")
    client = ElevenLabs(
            api_key=key,
    )

def generate_voice(prompt):

    global audio
    global client
    # audio = client.text_to_speech.convert(
    #     voice_id="JBFqnCBsd6RMkjVDRZzb",
    #     optimize_streaming_latency="0",
    #     output_format="mp3_22050_32",
    #     text=prompt,
    #     voice_settings=VoiceSettings(
    #         stability=0.1,
    #         similarity_boost=0.3,
    #         style=0.2,
    #     ),
    # )

    voice = Voice(
        voice_id="cgSgspJ2msm6clMCkdW9",
        settings = VoiceSettings(
            stability=0,
            similarity_boost=0.75
        )
    )

    audio = client.generate(
        text=prompt,
        voice=voice
    )

    

    play(audio)

