from io import TextIOWrapper
from typing import Any, Dict, Iterator, List, Optional, Sequence

from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders.helpers import detect_file_encodings
import requests, json
from app.UOFastDataArray import *
from langchain_text_splitters import RecursiveJsonSplitter



class UOLoader(BaseLoader):
    """Load a `UniObject` file into a list of Documents.
    """

    def __init__(
        self,
        api_path: str,
        file_obj : file_dict_obj = None,
        meta_data : List[str] = None

    ):
        self.api_path = api_path
        self.file_obj = file_obj
        self.meta_data = meta_data
    

    def lazy_load(self) -> Iterator[Document]:
        try:
            with requests.post(self.api_path, data = self.file_obj.json()) as x_response:
                if x_response.status_code != 200:
                    print("error returned = ",x_response.status_code, json.loads(x_response.text).get("detail"))
                else:
                    uo_obj = x_response.text   
                    yield from self.__get_uo_request(uo_obj)
                    #yield from self.__JsonSplit(uo_obj)
                    
        except Exception as e:
                raise RuntimeError(f"Error calling API {self.api_path}")
        
    def __get_uo_request(self, uo_obj : str) -> Iterator[Document]:
        uo_data_obj = json.loads(uo_obj)
        all_docs = [Document]
        for i in range(len(uo_data_obj)):
            id_key=""
            try:
                row = uo_data_obj[i]
                id_key=row["_recID"]

            except Exception as e:
                RuntimeError(f"Error processing API {self.api_path} file {uo_data_obj.file_name}")
                
            d_content = json.loads(json.dumps(row))
            
            t_content=''
            for key in d_content:
                t_content += '\n' + key + ':' + str(d_content.get(key))

            metadata = {"source": self.file_obj.file_name} #, "sourceID" : id_key }
            #all_docs.append
            doc = (Document(page_content=t_content, metadata=metadata))
            yield doc

    def __JsonSplit(self, json_data):
        splitter = RecursiveJsonSplitter(max_chunk_size=2000)

        # Recursively split json data - If you need to access/manipulate the smaller json chunks
        try:
            yield splitter.create_documents(texts=json.loads(json_data), metadatas=self.meta_data)
        
            #json_chunks = splitter.split_json(json_data=json.loads(json_data))
        except Exception as e:
            print(str(e))
        # The splitter can also output documents
        #return docs


