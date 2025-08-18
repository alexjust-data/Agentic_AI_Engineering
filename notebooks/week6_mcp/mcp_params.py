# run_trader.py
# Ejecuta un Trader Agent con un Researcher como herramienta, conectando TODOS los MCP servers
# y añadiendo timeouts para evitar cuelgues (WouldBlock/CancelledError).

import os
import asyncio
from typing import List, Optional, Iterable, Set

# === Dependencias del framework de agentes (las que ya usas) ===
from agents import Agent  # tu clase Agent
from agents.run import Runner, RunConfig  # tu Runner y configuración
from agents.trace import trace  # el decorador/ctx para tracing

# === Importa tus parámetros y tools ya definidos ===
# Debes tener estos en mcp_params.py (ajusta los nombres si difieren)
from mcp_params import (
    trader_mcp_servers,          # List[YourMCPServer]
    researcher_mcp_servers,      # List[YourMCPServer]
    fetch_tool,                  # Tool para Fetch (si no lo tienes, crea uno sencillo)
    brave_tool,                  # Tool para Brave (si no lo tienes, crea uno sencillo)
    trader_instructions,         # str instrucciones del trader
    research_instructions,       # str instrucciones del researcher
)

# ---- Opcional: si ya tienes una función que construye el researcher tool, impórtala ----
try:
    from mcp_params import get_researcher_tool  # async def get_researcher_tool(...)
except ImportError:
    get_researcher_tool = None


# =========================
# Utilidades
# =========================
def _uniq(seq: Iterable) -> List:
    """Devuelve una lista sin duplicados preservando orden."""
    seen: Set[int] = set()
    out = []
    for x in seq:
        if id(x) in seen:
            continue
        seen.add(id(x))
        out.append(x)
    return out


async def connect_all_servers(servers: List) -> None:
    """Conecta todos los MCP servers necesarios antes de correr el agente."""
    # Evita duplicados si hay referencias a los mismos objetos en varias listas.
    for s in _uniq(servers):
        await s.connect()
    # Comprobación de sanidad
    for s in _uniq(servers):
        if getattr(s, "session", None) is None:
            raise RuntimeError(f"MCP server no conectado: {s}")


async def build_researcher_as_tool(
    mcp_servers: List,
    instructions: str,
    fetch_tool_obj,
    brave_tool_obj,
    model: str = "gpt-4o-mini",
    tool_name: str = "researcher_assist",
    max_turns: int = 5,
):
    """Crea un agente Researcher y lo expone como herramienta con límites.
       Si ya tienes get_researcher_tool(...), úsalo mejor.
    """
    researcher = Agent(
        name="researcher",
        instructions=instructions,
        tools=[fetch_tool_obj, brave_tool_obj],
        mcp_servers=mcp_servers,
        model=model,
    )
    return researcher.as_tool(tool_name=tool_name, max_turns=max_turns)


def build_trader_agent(
    agent_name: str,
    instructions: str,
    researcher_tool_obj,
    mcp_servers: List,
    model: str = "gpt-4o-mini",
    allowed_tools: Optional[Iterable[str]] = None,
) -> Agent:
    """Construye el trader. Puedes restringir herramientas con un allowlist “blanda” (por prompt)."""
    if allowed_tools:
        instructions = (
            instructions
            + "\n\nUsa solo estas herramientas: "
            + ", ".join(sorted(set(allowed_tools)))
        )

    trader = Agent(
        name=agent_name,
        instructions=instructions,
        tools=[researcher_tool_obj],
        mcp_servers=mcp_servers,
        model=model,
    )
    return trader


# =========================
# Ejecución principal
# =========================
async def run_once(
    agent_name: str,
    prompt: str,
    max_turns: int = 20,
    tool_timeout_seconds: int = 30,
    request_timeout_seconds: int = 60,
) -> str:
    """Conecta servers, construye researcher y trader, y ejecuta con timeouts."""
    # 1) Conecta TODOS los servers que se van a usar (trader + researcher)
    await connect_all_servers(trader_mcp_servers + researcher_mcp_servers)

    # 2) Crea el researcher como herramienta (con límite de turnos)
    if get_researcher_tool is not None:
        researcher_tool = await get_researcher_tool(researcher_mcp_servers)
    else:
        researcher_tool = await build_researcher_as_tool(
            mcp_servers=researcher_mcp_servers,
            instructions=research_instructions,
            fetch_tool_obj=fetch_tool,
            brave_tool_obj=brave_tool,
            model="gpt-4o-mini",
            tool_name="researcher_assist",
            max_turns=5,
        )

    # 3) Construye el trader (opcional: allowlist para evitar que elija tools problemáticas)
    allowed_tools = {"push", "get_snapshot_ticker", "accounts.read", "accounts.write", "fetch", "brave.search"}
    trader = build_trader_agent(
        agent_name=agent_name,
        instructions=trader_instructions,
        researcher_tool_obj=researcher_tool,
        mcp_servers=trader_mcp_servers,
        model="gpt-4o-mini",
        allowed_tools=allowed_tools,
    )

    # 4) Ejecutar con timeouts (evita cuelgues si una tool no responde)
    run_cfg = RunConfig(
        tool_timeout_seconds=tool_timeout_seconds,
        request_timeout_seconds=request_timeout_seconds,
    )

    with trace(agent_name):
        # Si tu versión no permite run_config, descomenta el wait_for de abajo
        result = await Runner.run(trader, prompt, max_turns=max_turns, run_config=run_cfg)

        # Alternativa fuerte por si tu Runner no soporta run_config:
        # result = await asyncio.wait_for(
        #     Runner.run(trader, prompt, max_turns=max_turns),
        #     timeout=90
        # )

    # El objeto result suele tener .final_output; si no, adapta aquí.
    return getattr(result, "final_output", str(result))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run Trader Agent once.")
    parser.add_argument("--agent-name", default="Trader-1", help="Nombre del agente trader.")
    parser.add_argument("--prompt", default="Analyse today and propose one synthetic trade.", help="Prompt inicial.")
    parser.add_argument("--max-turns", type=int, default=20)
    parser.add_argument("--tool-timeout", type=int, default=30)
    parser.add_argument("--request-timeout", type=int, default=60)
    args = parser.parse_args()

    # Ejecuta el loop
    output = asyncio.run(
        run_once(
            agent_name=args.agent_name,
            prompt=args.prompt,
            max_turns=args.max_turns,
            tool_timeout_seconds=args.tool_timeout,
            request_timeout_seconds=args.request_timeout,
        )
    )
    print("\n=== FINAL OUTPUT ===\n")
    print(output)


if __name__ == "__main__":
    main()




