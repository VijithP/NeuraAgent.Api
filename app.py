import os
import re
import subprocess
from pathlib import Path

import streamlit as st


AGENT_ROOT = Path(__file__).resolve().parent
RUN_SCRIPT = AGENT_ROOT / "scripts" / "run-agent.ps1"

ISSUE_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9]+-\d+$")


st.set_page_config(
    page_title="Project Management AI Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("Project Management AI Support Agent")

st.write(
    "Enter a Jira issue key. "
    "The agent will read the Jira ticket, read project context "
    "from Confluence, and analyse the local "
    "ProjectManagementServer repository."
)


# --------------------------------------------------
# Environment variable helper
# --------------------------------------------------

def get_env(name: str):
    value = os.getenv(name)

    if value:
        return value

    # Fall back to Windows User environment variables.
    try:
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                (
                    "[Environment]::GetEnvironmentVariable("
                    f"'{name}', 'User'"
                    ")"
                ),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        value = result.stdout.strip()

        if value:
            os.environ[name] = value
            return value

    except Exception:
        pass

    return None


# --------------------------------------------------
# Configuration
# --------------------------------------------------

project_path = get_env("PROJECT_REPO_PATH")
project_context = get_env("PROJECT_CONTEXT_PAGE")

jira_url = get_env("JIRA_BASE_URL")
jira_email = get_env("JIRA_EMAIL")
jira_token = get_env("JIRA_API_TOKEN")


st.subheader("Agent Configuration")

col1, col2, col3 = st.columns(3)


with col1:
    st.write("Repository")

    if project_path:
        st.success(project_path)
    else:
        st.error("PROJECT_REPO_PATH not configured")


with col2:
    st.write("Project Context")

    if project_context:
        st.success(project_context)
    else:
        st.warning("PROJECT_CONTEXT_PAGE not configured")


with col3:
    st.write("Jira")

    if jira_url and jira_email and jira_token:
        st.success("Jira configuration available")
    else:
        st.warning(
            "Jira REST configuration incomplete. "
            "This is OK if Jira is accessed through Atlassian MCP."
        )


# --------------------------------------------------
# Jira issue
# --------------------------------------------------

st.subheader("Process Jira Issue")

issue_key = st.text_input(
    "Jira Issue Key",
    placeholder="TEAM-1",
).strip().upper()


if st.button(
    "Run AI Agent",
    type="primary",
    disabled=not bool(issue_key),
):

    # --------------------------------------------------
    # Validate Jira issue key
    # --------------------------------------------------

    if not ISSUE_PATTERN.fullmatch(issue_key):
        st.error(
            "Invalid Jira issue key. "
            "Example: TEAM-1"
        )
        st.stop()

    # --------------------------------------------------
    # Validate PowerShell script
    # --------------------------------------------------

    if not RUN_SCRIPT.exists():
        st.error(
            f"Agent script not found: {RUN_SCRIPT}"
        )
        st.stop()

    if not project_path:
        st.error(
            "PROJECT_REPO_PATH is not configured."
        )
        st.stop()

    st.info(
        f"Starting agent for {issue_key}..."
    )

    # --------------------------------------------------
    # Build PowerShell command
    # --------------------------------------------------

    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(RUN_SCRIPT),

        # Explicit parameter is better than positional parameter.
        "-IssueKey",
        issue_key,
    ]

    try:

        process = subprocess.Popen(
            command,
            cwd=str(AGENT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        output_box = st.empty()

        output_lines = []

        workspace_trust_error = False
        mcp_permission_error = False

        if process.stdout:

            for line in process.stdout:

                output_lines.append(line)

                output_text = "".join(output_lines)

                output_box.code(
                    output_text,
                    language="text",
                )

                lower_line = line.lower()

                # ------------------------------------------
                # Claude workspace trust detection
                # ------------------------------------------

                if (
                    "workspace has not been trusted"
                    in lower_line
                ):
                    workspace_trust_error = True

                # ------------------------------------------
                # MCP permission detection
                # ------------------------------------------

                if (
                    "permission was denied"
                    in lower_line
                    or
                    "approve access to the atlassian"
                    in lower_line
                ):
                    mcp_permission_error = True

        return_code = process.wait()

        # --------------------------------------------------
        # Show helpful errors
        # --------------------------------------------------

        if workspace_trust_error:

            st.error(
                "Claude Code has not trusted this workspace yet."
            )

            st.code(
                f"""
cd "{AGENT_ROOT}"
claude
""",
                language="powershell",
            )

            st.info(
                "Run the commands above manually once, "
                "accept the Claude workspace trust dialog, "
                "then run /mcp and authenticate Atlassian."
            )

        elif mcp_permission_error:

            st.error(
                "Claude was not allowed to use the Atlassian "
                "MCP tools."
            )

            st.info(
                "Open Claude Code interactively from the agent "
                "folder, run /mcp, and approve/authenticate the "
                "required Jira and Confluence read tools."
            )

        elif return_code == 0:

            st.success(
                f"Agent completed for {issue_key}"
            )

        else:

            st.error(
                f"Agent failed with exit code {return_code}"
            )

    except FileNotFoundError:

        st.error(
            "PowerShell could not be started."
        )

    except Exception as ex:

        st.exception(ex)