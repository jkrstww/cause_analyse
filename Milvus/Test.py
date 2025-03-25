from pymilvus import model

embedding_fn = model.DefaultEmbeddingFunction()

docs = ['apple', 'hhh', 'banana']

vectors = embedding_fn(docs)

print(vectors[0].shape)