# Task Backlog

## High Priority
- [ ] **Test Full Application Functionality:** Verify JNI calls and database interactions beyond login.
- [ ] **Install MariaDB Connector C:** Set PATH for full JNI if needed.
- [ ] **DLL Placement:** Verify if DLLs need to be in `WEB-INF/lib` for production deployment.

## Configuration
- [ ] **Create INI Files:** `MBConfigure.ini` and `RDBConfigure.ini` if needed.
- [ ] **External Processes:** Start `exBroker.exe` and `exReplier.exe` (or mock them).

## Tech Debt
- [ ] **Refactor XML to JavaConfig:** Continue migrating any remaining `web.xml` parts if possible.
- [ ] **Logging:** Standardize Logback configuration.
