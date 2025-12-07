from typing import Optional, List, Dict
from pydantic import BaseModel

class TTSConfigForm(BaseModel):
    """
    Configuration for Text-to-Speech (TTS).
    """

    OPENAI_API_BASE_URL: str
    """Base URL for OpenAI-compatible TTS API."""

    OPENAI_API_KEY: str
    """API Key for OpenAI-compatible TTS API."""

    OPENAI_PARAMS: Optional[Dict] = None
    """Additional parameters for OpenAI TTS requests."""

    API_KEY: str
    """API Key for other TTS engines (e.g. ElevenLabs, Azure)."""

    ENGINE: str
    """The TTS engine to use (e.g. 'openai', 'elevenlabs', 'azure', 'transformers')."""

    MODEL: str
    """The model identifier to use (e.g. 'tts-1', 'eleven_multilingual_v2')."""

    VOICE: str
    """The voice identifier to use."""

    SPLIT_ON: str
    """Character or pattern to split text on (e.g. punctuation)."""

    AZURE_SPEECH_REGION: str
    """Azure Speech region (if using Azure engine)."""

    AZURE_SPEECH_BASE_URL: str
    """Azure Speech base URL (optional override)."""

    AZURE_SPEECH_OUTPUT_FORMAT: str
    """Azure Speech output format."""

class STTConfigForm(BaseModel):
    """
    Configuration for Speech-to-Text (STT).
    """

    OPENAI_API_BASE_URL: str
    """Base URL for OpenAI-compatible STT API."""

    OPENAI_API_KEY: str
    """API Key for OpenAI-compatible STT API."""

    ENGINE: str
    """The STT engine to use (e.g. 'openai', 'deepgram', 'azure', 'mistral', or empty for local Whisper)."""

    MODEL: str
    """The model identifier to use."""

    SUPPORTED_CONTENT_TYPES: List[str] = []
    """List of supported content types (MIME types) for uploads."""

    WHISPER_MODEL: str
    """Local Whisper model name (e.g. 'base', 'small')."""

    DEEPGRAM_API_KEY: str
    """Deepgram API Key."""

    AZURE_API_KEY: str
    """Azure Speech API Key for STT."""

    AZURE_REGION: str
    """Azure Speech region for STT."""

    AZURE_LOCALES: str
    """Comma-separated list of Azure locales."""

    AZURE_BASE_URL: str
    """Azure Speech base URL for STT."""

    AZURE_MAX_SPEAKERS: str
    """Maximum number of speakers for Azure diarization."""

    MISTRAL_API_KEY: str
    """Mistral API Key."""

    MISTRAL_API_BASE_URL: str
    """Mistral API Base URL."""

    MISTRAL_USE_CHAT_COMPLETIONS: bool
    """Whether to use Mistral Chat Completions API (for audio input) instead of Transcription API."""

class AudioConfigUpdateForm(BaseModel):
    """
    Form for updating audio configuration (TTS and STT).
    """

    tts: TTSConfigForm
    """TTS configuration."""

    stt: STTConfigForm
    """STT configuration."""

