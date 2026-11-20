# FocusFlow roadmap

## Milestone 0 — Repository and engineering foundation
- Independent private GitHub repository
- Repeatable local setup
- Linting and automated tests
- Android and Windows CI

## Milestone 1 — Reliable core
- Timer state machine and customizable durations
- Session persistence and recovery after app restart
- Task CRUD, priorities, due dates and study plans
- Settings and data migration

## Milestone 2 — Platform reliability
- Android notification channel and foreground-service assessment
- Android battery-optimization guidance
- Windows notifications and startup/background behavior
- Permission education and graceful degradation

## Milestone 3 — Focus protection
- Research supported app/website restriction approaches
- Explicit opt-in, emergency exit and safe recovery
- Usage tracking only with user-granted permissions

## Milestone 4 — Study experience
- Audio and soundscape controls
- Themes, wallpapers and accessibility
- Study rooms after privacy/security design

## Milestone 5 — Insights and sync
- Analytics, streaks, reports and CSV export
- Optional encrypted cloud sync
- Backup, restore and migration tools

## Release gates
- Unit and UI tests pass
- Android APK builds and installs on supported test devices
- Windows executable runs on a clean test machine
- Permissions and limitations documented
- No feature advertised as implemented unless verified
