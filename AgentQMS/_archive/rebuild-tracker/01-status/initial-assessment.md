### Project Assessment: KPX Topas Remake

Based on my survey of the project contents, I'll provide an overview of the architecture, key components, and a checklist of requirements to rebuild and compile the project successfully. The project is a Java-based web application for power system analysis (likely related to PSS/E simulations via Ellux API), using an older tech stack. The ".svn" folder contains Subversion version control data (thousands of files for tracking changes)—it's not core to the app and can be ignored or removed during rebuild.

#### Project Architecture Overview
- **Backend (Java)**: 
  - Framework: Spring MVC 4.3.22 (with Spring Security 4.2.3, WebSocket, and Thymeleaf templating).
  - ORM: MyBatis 3.5.0 for database interactions.
  - Database: MariaDB (via JDBC driver 2.6.1).
  - Configuration: Java-based (RootConfiguration.java), loading from `server.ini` (INI file in project root).
  - JNI Integration: Calls to external C libraries (elxJNI.jar) for Ellux API (power system simulation). Requires MariaDB Connector/C and JNI setup (detailed in `JNI설정및샘플.pptx`).
  - Real-time Features: WebSocket (Spring WebSocket) and Server-Sent Events (SSE) for live updates.
  - Security: Spring Security with custom configurations.
  - Logging: Logback.
  - Additional: eGovFramework (Korean gov framework), XSS filtering (Lucy), HWP document handling.

- **Frontend**:
  - Static Files: HTML, CSS, JS (jQuery, TUI Grid, etc.), served from `src/main/webapp/resources`.
  - Templating: Thymeleaf for dynamic pages.
  - Build: Babel transpiles ES6+ JS to ES5 (output to `es5js/` folder). Managed via npm (package.json).
  - No modern bundler (e.g., Webpack is present but basic); JS is manually transpiled.

- **Message Broker**:
  - Not a standard broker (e.g., no ActiveMQ, RabbitMQ, or Kafka). Instead, "brokers" refer to two Ellux API servers (external power simulation services) connected via JNI over TCP/IP.
  - Configured in `server.ini` (BROKER1 and BROKER2 sections with IP/port).
  - Used for API calls (e.g., inserting buses, lines, running simulations) via `ElluxApis.java` and JNI.

- **Other Components**:
  - NAS (Network-Attached Storage): SFTP-based file storage (configured in `server.ini`).
  - File Handling: Commons FileUpload, SSH (JSch) for NAS access.
  - Build: Maven (WAR packaging), with profiles for local (includes resources) and prod (separates static files via assembly plugin).
  - Version Control: Subversion (.svn folder)—can be discarded for Git-based rebuild.

- **Folder Structure Insights**:
  - `src/main/java`: Core logic (controllers, services, mappers).
  - `src/main/resources`: MyBatis mappers (XML), configs (logback.xml, XSS rules).
  - `src/main/webapp`: Static web content, JSPs, and libs (JARs for JNI/XSS).
  - `lib/`: Additional JARs (not in Maven).
  - `data.json`: Sample/test data.
  - `assembly_web_static_file_out.xml`: Maven config to package static files separately for prod.

The app appears monolithic (backend serves frontend), with heavy reliance on JNI for external computations. No microservices or cloud-native elements.

#### Requirements Checklist for Successful Compilation and Run
To rebuild incrementally, address these in order. Many files/libs are missing (e.g., JARs, configs), so you'll need to source or recreate them. Prioritize backend setup, then frontend, then JNI/Ellux.

1. **Java Development Environment**:
   - Install JDK 8 (OpenJDK 1.8.231 or compatible).
   - Install Maven 3.x.
   - Verify: `mvn -v` and `java -version`.

2. **Database Setup**:
   - Install MariaDB server (or MySQL-compatible).
   - Create database/schema (not provided; infer from MyBatis mappers in `src/main/resources/mapper/`—e.g., tables for buses, lines, users, etc.).
   - Populate with sample data if needed (use `data.json` as reference).
   - Ensure JDBC connectivity.

3. **Application Server**:
   - Install Apache Tomcat 8.5.571 (or compatible servlet container).
   - Configure for WAR deployment.

4. **JNI and Ellux API Setup** (Critical for Core Functionality)**:
   - Install MariaDB Connector/C 3.1.9 (Windows MSI; set env var `MARIADB_CONNECTOR_C_DIR`).
   - Follow `JNI설정및샘플.pptx` for JNI library registration (likely involves compiling/linking C code and setting `java.library.path`).
   - Source/recreate `elxJNI.jar` (system-scoped in pom.xml; path: `src/main/webapp/WEB-INF/lib/elxJNI.jar`).
   - Ensure Ellux servers (brokers) are running and accessible (external dependencies; IPs/ports in `server.ini`).
   - Test JNI calls (e.g., via `JNIRequest.Connect`).

5. **Configuration Files**:
   - Create `server.ini` in project root (INI format; sections: [DB], [BROKER1], [BROKER2], [NAS]). Example:
     ```
     [DB]
     URL=jdbc:mariadb://localhost:3306/topas
     USERNAME=user
     PASSWORD=pass
     [BROKER1]
     IP=192.168.1.10
     PORT=1234
     [BROKER2]
     IP=192.168.1.11
     PORT=1234
     [NAS]
     IP=192.168.1.20
     PORT=22
     ID=nasuser
     PASSWORD=naspass
     ```
   - Missing JARs: Source `lucy-xss-servlet-2.0.0.jar`, `lucy-xss-1.6.3.jar`, `ini4j-0.5.4.jar`, `ini4j-0.5.4-jdk14.jar` (system-scoped in pom.xml; place in `src/main/webapp/WEB-INF/lib/`).

6. **Frontend Build**:
   - Install Node.js/npm.
   - Run `npm install` (from package.json).
   - Transpile JS: `npm run babel` (watches `src/main/webapp/resources/js/` → `es5js/`).
   - For prod, use Maven assembly to separate static files.

7. **Build and Deploy**:
   - Local dev: `mvn clean install` (uses local profile; includes resources in WAR).
   - Prod: `mvn clean install -P prod` (excludes resources; generates `ROOT.war` + `kpx-topas-resource.zip`).
   - Deploy WAR to Tomcat.
   - Access app (e.g., http://localhost:8080).
