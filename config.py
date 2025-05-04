token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQ1ZDdhZjIxLWFmZDEtNGI4Yy1hNzJhLWQ0YzhjMmY1YzhmZSJ9.Er6kRKACaa1gz7wbLxhVcDhtNKpCuQQkUOgR2yHx7p8" #openwebui laptop

IP_ADDRESS = '192.168.50.32'
PORT = 8080                                     # 11434       for ollama
ENDPOINT = '/api/chat/completions'              # '/api/chat' for ollama
URL = f"http://{IP_ADDRESS}:{PORT}{ENDPOINT}"
HEADERS = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}  # {"Content-Type": "application/json"} for ollama


MODEL = "llama31-8b-test"