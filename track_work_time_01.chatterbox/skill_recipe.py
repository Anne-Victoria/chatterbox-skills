from chatterbox.util.time import now_at_location

from chatterbox.util.format import pronounce_number


from chatterbox.builder.skill_builder import SkillBuilder


def create_skill():
  s = SkillBuilder('Track Work Time 01')
  s.get_utterance()
  s.add_keyword("start working", samples = [''' start working ''', "start working", "start working"], action="require", intent_name="intent name2")
  s.add_code_line("self.speak_dialog(''' Tracking the time for you ''', wait=True)")
  s.add_code_line("global startTime")
  s.add_code_line("startTime = now_at_location(''' germany ''')")
  s.add_code_line("global startTimeHour")
  s.add_code_line("startTimeHour = startTime.hour")
  s.add_code_line("global startTimeMinute")
  s.add_code_line("startTimeMinute = startTime.minute")
  s.add_code_line("self.speak(str(pronounce_number(startTimeHour)), wait=True)")
  s.add_code_line("self.speak(str(pronounce_number(startTimeMinute)), wait=True)")
  s.add_adapt_intent("intent name2")
  s.get_utterance()
  s.add_keyword("done with work", samples = [''' done with work ''', "done with work", "done with work"], action="require", intent_name="intent name18")
  s.add_code_line("self.speak_dialog(''' Stopping the time tracking ''', wait=True)")
  s.add_code_line("global endTime")
  s.add_code_line("endTime = now_at_location(''' germany ''')")
  s.add_code_line("global endTimeHour")
  s.add_code_line("endTimeHour = endTime.hour")
  s.add_code_line("global endTimeMinute")
  s.add_code_line("endTimeMinute = endTime.minute")
  s.add_code_line("self.speak_dialog(''' You worked for ''', wait=True)")
  s.add_code_line("self.speak(str(pronounce_number((endTimeHour - startTimeHour))), wait=True)")
  s.add_code_line("self.speak_dialog(''' hours and ''', wait=True)")
  s.add_code_line("self.speak(str(pronounce_number((endTimeMinute - startTimeMinute))), wait=True)")
  s.add_code_line("self.speak_dialog(''' minutes ''', wait=True)")
  s.add_adapt_intent("intent name18")
  s.build_skill()
