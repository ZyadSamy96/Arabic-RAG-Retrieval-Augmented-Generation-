from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation, CLIPProcessor, CLIPModel
from Configuration.configuration import RAG
import torch


class Encoder:
    def __init__(self, model_name=None):

        if model_name is None:
            model_name = RAG.MODEL_NAME
            

        self.text_model = CLIPModel.from_pretrained(model_name)
        self.image_model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)

    def get_image_embeddings(self, images):

        inputs = self.processor(images=images, return_tensors="pt")
        with torch.no_grad():
            image_embeddings = self.image_model.get_image_features(**inputs)
        return image_embeddings

    def get_text_embeddings(self, texts):

        inputs = self.processor(text=texts, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            text_embeddings = self.text_model.get_text_features(**inputs)
        return text_embeddings


