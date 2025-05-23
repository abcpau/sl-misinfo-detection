# token1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQ1ZDdhZjIxLWFmZDEtNGI4Yy1hNzJhLWQ0YzhjMmY1YzhmZSJ9.Er6kRKACaa1gz7wbLxhVcDhtNKpCuQQkUOgR2yHx7p8" #openwebui laptop
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImZkY2FjYjUxLTdjMGYtNDE0Ni05NjZmLWI1NzAwNWI3ZTkyYSJ9.mLsgUx9N2pqmJxcNPTiUxLBq-2-F4GAF8SYroQX6QtQ" #openwebui pc

IP_ADDRESS = 'localhost'
PORT = 8080                                     # 11434       for ollama
ENDPOINT = '/api/chat/completions'              # '/api/chat' for ollama
URL = f"http://{IP_ADDRESS}:{PORT}{ENDPOINT}"
HEADERS = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}  # {"Content-Type": "application/json"} for ollama


OPEN_WEBUI_MODEL = "llama3x-nli"
OLLAMA_MODEL = "llama3.3:70b"