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
entry = None
endTimeHour = None
endTimeMinute = None
i = None


class Track_work_time_01_chatterboxSkill(ChatterboxSkill):
    def initialize(self):
        utterance = utterance_remainder = ''
        message_data = {}

    @intent_handler(IntentBuilder("intent_name12").require('start_working'))
    def handle_intent_name12Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, entry, endTimeHour, endTimeMinute, i
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
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, entry, endTimeHour, endTimeMinute, i
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
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, entry, endTimeHour, endTimeMinute, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.saveTimesheet()
        self.speak_dialog("saved your timesheet", wait=True)

    @intent_handler(IntentBuilder("intent_name15").require('tell_me_all_times'))
    def handle_intent_name15Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, entry, endTimeHour, endTimeMinute, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak(str(timesheet), wait=True)

    @intent_handler(IntentBuilder("intent_name16").require('im_done_for_today'))
    def handle_intent_name16Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, entry, endTimeHour, endTimeMinute, i
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
            if i == 1:
                self.speak_dialog("entries", wait=True)
            self.speak(str(pronounce_number((entry[0]))), wait=True)
            self.speak(str(pronounce_number((entry[1]))), wait=True)
            self.speak(str((entry[2])), wait=True)
        self._in_loop = False

    @intent_handler(IntentBuilder("intent_name26").require('resume_working'))
    def handle_intent_name26Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, entry, endTimeHour, endTimeMinute, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("I am resuming time tracking.", wait=True)
        currentDateTime = now_at_location("germany")
        currentHour = currentDateTime.hour
        currentMinute = currentDateTime.minute
        timesheet.append([currentHour, currentMinute, "work"])

    @intent_handler(IntentBuilder("intent_name44").require('whats_the_time_tracking_status'))
    def handle_intent_name44Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, entry, endTimeHour, endTimeMinute, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("todo", wait=True)
        entry = timesheet[-1]
        self.speak(str((entry[-1])), wait=True)

    @intent_handler(IntentBuilder("intent_name46").require('how_long_have_i_worked_already'))
    def handle_intent_name46Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, entry, endTimeHour, endTimeMinute, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("todo", wait=True)

    @intent_handler(IntentBuilder("intent_name48").require('how_long_did_i_work_today'))
    def handle_intent_name48Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, endTime, entry, endTimeHour, endTimeMinute, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("todo", wait=True)

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
