"""Message handler for Slack API operations."""
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackPermissionError(Exception):
    """Raised when the Slack API rejects a call due to token type or missing scopes."""

    def __init__(self, *, method: str, error: str, needed: str | None = None, provided: str | None = None):
        self.method = method
        self.error = error
        self.needed = needed
        self.provided = provided
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        parts = [f"{self.method}: {self.error}"]
        if self.needed:
            parts.append(f"needed={self.needed}")
        if self.provided:
            parts.append(f"provided={self.provided}")
        return " ".join(parts)


class MessageHandler:
    """Handles Slack message operations."""
    
    def __init__(self, client: WebClient):
        self.client = client
        self.message_cache = {}  # msg_id -> {channel, ts}
        self.channel_cache = {}  # id/name -> channel info
        self.user_cache = {}     # id/name -> user info
    
    # ============= Message ID Management =============
    
    def generate_message_id(self, channel: str, ts: str) -> str:
        """Generate 8-char message ID."""
        msg_hash = hashlib.md5(f"{channel}:{ts}".encode()).hexdigest()[:8]
        self.message_cache[msg_hash] = {"channel": channel, "ts": ts}
        return msg_hash
    
    # ============= Channel Operations =============
    
    def get_channels(self, types: str = "public_channel") -> List[Dict]:
        """Get channels/conversations for the given types.

        Default is public channels only, to minimize required scopes.
        """
        try:
            result = self.client.conversations_list(
                types=types,
                exclude_archived=True,
                limit=1000,
            )
            channels = result.get("channels", [])

            # Cache channels
            for channel in channels:
                self.channel_cache[channel["id"]] = channel
                if "name" in channel:
                    self.channel_cache[channel["name"]] = channel

            return channels
        except SlackApiError as e:
            data = getattr(e.response, "data", {}) or {}
            error = data.get("error", "unknown_error")
            raise SlackPermissionError(
                method="conversations.list",
                error=error,
                needed=data.get("needed"),
                provided=data.get("provided"),
            ) from e
    
    def get_channel(self, channel_id: str) -> Optional[Dict]:
        """Get channel info."""
        if channel_id in self.channel_cache:
            return self.channel_cache[channel_id]
        
        try:
            result = self.client.conversations_info(channel=channel_id)
            channel = result["channel"]
            self.channel_cache[channel_id] = channel
            return channel
        except SlackApiError as e:
            data = getattr(e.response, 'data', {}) or {}
            error = data.get('error', 'unknown_error')
            raise SlackPermissionError(method='conversations.info', error=error, needed=data.get('needed'), provided=data.get('provided')) from e
    
    def resolve_channel(self, identifier: str, types: str = "public_channel") -> Optional[str]:
        """Resolve channel name/ID to channel ID using the allowed conversation types."""
        identifier = identifier.lstrip("#")

        # Already an ID
        if identifier.startswith(("C", "D", "G")):
            return identifier

        # Check cache
        if identifier in self.channel_cache:
            return self.channel_cache[identifier].get("id")

        # Refresh cache with allowed types
        self.get_channels(types=types)
        if identifier in self.channel_cache:
            return self.channel_cache[identifier].get("id")

        return None
    
    # ============= User Operations =============
    
    def get_users(self) -> List[Dict]:
        """Get all users."""
        try:
            result = self.client.users_list()
            users = result.get("members", [])
            
            # Cache users
            for user in users:
                self.user_cache[user["id"]] = user
                self.user_cache[user["name"]] = user
            
            return users
        except SlackApiError as e:
            data = getattr(e.response, 'data', {}) or {}
            error = data.get('error', 'unknown_error')
            raise SlackPermissionError(method='users.list', error=error, needed=data.get('needed'), provided=data.get('provided')) from e
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user info."""
        if user_id in self.user_cache:
            return self.user_cache[user_id]
        
        try:
            result = self.client.users_info(user=user_id)
            user = result["user"]
            self.user_cache[user_id] = user
            return user
        except SlackApiError as e:
            data = getattr(e.response, 'data', {}) or {}
            error = data.get('error', 'unknown_error')
            raise SlackPermissionError(method='users.info', error=error, needed=data.get('needed'), provided=data.get('provided')) from e
    
    def resolve_user(self, identifier: str) -> Optional[str]:
        """Resolve username/ID to user ID."""
        identifier = identifier.lstrip("@")
        
        # Already an ID
        if identifier.startswith("U"):
            return identifier
        
        # Check cache
        if identifier in self.user_cache:
            return self.user_cache[identifier].get("id")
        
        # Search users
        self.get_users()
        if identifier in self.user_cache:
            return self.user_cache[identifier].get("id")
        
        return None
    
    # ============= Message Operations =============
    
    def get_messages(self, channel_id: str, limit: int = 20, 
                    latest: Optional[str] = None) -> List[Dict]:
        """Get messages from channel."""
        try:
            kwargs = {"channel": channel_id, "limit": limit}
            if latest:
                kwargs["latest"] = latest
            
            result = self.client.conversations_history(**kwargs)
            messages = result.get("messages", [])
            
            # Add message IDs
            for msg in messages:
                msg["msg_id"] = self.generate_message_id(channel_id, msg["ts"])
            
            return messages
        except SlackApiError as e:
            data = getattr(e.response, 'data', {}) or {}
            error = data.get('error', 'unknown_error')
            raise SlackPermissionError(method='conversations.history', error=error, needed=data.get('needed'), provided=data.get('provided')) from e
    
    def send_message(self, channel_id: str, text: str, 
                    thread_ts: Optional[str] = None) -> Optional[Dict]:
        """Send message to channel."""
        try:
            kwargs = {"channel": channel_id, "text": text}
            if thread_ts:
                kwargs["thread_ts"] = thread_ts
            
            result = self.client.chat_postMessage(**kwargs)
            return result
        except SlackApiError as e:
            data = getattr(e.response, 'data', {}) or {}
            error = data.get('error', 'unknown_error')
            raise SlackPermissionError(method='chat.postMessage', error=error, needed=data.get('needed'), provided=data.get('provided')) from e
    
    def get_thread_replies(self, channel_id: str, thread_ts: str) -> List[Dict]:
        """Get thread replies."""
        try:
            result = self.client.conversations_replies(
                channel=channel_id,
                ts=thread_ts
            )
            messages = result.get("messages", [])
            
            # Add message IDs
            for msg in messages:
                msg["msg_id"] = self.generate_message_id(channel_id, msg["ts"])
            
            return messages
        except SlackApiError as e:
            data = getattr(e.response, 'data', {}) or {}
            error = data.get('error', 'unknown_error')
            raise SlackPermissionError(method='conversations.replies', error=error, needed=data.get('needed'), provided=data.get('provided')) from e
    
    def search_messages(self, query: str, count: int = 20) -> List[Dict]:
        """Search messages."""
        try:
            result = self.client.search_messages(query=query, count=count)
            matches = result.get("messages", {}).get("matches", [])
            
            # Add message IDs
            for msg in matches:
                channel_id = msg.get("channel", {}).get("id", "")
                if channel_id:
                    msg["msg_id"] = self.generate_message_id(channel_id, msg["ts"])
            
            return matches
        except SlackApiError as e:
            print(f"Error searching: {e.response['error']}")
            return []
    
    # ============= Formatting =============
    
    def format_message(self, msg: Dict, compact: bool = True) -> str:
        """Format message for display."""
        user = self.get_user(msg.get("user", ""))
        username = user["name"] if user else msg.get("user", "unknown")
        
        ts = float(msg.get("ts", 0))
        time_str = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        
        text = msg.get("text", "")
        msg_id = msg.get("msg_id", "????????")
        
        thread_marker = "🧵" if msg.get("reply_count", 0) > 0 else ""
        
        if compact:
            first_line = text.split("\n")[0][:80]
            return f"[{msg_id}] {time_str} {username}: {first_line} {thread_marker}"
        else:
            thread_info = f"\n  └─ {msg.get('reply_count', 0)} replies" if msg.get("reply_count") else ""
            return f"[{msg_id}] {time_str} {username}:\n  {text}{thread_info}"
