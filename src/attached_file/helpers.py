from django.conf import settings
import requests


class ExternalStorageManage:
    """
    Class for work with external storage api.
    Methods:
          get_upload_link(self, file_name: str)
          get_download_link(self, file_name)
    Setup `EXTERNAL_STORAGE_TOKEN` environment variable before use.
    """

    headers = {
        'Accept': 'application/json',
        'Authorization': f'OAuth {settings.EXTERNAL_STORAGE_TOKEN}'
    }

    action = {
        'upload_file': 'https://cloud-api.yandex.net/v1/disk/resources/upload?path=',
        'download_file': 'https://cloud-api.yandex.net/v1/disk/resources/download?path='
    }

    def get_upload_link(self, file_name: str):
        """
        Generate link for upload file in storage.
        :param file_name: name for upload file.
        :type file_name: str.
        :return: link for upload file.
        :rtype: str.
        """

        request_json = requests.get(
            url=self.action['upload_file'] + file_name,
            headers=self.headers
        ).json()
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
