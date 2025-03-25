from normalUtils import get_encoding

baseline_path = "D:\cause_analyse\llamaProject\static\\files\\base.txt"
base_set = set()

encoding = get_encoding(baseline_path)
with open(baseline_path, 'r', encoding=encoding) as f:
    lines = f.readlines()
    for line in lines:
        base_set.add((line.strip()))

test_path = "D:\cause_analyse\llamaProject\causeDiscovery\output_pair.txt"
test_set = set()

encoding = get_encoding(test_path)
with open(test_path, 'r', encoding=encoding) as f:
    lines = f.readlines()
    for line in lines:
        test_set.add((line.strip().replace("->", ",")))

test2_path = "D:\cause_analyse\llamaProject\causeDiscovery\output_pair2.txt"
test2_set = set()

encoding = get_encoding(test2_path)
with open(test2_path, 'r', encoding=encoding) as f:
    lines = f.readlines()
    for line in lines:
        test2_set.add((line.strip().replace("->", ",")))


both_set = test_set & base_set
both_set2 = test2_set & base_set

accuracy = float(len(both_set)/len(test_set))
recall = float(len(both_set)/len(base_set))
f = accuracy*recall/(accuracy+recall)
print(f"accuracy:{accuracy}, recall:{recall}, f:{f}")

accuracy2 = float(len(both_set2)/len(test2_set))
recall2 = float(len(both_set2)/len(base_set))
f2 = accuracy2*recall2/(accuracy2+recall2)
print(f"accuracy:{accuracy2}, recall:{recall2}, f:{f2}")