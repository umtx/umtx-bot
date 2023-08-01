from ics import Calendar, Event

from dateutil.parser import parse

def build_ics(data):
    cal = Calendar()

    for item in data:
        for class_date in item["sessionclass"]["classclassdate"]:
            event = Event()
            event.name = item["sessionclass"]["ses_coursenameen"]
            event.begin = parse(class_date["ses_start"])
            event.end = parse(class_date["ses_stop"])
            event.location = class_date["classdateroom"]["ses_roomname"]
            event.description = f"Faculty: {class_date['ses_facultyname']}\nCourse: {item['ses_course']}"

            cal.events.add(event)
    return cal
def main(data):

    calendar = build_ics(data)

    # Write the calendar to an .ics file
    with open('calendar.ics', 'w') as file:
        file.write(str(calendar))