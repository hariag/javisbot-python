#!/usr/bin/env python

from pathlib import Path

from jarvisbot import JarvisBot

# gets OPENAI_API_KEY from your environment variables
jtts = JarvisBot(api_key="123",
              base_url="http://fdcc8280fb7b28a619.jarvisbot.live/ttsapi/v1")

jasr = JarvisBot(api_key="123",
              base_url="http://9c90dfd6261a908c68.jarvisbot.live/asrapi/v1")

speech_file_path = Path(__file__).parent / "speech.mp3"


def main() -> None:
    # Create text-to-speech audio file
    with jtts.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="female",
            input="the quick brown fox jumped over the lazy dogs",
    ) as response:
        response.stream_to_file(speech_file_path)

    # Create transcription from audio file
    transcription = jasr.audio.transcriptions.create(
        model="whisper-1",
        file=speech_file_path,
    )
    print(transcription.model_extra.get("texts")[0])


if __name__ == "__main__":
    main()
