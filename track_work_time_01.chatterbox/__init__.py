from chatterbox.skills.core import intent_handler
from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxFallbackSkill
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.util.time import now_at_location
from chatterbox.util.format import pronounce_number
from chatterbox.audio import stop_speaking


def upRange(start, stop, step):
    while start <= stop:
        yield start
        start += abs(step)


def downRange(start, stop, step):
    while start >= stop:
        yield start
        start -= abs(step)


message_data = None
utterance = None
utterance_remainder = None
currentDateTime = None
currentHour = None
currentMinute = None
timesheet = None
endTime = None
endTimeHour = None
endTimeMinute = None
i = None
entry = None


class Track_work_time_01_chatterboxSkill(ChatterboxSkill):
    def initialize(self):
        utterance = utterance_remainder = ''
        message_data = {}

    @intent_handler(IntentBuilder("intent_name12").require('start_working'))
    def handle_intent_name12Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, endTimeHour, endTimeMinute, i, entry
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("I am starting to track your work time", wait=True)
        currentDateTime = now_at_location("germany")
        currentHour = currentDateTime.hour
        currentMinute = currentDateTime.minute
        timesheet = []
        timesheet.append([currentHour, currentMinute, "work"])

    @intent_handler(IntentBuilder("intent_name13").require('im_taking_a_break'))
    def handle_intent_name13Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, endTimeHour, endTimeMinute, i, entry
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("I am pausing the time tracking.", wait=True)
        currentDateTime = now_at_location("germany")
        currentHour = currentDateTime.hour
        currentMinute = currentDateTime.minute
        timesheet.append([currentHour, currentMinute, "break"])

    @intent_handler(IntentBuilder("intent_name14").require('save_timesheet'))
    def handle_intent_name14Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, endTimeHour, endTimeMinute, i, entry
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.saveTimesheet()
        self.speak_dialog("saved your timesheet", wait=True)

    @intent_handler(IntentBuilder("intent_name15").require('output_timesheet'))
    def handle_intent_name15Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, endTimeHour, endTimeMinute, i, entry
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak(str(timesheet), wait=True)

    @intent_handler(IntentBuilder("intent_name16").require('done_with_work'))
    def handle_intent_name16Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, endTimeHour, endTimeMinute, i, entry
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("Stopping the time tracking", wait=True)
        endTime = now_at_location("germany")
        endTimeHour = endTime.hour
        endTimeMinute = endTime.minute
        timesheet.append([currentHour, currentMinute, "end"])
        self._in_loop = True
        i_end = float(len(timesheet))
        for i in (1 <= i_end) and upRange(1, i_end, 1) or downRange(1, i_end, 1):
            if not self._in_loop:
                return
            entry = timesheet[int(i - 1)]
            self.speak(str(entry), wait=True)
            if i == 1:
                self.speak_dialog("todo: skip first entry", wait=True)
        self._in_loop = False
        self.speak_dialog("You worked for", wait=True)
        self.speak(str(pronounce_number((endTimeHour - currentHour))), wait=True)
        self.speak_dialog("hours and", wait=True)
        self.speak(str(pronounce_number(
            (endTimeMinute - currentMinute))), wait=True)
        self.speak_dialog("minutes", wait=True)

    @intent_handler(IntentBuilder("intent_name26").require('resume_work'))
    def handle_intent_name26Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, endTimeHour, endTimeMinute, i, entry
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("I am resuming time tracking.", wait=True)
        currentDateTime = now_at_location("germany")
        currentHour = currentDateTime.hour
        currentMinute = currentDateTime.minute
        timesheet.append([currentHour, currentMinute, "work"])

    def stop(self):
        stopped = False
        utterance = utterance_remainder = "stop"
        message_data = {}
        if self._in_loop:
            # stop loops that obey convention and use this flag
            self._in_loop = False
            stopped = True
        # set a flag for intents to react to
        self._should_stop = True
        # just ensuring syntax
        return stopped

    def shutdown(self):
        utterance = utterance_remainder = ''
        message_data = {}
        self.stop()

    def saveTimesheet(self):
        global utterance, utterance_remainder

        try:
            utterance = message.data['utterance']
        except:
            try:
                utterance = message.data['utterances'][0]
            except:
                utterance = utterance or ''
        try:
            utterance_remainder = message.utterance_remainder() or utterance_remainder or ''
        except:
            utterance_remainder = utterance_remainder or ''
        try:
            message_data = message.data
        except:
            message_data = {}
        # Describe this function...
        self.do_pickle("someTestName", timesheet)


def create_skill():
    return Track_work_time_01_chatterboxSkill()
