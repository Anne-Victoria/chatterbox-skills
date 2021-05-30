from chatterbox.skills.core import intent_handler
from adapt.intent import IntentBuilder
from chatterbox.skills.core import ChatterboxFallbackSkill
from chatterbox.skills.core import ChatterboxSkill
from chatterbox.util.time import now_at_location
from chatterbox.util.format import pronounce_number
from chatterbox.audio import stop_speaking

message_data = None
utterance = None
utterance_remainder = None
startTime = None
startTimeHour = None
startTimeMinute = None
endTime = None
endTimeHour = None
endTimeMinute = None


class Track_work_time_01_chatterboxSkill(ChatterboxSkill):
    def initialize(self):
        utterance = utterance_remainder = ''
        message_data = {}

    @intent_handler(IntentBuilder("intent_name2").require('start_working'))
    def handle_intent_name2Intent(self, message):
        global message_data, utterance, utterance_remainder, startTime, startTimeHour, startTimeMinute, endTime, endTimeHour, endTimeMinute
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("Tracking the time for you", wait=True)
        startTime = now_at_location("germany")
        startTimeHour = startTime.hour
        startTimeMinute = startTime.minute
        self.speak(str(pronounce_number(startTimeHour)), wait=True)
        self.speak(str(pronounce_number(startTimeMinute)), wait=True)

    @intent_handler(IntentBuilder("intent_name18").require('done_with_work'))
    def handle_intent_name18Intent(self, message):
        global message_data, utterance, utterance_remainder, startTime, startTimeHour, startTimeMinute, endTime, endTimeHour, endTimeMinute
        utterance = message.data['utterance']
        utterance_remainder = message.utterance_remainder() or ''
        message_data = message.data

        self.speak_dialog("Stopping the time tracking", wait=True)
        endTime = now_at_location("germany")
        endTimeHour = endTime.hour
        endTimeMinute = endTime.minute
        self.speak_dialog("You worked for", wait=True)
        self.speak(str(pronounce_number(
            (endTimeHour - startTimeHour))), wait=True)
        self.speak_dialog("hours and", wait=True)
        self.speak(str(pronounce_number(
            (endTimeMinute - startTimeMinute))), wait=True)
        self.speak_dialog("minutes", wait=True)

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


def create_skill():
    return Track_work_time_01_chatterboxSkill()
