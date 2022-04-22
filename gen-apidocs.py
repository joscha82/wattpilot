import json
import yaml

WATTPILOT_API_FILE = "src/wattpilot/ressources/wattpilot.yaml"

# Property code formatting:
def pc(prop,key,alt=''):
    return f"`{prop[key]}`" if key in prop and prop[key] != "" else alt

# Property key/alias formatting:
def pk(prop):
    return pc(prop,'key','-') + "<br>" + pc(prop,'alias','-')

# Property type formatting:
def pt(prop):
    return pc(prop,'jsonType','-') + "<br>" + pc(prop,'type','-')

# Property value formatting:
def pv(prop,key,alt=''):
    return prop[key] if key in prop else alt

# Property Home Assistant info formatting:
def ha(prop):
    return ':heavy_check_mark:' if 'homeAssistant' in prop else ':white_large_square:'

# Message and property example formatting:
def e(d):
    return f"`{json.dumps(d['example'])}`" if "example" in d else ""

with open(WATTPILOT_API_FILE, 'r') as stream:
    wpapidef = yaml.safe_load(stream)

s = "# Wattpilot API Description\n\n"

s += "## WebSocket Message Types\n\n"
s += "| Key | Title | Description | Example |\n"
s += "|-----|-------|-------------|---------|\n"
for msg in wpapidef["messages"]:
    s += f"| `{msg['key']}` | {msg['title']} | {msg['description']} | {e(msg)} |\n"
s += "\n"

s += "## WebSocket API Properties\n\n"
s += "| Key/Alias | Title | R/W | JSON/API Type | Category | HA Enabled | Description | Example |\n"
s += "|-----------|-------|-----|---------------|----------|------------|-------------|---------|\n"
for p in wpapidef["properties"]:
    s += f"| {pk(p)} | {pv(p,'title')} | {pv(p,'rw')} | {pt(p)} | {pv(p,'category')} | {ha(p)} | {pv(p,'description')} | {e(p)} |\n"

print(s, end='')
