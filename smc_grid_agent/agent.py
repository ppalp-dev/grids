"""SMC + Grid Bots agent for Pionex Futures.

Runs an interactive Claude agent that uses the Pionex MCP server tools
(mcp__Pionex__*) to analyze market structure and propose/manage grid bots.

The agent NEVER places real orders without explicit user confirmation in the
conversation — that rule lives in system_prompt.md and is enforced by the
model's instructions, not by this script.
"""
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")


def build_options() -> ClaudeAgentOptions:
    system_prompt = (BASE_DIR / "system_prompt.md").read_text(encoding="utf-8")

    mcp_command = os.environ.get("PIONEX_MCP_COMMAND")
    mcp_args = os.environ.get("PIONEX_MCP_ARGS", "")
    if not mcp_command:
        print(
            "ERROR: define PIONEX_MCP_COMMAND (y opcionalmente PIONEX_MCP_ARGS) "
            "en tu archivo .env para poder lanzar el MCP server de Pionex.",
            file=sys.stderr,
        )
        sys.exit(1)

    mcp_servers = {
        "Pionex": {
            "command": mcp_command,
            "args": [a for a in mcp_args.split(",") if a],
            "env": {
                "PIONEX_API_KEY": os.environ.get("PIONEX_API_KEY", ""),
                "PIONEX_API_SECRET": os.environ.get("PIONEX_API_SECRET", ""),
            },
        }
    }

    return ClaudeAgentOptions(
        system_prompt=system_prompt,
        mcp_servers=mcp_servers,
        allowed_tools=["mcp__Pionex__*"],
        permission_mode="default",
    )


async def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: define ANTHROPIC_API_KEY en tu archivo .env", file=sys.stderr)
        sys.exit(1)

    options = build_options()

    print("Agente SMC + Grid Bots (Pionex Futures) — escribe 'salir' para terminar.\n")

    async with ClaudeSDKClient(options=options) as client:
        while True:
            try:
                user_input = input("Tu: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if user_input.lower() in {"salir", "exit", "quit"}:
                break
            if not user_input:
                continue

            await client.query(user_input)
            async for message in client.receive_response():
                text = getattr(message, "text", None)
                if text:
                    print(f"\nAgente: {text}\n")


if __name__ == "__main__":
    asyncio.run(main())
