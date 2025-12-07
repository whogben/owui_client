from typing import Optional
from pathlib import Path
from owui_client.client_base import ResourceBase
from owui_client.models.audio import AudioConfigUpdateForm

class AudioClient(ResourceBase):
    """
    Client for Audio endpoints (TTS and STT).
    """

    async def get_config(self) -> dict:
        """
        Get the current audio configuration.

        This includes settings for both Text-to-Speech (TTS) and Speech-to-Text (STT) engines,
        such as API keys, base URLs, models, and voice settings.

        Returns:
            dict: The current configuration, with keys 'tts' and 'stt'.
        """
        return await self._request("GET", "/v1/audio/config")

    async def update_config(self, form_data: AudioConfigUpdateForm) -> dict:
        """
        Update the audio configuration.

        Args:
            form_data: The configuration data to update.

        Returns:
            dict: The updated configuration.
        """
        return await self._request("POST", "/v1/audio/config/update", json=form_data.model_dump())

    async def transcribe(self, file_path: str | Path, language: Optional[str] = None) -> dict:
        """
        Transcribe an audio file to text.

        Uses the configured STT engine (e.g. Whisper, OpenAI, Deepgram, Azure, Mistral).
        Automatically handles audio conversion and chunking if necessary.

        Args:
            file_path: Path to the audio file to transcribe.
            language: Optional language code (e.g. "en") to guide transcription.

        Returns:
            dict: A dictionary containing the transcription result, typically `{"text": "...", "filename": "..."}`.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as f:
            # Read file content into memory to safely close the file handle
            content = f.read()
            
        files = {"file": (file_path.name, content)}
        
        data = {}
        if language:
            data["language"] = language

        return await self._request("POST", "/v1/audio/transcriptions", files=files, data=data)

    async def speech(
        self,
        input_text: str,
        model: Optional[str] = None,
        voice: Optional[str] = None,
        save_path: Optional[str | Path] = None,
    ) -> bytes:
        """
        Generate speech from text (Text-to-Speech).

        Uses the configured TTS engine (e.g. OpenAI, ElevenLabs, Azure, Transformers).

        Args:
            input_text: The text to convert to speech.
            model: Optional model identifier to override the default configuration.
            voice: Optional voice identifier to override the default configuration.
            save_path: Optional file path to save the generated audio to.

        Returns:
            bytes: The generated audio content in bytes.
        """
        payload = {"input": input_text}
        if model:
            payload["model"] = model
        if voice:
            payload["voice"] = voice

        response_bytes = await self._request(
            "POST",
            "/v1/audio/speech",
            json=payload,
            model=bytes,
        )

        if save_path:
            with open(save_path, "wb") as f:
                f.write(response_bytes)

        return response_bytes

    async def get_models(self) -> dict:
        """
        Get available audio models for the configured TTS engine.

        Returns:
            dict: A dictionary containing a list of models, e.g. `{"models": [{"id": "tts-1"}, ...]}`.
        """
        return await self._request("GET", "/v1/audio/models")

    async def get_voices(self) -> dict:
        """
        Get available voices for the configured TTS engine.

        Returns:
            dict: A dictionary containing a list of voices, e.g. `{"voices": [{"id": "alloy", "name": "alloy"}, ...]}`.
        """
        return await self._request("GET", "/v1/audio/voices")
