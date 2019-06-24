from subprocess import Popen, PIPE, time

scpt = '''
tell application "System Events"
	keystroke "%" using command down
	delay 1.0
	keystroke return
end tell'''


args = ['2', '2']


p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
stdout, stderr = p.communicate(scpt)
recording_time = time.time()
print ("screen recording...", recording_time)
