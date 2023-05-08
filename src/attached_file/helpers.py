import logging

from dataclasses import dataclass, asdict
import asyncio
import time

import aiohttp
from django.conf import settings
from django.core.cache import cache
import requests

logger = logging.getLogger('attached_file.helpers')

class AsyncRequestsManager:

    @dataclass
    class Request:
        url: str
        headers: dict
        method: str

    def do_async_requests(self, requests: list[Request]) -> list[dict]:
        results = asyncio.run(self.main(requests))

        return results

    async def main(self, requests: list[Request]):
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_data(session, request) for request in requests]
            results = await asyncio.gather(*tasks)
            return results
    
    @staticmethod
    async def _fetch_data(session: aiohttp.ClientSession, request: Request):
        async with session.request(**asdict(request)) as response:
            
            data = await response.json()
            return data



class ExternalStorageManage:
    """
    Class for work with external storage api.
    Methods:
          get_upload_link(self, file_name: str)
          get_download_link(self, file_name)
    Setup `EXTERNAL_STORAGE_TOKEN` environment variable before use.
    """

    @dataclass
    class Action:
        base_url: str
        method: str
        headers: dict

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {settings.EXTERNAL_STORAGE_TOKEN}'
    }

    action: dict[str, Action]

    def __init__(self) -> None:
        base_URL = settings.IMAGE_SERVICE_URL
        self.action = {
            'upload_file': self.Action(
                base_url= base_URL + '/image-service/api/v1/upload_link/{path}',
                method='GET', 
                headers=self.headers
            ),
            'download_file': self.Action(
                base_url= base_URL + '/image-service/api/v1/download_link/{path}',
                method='GET',
                headers=self.headers
            ),
            'delete_file': self.Action(
                base_url= base_URL + '/image-service/api/v1/delete_file/{path}/',
                method='DELETE',
                headers=self.headers
            )
        }

    def get_upload_link(self, file_name: str):
        """
        Generate link for upload file in storage.
        :param file_name: name for upload file.
        :type file_name: str.
        :return: link for upload file.
        :rtype: str.
        """

        try:
            request_json = requests.get(
                url=self.action['upload_file'].base_url.format(path=file_name),
                headers=self.headers
            ).json()
        except requests.exceptions.RequestException as e:
            logger.exception('{e}'.format(
                e=e
            ))
            raise e

        return request_json['href']

    def get_download_link(self, file_name):
        """
        Generate link for download file in storage.
        :param file_name: name for download file.
        :type file_name: str.
        :return: link for download file.
        :rtype: str.
        """

        request_json = requests.get(
            url=self.action['download_file'] + file_name,
            headers=self.headers
        ).json()
        return request_json['href']
    
    def delete_files(self, file_names: list[str]):
        self._delete_from_cache(file_names)
        self._do_requests(file_names, self.action['delete_file'])

    def get_download_links(self, file_names: list[str]):

        file_cache = self._check_in_cache(file_names)
        files_not_cache = [file_name for file_name in file_names if file_name not in file_cache]

        if files_not_cache is not None:
            cache.set_many(
                {file_name: link for file_name, link in zip(files_not_cache, self._do_requests(files_not_cache, self.action['download_file']))}
            )
            file_cache = self._check_in_cache(file_names)
        
        return [file_cache[file_name] for file_name in file_names]
    
    def _do_requests(self, file_names: list[str], action: Action) -> list[str]:

        async_manager = AsyncRequestsManager()

        async_requests = [
            async_manager.Request(
                url=action.base_url.format(path=file_name),
                headers=action.headers,
                method=action.method
            )
            for file_name in file_names]

        responses = async_manager.do_async_requests(async_requests)
        return [response.get('href') for response in responses if response is not None]
    

    def _check_in_cache(self, file_names: list[str]) -> dict:
        return {file_name: cache.get(file_name) for file_name in file_names if cache.has_key(file_name)}
    
    def _delete_from_cache(self, file_names: list[str]) -> None:
        cache.delete_many(file_names)
