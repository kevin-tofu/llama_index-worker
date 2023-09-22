from typing import Optional
from typing import NamedTuple, Literal
from fastapi import BackgroundTasks
import uuid
from llama_index import ServiceContext
import filerouter

from llama_index_server.config import Config
from llama_index_server.logconf import mylogger
from llama_index_server import func_llamaindex
logger = mylogger(__name__)


class myProcessor(filerouter.processor):
    def __init__(self, cfg: Config):
        super().__init__()

        self.cfg = cfg


    async def post_file_process(
        self,
        process_name: str,
        data: filerouter.fileInfo | list[filerouter.fileInfo],
        file_dst_path: Optional[str] = None,
        bgtask: BackgroundTasks=BackgroundTasks(),
        **kwargs
    ):
        logger.info(f"process - {process_name}")
        
        if isinstance(data, filerouter.fileInfo):
            
            index_id = str(uuid.uuid4())
            storage = func_llamaindex.get_storage_context(
                self.cfg.redis,
                index_id
            )
            service = func_llamaindex.get_service_context()

            index = func_llamaindex.docs2index(
                [data.path],
                index_id,
                storage,
                service,
            )
            return dict(
                status='OK',
                index_id=index_id
            )

    # ac54328c-8973-4091-a112-19a038c03e61
    def query(
        self,
        index_id: str,
        query: str
    ):
        print(index_id)
        print(query)
        index = func_llamaindex.load_index_fromRedis(
            index_id,
            self.cfg.redis
        )
        res = func_llamaindex.ask(
            index,
            query
        )
        print(res)
        print(type(res))
        # <class 'llama_index.response.schema.StreamingResponse'>

        return res