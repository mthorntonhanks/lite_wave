import struct

class wav_file():
    """Represents an individual audio file of type WAVE
    """
    
    def __init__(self):
        self.chunk_id = ''
        self.riff_chunk_size = 0
        self.format = ''

        self._audio_format = 0
        self.num_channels = 0
        self.sample_rate = 0
        self.byte_rate = 0
        self.block_align = 0
        self.bits_per_sample = 0

        self._chunks = {}

        self.byte_order = 'little'

    @property
    def audio_format(self):
        """1 = PCM Linear
        Other values indicate compression methods
        """
        return self._audio_format

    @audio_format.setter
    def audio_format(self, value):
        self._audio_format = value

    @property
    def chunk_ids(self):
        """List of chunk IDs in the order they occur in the file
        """
        return tuple(self._chunks)

    @property
    def byte_sign(self):
        return self.bits_per_sample == 16

    def get_chunk_size(self, id):
        #fmt_: don't allow access to chunk data - use object properties instead
        #data, LIST, etc: get chunk size from private list
        return len(self._chunks[id])

    def get_chunk_data(self, id):
        #data, LIST, etc: get chunk data from private list
        #fmt_: don't allow access to chunk data - use object properties instead
        return self._chunks[id]

    def set_chunk_data(self, id, data):
        """Modify the data bytes of the specified chunk
        """
        self._chunks.update({id: data})

    def get_sample_data(self):
        sample_bytes = self._chunks['data']
        sample_ints = []
        for index in range(0, len(sample_bytes), 2):
            sample = int.from_bytes(sample_bytes[index:index+2], byteorder='little', signed=True)
            sample_ints.append(sample)

        return sample_ints
    
def load(file_name: str) -> wav_file:
    """Loads a wav file from file storage into an object and returns the object

    Parameters
    ----------
    file_name : str
        File name to be loaded from file storage
    
    Returns
    -------
    wav_file
    """

    #Open file
    f = open(file_name, 'rb')

    #Read RIFF ChunkID
    f.seek(0)
    b = f.read(4)

    au_fi = wav_file()
    au_fi.chunk_id = b.decode()

    #Read RIFF chunk size (should equal file_size - 8)
    b = f.read(4)
    t = struct.unpack('<i', b)
    riff_chunk_size = t[0]
    au_fi.riff_chunk_size = riff_chunk_size

    #Running total of bytes processed
    run_total_bytes = 0

    #Read Format
    b = f.read(4)
    run_total_bytes += 4
    au_fi.format = b.decode()

    #Initialise variable-length hash map of sub-chunks
    chunks = {}
    
    #Iterate through sub-chunks
    while run_total_bytes < riff_chunk_size:
        #Read sub-chunk ID
        sub_chunk_id = f.read(4)
        run_total_bytes += 4

        #Read sub-chunk size
        b = f.read(4)
        run_total_bytes += 4
        t = struct.unpack('<i', b)
        sub_chunk_size = t[0]

        if sub_chunk_id == b'data':
            b = f.read(sub_chunk_size)
            run_total_bytes += sub_chunk_size

        elif sub_chunk_id == b'fmt ':
            #Display the audio format
            b = f.read(sub_chunk_size)
            run_total_bytes += sub_chunk_size
            unpack_str = '<hhiihh'
            t = struct.unpack(unpack_str, b[:16])

            au_fi.audio_format = t[0]
            au_fi.num_channels = t[1]
            au_fi.sample_rate = t[2]
            au_fi.byte_rate = t[3]
            au_fi.block_align = t[4]
            au_fi.bits_per_sample = t[5]

        else:
            b = f.read(sub_chunk_size)
            run_total_bytes += sub_chunk_size

        chunks.update({sub_chunk_id.decode(): b})

    au_fi._chunks = chunks
    
    f.close()
    return au_fi

def save(f : wav_file, file_name : str):
    """Saves a wav_file object to a new file on storage

    Parameters
    ----------
    f : wav_file
        Object to be saved as a new file
    file_name : str
        File name of the new file
    
    Returns
    -------
    None
    """

    with open(file_name, 'wb') as file:
        

        #Write Chunk_ID
        file.write(f.chunk_id.encode())

        #Write RIFF chunk size (should equal file_size - 8)
        b = struct.pack('<i', f.riff_chunk_size)
        file.write(b)

        file.write(f.format.encode())

        for id in f.chunk_ids:
            #Write sub-chunk
            file.write(id.encode())
            b = struct.pack('<i', f.get_chunk_size(id))
            file.write(b)

            if id == 'fmt ':
                b = struct.pack('<hhiihh', f.audio_format, f.num_channels, f.sample_rate, f.byte_rate, f.block_align, f.bits_per_sample)
                file.write(b)

                #If sub-chunk is more than the standard 16 bytes, write the remaining bytes
                if f.get_chunk_size(id) > 16:
                    file.write(f.get_chunk_data(id)[16:])
            else:
                file.write(f.get_chunk_data(id))
