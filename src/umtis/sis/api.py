import umtis.network_json as network
import umtis.utils as utils
class UMT_SIS:
    def __init__(self, API_KEY, UID):
        self.API_KEY = API_KEY
        self.UID = UID
    def get_academic_year(self):
        url = f"https://apisis.umt.edu.vn/api/v1.0/select/academicyears?currentdate={utils.today_in_ymd()}"
        list_academic_year = network.get(url, self.API_KEY)
        # print(list_academic_year)
        return list_academic_year

    def get_term(self, year_id: str):
        url = f"https://apisis.umt.edu.vn/api/v1.0/select/terms?academicyearid={year_id}"
        list_term = network.get(url, self.API_KEY)
        return list_term

    def get_calendar(self, term_id):
        url = f"https://apisis.umt.edu.vn/api/v1.0/sessions/students/schedule?ses_studentid={self.UID}&ses_termid={term_id}"
        calendar = network.get(url, self.API_KEY)
        return calendar
