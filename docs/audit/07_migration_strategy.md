# Migration Strategy: Scattered to Containerized

**Date**: 2025-11-09  
**Design Scope**: Migration from Current to Containerized Structure  
**Status**: Migration Plan

## Executive Summary

This document provides a step-by-step migration strategy to move from the current scattered framework structure to the containerized `AgentQMS/` structure, with backward compatibility support and automated migration tools.

---

## Migration Overview

### Current Structure (Scattered)
```
project_root/
├── agent/                    # Framework
├── agent_tools/             # Framework
├── quality_management_framework/  # Framework
├── scripts/                 # Mixed
├── artifacts/               # Project
└── docs/                    # Mixed
```

### Target Structure (Containerized)
```
project_root/
├── AgentQMS/                # Framework container
│   ├── agent/
│   ├── agent_tools/
│   ├── conventions/         # Renamed from quality_management_framework
│   ├── agent_scripts/       # Renamed from scripts
│   └── config/
├── artifacts/               # Project (unchanged)
└── docs/                    # Project (unchanged)
```

---

## Migration Phases

### Phase 1: Preparation (Pre-Migration)

**Goal**: Prepare for migration without breaking existing functionality

**Steps**:

1. **Backup Current Structure**
   ```bash
   # Create backup
   tar -czf framework_backup_$(date +%Y%m%d).tar.gz \
       agent/ agent_tools/ quality_management_framework/ scripts/
   ```

2. **Audit Current Structure**
   ```bash
   # Identify all framework files
   python scripts/audit_framework_files.py --list-all
   ```

3. **Check for Customizations**
   ```bash
   # Find project-specific modifications
   python scripts/check_customizations.py
   ```

4. **Update Framework Version**
   - Ensure framework is up-to-date
   - Check for breaking changes

**Deliverables**:
- ✅ Backup created
- ✅ Framework files identified
- ✅ Customizations documented
- ✅ Framework version verified

---

### Phase 2: Dual Support Implementation

**Goal**: Support both old and new structures simultaneously

**Implementation**:
```python
# AgentQMS/agent_tools/utils/paths.py

def detect_structure() -> str:
    """Detect current project structure."""
    project_root = get_project_root()
    
    # Check for new structure
    if (project_root / "AgentQMS").exists():
        return "containerized"
    
    # Check for old structure
    if (project_root / "agent_tools").exists():
        return "scattered"
    
    return "unknown"

def get_framework_root() -> Path:
    """Get framework root (supports both structures)."""
    structure = detect_structure()
    project_root = _find_project_root()
    
    if structure == "containerized":
        return project_root / "AgentQMS"
    elif structure == "scattered":
        # Return project root (framework is scattered)
        return project_root
    else:
        raise RuntimeError("Unknown project structure")

def get_agent_tools_dir() -> Path:
    """Get agent_tools directory (supports both structures)."""
    structure = detect_structure()
    project_root = _find_project_root()
    
    if structure == "containerized":
        return project_root / "AgentQMS" / "agent_tools"
    elif structure == "scattered":
        return project_root / "agent_tools"
    else:
        raise RuntimeError("Unknown project structure")
```

**Benefits**:
- Framework works in both structures
- Gradual migration possible
- No breaking changes

---

### Phase 3: Automated Migration Tool

**Goal**: Provide automated tool to migrate structure

**Implementation**:
```python
# AgentQMS/agent_scripts/migrate_structure.py

#!/usr/bin/env python3
"""
Migrate framework from scattered to containerized structure.

Usage:
    python migrate_structure.py --dry-run    # Preview changes
    python migrate_structure.py              # Perform migration
    python migrate_structure.py --rollback   # Rollback migration
"""

import argparse
import shutil
from pathlib import Path
from typing import List, Tuple

class StructureMigrator:
    """Migrate framework structure."""
    
    def __init__(self, project_root: Path, dry_run: bool = False):
        self.project_root = project_root
        self.dry_run = dry_run
        self.migration_log: List[Tuple[str, Path, Path]] = []
    
    def migrate(self) -> bool:
        """Perform migration."""
        print("🔄 Starting framework structure migration...")
        
        # 1. Validate current structure
        if not self._validate_current_structure():
            print("❌ Current structure validation failed")
            return False
        
        # 2. Create AgentQMS container
        container = self.project_root / "AgentQMS"
        if not self.dry_run:
            container.mkdir(exist_ok=True)
        print(f"✅ Created container: {container}")
        
        # 3. Move framework directories
        moves = [
            ("agent", "agent"),
            ("agent_tools", "agent_tools"),
            ("quality_management_framework", "conventions"),
            ("scripts", "agent_scripts"),
        ]
        
        for old_name, new_name in moves:
            old_path = self.project_root / old_name
            new_path = container / new_name
            
            if old_path.exists():
                if not self.dry_run:
                    shutil.move(str(old_path), str(new_path))
                self.migration_log.append(("move", old_path, new_path))
                print(f"✅ Moved {old_name}/ → AgentQMS/{new_name}/")
            else:
                print(f"⚠️  {old_name}/ not found, skipping")
        
        # 4. Create config directory
        config_dir = container / "config"
        if not self.dry_run:
            config_dir.mkdir(exist_ok=True)
        print(f"✅ Created config directory: {config_dir}")
        
        # 5. Create .agentqms metadata
        metadata_dir = self.project_root / ".agentqms"
        if not self.dry_run:
            metadata_dir.mkdir(exist_ok=True)
            (metadata_dir / "version").write_text("0.1.0")
            (metadata_dir / "migrated").write_text(str(Path.cwd()))
        print(f"✅ Created metadata: {metadata_dir}")
        
        # 6. Update path references (if needed)
        self._update_path_references()
        
        # 7. Validate new structure
        if not self._validate_new_structure():
            print("❌ New structure validation failed")
            if not self.dry_run:
                self.rollback()
            return False
        
        print("✅ Migration completed successfully!")
        return True
    
    def _validate_current_structure(self) -> bool:
        """Validate that current structure can be migrated."""
        required_dirs = ["agent_tools"]  # At minimum
        
        for dir_name in required_dirs:
            if not (self.project_root / dir_name).exists():
                print(f"❌ Required directory not found: {dir_name}/")
                return False
        
        return True
    
    def _validate_new_structure(self) -> bool:
        """Validate new containerized structure."""
        container = self.project_root / "AgentQMS"
        
        if not container.exists():
            return False
        
        required_dirs = ["agent_tools"]
        for dir_name in required_dirs:
            if not (container / dir_name).exists():
                return False
        
        return True
    
    def _update_path_references(self):
        """Update path references in code and config."""
        # This would update hardcoded paths in:
        # - Makefile
        # - Config files
        # - Documentation
        # Implementation depends on specific references
        pass
    
    def rollback(self):
        """Rollback migration."""
        print("🔄 Rolling back migration...")
        
        container = self.project_root / "AgentQMS"
        
        # Reverse moves
        for action, old_path, new_path in reversed(self.migration_log):
            if action == "move" and new_path.exists():
                shutil.move(str(new_path), str(old_path))
                print(f"✅ Restored {old_path.name}/")
        
        # Remove container if empty
        if container.exists() and not any(container.iterdir()):
            container.rmdir()
            print(f"✅ Removed empty container: {container}")
        
        # Remove metadata
        metadata_dir = self.project_root / ".agentqms"
        if metadata_dir.exists():
            shutil.rmtree(metadata_dir)
            print(f"✅ Removed metadata: {metadata_dir}")
        
        print("✅ Rollback completed")

def main():
    parser = argparse.ArgumentParser(description="Migrate framework structure")
    parser.add_argument("--dry-run", action="store_true",
                       help="Preview changes without applying")
    parser.add_argument("--rollback", action="store_true",
                       help="Rollback previous migration")
    parser.add_argument("--project-root", type=Path,
                       help="Project root directory (default: current)")
    
    args = parser.parse_args()
    
    project_root = args.project_root or Path.cwd()
    migrator = StructureMigrator(project_root, dry_run=args.dry_run)
    
    if args.rollback:
        migrator.rollback()
    else:
        success = migrator.migrate()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

---

### Phase 4: Manual Migration Steps

**Goal**: Step-by-step manual migration guide

**Steps**:

1. **Create Container Directory**
   ```bash
   mkdir AgentQMS
   ```

2. **Move Framework Directories**
   ```bash
   mv agent AgentQMS/
   mv agent_tools AgentQMS/
   mv quality_management_framework AgentQMS/conventions
   mv scripts AgentQMS/agent_scripts
   ```

3. **Create Config Directory**
   ```bash
   mkdir -p AgentQMS/config
   ```

4. **Create Metadata Directory**
   ```bash
   mkdir -p .agentqms
   echo "0.1.0" > .agentqms/version
   ```

5. **Update Path References**
   ```bash
   # Update Makefile paths
   sed -i 's|../scripts/agent_tools|../AgentQMS/agent_tools|g' AgentQMS/agent/Makefile
   
   # Update Python imports (if needed)
   # Update documentation references
   ```

6. **Validate Migration**
   ```bash
   python AgentQMS/agent_tools/compliance/validate_boundaries.py
   ```

7. **Test Framework**
   ```bash
   cd AgentQMS/agent
   make discover
   make validate
   ```

---

### Phase 5: Cleanup (Post-Migration)

**Goal**: Remove old structure and update references

**Steps**:

1. **Verify Migration Success**
   ```bash
   # Test all framework functionality
   python AgentQMS/agent_tools/core/discover.py
   python AgentQMS/agent_tools/compliance/validate_artifacts.py --all
   ```

2. **Update Documentation**
   - Update README with new structure
   - Update path references in docs
   - Update examples

3. **Update CI/CD**
   - Update GitHub Actions paths
   - Update deployment scripts

4. **Remove Old Structure** (if automated migration)
   ```bash
   # Old directories should already be moved
   # Verify they're gone
   ls -la agent_tools/  # Should not exist
   ```

5. **Update Git Ignore**
   ```bash
   # Add to .gitignore if needed
   echo ".agentqms/" >> .gitignore  # Optional
   ```

---

## Migration Checklist

### Pre-Migration
- [ ] Backup current structure
- [ ] Audit framework files
- [ ] Document customizations
- [ ] Update framework to latest version
- [ ] Test current functionality

### Migration
- [ ] Run migration tool (or manual steps)
- [ ] Verify directory moves
- [ ] Update path references
- [ ] Create metadata directory
- [ ] Validate new structure

### Post-Migration
- [ ] Test all framework functionality
- [ ] Update documentation
- [ ] Update CI/CD scripts
- [ ] Remove old structure (if automated)
- [ ] Update .gitignore

### Validation
- [ ] Boundary validation passes
- [ ] All tools work
- [ ] Artifact creation works
- [ ] Documentation generation works
- [ ] CI/CD passes

---

## Rollback Strategy

### Automatic Rollback

If migration fails, the tool can automatically rollback:

```bash
python migrate_structure.py --rollback
```

### Manual Rollback

1. **Restore from Backup**
   ```bash
   tar -xzf framework_backup_YYYYMMDD.tar.gz
   ```

2. **Remove New Structure**
   ```bash
   rm -rf AgentQMS/
   rm -rf .agentqms/
   ```

3. **Verify Restoration**
   ```bash
   # Test framework functionality
   cd agent
   make discover
   ```

---

## Migration Scenarios

### Scenario 1: Clean Migration (No Customizations)

**Steps**:
1. Run automated migration tool
2. Verify functionality
3. Done

**Time**: ~5 minutes

---

### Scenario 2: Customized Framework

**Steps**:
1. Document customizations
2. Run migration tool
3. Reapply customizations in new structure
4. Verify functionality

**Time**: ~30 minutes

---

### Scenario 3: Mixed Structure (Partial Migration)

**Steps**:
1. Use dual support mode
2. Gradually migrate components
3. Test after each component
4. Complete migration when ready

**Time**: ~1-2 hours

---

## Common Issues & Solutions

### Issue 1: Path References Not Updated

**Symptom**: Tools fail with "file not found" errors

**Solution**:
```bash
# Update Makefile
sed -i 's|../scripts/agent_tools|../AgentQMS/agent_tools|g' AgentQMS/agent/Makefile

# Update Python imports
find AgentQMS/ -name "*.py" -exec sed -i 's|scripts.agent_tools|AgentQMS.agent_tools|g' {} \;
```

---

### Issue 2: Old Structure Still Exists

**Symptom**: Both old and new structures present

**Solution**:
```bash
# Verify migration completed
python AgentQMS/agent_tools/compliance/validate_boundaries.py

# If old structure is orphaned, remove it
rm -rf agent_tools/ quality_management_framework/
```

---

### Issue 3: Git History Lost

**Symptom**: Git doesn't track moved files

**Solution**:
```bash
# Use git mv to preserve history
git mv agent AgentQMS/agent
git mv agent_tools AgentQMS/agent_tools
# etc.
```

---

## Migration Timeline

### Recommended Timeline

- **Week 1**: Preparation and dual support implementation
- **Week 2**: Automated migration tool development
- **Week 3**: Testing and refinement
- **Week 4**: Production migration

### Phased Rollout

1. **Pilot Projects**: Migrate 1-2 projects first
2. **Fix Issues**: Address any problems found
3. **Documentation**: Update docs based on learnings
4. **Full Rollout**: Migrate remaining projects

---

## Success Criteria

### Migration Success

- ✅ All framework directories in `AgentQMS/`
- ✅ No old structure directories remaining
- ✅ All tools function correctly
- ✅ Boundary validation passes
- ✅ Documentation updated
- ✅ CI/CD updated and passing

### Validation Commands

```bash
# Verify structure
ls -la AgentQMS/

# Test functionality
cd AgentQMS/agent && make discover

# Validate boundaries
python AgentQMS/agent_tools/compliance/validate_boundaries.py

# Full validation
python AgentQMS/agent_tools/compliance/validate_artifacts.py --all
```

---

## Next Steps

1. **Review migration strategy** with stakeholders
2. **Implement dual support** in path resolution
3. **Develop migration tool** with dry-run support
4. **Test on pilot project**
5. **Refine based on results**
6. **Document lessons learned**
7. **Roll out to all projects**

---

**See Also**:
- `06_containerization_design.md` - Target structure
- `08_configuration_schema.md` - Configuration system
- `09_boundary_enforcement.md` - Boundary validation

