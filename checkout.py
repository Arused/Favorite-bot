from concurrent.futures import ThreadPoolExecutor
from requests import Session
import datetime
from threading import Semaphore


class FavsBot:
    def __init__(self):
        self.semaphore = Semaphore(150)
        self.session = Session()
        self.get = self.session.get
        self.susu = 0
        self.success = 0
        self.dateiname = "sessions.txt"

        with open(self.dateiname, 'r') as datei:
            for zeile in datei:
                self.susu += 1

    def process_session(self, sessionid):
        sessionid = sessionid.strip()  # Remove leading/trailing whitespace and newline characters

        url = f"https://api16-normal-c-alisg.tiktokv.com/aweme/v1/aweme/collect/?aweme_id={self.videoid}&action=1&collect_privacy_setting=6&iid=7254119074816722706&device_id=7253485051726579205&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=250204&version_name=25.2.4&device_platform=android&ab_version=25.2.4&ssmix=a&device_type=ASUS_I005DA&device_brand=Asus&language=en&os_api=28&os_version=9&openudid=ce2418a04c17972c&manifest_version_code=2022502040&resolution=1600*900&dpi=300&update_version_code=2022502040&_rticket=1689096775194&current_region=IL&app_type=normal&sys_region=US&mcc_mnc=42515&timezone_name=Asia%2FShanghai&residence=IL&app_language=en&carrier_region=IL&ac2=wifi&uoo=0&op_region=IL&timezone_offset=28800&build_number=25.2.4&host_abi=armeabi-v7a&locale=en&region=US&ts=1689096777&content_language=en%2C&cdid=31e9c062-ecfc-405d-b59a-684bc7af4dcb"

        headers = {
            'x-argus': 'VVdd0vGs1CW5dLIGQOKzEIdEGTarG0EAG2lAJDMzuVtJ3SvfXCe7BsysVsGJ1VQ5y+dOf6wKgfYW5rDIkXwNiOWce1saJfA/L3ximFHAwdLoId0kPewzYtQ5UqhPBEverCZaPscObHSRn9ZJl0pkJ1/hGmGEMa0Bx571dDuxsUfQSn4chsaW7xRsN3MECVQaYmiWWS4NusKFHnmCfnTtc7Kagb7fdReO8O1MWSkNhshuddhmv016mQPyJFq+Q/seSYbb4JA0yaKc3tWSlkCLlIhh',
            'cookie': f'sessionid={sessionid}; tt_webid_v2={sessionid}',
            'user-agent': 'com.zhiliaoapp.musically/2023000150 (Linux; U; Android 9; en; unknown; Build/PI;tt-ok/3.12.13.1)'
        }

        try:
            response = self.get(url, headers=headers)
            if b'"saved"' in response.content:
                print(f"Video ID: {self.videoid} - Saved")
                self.success += 1
            else:
                print(f"Video ID: {self.videoid} - Not Saved")
        except Exception as e:
            print(f"Video ID: {self.videoid} - Error occurred during the request: {str(e)}")

    def run(self):
        with ThreadPoolExecutor(max_workers=150) as executor:
            executor.map(self.process_session, open("sessions.txt", "r"))


def main():
    bot = FavsBot()
    bot.videoid = input("Aweme ID: ")
    bot.run()
    print(f"\nFinished processing sessions. Successful saves: {bot.success}")


if __name__ == '__main__':
    main()
