import yaml

WATTPILOT_API_FILE = "src/wattpilot/ressources/wattpilot.yaml"

def pc(prop,key,alt=''):
    return f"`{prop[key]}`" if key in prop and prop[key] != "" else alt

def pv(prop,key,alt=''):
    return prop[key] if key in prop else alt

def ha(prop):
    return ':heavy_check_mark:' if 'homeAssistant' in prop else ':white_large_square:'

with open(WATTPILOT_API_FILE, 'r') as stream:
    wpapidef = yaml.safe_load(stream)

s = "# Wattpilot API Description\n\n"

s += "## WebSocket Message Types\n\n"
s += "| Key | Title | Description | Example |\n"
s += "|-----|-------|-------------|---------|\n"
for msg in wpapidef["messages"]:
    s += f"| `{msg['key']}` | {msg['title']} | {msg['description']} |  |\n"
s += "\n"

s += "## Wattpilot Properties\n\n"
s += "| Key | Alias | Title | R/W | JSON Type | API Type | Category | HA Enabled | Description | Example |\n"
s += "|-----|-------|-------|-----|-----------|----------|----------|------------|-------------|---------|\n"
for p in wpapidef["properties"]:
    s += f"| {pc(p,'key')} | {pc(p,'alias')} | {pv(p,'title')} | {pv(p,'rw')} | {pc(p,'jsonType')} | {pc(p,'type')} | {pv(p,'category')} | {ha(p)} | {pv(p,'description')} | {pc(p,'example')} |\n"

print(s, end='')
