from dataclasses import dataclass
import http.cookiejar

class Cookie:
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    @staticmethod
    def getCookies(self) -> dict[str, str]:
        if self.file_path == None:
            raise FileNotFoundError

        cookies = {}
        cookie_jar = http.cookiejar.MozillaCookieJar(self.file_path)
        cookie_jar.load()
        for cookie in cookie_jar:
            cookies[cookie.name] = cookie.value
        return cookies
    
    @staticmethod
    def getHeader(cookies: dict[str,str]):
        return "; ".join([f"{name}={value}" for name, value in cookies.items()])