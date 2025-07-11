"""
RAG Pipeline for TrustVoice Analytics
Handles data processing, vectorization, and retrieval for financial complaints analysis
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from transformers import pipeline

class RAGPipeline:
    def __init__(self, chroma_path="vector_store/chromadb_sample_dataset", collection_name="consumer_complaints"):
        self.chroma_client = chromadb.PersistentClient(
            path=chroma_path,
            settings=Settings(anonymized_telemetry=False, allow_reset=True)
        )
        self.collection = self.chroma_client.get_collection(collection_name)
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def search_similar_complaints(self, query, top_k=5):
        query_embedding = self.embedding_model.encode([query])
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k,
            include=['metadatas', 'documents', 'distances']
        )
        similar_complaints = []
        if results['metadatas'] and results['metadatas'][0]:
            for i, metadata in enumerate(results['metadatas'][0]):
                complaint_info = metadata.copy()
                complaint_info['similarity_score'] = 1 - results['distances'][0][i]
                complaint_info['document'] = results['documents'][0][i] if results['documents'] and results['documents'][0] else ""
                similar_complaints.append(complaint_info)
        return similar_complaints

    def generate_answer_with_llm(self, query, top_k=5, model_name="google/flan-t5-base", max_length=256):
        similar_complaints = self.search_similar_complaints(query, top_k=top_k)
        if not similar_complaints:
            return "No relevant context found to answer the question."
        context = "\n".join([c.get('document', '') for c in similar_complaints if c.get('document', '')])
        if not context:
            return "No relevant context found to answer the question."
        prompt = (
            "You are a financial analyst assistant for CrediTrust. "
            "Your task is to answer questions about customer complaints. "
            "Use the following retrieved complaint excerpts to formulate your answer. "
            "If the context doesn't contain the answer, state that you don't have enough information.\n"
            f"Context: {context}\n"
            f"Question: {query}\n"
            "Answer:"
        )
        try:
            generator = pipeline("text2text-generation", model=model_name)
            result = generator(prompt, max_length=max_length, truncation=True)
            answer = result[0]['generated_text'] if result and 'generated_text' in result[0] else result[0].get('text', '')
            return answer.strip()
        except Exception as e:
            import logging
            logging.error(f"❌ Error generating answer with LLM: {e}")
            return f"Error generating answer: {e}" 