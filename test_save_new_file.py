import lite_wave as lw
import filecmp

print('=' * 60, '''
Test that a file can be saved as a new file
''')

#Load file from storage into an object
file_name = 'samples/windows_ding.wav'
f = lw.load(file_name)

run_count = 0
failed_tests = list()

#Save file as a new file
new_file_name = 'samples/windows_ding_new.wav'
run_count += 1
lw.save(f, new_file_name)

#Compare both files in storage and check they match exactly
run_count += 1
if not filecmp.cmp(file_name, new_file_name):
    failed_tests.append('020')

print(f'Tests run: {run_count}, tests passed: {run_count - len(failed_tests)}')
if len(failed_tests) > 0:
    print(f'Failed tests: {failed_tests}')
input('Press Enter to finish..')
