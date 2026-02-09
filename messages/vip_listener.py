"""VIP message listener and filtering."""
from typing import List, Dict


class VIPListener:
    """Handles VIP message filtering."""
    
    def __init__(self, message_handler, settings):
        self.handler = message_handler
        self.settings = settings
    
    def get_vip_messages(self, limit_per_channel: int = 50) -> List[Dict]:
        """Get recent messages from VIP users."""
        vip_users = self.settings.get_vip_users()
        vip_user_ids = [u['id'] for u in vip_users]
        
        if not vip_user_ids:
            return []
        
        vip_messages = []
        channels = self.handler.get_channels()
        
        for channel in channels:
            if not channel.get('is_member'):
                continue
            
            messages = self.handler.get_messages(channel['id'], limit_per_channel)
            
            for msg in messages:
                if msg.get('user') in vip_user_ids:
                    msg['channel_id'] = channel['id']
                    msg['channel_name'] = channel['name']
                    vip_messages.append(msg)
        
        vip_messages.sort(key=lambda x: float(x.get('ts', 0)), reverse=True)
        return vip_messages
    
    def format_vip_message(self, msg: Dict, compact: bool = True) -> str:
        """Format VIP message with channel context."""
        base_format = self.handler.format_message(msg, compact)
        channel_name = msg.get('channel_name', 'unknown')
        
        if compact:
            return f"#{channel_name:15} | {base_format}"
        else:
            return f"Channel: #{channel_name}\n{base_format}"
