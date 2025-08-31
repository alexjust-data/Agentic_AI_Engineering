from traders import Trader
from typing import List
import asyncio
from tracers import LogTracer
from agents import add_trace_processor
from market import is_market_open
from dotenv import load_dotenv
import os

load_dotenv(override=True)

RUN_EVERY_N_MINUTES = int(os.getenv("RUN_EVERY_N_MINUTES", "60"))
RUN_EVEN_WHEN_MARKET_IS_CLOSED = (
    os.getenv("RUN_EVEN_WHEN_MARKET_IS_CLOSED", "false").strip().lower() == "true"
)
USE_MANY_MODELS = os.getenv("USE_MANY_MODELS", "true").strip().lower() == "true"

names = ["Warren", "George", "Ray", "Cathie"]
lastnames = ["Patience", "Bold", "Systematic", "Crypto"]

# ---------- OpenAI-only model map ----------
# Pick any OpenAI models you have access to.
OPENAI_MODEL_MAP = {
    "Warren": "gpt-4o-mini",   # value / patient
    "George": "gpt-4o",        # a bit bolder
    "Ray":    "gpt-4.1-mini",  # systematic / fast
    "Cathie": "gpt-4o-mini",   # innovation / quick
}

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

if USE_MANY_MODELS:
    model_names = [OPENAI_MODEL_MAP[n] for n in names]
    short_model_names = model_names
else:
    model_names = [DEFAULT_OPENAI_MODEL] * len(names)
    short_model_names = [DEFAULT_OPENAI_MODEL] * len(names)
# -------------------------------------------


def create_traders() -> List[Trader]:
    traders = []
    for name, lastname, model_name in zip(names, lastnames, model_names):
        traders.append(Trader(name, lastname, model_name))
    return traders


async def run_every_n_minutes():
    add_trace_processor(LogTracer())
    traders = create_traders()

    # Toggle here if you want to try concurrent later
    SEQUENTIAL_TRADERS = True

    while True:
        if RUN_EVEN_WHEN_MARKET_IS_CLOSED or is_market_open():
            if SEQUENTIAL_TRADERS:
                for t in traders:
                    await t.run()
            else:
                await asyncio.gather(*[t.run() for t in traders])
        else:
            print("Market is closed, skipping run")
        await asyncio.sleep(RUN_EVERY_N_MINUTES * 60)



if __name__ == "__main__":
    print(f"Starting scheduler to run every {RUN_EVERY_N_MINUTES} minutes")
    asyncio.run(run_every_n_minutes())
