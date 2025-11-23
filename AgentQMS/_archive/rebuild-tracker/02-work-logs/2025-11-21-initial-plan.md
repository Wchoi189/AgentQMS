---
timestamp: November 21, 2025, 14:30
---

# KPX Topas Remake Implementation Plan (Legacy)

## Status Summary
- **Last Completed**: Fixed port conflict (changed MariaDB to 3307).
- **Current Task**: Containers starting.
- **Next Task**: Test app access and SSH.

## Progress Tracker

### Phase 0: Optional Docker Setup (For Isolation)
- [x] Install Docker Desktop
- [x] Build Dockerfile and docker-compose
- [x] Handle custom Tomcat libs
- [x] Add SSH support
- [x] Add ports for future frontend (Next.js 3000, Vite 5173)
- [x] Repurpose .bashrc with PS1 and convenience features
- [ ] Test containerized build
- [ ] Run services (app, MariaDB)
- [ ] Access app in container

### Phase 2: Database Setup
- [ ] Install MariaDB server
- [ ] Create database (e.g., topasdb)
- [ ] Infer/create schema from MyBatis mappers
- [ ] Populate with sample data (data.json)
- [ ] Test JDBC connection

### Phase 3: JNI and Ellux Setup
- [ ] Install MariaDB Connector C 3.1.9
- [ ] Set PATH for MariaDB lib
- [ ] Copy DLLs from topas64_dev\bin to src/main/webapp/WEB-INF/lib
- [ ] Source/create elxJNI.jar
- [ ] Create server.ini with DB/Broker/NAS configs
- [ ] Locate/source exBroker.exe and exReplier.exe
- [ ] Test JNI connections (run exes first, then Java)

### Phase 4: Build and Compile
- [ ] Maven clean compile (local profile)
- [ ] Resolve any missing dependencies/JARs
- [ ] Fix compilation errors
- [ ] Run Maven package (WAR generation)

### Phase 5: Deployment and Testing
- [ ] Deploy WAR to Tomcat
- [ ] Start Tomcat
- [ ] Test basic app startup (login page)
- [ ] Test database connectivity
- [ ] Test JNI calls (if brokers available)
- [ ] Test WebSocket/SSE features

### Phase 6: Frontend Build
- [ ] Install Node.js/npm
- [ ] Run npm install
- [ ] Transpile JS: npm run babel
- [ ] Test frontend loading

### Phase 7: Integration Testing
- [ ] End-to-end testing (full workflows)
- [ ] Validate NAS/SFTP
- [ ] Check HWP handling
- [ ] Performance/load testing (basic)

### Phase 8: Incremental Modernization
- [ ] Upgrade to Spring Boot 2.x (keep Java 8)
- [ ] Replace XML configs with Java config
- [ ] Add embedded Tomcat
- [ ] Modernize frontend (Vite/React later)
- [ ] Containerize with Docker

### Phase 9: Full Modernization (Future)
- [ ] Java 11+, Spring Boot 3
- [ ] Microservices if needed
- [ ] CI/CD pipeline

## Notes
- Prioritize getting existing version running before major changes.
- Update this tracker after each task completion.
- Use sub-trackers for complex phases (e.g., JNI setup).
