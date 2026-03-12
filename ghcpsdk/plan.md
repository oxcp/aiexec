## Objective
Create a GitHub Copilot SDK sample (`analyze_prs.py`) to analyze and summarize PRs in the repository `kylercai/javademo`.

## Steps
1. Create `analyze_prs.py` which uses the `copilot` Python SDK.
2. The script will:
   - Initialize `CopilotClient`.
   - Start a session.
   - Send a prompt to summarize PRs in `kylercai/javademo`.
   - Print the response.
3. Run the script to verify functionality (if authentication allows).
4. If successful, the script serves as the requested sample.

## Status
- [x] Create `analyze_prs.py` which uses the `copilot` Python SDK.
- [x] Run the script to verify functionality (if authentication allows).

## Notes
- Script `analyze_prs.py` created and verified.
- Uses `gh` CLI for fetching data (RAG pattern) to overcome network permissions in the agent environment.
- Successfully summarized 5 PRs.