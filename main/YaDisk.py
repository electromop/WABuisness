import requests


class YaDisk:
    BASE_URL = "https://cloud-api.yandex.net"

    def __init__(self, token):
        self._token = token
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':
                         f'OAuth {token}'}

    def get_files(self) -> dict:
        res = requests.get(f"{self.BASE_URL}/v1/disk/resources/files?limit=100", headers=self._headers)
        res.raise_for_status()
        return res.json()["items"]

    def download_file(self, path_from: str, path_to: str):
        res = requests.get(f"{self.BASE_URL}/v1/disk/resources/download?path={path_from}", headers=self._headers)
        res.raise_for_status()
        url = res.json()["href"]
        self._download(url, path_to)

    def _download(self, url, local_file):
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(local_file, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
        except Exception as e:
            return None
        return local_file

    def listdir(self, path: str):
        res = requests.get(f"{self.BASE_URL}/v1/disk/resources?path={path}", headers=self._headers)
        #res.raise_for_status()
        return res.json()["_embedded"]["items"] if res.status_code == 200 else []

