# Permissions matrix

This app uses Slack's **Web API** via `slack_sdk.WebClient`. Authentication (`auth.test`) may succeed even when a token cannot read channels/messages. For each command below, the table lists the Slack API methods called and the **minimum** OAuth scopes required.

> Defaults: the app now defaults to `--types public_channel` to minimize scopes.

## Commands → API methods → required scopes

| Command / Flag | Slack Web API methods | Minimum scopes (user `xoxp` or bot `xoxb`) | Notes |
|---|---|---|---|
| `--channels` | `conversations.list` | `channels:read` | With `--types public_channel` only. Add `groups:read`, `im:read`, `mpim:read` if you include those types. |
| `--show #channel -l N` | `conversations.list` (resolve), `conversations.history` | `channels:read`, `channels:history` | For public channels only. Private channels require `groups:read`, `groups:history`. DMs require `im:*` / `mpim:*`. |
| `--send #channel "msg"` | `conversations.list` (resolve), `chat.postMessage` | `channels:read`, `chat:write` | Posting to private channels/DMs requires the corresponding conversation type scopes and membership. |
| `--vip` / `--vip-list` | (local only) + message retrieval below | depends | VIP listing itself is local; fetching VIP messages uses `conversations.history` and user lookup. |
| `--vip-add @user` / `--vip-remove @user` | `users.list` (cache) or `users.info` | `users:read` | Needed to resolve usernames to IDs. |
| VIP message fetch | `conversations.history`, `users.info` | `channels:history`, `users:read` | Requires the same conversation-type scope as the source (public/private/DM). |
| `--search "query"` | `search.messages` | `search:read` | Search is often restricted by workspace policy; may fail even with scopes. |
| `--recap` | `conversations.list`, `conversations.history` | `channels:read`, `channels:history` | Uses selected `--types`. Interactive mode is terminal-only. |

## Token types (what’s actually supported)

- **`xoxb-…` Bot token (recommended)**: Web API token; best for CLI tools. Must have the scopes above.
- **`xoxp-…` User token**: Web API token; works if your workspace allows it and the token has scopes.
- **`xapp-…` App-level token**: **NOT** a Web API token. Used only for Socket Mode. This app will authenticate via `auth.test` in some cases but Web API calls will fail.
- **`xoxe…` Enterprise tokens**: often short-lived and/or restricted. This app **does not** implement OAuth refresh; if your token expires you must refresh it outside the app.

