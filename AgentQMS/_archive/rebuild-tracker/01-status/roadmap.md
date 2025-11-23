# Project Roadmap

## Phase 1: Stabilization (Current)
**Goal:** Get the existing legacy application running in a containerized environment with minimal code changes.
- [x] Dockerize Environment (Tomcat, MariaDB)
- [x] Fix Build System (Maven)
- [x] JNI Integration
- [x] Basic Login Functionality
- [ ] Full Application Functionality Testing

## Phase 2: Incremental Modernization
**Goal:** Improve developer experience and maintainability without rewriting the core logic.
- [ ] **Backend:** Migrate to Spring Boot 2.x (Java 8 compatible)
  - Replace XML configuration with JavaConfig
  - Use Embedded Tomcat
- [ ] **Frontend:** Introduce modern build tool (Vite/Webpack) while keeping jQuery/Thymeleaf
- [ ] **CI/CD:** Basic GitHub Actions pipeline

## Phase 3: Architecture Evolution (Future)
**Goal:** Upgrade technology stack to modern standards.
- [ ] Upgrade to Java 17/21
- [ ] Upgrade to Spring Boot 3.x
- [ ] Refactor Frontend to React/Vue
- [ ] Container Orchestration (K8s)
