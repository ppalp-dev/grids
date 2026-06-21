# SMC Grid Agent (Pionex Futures)

Agente conversacional construido con el [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk) que
combina analisis Smart Money Concepts (SMC) con los bots de grid de futuros de Pionex.

El agente **propone** rangos y parametros de grid; nunca crea, modifica ni cierra
un bot con dinero real sin tu confirmacion explicita en la conversacion (ver
`system_prompt.md`, seccion "FLUJO DE TRABAJO", paso 6).

## Requisitos

- Python 3.10+
- Una API key de Anthropic (`ANTHROPIC_API_KEY`)
- Credenciales de Pionex (solo lectura + trading de bots/futuros, **sin retiros**)
- Un servidor MCP de Pionex que expone las herramientas `mcp__Pionex__*`

## Instalacion

```powershell
cd smc_grid_agent
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edita `.env` con:
- `ANTHROPIC_API_KEY`
- `PIONEX_API_KEY`, `PIONEX_API_SECRET`
- `PIONEX_MCP_COMMAND` / `PIONEX_MCP_ARGS`: el comando para lanzar el MCP server
  de Pionex que ya tienes conectado en este entorno (revisa como lo instalaste/
  configuraste para reproducir el mismo comando aqui).

## Uso

```powershell
python agent.py
```

Conversa con el agente en espanol. Ejemplos:

- "Analiza BTC y dime si hay una buena oportunidad de grid"
- "Monta un grid en ETH neutral con 2x"
- "Cierra el bot X"

## Seguridad

- Nunca compartas tu `PIONEX_API_SECRET`.
- No actives permisos de retiro en la API key de Pionex.
- Revisa siempre el plan que el agente propone (rango, leverage, stop loss)
  antes de confirmar la creacion de un bot.
- Esto es una herramienta de analisis, no asesoramiento financiero.
