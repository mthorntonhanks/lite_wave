'''
No need to write lots of tests with different files..
Write a new test when a defect occurs
'''

import os
import lite_wave as lw

run_count = 0
failed_tests = list()

print('=' * 60, '''
Test a file can be loaded from storage into an object and its properties read
''')

file_name = 'samples/windows_ding.wav'

#Load file from storage into an object
f = lw.load(file_name)

run_count += 1
if f.chunk_id != 'RIFF':
    failed_tests.append('010')

run_count += 1
if f.riff_chunk_size != 101088:
    failed_tests.append('020')

#RIFF chunk size should equal (file size - 8)
run_count += 1
if f.riff_chunk_size != os.stat(file_name).st_size - 8:
    failed_tests.append('030')
    
run_count += 1
if f.format != 'WAVE':
    failed_tests.append('040')

run_count += 1
#if f.sub_chunk_ids[0] != 'fmt ':
if f.chunk_ids[0] != 'fmt ':
    failed_tests.append('050')
    
run_count += 1
if f.audio_format != 1:
    failed_tests.append('060')

run_count += 1
if f.num_channels != 2:
    failed_tests.append('070')

run_count += 1
if f.sample_rate != 44100:
    failed_tests.append('080')

run_count += 1
if f.byte_rate != 176400:
    failed_tests.append('090')

run_count += 1
if f.block_align != 4:
    failed_tests.append('100')

run_count += 1
if f.bits_per_sample != 16:
    failed_tests.append('110')

run_count += 1
#if f.sub_chunk_ids[1] != 'data':
if f.chunk_ids[1] != 'data':
    failed_tests.append('120')

run_count += 1
#if f.sub_chunk_sizes[1] != 100980:
if f.get_chunk_size('data') != 100980:
    failed_tests.append('130')

run_count += 1
if f.chunk_ids[2] != 'LIST':
    failed_tests.append('140')

run_count += 1
if f.get_chunk_size('LIST') != 64:
    failed_tests.append('150')

#RIFF chunk size should equal:
#  4 + 4 + 4 + fmt size + 4 + 4 + data size + 4 + 4 + sub chunk 3 size
run_count += 1
if not (f.riff_chunk_size == 12 + f.get_chunk_size('fmt ') + 8 + f.get_chunk_size('data') + 8 + f.get_chunk_size('LIST')):
    failed_tests.append('160')

file_name = 'samples/09 track 9.wav'

#Load file from storage into an object
f = lw.load(file_name)

run_count += 1
if f.chunk_id != 'RIFF':
    failed_tests.append('200')

run_count += 1
if f.riff_chunk_size != 3199144:
    failed_tests.append('210')

#RIFF chunk size should equal (file size - 8)
run_count += 1
if f.riff_chunk_size != os.stat(file_name).st_size - 8:
    failed_tests.append('220')
    
run_count += 1
if f.format != 'WAVE':
    failed_tests.append('230')

run_count += 1
if f.chunk_ids[0] != 'LIST':
    failed_tests.append('240')

run_count += 1
if f.get_chunk_size('LIST') != 378:
    failed_tests.append('250')

run_count += 1
if f.chunk_ids[1] != 'fmt ':
    failed_tests.append('270')
    
run_count += 1
if f.audio_format != 1:
    failed_tests.append('280')

run_count += 1
if f.num_channels != 2:
    failed_tests.append('290')

run_count += 1
if f.sample_rate != 44100:
    failed_tests.append('300')

run_count += 1
if f.byte_rate != 176400:
    failed_tests.append('310')

run_count += 1
if f.block_align != 4:
    failed_tests.append('320')

run_count += 1
if f.bits_per_sample != 16:
    failed_tests.append('330')

run_count += 1
if f.chunk_ids[2] != 'data':
    failed_tests.append('340')

run_count += 1
if f.get_chunk_size('data') != 3198720:
    failed_tests.append('350')

#RIFF chunk size should equal:
#  4 + 4 + 4 + fmt size + 4 + 4 + data size + 4 + 4 + sub chunk 3 size
run_count += 1
if not (f.riff_chunk_size == 12 + f.get_chunk_size('fmt ') + 8 + f.get_chunk_size('data') + 8 + f.get_chunk_size('LIST')):
    failed_tests.append('360')

print(f'Tests run: {run_count}, tests passed: {run_count - len(failed_tests)}')
print(f'Failed tests: {failed_tests}')
input('Press Enter to finish..')
