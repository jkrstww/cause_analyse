from pymilvus import MilvusClient
from pymilvus import model
from normalUtils import get_encoding

client = MilvusClient("milvus_demo.db")

if client.has_collection(collection_name="demo_collection"):
    client.drop_collection(collection_name="demo_collection")
client.create_collection(
    collection_name="demo_collection",
    dimension=768,  # The vectors we will use in this demo has 768 dimensions
)

# This will download a small embedding model "paraphrase-albert-small-v2" (~50MB).
embedding_fn = model.DefaultEmbeddingFunction()

encoding = get_encoding("D:\cause_analyse\llamaProject\static\\files\\book2.txt")
with open("D:\cause_analyse\llamaProject\static\\files\\book2.txt", 'r') as f:
    lines = f.read()
f.close()

docs = lines.split("。")

vectors = embedding_fn.encode_documents(docs)

# Each entity has id, vector representation, raw text, and a subject label that we use
# to demo metadata filtering later.
data = [
    {"id": i, "vector": vectors[i], "text": docs[i], "subject": "变压器"}
    for i in range(len(vectors))
]

res = client.insert(collection_name="demo_collection", data=data)

query_vectors = embedding_fn.encode_queries(["变压器发热"])

answer = client.search(
    collection_name="demo_collection",  # target collection
    data=query_vectors,  # query vectors
    limit=2,  # number of returned entities
    output_fields=["text", "变压器"],  # specifies fields to be returned
)

print(res)
