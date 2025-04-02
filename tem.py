from normalUtils import get_encoding

encoding = get_encoding('./normal_output.json')
print(encoding)
with open('./normal_output.json', 'r', encoding=encoding) as f:
    lines = f.readlines()
f.close()

with open('./normal_output2.json', 'w', encoding='UTF-8') as f:
    for line in lines:
        decoded_str = line.encode('utf-8').decode('unicode_escape')
        f.write(decoded_str)
f.close()