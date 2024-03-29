from chatterbox.util.time import now_at_location

from chatterbox.util.format import pronounce_number

def upRange(start, stop, step):
  while start <= stop:
    yield start
    start += abs(step)

def downRange(start, stop, step):
  while start >= stop:
    yield start
    start -= abs(step)


from chatterbox.builder.skill_builder import SkillBuilder


def create_skill():
  s = SkillBuilder('Track Work Time 01')
  s.get_utterance()
  s.add_keyword("start working", samples = [''' start working ''', "start working", "start working"], action="require", intent_name="intent name29")
  s.add_code_line("self.speak_dialog(''' I am starting to track your work time ''', wait=True)")
  s.add_code_line("global currentDateTime")
  s.add_code_line("currentDateTime = now_at_location(''' germany ''')")
  s.add_code_line("global currentHour")
  s.add_code_line("currentHour = currentDateTime.hour")
  s.add_code_line("global currentMinute")
  s.add_code_line("currentMinute = currentDateTime.minute")
  s.add_code_line("global timesheet")
  s.add_code_line("timesheet = []")
  s.add_code_line("timesheet.append([currentHour, currentMinute, ''' work '''])")
  s.add_adapt_intent("intent name29")
  s.get_utterance()
  s.add_keyword("im taking a break", samples = [''' i'm taking a break ''', "im taking a break", "i m taking a break"], action="require", intent_name="intent name30")
  s.add_code_line("self.speak_dialog(''' I am pausing the time tracking. ''', wait=True)")
  s.add_code_line("global currentDateTime")
  s.add_code_line("currentDateTime = now_at_location(''' germany ''')")
  s.add_code_line("global currentHour")
  s.add_code_line("currentHour = currentDateTime.hour")
  s.add_code_line("global currentMinute")
  s.add_code_line("currentMinute = currentDateTime.minute")
  s.add_code_line("timesheet.append([currentHour, currentMinute, ''' break '''])")
  s.add_adapt_intent("intent name30")
  s.get_utterance()
  s.add_keyword("resume working", samples = [''' resume working ''', "resume working", "resume working"], action="require", intent_name="intent name31")
  s.add_code_line("self.speak_dialog(''' I am resuming time tracking. ''', wait=True)")
  s.add_code_line("global currentDateTime")
  s.add_code_line("currentDateTime = now_at_location(''' germany ''')")
  s.add_code_line("global currentHour")
  s.add_code_line("currentHour = currentDateTime.hour")
  s.add_code_line("global currentMinute")
  s.add_code_line("currentMinute = currentDateTime.minute")
  s.add_code_line("timesheet.append([currentHour, currentMinute, ''' work '''])")
  s.add_adapt_intent("intent name31")
  s.get_utterance()
  s.add_keyword("im done for today", samples = [''' i'm done for today ''', "im done for today", "i m done for today"], action="require", intent_name="intent name32")
  s.add_code_line("self.speak_dialog(''' Stopping the time tracking ''', wait=True)")
  s.add_code_line("global currentDateTime")
  s.add_code_line("currentDateTime = now_at_location(''' germany ''')")
  s.add_code_line("global currentHour")
  s.add_code_line("currentHour = currentDateTime.hour")
  s.add_code_line("global currentMinute")
  s.add_code_line("currentMinute = currentDateTime.minute")
  s.add_code_line("timesheet.append([currentHour, currentMinute, ''' end '''])")
  s.set_default_stop()
  s.add_code_line("self._in_loop=True")
  s.add_code_line("i_end = float(len(timesheet))")
  s.add_code_line("for i in (1 <= i_end) and upRange(1, i_end, 1) or downRange(1, i_end, 1):")
  s.add_code_line("  if not self._in_loop:")
  s.add_code_line("    return")
  s.add_code_line("  global entry")
  s.add_code_line("  entry = timesheet[int(i - 1)]")
  s.add_code_line("  if i == 1:")
  s.add_code_line("    self.speak_dialog(''' These are your entries ''', wait=True)")
  s.add_code_line("  self.speak(str(pronounce_number((entry[1]))), wait=True)")
  s.add_code_line("  self.speak_dialog(''' minutes past ''', wait=True)")
  s.add_code_line("  self.speak(str(pronounce_number((entry[0]))), wait=True)")
  s.add_code_line("  self.speak(str((entry[2])), wait=True)")
  s.add_code_line("self._in_loop=False")
  s.add_adapt_intent("intent name32")
  s.get_utterance()
  s.add_keyword("whats the time tracking status", samples = [''' what's the time tracking status ''', "whats the time tracking status", "what s the time tracking status"], action="require", intent_name="intent name33")
  s.add_code_line("global entry")
  s.add_code_line("entry = timesheet[-1]")
  s.add_code_line("self.speak_dialog(''' You are currently on ''', wait=True)")
  s.add_code_line("self.speak(str((entry[-1])), wait=True)")
  s.add_adapt_intent("intent name33")
  s.get_utterance()
  s.add_keyword("how long have i worked already", samples = [''' how long have i worked already ''', "how long have i worked already", "how long have i worked already"], action="require", intent_name="intent name34")
  s.add_code_line("self.speak_dialog(''' todo ''', wait=True)")
  s.add_adapt_intent("intent name34")
  s.get_utterance()
  s.add_keyword("how long did i work today", samples = [''' how long did i work today? ''', "how long did i work today", "how long did i work today"], action="require", intent_name="intent name35")
  s.add_code_line("self.speak_dialog(''' todo ''', wait=True)")
  s.add_adapt_intent("intent name35")
  s.get_utterance()
  s.add_keyword("tell me all times", samples = [''' tell me all times ''', "tell me all times", "tell me all times"], action="require", intent_name="intent name36")
  s.add_code_line("self.speak(str(timesheet), wait=True)")
  s.add_adapt_intent("intent name36")
  s.get_utterance()
  s.add_keyword("save timesheet", samples = [''' save timesheet ''', "save timesheet", "save timesheet"], action="require", intent_name="intent name37")
  s.add_code_line("self.saveTimesheet()")
  s.add_code_line("self.speak_dialog(''' saved your timesheet ''', wait=True)")
  s.add_adapt_intent("intent name37")
  s.add_code_line("# Describe this function...")
  s.add_code_line("global entry, currentDateTime, timesheet, exampleParam, currentHour, currentMinute, i")
  s.add_code_line("self.do_pickle(''' someTestName ''',timesheet)")
  s.set_method_with_args(name="saveTimesheet", args={})
  s.add_code_line("# Describe this function...")
  s.add_code_line("global entry, currentDateTime, timesheet, exampleParam, currentHour, currentMinute, i")
  s.add_code_line("self.speak(str(exampleParam), wait=True)")
  s.add_code_line("self.speak(str(currentDateTime), wait=True)")
  s.add_code_line("return ''' example string '''")
  s.set_method_with_args(name="exampleFunction", args={})
  s.build_skill()
