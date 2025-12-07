from typing import List, Optional, Union, Dict
from pydantic import BaseModel
from owui_client.models.files import FileModel

class CollectionNameForm(BaseModel):
    """
    Form for specifying a collection name.
    """
    collection_name: Optional[str] = None
    """The name of the collection."""

class ProcessUrlForm(CollectionNameForm):
    """
    Form for processing a URL.
    """
    url: str
    """The URL to process."""

class SearchForm(BaseModel):
    """
    Form for search queries.
    """
    queries: List[str]
    """List of search queries."""

class OpenAIConfigForm(BaseModel):
    """
    Configuration for OpenAI embedding model.
    """
    url: str
    """The base URL for the OpenAI API."""
    key: str
    """The API key for the OpenAI API."""

class OllamaConfigForm(BaseModel):
    """
    Configuration for Ollama embedding model.
    """
    url: str
    """The base URL for the Ollama API."""
    key: str
    """The API key for the Ollama API."""

class AzureOpenAIConfigForm(BaseModel):
    """
    Configuration for Azure OpenAI embedding model.
    """
    url: str
    """The base URL for the Azure OpenAI API."""
    key: str
    """The API key for the Azure OpenAI API."""
    version: str
    """The API version for the Azure OpenAI API."""

class EmbeddingModelUpdateForm(BaseModel):
    """
    Form for updating the embedding model configuration.
    """
    openai_config: Optional[OpenAIConfigForm] = None
    """Configuration for OpenAI embedding model."""
    ollama_config: Optional[OllamaConfigForm] = None
    """Configuration for Ollama embedding model."""
    azure_openai_config: Optional[AzureOpenAIConfigForm] = None
    """Configuration for Azure OpenAI embedding model."""
    RAG_EMBEDDING_ENGINE: str
    """The embedding engine to use (e.g., 'ollama', 'openai')."""
    RAG_EMBEDDING_MODEL: str
    """The embedding model to use."""
    RAG_EMBEDDING_BATCH_SIZE: Optional[int] = 1
    """The batch size for embedding generation."""
    ENABLE_ASYNC_EMBEDDING: Optional[bool] = True
    """Whether to enable asynchronous embedding generation."""

class WebConfig(BaseModel):
    """
    Configuration for web search and retrieval.
    """
    ENABLE_WEB_SEARCH: Optional[bool] = None
    """Whether to enable web search."""
    WEB_SEARCH_ENGINE: Optional[str] = None
    """The web search engine to use."""
    WEB_SEARCH_TRUST_ENV: Optional[bool] = None
    """Whether to trust the environment variables for web search."""
    WEB_SEARCH_RESULT_COUNT: Optional[int] = None
    """The number of web search results to retrieve."""
    WEB_SEARCH_CONCURRENT_REQUESTS: Optional[int] = None
    """The number of concurrent web search requests."""
    WEB_LOADER_CONCURRENT_REQUESTS: Optional[int] = None
    """The number of concurrent web loader requests."""
    WEB_SEARCH_DOMAIN_FILTER_LIST: Optional[List[str]] = []
    """List of domains to filter from web search results."""
    BYPASS_WEB_SEARCH_EMBEDDING_AND_RETRIEVAL: Optional[bool] = None
    """Whether to bypass embedding and retrieval for web search results."""
    BYPASS_WEB_SEARCH_WEB_LOADER: Optional[bool] = None
    """Whether to bypass the web loader for web search results."""
    OLLAMA_CLOUD_WEB_SEARCH_API_KEY: Optional[str] = None
    """API key for Ollama Cloud web search."""
    SEARXNG_QUERY_URL: Optional[str] = None
    """The query URL for SearXNG."""
    YACY_QUERY_URL: Optional[str] = None
    """The query URL for YaCy."""
    YACY_USERNAME: Optional[str] = None
    """The username for YaCy."""
    YACY_PASSWORD: Optional[str] = None
    """The password for YaCy."""
    GOOGLE_PSE_API_KEY: Optional[str] = None
    """API key for Google Programmable Search Engine."""
    GOOGLE_PSE_ENGINE_ID: Optional[str] = None
    """Engine ID for Google Programmable Search Engine."""
    BRAVE_SEARCH_API_KEY: Optional[str] = None
    """API key for Brave Search."""
    KAGI_SEARCH_API_KEY: Optional[str] = None
    """API key for Kagi Search."""
    MOJEEK_SEARCH_API_KEY: Optional[str] = None
    """API key for Mojeek Search."""
    BOCHA_SEARCH_API_KEY: Optional[str] = None
    """API key for Bocha Search."""
    SERPSTACK_API_KEY: Optional[str] = None
    """API key for Serpstack."""
    SERPSTACK_HTTPS: Optional[bool] = None
    """Whether to use HTTPS for Serpstack."""
    SERPER_API_KEY: Optional[str] = None
    """API key for Serper."""
    SERPLY_API_KEY: Optional[str] = None
    """API key for Serply."""
    TAVILY_API_KEY: Optional[str] = None
    """API key for Tavily."""
    SEARCHAPI_API_KEY: Optional[str] = None
    """API key for SearchAPI."""
    SEARCHAPI_ENGINE: Optional[str] = None
    """The engine to use for SearchAPI."""
    SERPAPI_API_KEY: Optional[str] = None
    """API key for SerpAPI."""
    SERPAPI_ENGINE: Optional[str] = None
    """The engine to use for SerpAPI."""
    JINA_API_KEY: Optional[str] = None
    """API key for Jina."""
    BING_SEARCH_V7_ENDPOINT: Optional[str] = None
    """The endpoint for Bing Search V7."""
    BING_SEARCH_V7_SUBSCRIPTION_KEY: Optional[str] = None
    """The subscription key for Bing Search V7."""
    EXA_API_KEY: Optional[str] = None
    """API key for Exa."""
    PERPLEXITY_API_KEY: Optional[str] = None
    """API key for Perplexity."""
    PERPLEXITY_MODEL: Optional[str] = None
    """The model to use for Perplexity."""
    PERPLEXITY_SEARCH_CONTEXT_USAGE: Optional[str] = None
    """The search context usage for Perplexity."""
    PERPLEXITY_SEARCH_API_URL: Optional[str] = None
    """The search API URL for Perplexity."""
    SOUGOU_API_SID: Optional[str] = None
    """The SID for Sougou API."""
    SOUGOU_API_SK: Optional[str] = None
    """The SK for Sougou API."""
    WEB_LOADER_ENGINE: Optional[str] = None
    """The web loader engine to use."""
    ENABLE_WEB_LOADER_SSL_VERIFICATION: Optional[bool] = None
    """Whether to enable SSL verification for the web loader."""
    PLAYWRIGHT_WS_URL: Optional[str] = None
    """The WebSocket URL for Playwright."""
    PLAYWRIGHT_TIMEOUT: Optional[int] = None
    """The timeout for Playwright."""
    FIRECRAWL_API_KEY: Optional[str] = None
    """API key for Firecrawl."""
    FIRECRAWL_API_BASE_URL: Optional[str] = None
    """The base URL for Firecrawl."""
    TAVILY_EXTRACT_DEPTH: Optional[str] = None
    """The extract depth for Tavily."""
    EXTERNAL_WEB_SEARCH_URL: Optional[str] = None
    """The URL for external web search."""
    EXTERNAL_WEB_SEARCH_API_KEY: Optional[str] = None
    """The API key for external web search."""
    EXTERNAL_WEB_LOADER_URL: Optional[str] = None
    """The URL for external web loader."""
    EXTERNAL_WEB_LOADER_API_KEY: Optional[str] = None
    """The API key for external web loader."""
    YOUTUBE_LOADER_LANGUAGE: Optional[List[str]] = None
    """List of languages for YouTube loader."""
    YOUTUBE_LOADER_PROXY_URL: Optional[str] = None
    """The proxy URL for YouTube loader."""
    YOUTUBE_LOADER_TRANSLATION: Optional[str] = None
    """The translation language for YouTube loader."""

class ConfigForm(BaseModel):
    """
    Configuration form for retrieval settings.
    """
    # RAG settings
    RAG_TEMPLATE: Optional[str] = None
    """Template for RAG."""
    TOP_K: Optional[int] = None
    """Top K results to retrieve."""
    BYPASS_EMBEDDING_AND_RETRIEVAL: Optional[bool] = None
    """Whether to bypass embedding and retrieval."""
    RAG_FULL_CONTEXT: Optional[bool] = None
    """Whether to use full context for RAG."""

    # Hybrid search settings
    ENABLE_RAG_HYBRID_SEARCH: Optional[bool] = None
    """Whether to enable hybrid search."""
    ENABLE_RAG_HYBRID_SEARCH_ENRICHED_TEXTS: Optional[bool] = None
    """Whether to enable enriched texts for hybrid search."""
    TOP_K_RERANKER: Optional[int] = None
    """Top K results for reranker."""
    RELEVANCE_THRESHOLD: Optional[float] = None
    """Relevance threshold for search results."""
    HYBRID_BM25_WEIGHT: Optional[float] = None
    """Weight for BM25 in hybrid search."""

    # Content extraction settings
    CONTENT_EXTRACTION_ENGINE: Optional[str] = None
    """Engine for content extraction."""
    PDF_EXTRACT_IMAGES: Optional[bool] = None
    """Whether to extract images from PDFs."""

    DATALAB_MARKER_API_KEY: Optional[str] = None
    """API key for DataLab Marker."""
    DATALAB_MARKER_API_BASE_URL: Optional[str] = None
    """Base URL for DataLab Marker API."""
    DATALAB_MARKER_ADDITIONAL_CONFIG: Optional[str] = None
    """Additional configuration for DataLab Marker."""
    DATALAB_MARKER_SKIP_CACHE: Optional[bool] = None
    """Whether to skip cache for DataLab Marker."""
    DATALAB_MARKER_FORCE_OCR: Optional[bool] = None
    """Whether to force OCR for DataLab Marker."""
    DATALAB_MARKER_PAGINATE: Optional[bool] = None
    """Whether to paginate results for DataLab Marker."""
    DATALAB_MARKER_STRIP_EXISTING_OCR: Optional[bool] = None
    """Whether to strip existing OCR for DataLab Marker."""
    DATALAB_MARKER_DISABLE_IMAGE_EXTRACTION: Optional[bool] = None
    """Whether to disable image extraction for DataLab Marker."""
    DATALAB_MARKER_FORMAT_LINES: Optional[bool] = None
    """Whether to format lines for DataLab Marker."""
    DATALAB_MARKER_USE_LLM: Optional[bool] = None
    """Whether to use LLM for DataLab Marker."""
    DATALAB_MARKER_OUTPUT_FORMAT: Optional[str] = None
    """Output format for DataLab Marker."""

    EXTERNAL_DOCUMENT_LOADER_URL: Optional[str] = None
    """URL for external document loader."""
    EXTERNAL_DOCUMENT_LOADER_API_KEY: Optional[str] = None
    """API key for external document loader."""

    TIKA_SERVER_URL: Optional[str] = None
    """URL for Tika server."""
    DOCLING_SERVER_URL: Optional[str] = None
    """URL for Docling server."""
    DOCLING_API_KEY: Optional[str] = None
    """API key for Docling."""
    DOCLING_PARAMS: Optional[Dict] = None
    """Parameters for Docling."""
    DOCUMENT_INTELLIGENCE_ENDPOINT: Optional[str] = None
    """Endpoint for Document Intelligence."""
    DOCUMENT_INTELLIGENCE_KEY: Optional[str] = None
    """Key for Document Intelligence."""
    DOCUMENT_INTELLIGENCE_MODEL: Optional[str] = None
    """Model for Document Intelligence."""
    MISTRAL_OCR_API_BASE_URL: Optional[str] = None
    """Base URL for Mistral OCR API."""
    MISTRAL_OCR_API_KEY: Optional[str] = None
    """API key for Mistral OCR."""

    # MinerU settings
    MINERU_API_MODE: Optional[str] = None
    """API mode for MinerU."""
    MINERU_API_URL: Optional[str] = None
    """URL for MinerU API."""
    MINERU_API_KEY: Optional[str] = None
    """API key for MinerU."""
    MINERU_PARAMS: Optional[Dict] = None
    """Parameters for MinerU."""

    # Reranking settings
    RAG_RERANKING_MODEL: Optional[str] = None
    """Model for RAG reranking."""
    RAG_RERANKING_ENGINE: Optional[str] = None
    """Engine for RAG reranking."""
    RAG_EXTERNAL_RERANKER_URL: Optional[str] = None
    """URL for external reranker."""
    RAG_EXTERNAL_RERANKER_API_KEY: Optional[str] = None
    """API key for external reranker."""

    # Chunking settings
    TEXT_SPLITTER: Optional[str] = None
    """Text splitter to use."""
    CHUNK_SIZE: Optional[int] = None
    """Size of text chunks."""
    CHUNK_OVERLAP: Optional[int] = None
    """Overlap between text chunks."""

    # File upload settings
    FILE_MAX_SIZE: Optional[int] = None
    """Maximum size of uploaded files."""
    FILE_MAX_COUNT: Optional[int] = None
    """Maximum count of uploaded files."""
    FILE_IMAGE_COMPRESSION_WIDTH: Optional[int] = None
    """Width for image compression."""
    FILE_IMAGE_COMPRESSION_HEIGHT: Optional[int] = None
    """Height for image compression."""
    ALLOWED_FILE_EXTENSIONS: Optional[List[str]] = None
    """List of allowed file extensions."""

    # Integration settings
    ENABLE_GOOGLE_DRIVE_INTEGRATION: Optional[bool] = None
    """Whether to enable Google Drive integration."""
    ENABLE_ONEDRIVE_INTEGRATION: Optional[bool] = None
    """Whether to enable OneDrive integration."""

    # Web search settings
    web: Optional[WebConfig] = None
    """Web search configuration."""

class ProcessFileForm(BaseModel):
    """
    Form for processing a file.
    """
    file_id: str
    """The ID of the file to process."""
    content: Optional[str] = None
    """The content of the file."""
    collection_name: Optional[str] = None
    """The name of the collection."""

class ProcessTextForm(BaseModel):
    """
    Form for processing text.
    """
    name: str
    """The name of the text."""
    content: str
    """The text content."""
    collection_name: Optional[str] = None
    """The name of the collection."""

class QueryDocForm(BaseModel):
    """
    Form for querying a document.
    """
    collection_name: str
    """The name of the collection to query."""
    query: str
    """The search query."""
    k: Optional[int] = None
    """Number of results to retrieve."""
    k_reranker: Optional[int] = None
    """Number of results to rerank."""
    r: Optional[float] = None
    """Relevance threshold."""
    hybrid: Optional[bool] = None
    """Whether to use hybrid search."""
    hybrid_bm25_weight: Optional[float] = None
    """Weight for BM25 in hybrid search."""

class QueryCollectionsForm(BaseModel):
    """
    Form for querying multiple collections.
    """
    collection_names: List[str]
    """List of collection names to query."""
    query: str
    """The search query."""
    k: Optional[int] = None
    """Number of results to retrieve."""
    k_reranker: Optional[int] = None
    """Number of results to rerank."""
    r: Optional[float] = None
    """Relevance threshold."""
    hybrid: Optional[bool] = None
    """Whether to use hybrid search."""
    hybrid_bm25_weight: Optional[float] = None
    """Weight for BM25 in hybrid search."""
    enable_enriched_texts: Optional[bool] = None
    """Whether to enable enriched texts."""

class DeleteForm(BaseModel):
    """
    Form for deleting a file from a collection.
    """
    collection_name: str
    """The name of the collection."""
    file_id: str
    """The ID of the file to delete."""

class BatchProcessFilesForm(BaseModel):
    """
    Form for batch processing files.
    """
    files: List[FileModel]
    """List of files to process."""
    collection_name: str
    """The name of the collection."""

class BatchProcessFilesResult(BaseModel):
    """
    Result of a batch file processing operation.
    """
    file_id: str
    """The ID of the file."""
    status: str
    """The status of the processing."""
    error: Optional[str] = None
    """The error message if processing failed."""

class BatchProcessFilesResponse(BaseModel):
    """
    Response for batch process files request.
    """
    results: List[BatchProcessFilesResult]
    """List of successful results."""
    errors: List[BatchProcessFilesResult]
    """List of failed results."""

