import json

msg = '{"un": "wew"}'
print json.loads(msg)["un"]
