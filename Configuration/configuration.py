from Configuration.helpers import get_env_variable


class RAG: 
    DEVICE = get_env_variable("MODEL_DEVICE")
    MODEL_NAME = get_env_variable("MODEL_NAME")

class QDRANT:
    URL = get_env_variable("URL")
    API_KEY = get_env_variable("API_KEY")
    TOP_K = get_env_variable("TOP_K")
    
class Service:
    HOST = get_env_variable("HOST")
    PORT = get_env_variable("PORT")  
        