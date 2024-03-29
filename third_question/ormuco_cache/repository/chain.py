from ormuco_cache.repository.base import BaseRepository
from ormuco_cache.repository.memory import MemoryRepository
from ormuco_cache.repository.network import ClientNetworkRepository, ServerNetworkRepository


class ChainClientRepository(BaseRepository):
    def __init__(self, settings):
        super().__init__(settings)
        self.memory_repository = MemoryRepository(settings)
        self.network_repository = ClientNetworkRepository(settings)

    def retrieve(self, key):
        cache_item = self.memory_repository.retrieve(key)
        if cache_item != None:
            return cache_item

        cache_item = self.network_repository.retrieve(key)
        if cache_item != None:
            self.memory_repository.store(cache_item)

        return cache_item

    def store(self, cache_item):
        self.memory_repository.store(cache_item)
        self.network_repository.store(cache_item)
        return True


class ChainServerRepository(ChainClientRepository):
    def __init__(self, settings):
        super().__init__(settings)
        self.memory_repository = MemoryRepository(settings)
        self.network_repository = ServerNetworkRepository(settings)
