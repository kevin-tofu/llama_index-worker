

from fastapi import APIRouter, File, UploadFile, Header, Depends
from fastapi import BackgroundTasks
import filerouter
from filerouter import processType

from llama_index_server.handler import myProcessor
from llama_index_server.config import Config

# from routes.detection_depends import params_detector, params_model


def get_router(
    cfg: Config
) -> APIRouter:

    test_config = dict(
        data_path = "./temp"
    )

    handler = filerouter.router(
        myProcessor(cfg), 
        filerouter.config(**test_config)
    )
    router = APIRouter(prefix="")


    @router.post('/file')
    async def post_file(
        file: UploadFile = File(...),
        bgtask: BackgroundTasks = BackgroundTasks(),
        # params: dict = Depends(params_model)
    ):  
        """
        """
        params = dict()
        return await handler.post_file(
            "patch-model",
            processType.FILE,
            file,
            None,
            bgtask=bgtask,
            **params
        )

    @router.post('/index/{index_id}/query')
    def post_query(
        index_id: str,
        query: str
        # params: dict = Depends(params_model)
    ):  
        """
        """
        # params = dict()
        return handler.processor.query(
            index_id,
            query
        )

    return router