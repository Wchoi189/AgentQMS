# Current Project State

**Last Updated:** 2025-11-21
**Status:** 🟢 Operational (Basic Login Flow)

## System Health
- **Tomcat:** Running (Port 8080)
- **Database:** MariaDB 10.6 Running (Port 3307 -> 3306)
- **Brokers:** Dummy brokers running (Ports 12345, 12346)
- **Build:** Maven Build Success (WAR)
- **Deployment:** Docker Container `docker-app-1`

## Recent Achievements
- **Login Flow:** Fixed HTTP 405 error by implementing Post-Redirect-Get pattern in `LoginFailureHandler`.
- **Spring Security:** Successfully configured with `springSecurityFilterChain` in `web.xml`.
- **JNI:** Enabled and linked.

## Active Configuration
- **Login URL:** `/login`
- **Failure URL:** `/login?errorMsg=...`
- **Default User:** `admin` / `admin` (or as configured in DB)

## Known Issues
- None currently blocking.
