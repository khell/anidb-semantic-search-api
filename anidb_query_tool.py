from datasets import load_dataset, Dataset
from sentence_transformers import SentenceTransformer, util
from huggingface_hub import hf_hub_download
import torch
from logger import logger
import os

# Change to "cpu" if not on Mac or "cuda" if available
TORCH_DEVICE = torch.device(os.getenv("TORCH_DEVICE", "mps"))
# Default embeddings were generated using this model
MODEL = 'all-mpnet-base-v2'

class AnidbIdQueryTool:
  embedder: SentenceTransformer = SentenceTransformer(MODEL)
  dataset: Dataset = None
  embeddings: torch.Tensor = None
  
  def load_all(self):
    logger.info("Loading raw datasets...")
    self.load_dataset()

    logger.info("Loading embeddings...")
    self.load_embedding()

    logger.info("Data loaded and ready")

  def load_dataset(self):
    self.dataset = load_dataset('khellific/anidb-series-embeddings', data_dir="raw", sep="|", split="train", column_names=['id', 'type', 'language', 'title'])
    
  def load_embedding(self):
    try:
      embedding_path = hf_hub_download("khellific/anidb-series-embeddings", "embeddings/corpus.pt", repo_type="dataset")
      self.embeddings = torch.load(embedding_path, map_location=TORCH_DEVICE)
      return
    except Exception as e:
      logger.info(f"Could not load embedding due to {e}.")
  
  def get_anidb_id(self, query: str):
    query_embedding = self.embedder.encode(query, convert_to_tensor=True, device=TORCH_DEVICE)
    matches = util.semantic_search(query_embedding, self.embeddings, top_k=1)[0][0]
    matched_row = self.dataset[matches['corpus_id']]
    return { "id": f"anidb-{matched_row['id']}", "name": matched_row['title'], "score": matches["score"] }