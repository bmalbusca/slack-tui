"""Autocomplete functionality for channels and users."""
from typing import List, Tuple


def fuzzy_match_channels(query: str, channels: List[dict]) -> List[Tuple[dict, int]]:
    """Fuzzy match channels by name."""
    query = query.lower().strip('#')
    matches = []
    
    for channel in channels:
        name = channel['name'].lower()
        
        if name == query:
            matches.append((channel, 100))
        elif name.startswith(query):
            matches.append((channel, 90))
        elif query in name:
            matches.append((channel, 70))
        elif all(c in name for c in query):
            matches.append((channel, 50))
    
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def fuzzy_match_users(query: str, users: List[dict]) -> List[Tuple[dict, int]]:
    """Fuzzy match users by name."""
    query = query.lower().strip('@')
    matches = []
    
    for user in users:
        if user.get('deleted'):
            continue
        
        username = user['name'].lower()
        real_name = user.get('real_name', '').lower()
        
        if username == query:
            matches.append((user, 100))
        elif real_name == query:
            matches.append((user, 95))
        elif username.startswith(query):
            matches.append((user, 90))
        elif query in username or query in real_name:
            matches.append((user, 70))
    
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def display_matches(matches: List[Tuple[dict, int]], match_type: str = "channel"):
    """Display numbered list of matches."""
    if not matches:
        print(f"No {match_type}s found.")
        return
    
    print(f"\nFound {len(matches)} {match_type}(s):\n")
    
    for idx, (item, score) in enumerate(matches, 1):
        if match_type == "channel":
            name = item['name']
            topic = item.get('topic', {}).get('value', 'No topic')[:60]
            print(f"  {idx}. #{name}")
            print(f"     {topic}\n")
        else:
            username = item['name']
            real_name = item.get('real_name', '')
            print(f"  {idx}. @{username} ({real_name})\n")
