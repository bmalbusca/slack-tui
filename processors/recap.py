"""Channel recap manager with Q/E navigation."""
from datetime import datetime
from typing import List, Dict, Optional
import time


class RecapManager:
    """Manages channel recaps."""
    
    def __init__(self, message_handler):
        self.handler = message_handler
        self.recaps = []
        self.current_index = 0
    
    def generate_recaps(self, types: str = "public_channel", messages_per_channel: int = 10) -> List[Dict]:
        """Generate recaps for all channels."""
        channels = self.handler.get_channels(types=types)
        member_channels = [c for c in channels if c.get('is_member')]
        
        self.recaps = []
        
        for channel in member_channels:
            try:
                messages = self.handler.get_messages(channel['id'], messages_per_channel)
                
                if not messages:
                    continue
                
                recap = self._create_recap(channel, messages)
                self.recaps.append(recap)
            except Exception as e:
                continue
        
        self.recaps.sort(key=lambda x: x['latest_timestamp'], reverse=True)
        self.current_index = 0
        return self.recaps
    
    def _create_recap(self, channel: Dict, messages: List[Dict]) -> Dict:
        """Create recap summary for a channel."""
        participants = set(msg.get('user') for msg in messages if msg.get('user'))
        latest_ts = max(float(msg['ts']) for msg in messages)
        threads = sum(1 for msg in messages if msg.get('reply_count', 0) > 0)
        
        return {
            'channel_id': channel['id'],
            'channel_name': channel['name'],
            'channel_topic': channel.get('topic', {}).get('value', ''),
            'total_messages': len(messages),
            'participants': len(participants),
            'threads': threads,
            'latest_timestamp': latest_ts,
            'preview_messages': messages[:5]
        }
    
    def get_current_recap(self) -> Optional[Dict]:
        """Get current recap."""
        if not self.recaps or self.current_index >= len(self.recaps):
            return None
        return self.recaps[self.current_index]
    
    def next_recap(self) -> Optional[Dict]:
        """Move to next recap."""
        if not self.recaps:
            return None
        self.current_index = (self.current_index + 1) % len(self.recaps)
        return self.get_current_recap()
    
    def previous_recap(self) -> Optional[Dict]:
        """Move to previous recap."""
        if not self.recaps:
            return None
        self.current_index = (self.current_index - 1) % len(self.recaps)
        return self.get_current_recap()
    
    def format_recap(self, recap: Dict, detailed: bool = False) -> str:
        """Format recap for display."""
        channel_name = recap['channel_name']
        total_messages = recap['total_messages']
        participants = recap['participants']
        threads = recap['threads']
        
        time_ago = self._time_ago(recap['latest_timestamp'])
        
        output = [
            f"{'='*60}",
            f"  #{channel_name}",
            f"{'='*60}",
            ""
        ]
        
        if recap['channel_topic']:
            output.append(f"  📝 {recap['channel_topic']}")
            output.append("")
        
        output.append(f"  📊 Activity Summary:")
        output.append(f"     • {total_messages} messages")
        output.append(f"     • {participants} participants")
        output.append(f"     • {threads} threads")
        output.append(f"     • Last active: {time_ago}")
        output.append("")
        
        if detailed:
            output.append(f"  💬 Recent Messages:")
            output.append("")
            
            for msg in recap['preview_messages']:
                formatted = self.handler.format_message(msg, compact=True)
                output.append(f"     {formatted}")
            
            output.append("")
        
        output.append(f"  {'─'*56}")
        output.append(f"  [Q] Previous   |   [{self.current_index + 1}/{len(self.recaps)}]   |   [E] Next")
        output.append(f"  {'─'*56}")
        
        return '\n'.join(output)
    
    def _time_ago(self, timestamp: float) -> str:
        """Format timestamp as relative time."""
        now = time.time()
        diff = now - timestamp
        
        if diff < 60:
            return "just now"
        elif diff < 3600:
            mins = int(diff / 60)
            return f"{mins} minute{'s' if mins != 1 else ''} ago"
        elif diff < 86400:
            hours = int(diff / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = int(diff / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
