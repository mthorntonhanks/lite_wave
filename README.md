# Introduction
lite_wave is a Python module for reading and writing sound files in the WAVE format.

It is intended as a stable, easy-to-use building block for manipulating wav files, without needing to know how to load a file from disk / storage, or to save a file to storage. 

We encourage contributions and enhancements which:
 - make it easier for client code to work with wav_file objects
 - fix bugs
 - improve the performance or efficiency

We are not looking for contributions which 'bloat' the module beyond its basic purpose of ***reading and writing wav files***. It's the job of the user / developer to write their own modules to do funky sound manipulations :)

# Usage
Below are some examples of things you can do using lite_wave. You can also find example code in the automated test scripts (test_*.py). 


## Read a wav file to discover its parameters
For example, discover the sample rate, bit rate, duration, and so on.
```
import lite_wave as lw
f = lw.load('sound_file.wav')
print(f'sample rate: {f.sample_rate}')
```

## Manipulate the parameters of a wav file and save as a new file
For example, increase or decrease the sample rate
```
f = lw.load('original.wav')
f.sample_rate *= 2
f.byte_rate *= 2
lw.save(f, 'modified.wav')
```

## Manipulate the sound samples
For example, reverse the sound or do whatever funky manipulations you can think of :)
```
f = lw.load('original.wav')
samples = f.get_chunk_data('data')
new_samples = my_func_to_manipulate_samples(samples)
f.set_chunk_data('data', new_samples)
lw.save(f, 'modified.wav')
```
In the above code, *samples* and *new_samples* are byte arrays. Alternatively, integer arrays can be used with methods *get_sample_data* and *set_sample_data*. As follows:
```
samples = f.get_sample_data()
new_samples = my_func_to_manipulate_samples(samples)
f.set_sample_data(new_samples)
```

## Create a wav file from scratch
```
f = lw.wav_file()
f.bits_per_sample = 8
f.sample_rate = 44100
#and so on..
lw.save(f, 'new.wav')
```
