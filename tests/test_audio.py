import pytest
import wave
from pathlib import Path
from owui_client.models.audio import AudioConfigUpdateForm, TTSConfigForm, STTConfigForm

@pytest.mark.asyncio
async def test_audio_endpoints(client, mock_openai_server):
    # 1. Get Models
    models = await client.audio.get_models()
    assert isinstance(models, dict)
    assert "models" in models

    # 2. Get Voices
    voices = await client.audio.get_voices()
    assert isinstance(voices, dict)
    assert "voices" in voices

    # 3. Configure STT to use OpenAI (mock)
    # Constructing a valid form with dummy data + our specific change
    tts_config = TTSConfigForm(
        OPENAI_API_BASE_URL=mock_openai_server,
        OPENAI_API_KEY="sk-mock",
        API_KEY="sk-mock",
        ENGINE="openai",
        MODEL="tts-1",
        VOICE="alloy",
        SPLIT_ON="punctuation",
        AZURE_SPEECH_REGION="eastus",
        AZURE_SPEECH_BASE_URL="",
        AZURE_SPEECH_OUTPUT_FORMAT="audio-16khz-128kbitrate-mono-mp3"
    )
    
    stt_config = STTConfigForm(
        OPENAI_API_BASE_URL=mock_openai_server,
        OPENAI_API_KEY="sk-mock",
        ENGINE="openai",
        MODEL="whisper-1",
        WHISPER_MODEL="base",
        DEEPGRAM_API_KEY="",
        AZURE_API_KEY="",
        AZURE_REGION="eastus",
        AZURE_LOCALES="en-US",
        AZURE_BASE_URL="",
        AZURE_MAX_SPEAKERS="1",
        MISTRAL_API_KEY="",
        MISTRAL_API_BASE_URL="",
        MISTRAL_USE_CHAT_COMPLETIONS=False
    )
    
    update_form = AudioConfigUpdateForm(tts=tts_config, stt=stt_config)
    
    updated = await client.audio.update_config(update_form)
    assert updated["stt"]["ENGINE"] == "openai"
    assert updated["stt"]["OPENAI_API_BASE_URL"] == mock_openai_server
    
    # 4. Transcribe
    # Create a dummy audio file (WAV)
    dummy_file = Path("test_audio.wav")
    try:
        with wave.open(str(dummy_file), 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(44100)
            wav_file.writeframes(b'\x00\x00' * 1000) # Short silence

        # The backend might fail if it tries to process silence or if pydub fails, 
        # but we are testing the client flow and integration with configured provider.
        # The mock server returns a fixed response so if it reaches the mock, it succeeds.
        result = await client.audio.transcribe(dummy_file)
        assert "text" in result
        # Our mock returns "This is a mock transcription."
        # Wait, the backend might wrap it or process it. 
        # In audio.py: data = {"text": transcript}
        assert result["text"] == "This is a mock transcription."
        
    finally:
        if dummy_file.exists():
            dummy_file.unlink()

    # 5. Speech (TTS)
    speech_file = Path("test_speech.mp3")
    try:
        # This should hit the mock server /audio/speech
        # Note: The backend implementation checks request.app.state.config.TTS_ENGINE == "openai"
        # We set TTS_ENGINE="openai" in step 3 via tts_config
        
        audio_bytes = await client.audio.speech(
            input_text="Hello world",
            model="tts-1",
            voice="alloy",
            save_path=speech_file
        )
        assert len(audio_bytes) > 0
        assert speech_file.exists()
        
        # Verify content from mock (mock returns "FAKE_MP3_DATA")
        assert audio_bytes == b"FAKE_MP3_DATA"
    finally:
        if speech_file.exists():
            speech_file.unlink()
