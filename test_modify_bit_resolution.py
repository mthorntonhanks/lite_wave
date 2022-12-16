import lite_wave as lw

print('=' * 60, '''
Test modifying a file from 16-bit samples to 8-bit samples
''')

run_count = 0
failed_tests = list()

#Load file from storage into an object
file_name = 'samples/09 Track 9.wav'
f = lw.load(file_name)

#Method 1: Get / modify / update samples as bytes
data = f.get_chunk_data('data')
data_mod = bytearray(len(data) // 2)
factor = 2 ** 16 / 2 ** 8
for byt in range(0, len(data), 2):
    #Modify this 16-bit sample to an 8-bit sample
    sample = int.from_bytes(data[byt:byt+2], byteorder='little', signed=True)
    sample += 32768
    sample = int(sample / factor)
    data_mod[int(byt /2)] = sample #int.to_bytes(sample, 1, 'little')

#f.set_chunk_data('data', data_mod)
f.bits_per_sample = 8
f.set_sample_data(data_mod)

#Modify bits per sample, byte_rate, block_align, riff_chunk_size
#(Alternatively, wav_file could provide method/s for re-calculating byte rate, block_align and riff_chunk_size)
f.bits_per_sample = 8
f.byte_rate = int(f.byte_rate / 2)
f.block_align = int(f.block_align / 2)
f.riff_chunk_size = 1599784

#Save file as a new file
new_file_name = 'samples/09 Track 9_new.wav'
lw.save(f, new_file_name)

#Load and verify the new file
run_count += 1
f_new = lw.load(new_file_name)

'''
Original values
===============
f.riff_chunk_size = (file size - 8)
                    = (4 + 4 + 4 + fmt size + 4 + 4 + data size + 4 + 4 + sub chunk 3 size) = 3199144
                    = (4 + 4 + 4 + 18       + 4 + 4 + 3198720   + 4 + 4 + 378             ) = 3199144
f.sample_rate = 44100
f.byte_rate = 176400
f.block_align = 4
f.bits_per_sample = 16
f.get_chunk_size('fmt ') = 18
f.get_chunk_size('data') = 3198720
f.get_chunk_size('LIST') = 378

Expected values
===============
f.riff_chunk_size = (file size - 8)
                    = (4 + 4 + 4 + fmt size + 4 + 4 + data size + 4 + 4 + sub chunk 3 size) = 3199144
                    = (4 + 4 + 4 + 18       + 4 + 4 + 1599360   + 4 + 4 + 378             ) = 1599784
f.sample_rate = 44100
f.byte_rate = 88200
f.block_align = 2
f.bits_per_sample = 8
f.get_chunk_size('fmt ') = 18
f.get_chunk_size('data') = 3198720 / 2 = 1599360
f.get_chunk_size('LIST') = 378
'''

failure = None
if f_new.chunk_id != f.chunk_id:
    failure = 'chunk_id'
if f_new.riff_chunk_size != 1599784:
    failure = 'riff_chunk_size'
if f_new.format != f.format:
    failure = 'format'
if f_new.get_chunk_size('fmt ') != 18:
    failure = "get_chunk_size('fmt ')"
if f_new.audio_format != f.audio_format:
    failure = 'audio_format'
if f_new.num_channels != f.num_channels:
    failure = 'num_channels'
if f_new.sample_rate != f.sample_rate:
    failure = 'sample_rate'
if f_new.byte_rate != 88200:
    failure = 'byte_rate'
if f_new.block_align != 2:
    failure = 'block_align'
if f_new.bits_per_sample != 8:
    failure = 'bits_per_sample'
if f_new.get_chunk_size('data') != 1599360:
    failure = "get_chunk_size('data')"
if f_new.chunk_ids != f.chunk_ids:
    failure = 'chunk_ids'
if f_new.get_chunk_data('LIST') != f.get_chunk_data('LIST'):
    failure = "get_chunk_data('LIST')"
if failure is not None:
    failed_tests.append(f'010 | {failure}')

#Verify the data samples
data_new = f_new.get_sample_data()
for sample in range(len(data_new)):
    if data_new[sample] != data_mod[sample]:
        failed_tests.append(f'020')
        break
run_count += 1

print(f'Tests run: {run_count}, tests passed: {run_count - len(failed_tests)}')
if len(failed_tests) > 0:
    print(f'Failed tests: {failed_tests}')
input('Press Enter to finish..')
