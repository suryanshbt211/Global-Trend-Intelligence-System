import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import HDBSCAN
import umap
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')

class NLPAnalyzer:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings_cache = {}
        
    def cluster_related_topics(self, queries: List[str], n_clusters: int = 5):
        if not queries or len(queries) < 3:
            return {"clusters": [], "message": "Not enough queries for clustering"}
        
        embeddings = self.model.encode(queries)
        reducer = umap.UMAP(n_components=min(5, len(queries)-1), random_state=42)
        reduced_embeddings = reducer.fit_transform(embeddings)
        clusterer = HDBSCAN(min_cluster_size=2, min_samples=1)
        labels = clusterer.fit_predict(reduced_embeddings)
        
        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(queries[idx])
        
        result = []
        for label, cluster_queries in clusters.items():
            result.append({
                "cluster_id": int(label),
                "size": len(cluster_queries),
                "queries": cluster_queries,
                "label": "Noise" if label == -1 else f"Topic {label}"
            })
        
        return {
            "clusters": result,
            "total_clusters": len([c for c in result if c['cluster_id'] != -1]),
            "noise_points": len(clusters.get(-1, []))
        }
    
    def get_topic_similarity(self, query1: str, query2: str):
        emb1 = self.model.encode([query1])[0]
        emb2 = self.model.encode([query2])[0]
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return float(similarity)
