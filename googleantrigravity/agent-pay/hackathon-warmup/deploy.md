# Deployment Instructions

1. **Generate the Web Page**:
   Run the pipeline to create your `index.html`.
   ```bash
   python process_pdf.py your_document.pdf
   python generate_web.py your_document.pdf.md
   ```

2. **Prepare for GitHub Pages**:
   - Rename the generated HTML file to `index.html` if it isn't already.
   - Create a new folder (e.g., `docs/`) or push to a `gh-pages` branch.

3. **Push to GitHub**:
   ```bash
   git add index.html
   git commit -m "Add generated web page"
   git push origin main
   ```

4. **Enable GitHub Pages**:
   - Go to your repository Settings -> Pages.
   - Select the source (e.g., `main` branch, `/` root or `/docs` folder).
   - Save.

5. **Verify**:
   - Visit the provided URL (usually `https://<username>.github.io/<repo-name>/`).
