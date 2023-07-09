from dataclasses import dataclass
import http.cookiejar

class CookieReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def read_cookies(self) -> dict[str, str]:
        try:
            cookies = {}
            cookie_jar = http.cookiejar.MozillaCookieJar(self.file_path)
            cookie_jar.load()
            for cookie in cookie_jar:
                cookies[cookie.name] = cookie.value
            return cookies
        except FileNotFoundError:
            # Handle file not found error
            return []