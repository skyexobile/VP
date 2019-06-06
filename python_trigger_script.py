from subprocess import Popen, PIPE

scpt = '''
tell application "System Events"
	keystroke "%" using command down
	delay 1.0
	keystroke return
end tell'''


args = ['2', '2']


p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
stdout, stderr = p.communicate(scpt)

print (p.returncode, stdout, stderr)
