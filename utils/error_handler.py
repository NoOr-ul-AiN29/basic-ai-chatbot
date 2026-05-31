def handle_error(error: Exception) -> str:
    msg = str(error).lower()

    if "authentication" in msg or "invalid api key" in msg or "api key" in msg:
        return (
            "🔑 **Authentication Error:** Your API key is invalid or missing.\n\n"
            "**Fix:** Check that `GROQ_API_KEY` is set correctly in your environment."
        )

    if "rate limit" in msg or "quota" in msg or "429" in msg:
        return (
            "⏳ **Rate Limit Reached:** You've hit your API quota or are sending too many requests.\n\n"
            "**Fix:** Wait a moment, then try again."
        )

    if "connection" in msg or "network" in msg or "timeout" in msg:
        return (
            "🌐 **Connection Error:** Unable to reach the API server.\n\n"
            "**Fix:** Check your internet connection and try again."
        )

    if any(code in msg for code in ["400", "404", "500", "502", "503"]):
        return (
            f"⚠️ **API Error:** {str(error)}\n\n"
            "**Fix:** Review the error message above and adjust your request."
        )

    return (
        f"❌ **Unexpected Error:** {str(error)}\n\n"
        "Please try again. If the problem persists, check the server logs."
    )
