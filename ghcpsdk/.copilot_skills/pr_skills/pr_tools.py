from copilot import define_tool
import subprocess
import json

print("Importing pr_tools module...")

@define_tool(
    name="get_pr_details",
    description="Fetch details of a pull request from a GitHub repository using 'gh' CLI."
)
def get_pr_details(args, context) -> str:
    """
    Fetch details of a pull request.

    Args:
        args: Dictionary containing 'repo' and 'pr_number'.
        context: Tool execution context.

    Returns:
        JSON string with PR details.
    """
    print(f"Executing tool: get_pr_details(args={args})")
    
    # Extract arguments
    repo = args.get("repo")
    pr_number = args.get("pr_number")

    if not repo or not pr_number:
        return json.dumps({"error": "Missing repo or pr_number argument"})

    try:
        cmd = [
            "gh", "pr", "view",
            str(pr_number),
            "--repo", repo,
            "--json", "number,title,body,author,url,state,createdAt"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return json.dumps({"error": f"Failed to fetch PR details: {e.stderr}"})
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"})

@define_tool(
    name="list_prs",
    description="List pull requests in a GitHub repository."
)
def list_prs(args, context) -> str:
    """
    List pull requests in a repository.

    Args:
        args: Dictionary containing 'repo' and optional 'state' (open/closed/merged/all, default: all) and 'limit' (default: 10).
        context: Tool execution context.

    Returns:
        JSON string with list of PRs (number, title, author, state).
    """
    print(f"Executing tool: list_prs(args={args})")
    
    repo = args.get("repo")
    state = args.get("state", "all")
    limit = args.get("limit", 10)

    if not repo:
        return json.dumps({"error": "Missing repo argument"})

    try:
        cmd = [
            "gh", "pr", "list",
            "--repo", repo,
            "--state", state,
            "--limit", str(limit),
            "--json", "number,title,author,state,url"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return json.dumps({"error": f"Failed to list PRs: {e.stderr}"})
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"})
