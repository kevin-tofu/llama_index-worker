import os
# import config
# os.environ["OPENAI_API_KEY"] = config.config_org.openai_key

from llama_index.node_parser import SimpleNodeParser
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.storage.storage_context import StorageContext
from llama_index.indices.base import BaseIndex
from llama_index import load_index_from_storage

from llama_index import SimpleDirectoryReader
from llama_index import ServiceContext, LLMPredictor, OpenAIEmbedding, PromptHelper
from llama_index.llms import OpenAI
from llama_index.text_splitter import TokenTextSplitter
from llama_index.node_parser import SimpleNodeParser
from llama_index.callbacks import LlamaDebugHandler, CallbackManager
from llama_index import ServiceContext
from llama_index.storage.docstore import RedisDocumentStore
from llama_index.storage.index_store import RedisIndexStore
from llama_index.vector_stores import RedisVectorStore
from llama_index.storage.storage_context import StorageContext

from llama_index_server.config import RedisConfig


def get_storage_context(
    cfg: RedisConfig,
    index_id: str
) -> StorageContext:

    docstore = RedisDocumentStore.from_host_and_port(
        host=cfg.redis_host,
        port=cfg.redis_port,
        # namespace="llama_index"
        # namespace=index_id
    )
    index_store=RedisIndexStore.from_host_and_port(
        host=cfg.redis_host,
        port=cfg.redis_port,
        # namespace="llama_index"
        # namespace=index_id
    )

    vector_store = RedisVectorStore(
        index_name=index_id,
        # index_prefix="llama",
        redis_url=f"redis://{cfg.redis_host}:{str(cfg.redis_port)}",
        overwrite=True,
    )

    storage_context = StorageContext.from_defaults(
        docstore=docstore,
        index_store=index_store,
        vector_store=vector_store
    )
    return storage_context

def get_service_context(
) -> ServiceContext:

    llm = OpenAI(
        model='text-davinci-003',
        temperature=0,
        max_tokens=256
    )
    embed_model = OpenAIEmbedding()
    node_parser = SimpleNodeParser.from_defaults(
    text_splitter=TokenTextSplitter(chunk_size=1024, chunk_overlap=20)
    )
    prompt_helper = PromptHelper(
        context_window=4096, 
        num_output=256, 
        chunk_overlap_ratio=0.1, 
        chunk_size_limit=None
    )
    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    callback_manager = CallbackManager([llama_debug])

    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
        node_parser=node_parser,
        callback_manager=callback_manager,
        prompt_helper=prompt_helper
    )
    return service_context


def docs2index(
    docs_path: list[str],
    index_id: str,
    storage: StorageContext,
    service: ServiceContext,
# ) -> BaseIndex:
) -> VectorStoreIndex:
    reader = SimpleDirectoryReader(
        input_files=docs_path
    )
    docs = reader.load_data()
    for d, p in zip(docs, docs_path):
        d.metadata = {
            'filename': os.path.basename(p)
        }

    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents(docs)
    storage.docstore.add_documents(nodes)

    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage,
        service_context=service
    )
    index.set_index_id(index_id)
    return index


def load_index_fromRedis(
    index_id: str,
    cfg_redis: RedisConfig
) -> BaseIndex:

    storage = get_storage_context(
        cfg_redis,
        index_id
    )

    # if loading an index from a persist_dir containing multiple indexes
    index = load_index_from_storage(
        storage,
        index_id=index_id
    )
    index._service_context = get_service_context()
    return index



def ask(
    index: BaseIndex,
    question: str
):
    query_engine = index.as_query_engine(
        # retriever_mode=ListRetriverMode.EMBEDDING,
        similarity_top_k=10,
        streaming=True
    )
    response = query_engine.query(
        question
    )
    return response


def add_document(
    index,
    data_path: str
):
    documents = SimpleDirectoryReader(data_path).load_data()
    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents(documents)

    index.insert_nodes(nodes)

