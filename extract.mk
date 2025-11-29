.PHONY: extract-tar
extract-tar:
	@echo "Extracting tar file..."
	@python3 -c "import tarfile; t = tarfile.open('agentqms-export.tar.gz', 'r:gz'); print(f'Extracting {len(t.getnames())} files...'); t.extractall('.'); print('Done')"
	@echo "Creating backup branch..."
	@git branch backup-before-refactor-merge-$$(date +%Y%m%d-%H%M%S) || true
	@echo "Creating refactor/main branch..."
	@git checkout -b refactor/main 2>/dev/null || git checkout refactor/main
	@echo "Staging changes..."
	@git add -A
	@echo "Committing..."
	@git commit -m "Extract integration test updates from agentqms-export.tar.gz" || echo "No changes to commit"
