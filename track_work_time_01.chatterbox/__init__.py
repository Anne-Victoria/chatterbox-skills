import datetime
import pytz
from chatterbox.skills.core import intent_handler
from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxFallbackSkill
from chatterbox.skills.core import ChatterboxSkill
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

viennaTZ = pytz.timezone('Europe/Vienna')

class Track_work_time_01_chatterboxSkill(ChatterboxSkill):
    def initialize(self):
        utterance = utterance_remainder = ''
        message_data = {}

    # start working
    @intent_handler(IntentBuilder("intent_name29").require('start_working'))
    def handle_intent_name29Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        print(viennaTZ)

        self.speak_dialog("I am starting to track your work time", wait=True)
        currentDateTime = datetime.datetime.now(tz=viennaTZ) 

        timesheet = []
        timesheet.append([currentDateTime, "work"])

    # taking a break
    @intent_handler(IntentBuilder("intent_name30").require('im_taking_a_break'))
    def handle_intent_name30Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("I am pausing the time tracking.", wait=True)
        currentDateTime = datetime.datetime.now(tz=viennaTZ) 
        timesheet.append([currentDateTime, "break"])

    # resuming work
    @intent_handler(IntentBuilder("intent_name31").require('resume_working'))
    def handle_intent_name31Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("I am resuming time tracking.", wait=True)
        currentDateTime = datetime.datetime.now(tz=viennaTZ) 
        timesheet.append([currentDateTime, "work"])

    # finishing for the day
    @intent_handler(IntentBuilder("intent_name32").require('im_done_for_today'))
    def handle_intent_name32Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("Stopping the time tracking", wait=True)
        currentDateTime = datetime.datetime.now(tz=viennaTZ) 
        timesheet.append([currentDateTime, "end"])
        minutesWorked = 0
        minutesOnBreak = 0
        self._in_loop = True
        i_end = float(len(timesheet))
        # note: i starts at 1
        for i in (1 <= i_end) and upRange(1, i_end, 1) or downRange(1, i_end, 1):
            if not self._in_loop:
                return
            entry = timesheet[int(i - 1)]
            entryTime = entry[0]
            entryType = entry[1]
            if not i == 1:
                prevEntry = timesheet[int(i - 2)]
                prevTime = prevEntry[0]
                prevType = prevEntry[1]
                diff = entryTime - prevTime
                if prevType == "work":
                    minutesWorked = minutesWorked + int(diff.seconds / 60)
                else:
                    minutesOnBreak = minutesOnBreak + int(diff.seconds / 60)
            # self.speak(str(entry[0]), wait=True)
            # self.speak(str(entry[1]), wait=True)
        self.speak("you worked", wait=True)
        if not (minutesWorked // 60) == 0:
            self.speak(str(minutesWorked // 60), wait=True)
            self.speak("hours", wait=True)
        self.speak(str(minutesWorked % 60), wait=True)
        if minutesWorked % 60 == 0:
            self.speak("zero", wait=True)
        self.speak("minutes", wait=True)

        self.speak("you were on break", wait=True)
        if not (minutesOnBreak // 60) == 0:
            self.speak(str(minutesOnBreak // 60), wait=True)
            self.speak("hours", wait=True)
        self.speak(str(minutesOnBreak % 60), wait=True)
        if  minutesOnBreak % 60 == 0:
            self.speak("zero", wait=True)
        self.speak("minutes", wait=True)
        
        self._in_loop = False

    # getting current status
    @intent_handler(IntentBuilder("intent_name33").require('whats_the_time_tracking_status'))
    def handle_intent_name33Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        entry = timesheet[-1]
        self.speak_dialog("You are currently on", wait=True)
        self.speak(str((entry[-1])), wait=True)

    # how long have I worked so far?
    @intent_handler(IntentBuilder("intent_name34").require('how_long_have_i_worked_already'))
    def handle_intent_name34Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("todo", wait=True)

    # getting total work hours
    @intent_handler(IntentBuilder("intent_name35").require('how_long_did_i_work_today'))
    def handle_intent_name35Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("todo", wait=True)

    # getting all times
    @intent_handler(IntentBuilder("intent_name36").require('tell_me_all_times'))
    def handle_intent_name36Intent(self, message):
        global message_data, utterance, utterance_remainder, currentDateTime, currentHour, currentMinute, timesheet, entry, exampleParam, i
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("These are your entries from today", wait=True)
        self._in_loop = True
        i_end = float(len(timesheet))
        # note: i starts at 1
        for i in (1 <= i_end) and upRange(1, i_end, 1) or downRange(1, i_end, 1):
            if not self._in_loop:
                return
            entry = timesheet[int(i - 1)]
            entryTime = entry[0]
            entryType = entry[1]
            if not i == 1:
                prevEntry = timesheet[int(i - 2)]
                prevTime = prevEntry[0]
                prevType = prevEntry[1]
                diff = entryTime - prevTime
                self.speak_dialog("At", wait=True)
                self.speak_dialog(prevTime.strftime("%H %M"), wait=True)
                entryDuration = int(diff.seconds / 60)
                hourPart = entryDuration // 60
                minutePart = entryDuration % 60
                if prevType == "work":
                    self.speak_dialog("you worked for", wait=True)
                else:
                    self.speak_dialog("you were on break for", wait=True)
                if not hourPart == 0:
                    self.speak(hourPart, wait=True)
                    self.speak("hours and", wait=True)
                self.speak(minutePart, wait=True)
                if minutePart == 0:
                    self.speak("zero", wait=True)
                self.speak("minutes", wait=True)
                
        self._in_loop = False


    # saving timesheet
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

    # UTILITY: save timesheet
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

    # UTILITY: example function
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
