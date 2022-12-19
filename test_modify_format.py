import lite_wave as lw

print('=' * 60, '''
Run test(s) to modify a file's format, but not its sample data
''')

#Load file from storage into an object
file_name = 'samples/09 Track 9.wav'
f = lw.load(file_name)

run_count = 0
failed_tests = list()

#Modify the file's format as follows:
#1. Modify from stereo to mono. This will cause the pitch to reduce by 50%
#2. Double the sample rate. This will restore the pitch :)
f.num_channels = 1
f.block_align = 2
f.sample_rate *= 2
f.byte_rate = f.sample_rate * f.block_align

#Save file as a new file
new_file_name = 'samples/09 Track 9_new.wav'
run_count += 1
lw.save(f, new_file_name)

print(f'Tests run: {run_count}, tests passed: {run_count - len(failed_tests)}')
if len(failed_tests) > 0:
    print(f'Failed tests: {failed_tests}')
input('Press Enter to finish..')
