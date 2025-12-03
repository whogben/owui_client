from typing import Optional
from pathlib import Path
from owui_client.client_base import ResourceBase
from owui_client.models.audio import AudioConfigUpdateForm

class AudioClient(ResourceBase):
    async def get_config(self) -> dict:
        """
        Get current audio configuration.
        
        Returns:
            dict: Current configuration
        """
        return await self._request("GET", "/v1/audio/config")

    async def update_config(self, form_data: AudioConfigUpdateForm) -> dict:
        """
        Update audio configuration.
        
        Args:
            form_data: The configuration data
            
        Returns:
            dict: The updated configuration
        """
        return await self._request("POST", "/v1/audio/config/update", json=form_data.model_dump())

    async def transcribe(self, file_path: str | Path, language: Optional[str] = None) -> dict:
        """
        Transcribe an audio file.
        
        Args:
            file_path: Path to the audio file
            language: Optional language code (e.g. "en")
            
        Returns:
            dict: The transcription result
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
        Generate speech from text (TTS).

        :param input_text: The text to convert to speech
        :param model: Optional model override
        :param voice: Optional voice override
        :param save_path: Optional path to save the audio file
        :return: Audio bytes
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
        Get available audio models.
        
        Returns:
            dict: List of available models
        """
        return await self._request("GET", "/v1/audio/models")

    async def get_voices(self) -> dict:
        """
        Get available voices.
        
        Returns:
            dict: List of available voices
        """
        return await self._request("GET", "/v1/audio/voices")
