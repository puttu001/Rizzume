async def test_synthesize_speech_returns_audio(async_client, mock_tts_synthesize) -> None:
    response = await async_client.post("/speech", json={"text": "Tell me about yourself."})
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert response.content == b"fake-mp3-bytes"
    mock_tts_synthesize.assert_called_once_with("Tell me about yourself.")
