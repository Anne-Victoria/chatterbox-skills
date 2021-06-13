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
entry = None
exampleParam = None
i = None


class Track_work_time_01_chatterboxSkill(ChatterboxSkill):
    def initialize(self):
        utterance = utterance_remainder = ''
        message_data = {}

    @intent_handler(IntentBuilder("intent_name29").require('start_working'))
    def handle_intent_name29Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("I am starting to track your work time", wait=True)
        currentDateTime = now_at_location("germany")
        currentHour = currentDateTime.hour
        currentMinute = currentDateTime.minute
        timesheet = []
        timesheet.append([currentHour, currentMinute, "work"])

    @intent_handler(IntentBuilder("intent_name30").require('im_taking_a_break'))
    def handle_intent_name30Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("I am pausing the time tracking.", wait=True)
        currentDateTime = now_at_location("germany")
        currentHour = currentDateTime.hour
        currentMinute = currentDateTime.minute
        timesheet.append([currentHour, currentMinute, "break"])

    @intent_handler(IntentBuilder("intent_name31").require('resume_working'))
    def handle_intent_name31Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("I am resuming time tracking.", wait=True)
        currentDateTime = now_at_location("germany")
        currentHour = currentDateTime.hour
        currentMinute = currentDateTime.minute
        timesheet.append([currentHour, currentMinute, "work"])

    @intent_handler(IntentBuilder("intent_name32").require('im_done_for_today'))
    def handle_intent_name32Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("Stopping the time tracking", wait=True)
        currentDateTime = now_at_location("germany")
        currentHour = currentDateTime.hour
        currentMinute = currentDateTime.minute
        timesheet.append([currentHour, currentMinute, "end"])
        self._in_loop = True
        i_end = float(len(timesheet))
        for i in (1 <= i_end) and upRange(1, i_end, 1) or downRange(1, i_end, 1):
            if not self._in_loop:
                return
            entry = timesheet[int(i - 1)]
            if i == 1:
                self.speak_dialog("These are your entries", wait=True)
            self.speak(str(pronounce_number((entry[1]))), wait=True)
            self.speak_dialog("minutes past", wait=True)
            self.speak(str(pronounce_number((entry[0]))), wait=True)
            self.speak(str((entry[2])), wait=True)
        self._in_loop = False

    @intent_handler(IntentBuilder("intent_name33").require('whats_the_time_tracking_status'))
    def handle_intent_name33Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        entry = timesheet[-1]
        self.speak_dialog("You are currently on", wait=True)
        self.speak(str((entry[-1])), wait=True)

    @intent_handler(IntentBuilder("intent_name34").require('how_long_have_i_worked_already'))
    def handle_intent_name34Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("todo", wait=True)

    @intent_handler(IntentBuilder("intent_name35").require('how_long_did_i_work_today'))
    def handle_intent_name35Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("todo", wait=True)

    @intent_handler(IntentBuilder("intent_name36").require('tell_me_all_times'))
    def handle_intent_name36Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak(str(timesheet), wait=True)

    @intent_handler(IntentBuilder("intent_name37").require('save_timesheet'))
    def handle_intent_name37Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.saveTimesheet()
        self.speak_dialog("saved your timesheet", wait=True)

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

    def exampleFunction(self):
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
        self.speak(str(exampleParam), wait=True)
        self.speak(str(currentDateTime), wait=True)
        return "example string"


def create_skill():
    return Track_work_time_01_chatterboxSkill()
