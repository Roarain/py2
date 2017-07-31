import yaml

with open('/PycharmProjects/code1/program2/config/properties','rb') as f:
    content = f.read()

cfg = yaml.load(content)

filename = cfg['file_metadata']['filename']
filepath = cfg['file_metadata']['filepath']
with open(filepath,'rb') as f:
    fielsize = len(f.read())

cfg['file_metadata']['filesize'] = fielsize

print cfg



