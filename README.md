# SDG-SOAS — Online CLO-to-SDG Concept Mapper

Free Streamlit interface for the existing v0.6 rule engine. **Experimental; human review required.**

## Deploy without Terminal
1. On your public GitHub `SDG-SOAS` repository, click **Add file → Upload files**.
2. Upload `streamlit_app.py`, `engine.py`, `concept_rules.json`, `requirements.txt`, and optionally `README.md` and `.gitignore` (GitHub browser may hide dotfiles).
3. Click **Commit changes**.
4. Visit https://share.streamlit.io/ and sign in with GitHub.
5. Create an app using repository `LeilaIssa2023/SDG-SOAS`, branch `main`, entrypoint `streamlit_app.py`. If the account spelling differs, select your repository from the menu.
6. Deploy. Streamlit will install the single dependency automatically. Share the generated Streamlit URL after checking it.

No compilation, shell, or local server is needed. **GitHub Pages alone will not run this Python application.**

## Security and limitations
- This application is hosted by Streamlit, not on your Mac; it has no connection to your Mac files.
- It is public unless you separately configure access restrictions. Do not upload private SoAS workbooks, student data, secrets, or passwords.
- Uploaded CSVs are handled in application memory and not intentionally written to disk by this code. The hosting provider processes submitted data; do not send confidential CLOs or personal information without institutional approval.
- The engine does not independently validate SDG targets or guarantee accuracy.
- Free hosting may sleep or impose usage limits.

## Files
- `streamlit_app.py`: hosted user interface
- `engine.py`: same v0.6 classification logic
- `concept_rules.json`: same v0.6 concept dictionary
- `requirements.txt`: Streamlit dependency
