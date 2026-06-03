import pytest
from owui_client.models.utils import CodeForm, MarkdownForm

@pytest.mark.asyncio
async def test_get_gravatar(client):
    email = "test@example.com"
    # Gravatar URL usually contains md5 of email
    url = await client.utils.get_gravatar(email)
    assert isinstance(url, str)
    assert "gravatar.com" in url

@pytest.mark.asyncio
async def test_format_code(client):
    code = "def foo():\n  print('hello')"
    form = CodeForm(code=code)
    result = await client.utils.format_code(form)
    assert isinstance(result, dict)
    assert "code" in result
    # Black formatting might change quotes
    assert "def foo():" in result["code"]

@pytest.mark.asyncio
@pytest.mark.xfail(
    reason="The /v1/utils/markdown endpoint was removed in Open WebUI 0.9.6; "
           "the client method is retained for forward compatibility. "
           "Remove or update this test if the endpoint returns in a future release.",
    strict=False,
)
async def test_markdown(client):
    md = "# Hello\n* world"
    form = MarkdownForm(md=md)
    result = await client.utils.get_html_from_markdown(form)
    assert isinstance(result, dict)
    assert "html" in result
    assert "<h1>Hello</h1>" in result["html"]

