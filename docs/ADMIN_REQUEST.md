# Minimal Slack admin request template

Below are two options you can send to Slack admins. Pick A (minimal) or B (full).

---

## A) Minimal (public channels read-only)

Hi team,

I’m using a small internal terminal tool to **read recent messages from public channels** I’m a member of (no DMs/private channels required).  
Could you approve an internal Slack app install and grant a token with the minimum scopes below?

**Minimum scopes**
- `channels:read` (list public channels)
- `channels:history` (read message history in public channels)
- `users:read` (optional; only needed to resolve usernames / display sender info)

This would enable:
- listing my public channels
- fetching the last N messages from a public channel
- generating a simple recap of public channels

Thanks!

---

## B) Full functionality (public + private + DMs + search + send)

Hi team,

I’m using a small internal terminal tool to interact with Slack (read messages, generate recaps, optional sending).  
Could you approve an internal Slack app install and grant a token with the scopes below?

**Scopes (full set used by the tool)**
- Public channels: `channels:read`, `channels:history`
- Private channels: `groups:read`, `groups:history`
- DMs: `im:read`, `im:history`
- Group DMs: `mpim:read`, `mpim:history`
- User resolution: `users:read`
- Posting messages (optional): `chat:write`
- Search (optional): `search:read`

Why:
- `conversations.list/history` need the corresponding `*:read` / `*:history` scopes for each conversation type
- posting uses `chat.postMessage`
- user lookup uses `users.list/info`
- search uses `search.messages`

Thanks!

