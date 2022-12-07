import lite_wave as lw

print('=' * 60, '''
Test manipulating the 'data' chunk - e.g. change the amplitude / volume of samples,
whilst keeping same format (i.e. bit resolution, sample rate etc)
''')

#Load file from storage into an object
file_name = 'samples/09 Track 9.wav'
f = lw.load(file_name)

run_count = 0
failed_tests = list()

#Modify data chunk
data = f.get_chunk_data('data')
data_mod = bytearray(data)
for index in range(0, len(data_mod), 2):
    #Modify amplitude of this sample to 25%
    sample = int.from_bytes(data_mod[index:index+2], byteorder='little', signed=True)
    sample //= 4
    data_mod[index:index+2] = int.to_bytes(sample, 2, byteorder='little', signed=True)
    #if not index % 100000:
        #print('{:.1f}%'.format(index / len(data_mod) * 100))

f.set_chunk_data('data', data_mod)

#Save file as a new file
new_file_name = 'samples/09 Track 9_new.wav'
run_count += 1
lw.save(f, new_file_name)

#Load and verify the new file
run_count += 1
f_new = lw.load(new_file_name)

failure = None
if f_new.audio_format != f.audio_format:
    failure = 'audio_format'
if f_new.bits_per_sample != f.bits_per_sample:
    failure = 'bits_per_sample'
if f_new.block_align != f.block_align:
    failure = 'block_align'
if f_new.byte_rate != f.byte_rate:
    failure = 'byte_rate'
if f_new.chunk_id != f.chunk_id:
    failure = 'chunk_id'
if f_new.chunk_ids != f.chunk_ids:
    failure = 'chunk_ids'
if f_new.format != f.format:
    failure = 'chunk_ids'
if f_new.get_chunk_data('LIST') != f.get_chunk_data('LIST'):
    failure = "get_chunk_data('LIST')"
if f_new.get_chunk_size('fmt ') != f.get_chunk_size('fmt '):
    failure = "get_chunk_size('fmt ')"
if f_new.num_channels != f.num_channels:
    failure = 'num_channels'
if f_new.riff_chunk_size != f.riff_chunk_size:
    failure = 'riff_chunk_size'
if f_new.sample_rate != f.sample_rate:
    failure = 'sample_rate'
run_count += 1
if failure is not None:
    failed_tests.append(f'010 | {failure}')

data_new = f_new.get_chunk_data('data')
for index in range(0, len(data), 2):
    sample = int.from_bytes(data[index:index+2], byteorder='little', signed=True)
    sample_new = int.from_bytes(data_new[index:index+2], byteorder='little', signed=True)
    if sample_new != sample // 4:
        failed_tests.append('020')
        break

print(f'Tests run: {run_count}, tests passed: {run_count - len(failed_tests)}')
if len(failed_tests) > 0:
    print(f'Failed tests: {failed_tests}')
input('Press Enter to finish..')
