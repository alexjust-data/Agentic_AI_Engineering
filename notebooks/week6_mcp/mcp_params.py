# mcp_params.py
import os
import sys
from dotenv import load_dotenv
from market import is_paid_polygon, is_realtime_polygon

# Cargar .env
load_dotenv(override=True)

# === Paths absolutos (evitan "file not found") ===
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_SERVER = os.path.join(THIS_DIR, "accounts_server.py")
PUSH_SERVER     = os.path.join(THIS_DIR, "push_server.py")
MARKET_SERVER   = os.path.join(THIS_DIR, "market_server.py")  # wrapper free
MEMORY_DIR      = os.path.join(THIS_DIR, "memory")

# Asegurar carpeta memory existe
os.makedirs(MEMORY_DIR, exist_ok=True)

# Usa el MISMO Python que está ejecutando el notebook / script
PY = os.environ.get("PYTHON", sys.executable)

# === API KEYS ===
BRAVE_API_KEY   = os.getenv("BRAVE_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
brave_env = {"BRAVE_API_KEY": BRAVE_API_KEY} if BRAVE_API_KEY else None

# --- MARKET MCP ---
if (is_paid_polygon or is_realtime_polygon) and POLYGON_API_KEY:
    market_mcp = {
        "command": "uvx",
        "args": [
            "--from",
            "git+https://github.com/polygon-io/mcp_polygon@v0.1.0",
            "mcp_polygon",
        ],
        "env": {"POLYGON_API_KEY": POLYGON_API_KEY},
    }
else:
    # Ejecuta tu wrapper local con el MISMO intérprete
    market_mcp = {"command": PY, "args": [MARKET_SERVER]}

# --- TRADER SERVERS ---
trader_mcp_server_params = [
    {"command": PY, "args": [ACCOUNTS_SERVER]},
    {"command": PY, "args": [PUSH_SERVER]},
    market_mcp,
]

# --- RESEARCHER SERVERS (con memory robusto) ---
def researcher_mcp_server_params(name: str):
    db_path = os.path.join(MEMORY_DIR, f"{name.lower()}.db")

    params = [
        {
            "command": "npx",
            "args": ["-y", "mcp-memory-libsql"],
            "env": {
                "LIBSQL_URL": f"file:{db_path}",
                "MEMORY_VECTOR_SIZE": "4",        # fuerza dimensión 4
                "SQLITE_BUSY_TIMEOUT_MS": "5000", # evita locks cortos
                "SQLITE_JOURNAL_MODE": "WAL",     # concurrencia mejorada
            },
        },
    ]

    # BRAVE (Node) — sólo si hay API key
    if BRAVE_API_KEY:
        params.insert(
            0,
            {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                "env": brave_env,
            },
        )
    return params

# --- Avisos útiles ---
def warn_if_missing_keys():
    if (is_paid_polygon or is_realtime_polygon) and not POLYGON_API_KEY:
        print("⚠️  Falta POLYGON_API_KEY pero has activado paid/realtime; usaré el wrapper local (market_server.py).")
    if not BRAVE_API_KEY:
        print("ℹ️  BRAVE_API_KEY no encontrada: el servidor Brave NO se incluirá en researcher.")

