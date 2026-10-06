# Phase 2: Concurrency & Performance Optimization - Discussion Log

**Date:** 2026-10-06

## 1. Telemetry File Locking
**Options presented:**
- `os.replace` (atomic rename, zero dependencies)
- `filelock` (requires pip install, true cross-process lock)

**Selection:** `os.replace` (atomic rename, zero dependencies)

## 2. TigerGraph Error Surfacing
**Options presented:**
- `st.toast()` - Subtle notification, allows user to keep using the chat
- `st.error()` - Intrusive, prominent blocking error

**Selection:** `st.toast()` - Subtle notification, allows user to keep using the chat

## 3. Map Rendering Separation
**Options presented:**
- Pre-render static layer and overlay a dynamic outages layer (uses `@st.cache_data` for static graph)
- Use update triggers on a single layer (relies on PyDeck to manage state updates)

**Selection:** Pre-render static layer and overlay a dynamic outages layer (uses `@st.cache_data` for static graph)
