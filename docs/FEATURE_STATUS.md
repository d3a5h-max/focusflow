# Feature status

Status meanings: **Implemented** = present in this starter and testable; **Planned** = not implemented; **Platform research required** = feasibility and permissions must be assessed before coding.

| Feature | Status | Notes |
|---|---|---|
| Basic focus countdown | Implemented | 25-minute prototype; not yet persistent across process death |
| Start / pause / reset | Implemented | In-app while process is alive |
| Local task list | Implemented | SQLite persistence |
| Custom focus/break durations | Planned | Settings UI and validation needed |
| Session history and analytics | Planned | Requires session model |
| Reliable background timer | Platform research required | Android foreground service/notifications; Windows lifecycle |
| App blocking | Platform research required | Android restrictions and accessibility policy; Windows controls |
| Usage tracking | Platform research required | Android Usage Access; Windows privacy model |
| Website blocking | Platform research required | Browser/platform-specific options |
| Music, alarms, vibration | Planned | Platform-specific audio and notification layers |
| Themes and wallpapers | Planned | Asset and theme system |
| Study rooms / multiplayer | Planned | Requires backend, identity, moderation and network design |
| Cloud sync | Planned | Optional, with conflict and privacy design |
| CSV export | Planned | After session and task reporting models exist |
