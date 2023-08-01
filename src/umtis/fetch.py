from umtis.sis.api import UMT_SIS
from umtis.build import main as build_ics_main

from umtis import log
logger = log.setup_logging("MAIN")
def process(token, uid):
    SIS_SDK = UMT_SIS(token, uid)
    CALENDAR_ALL = []
    for year in SIS_SDK.get_academic_year():
        for term in SIS_SDK.get_term(year['academicyearid']):

            CALENDAR_ALL += SIS_SDK.get_calendar(term['ses_termid'])
    logger.info("FETCHED TOTAL: " + str(len(CALENDAR_ALL)))
    build_ics_main(CALENDAR_ALL)


def main(token, uid):
    process(token, uid)

def manual():
    token = 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJjY2I4Y2YwNC03NzIyLTQzZWQtYmFlNS0zM2Q1ZmQ3YTNlMTQiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vNjQyYThlNTctMzMyNi00ZjE1LTkwZWMtYjBmODcwYmE1MzJjL3YyLjAiLCJpYXQiOjE2ODg4OTQwMjMsIm5iZiI6MTY4ODg5NDAyMywiZXhwIjoxNjg4ODk3OTIzLCJuYW1lIjoiT25nIFRoYW5oIEJpbmgiLCJvaWQiOiI2NTg2NGU4OS03ZTA3LTQ3ZjMtOTdhYi1hZDUxZWRhZDBiY2IiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJiaW5oLjIyMDE3MDAwMDJAc3QudW10LmVkdS52biIsInJoIjoiMC5BVW9BVjQ0cVpDWXpGVS1RN0xENGNMcFRMQVRQdU13aWQtMUR1dVV6MWYxNlBoUktBUFkuIiwic3ViIjoiTW5xdFhhUlNrNnFfS0RSMXFtWG5MTXpZeDZyaDBVaGJGMllJT3F1NmIwSSIsInRpZCI6IjY0MmE4ZTU3LTMzMjYtNGYxNS05MGVjLWIwZjg3MGJhNTMyYyIsInV0aSI6InNYMHpvSDM5VWtTWkJKNVRJRlZFQUEiLCJ2ZXIiOiIyLjAifQ.RURS81VHlouOST-WDkeBGla7IY0WwI1P_D69r8zY1-qahTup_9NxvAriv-wnB01q68EEG2Jcg-emQLqXXk2ruR_knDACgKIsHORIokvj_W0oJks1qXUtHXfx_7I7BUYtru2jFdXUoNH8l1NwOinzbs0igSn2abp6CU6V5svVlQQ0kYAAzf8t7UyZ8IkT1HjxBmVKCuMNXp4UxuXQ7lUVLJTZIx8VQ4Iar9HpH6IMu5SiS3AaGQ1Es1-LIawFunR2ZE1-gH0RKCrV3xgYzIAEJ2RciBzWiBZCoQaLRFv3ajMP1b-eViMLFdZ6k5fZSVW4wIcWn7qeAm2p7cTZ_lpWTA'
    process(token)