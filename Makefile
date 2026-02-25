.PHONY: docs-site docs-site-build docs-site-preview docs-site-clean

RENDERER_DIR := tools/ansible-doc-renderer
SITE_DIR     := docs/_site
COLLECTION   := cisco.meraki_rm

# Build the renderer package (only if sources changed)
$(RENDERER_DIR)/out/cli.js: $(RENDERER_DIR)/src/*.ts $(RENDERER_DIR)/package.json
	cd $(RENDERER_DIR) && npm run build

# Generate the documentation site
docs-site: $(RENDERER_DIR)/out/cli.js
	@echo "==> Extracting plugin documentation..."
	ansible-doc --metadata-dump -t module --no-fail-on-errors $(COLLECTION) > /tmp/meraki-docs.json
	@echo "==> Rendering site..."
	node $(RENDERER_DIR)/out/cli.js \
		--input /tmp/meraki-docs.json \
		--output $(SITE_DIR) \
		--title "Cisco Meraki RM Collection" \
		--description "Ansible resource module collection for managing Cisco Meraki Dashboard infrastructure" \
		--version "$$(grep '^version:' galaxy.yml | awk '{print $$2}')"
	@echo "==> Site ready at $(SITE_DIR)/index.html"

# Preview the site with Python's built-in HTTP server
docs-site-preview: docs-site
	@echo "==> Serving at http://localhost:8000"
	cd $(SITE_DIR) && python3 -m http.server 8000

docs-site-build:
	cd $(RENDERER_DIR) && npm install && npm run build

docs-site-clean:
	rm -rf $(SITE_DIR)
	cd $(RENDERER_DIR) && npm run clean
