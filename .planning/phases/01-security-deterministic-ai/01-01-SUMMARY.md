# 01-01: Remove hardcoded credentials and implement `.env` configuration

## Summary of Changes
- Created `.env.example` with placeholders for TigerGraph credentials and OpenWeather API key.
- Created local `.env` for testing.
- Refactored `tigergraph_client.py` to remove plain-text passwords and instead use `os.getenv` for `TG_HOST`, `TG_GRAPH`, `TG_USERNAME`, `TG_PASSWORD`, and `TG_SECRET`.
- Moved `load_dotenv()` to the very top of `app.py` to ensure environment variables are loaded before any other imports that might depend on them.

## Status
Completed successfully.
