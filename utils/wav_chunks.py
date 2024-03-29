from matplotlib import pyplot as plt
import scipy.fft
import struct
import audioop
import numpy as np

Optional, index, tab, unrecognizedChunk, data = {}, 1, [], [], []


class Chunk:
    def __init__(self, id: str, size: int, data=None):
        self.id = id
        self.size = size
        self.data = data

    def __repr__(self):
        return str(self.id) + " - " + str(self.size)  # + " - " + str(self.data)

    def __str__(self):
        return f"Chunk ID: {self.id} Chunk size: {self.size}"

    pass

    def write(self, file):
        try:
            file.write(self.id.encode(encoding='utf-8'))
            file.write(self.size.to_bytes(4, byteorder="little", signed=True))
        except Exception:
            pass


class RIFFHeader(Chunk):
    class Contents:
        format: str

        def __init__(self, data: list):
            self.format = data[0]

        def __repr__(self):
            return f"\n\tFile format: {self.format}\n"

        pass

        def write(self, file):
            try:
                file.write(self.format.encode(encoding='utf-8'))
            except Exception:
                pass

    data: Contents

    def __init__(self, id: str, size: int, data: list):
        Chunk.__init__(self=self, id=id, size=size, data=None)
        self.data = RIFFHeader.Contents(data)

    def __repr__(self):
        return Chunk.__repr__(self) + "\n" + str(self.data)

    def __str__(self):
        return Chunk.__str__(self) + str(self.data)
    pass

    def write(self, file=None):
        Chunk.write(self, file)
        self.data.write(file)


class FmtChunk(Chunk):
    class Contents:
        audio_format: int
        num_channels: int
        sample_rate: int
        byte_rate: int
        block_align: int
        bits_per_sample: int
        num_extra_format_bytes: int
        extra_format_bytes: int

        def __init__(self, data: list):
            self.audio_format = data[0]
            self.num_channels = data[1]
            self.sample_rate = data[2]
            self.byte_rate = data[3]
            self.block_align = data[4]
            self.bits_per_sample = data[5]
            if data.index(data[-1]) > 5:
                self.num_extra_format_bytes = data[6]
                self.extra_format_bytes = data[7]

        def __repr__(self):
            list = str(self.audio_format) + " - " + str(self.num_channels) + " - " + str(self.sample_rate) + \
                   " - " + str(self.byte_rate) + " - " + str(self.block_align) + " - " + str(self.bits_per_sample)
            if data.index(data[-1]) > 5:
                list += " - " + str(self.num_extra_format_bytes) + " - " + str(self.extra_format_bytes)
            return list

        def __str__(self):
            ret = f"\t\tAudio format: {self.audio_format}"
            ret += f"\n\t\tNumber of channels: {self.num_channels}"
            ret += f"\n\t\tSample rate: {self.sample_rate}"
            ret += f"\n\t\tByte rate: {self.byte_rate}"
            ret += f"\n\t\tBlock align: {self.block_align}"
            ret += f"\n\t\tBits per sample: {self.bits_per_sample}"
            if len(data) > 5:
                ret += f"\n\t\tNumber of extra format bytes {self.num_extra_format_bytes}"
                ret += f"\n\t\tExtra format bytes {self.extra_format_bytes}"
            ret += "\n"
            return ret

        pass

        def write(self, file):
            try:
                file.write(self.audio_format.to_bytes(2, byteorder="little", signed=True))
                file.write(self.num_channels.to_bytes(2, byteorder="little", signed=True))
                file.write(self.sample_rate.to_bytes(4, byteorder="little", signed=True))
                file.write(self.byte_rate.to_bytes(4, byteorder="little", signed=True))
                file.write(self.block_align.to_bytes(2, byteorder="little", signed=True))
                file.write(self.bits_per_sample.to_bytes(2, byteorder="little", signed=True))
                try:
                    file.write(self.num_extra_format_bytes.to_bytes(2, byteorder="little", signed=True))
                    file.write(
                        self.extra_format_bytes.to_bytes(self.data.num_extra_format_bytes + 1, byteorder="little",
                                                         signed=True))
                    file.seek(-1, np.os.SEEK_END)
                    file.truncate()
                except Exception:
                    pass
            except Exception:
                pass

    data: Contents

    def __init__(self, id: str, size: int, data: list):
        Chunk.__init__(self=self, id=id, size=size, data=None)
        self.data = FmtChunk.Contents(data)

    def __repr__(self):
        return Chunk.__repr__(self) + "\n" + str(self.data)

    def __str__(self):
        return f"\t" + Chunk.__str__(self) + "\n" + str(self.data)


    pass

    def write(self, file=None):
        Chunk.write(self, file)
        self.data.write(file)


class factChunk(Chunk):
    class Contents:
        data: int

        def __init__(self, data: int):
            self.data = data

        def __repr__(self):
            return f"\n\t\tData: {self.data}\n"

        pass

        def write(self, file):
            try:
                file.write(self.data.to_bytes(4, byteorder="little", signed=True))
            except Exception:
                pass
    data: Contents

    def __init__(self, id: str, size: int, data: list):
        Chunk.__init__(self=self, id=id, size=size, data=None)
        self.data = factChunk.Contents(int.from_bytes(data[0], byteorder="little"))

    def __repr__(self):
        return Chunk.__repr__(self) + " - " + str(self.data)

    def __str__(self):
        return "\t" + Chunk.__str__(self) + str(self.data)
    pass

    def write(self, file):
        Chunk.write(self, file)
        self.data.write(file)


class INFOsubChunk(Chunk):
    class Contents:
        data: str

        def __init__(self, data: str):
            self.data = data

        def __repr__(self):
            return f"\t\t\t\tData: {self.data}\n"

        pass

        def write(self, file):
            try:
                file.write(self.data.encode(encoding="utf-8"))
            except Exception:
                pass
    data: Contents

    def __init__(self, id: str, size: int, data: list):
        Chunk.__init__(self=self, id=id, size=size, data=None)
        self.data = INFOsubChunk.Contents(bytes.decode(data[:]))

    def __repr__(self):
        return Chunk.__repr__(self) + " - " + str(self.data)

    def __str__(self):
        return f"\t\t\t" + Chunk.__str__(self) + "\n" + str(self.data)
    pass

    def write(self, file):
        Chunk.write(self, file)
        self.data.write(file)


class INFOChunk(Chunk):
    class Contents:
        IART: INFOsubChunk          # wykonawca
        INAM: INFOsubChunk          # tytuł utworu
        IPRD: INFOsubChunk          # tytuł albumu
        ICRD: INFOsubChunk          # data wydania
        IGNR: INFOsubChunk          # gatunek
        ICMT: INFOsubChunk          # komentarze
        ITRK: INFOsubChunk          # komentarze
        ISFT: INFOsubChunk          # oprogramowanie
        unrecognized = []           # nierozpoznany

        def __repr__(self):
            list = ""
            try:
                list += str(self.IART)
            except AttributeError:
                pass
            try:
                list += str(self.INAM)
            except AttributeError:
                pass
            try:
                list += str(self.IPRD)
            except AttributeError:
                pass
            try:
                list += str(self.ICRD)
            except AttributeError:
                pass
            try:
                list += str(self.IGNR)
            except AttributeError:
                pass
            try:
                list += str(self.ICMT)
            except AttributeError:
                pass
            try:
                list += str(self.ITRK)
            except AttributeError:
                pass
            try:
                list += str(self.ISFT)
            except AttributeError:
                pass
            try:
                for unrecognized in self.unrecognized:
                    try:
                        list += "\t\t\tNierozpoznany:\n"
                        list += str(unrecognized)
                    except Exception:
                        pass
            except Exception:
                pass
            return list

        def write(self, file):
            try:
                if 'INAM' in tab:
                    self.INAM.write(file)
            except AttributeError:
                pass
            try:
                if 'IPRD' in tab:
                    self.IPRD.write(file)
            except AttributeError:
                pass
            try:
                if 'IART' in tab:
                    self.IART.write(file)
            except AttributeError:
                pass
            try:
                if 'ICMT' in tab:
                    self.ICMT.write(file)
            except AttributeError:
                pass
            try:
                if 'ICRD' in tab:
                   self.ICRD.write(file)
            except AttributeError:
                pass
            try:
                if 'IGNR' in tab:
                    self.IGNR.write(file)
            except AttributeError:
                pass
            try:
                if 'ITRK' in tab:
                   self.ITRK.write(file)
            except AttributeError:
                pass
            try:
                if 'ISFT' in tab:
                    self.ISFT.write(file)
            except AttributeError:
                pass

    data: Contents

    def __init__(self, id: str, size: int, data: list):
        global index
        Chunk.__init__(self=self, id=id, size=size, data=None)
        self.data = INFOChunk.Contents()
        start = 0
        while start < len(data) - 1:
            subid = bytes.decode(data[start:start + 4])
            if len(subid):
                sizesubid = int.from_bytes(data[start + 4:start + 8], byteorder="little")
            if subid in self.Contents.__annotations__:
                exec(
                    "%s=%s" % ('self.data.' + subid, "INFOsubChunk(subid, sizesubid, data[start+8:start+sizesubid+8])"))
                Optional.update({index: subid})
                index += 1
            else:
                self.data.unrecognized.append(INFOsubChunk(subid, sizesubid, data[start + 8:start + sizesubid + 8]))
            start = start + sizesubid + 8

        if len(data) > 4 + start:
            self.data.unrecognized.append(INFOsubChunk(bytes.decode(data[start:start + 4]), len(data[start + 4:]), data[start + 4:]))

    def __repr__(self):
        return Chunk.__repr__(self) + "\n" + str(self.data)

    def __str__(self):
        return f"\t\t" + Chunk.__str__(self) + "\n" + str(self.data)
    pass

    def write(self, file):
        file.write(self.id.encode(encoding='utf-8'))
        self.data.write(file)


class CuesubChunk:
    class Contents:
        ID: str
        position: int
        data_chunk_ID: str
        chunk_start: int
        block_start: int
        sample_offset: int

        def __init__(self, data: list):
            self.ID = data[0]
            self.position = data[1]
            self.data_chunk_ID = data[2]
            self.chunk_start = data[3]
            self.block_start = data[4]
            self.sample_offset = data[5]

        def __repr__(self):
            list = str(self.ID) + " - " + str(self.position) + " - " + str(self.data_chunk_ID) + \
                   " - " + str(self.chunk_start) + " - " + str(self.block_start) + " - " + str(self.sample_offset)
            return list

        def __str__(self):
            ret = f"\t\tID: {self.ID}"
            ret += f"\n\t\tPosition: {self.position}"
            ret += f"\n\t\tData Chunk ID: {self.data_chunk_ID}"
            ret += f"\n\t\tChunk Start: {self.chunk_start}"
            ret += f"\n\t\tBlock Start: {self.block_start}"
            ret += f"\n\t\tSample Offset: {self.sample_offset}\n\n"
            return ret

        pass

        def write(self, file):
            try:
                file.write(self.ID.encode(encoding='utf-8'))
                file.write(self.position.to_bytes(4, byteorder="little", signed=True))
                file.write(self.data_chunk_ID.encode(encoding='utf-8'))
                file.write(self.chunk_start.to_bytes(4, byteorder="little", signed=True))
                file.write(self.block_start.to_bytes(4, byteorder="little", signed=True))
                file.write(self.sample_offset.to_bytes(4, byteorder="little", signed=True))
            except Exception:
                pass

    data: Contents

    def __init__(self, data: list):
        self.data = CuesubChunk.Contents(data)

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)

    pass

    def write(self, file=None):
        self.data.write(file)


class CueChunk(Chunk):
    class Contents:
        numPoints: int
        #Points: list[CuesubChunk]

        def __init__(self, numPoints: int):
            self.numPoints = numPoints

        def __repr__(self):
            list = "\t\tnumber of Points: " + str(self.numPoints) + "\n"
            for cue in self.Points:
                try:
                    list += str(cue)
                except AttributeError:
                    pass
            return list

        def write(self, file):
            file.write(self.numPoints.to_bytes(4, byteorder="little", signed=True))
            for cue in self.Points:
                try:
                    cue.write(file)
                except AttributeError:
                    pass

    data: Contents

    def __init__(self, id: str, size: int, data: list):
        global index
        Chunk.__init__(self=self, id=id, size=size, data=None)
        data = data[0]
        numPoints = int.from_bytes(data[:4], byteorder="little")
        self.data = CueChunk.Contents(numPoints)
        for start in range(numPoints):
            point = []
            for i in range(6):
                if start*24+i*4+8 > size:
                    print("Wrong format of point.")
                    break
                point.append(int.from_bytes(data[start*24+i*4+4:start*24+i*4+8], byteorder="little"))

            if len(point) == 6:
                self.data.Points.append(CuesubChunk(point))
            else:
                pass

    def __repr__(self):
        return Chunk.__repr__(self) + "\n" + str(self.data)

    def __str__(self):
        return "\t" + Chunk.__str__(self) + "\n" + str(self.data)

    pass

    def write(self, file):
        Chunk.write(self, file)
        self.data.write(file)


class ADTLsubChunk(Chunk):
    class Contents:
        cueID: str
        sample: str
        purpouse: str
        country: str
        lang: str
        dial: str
        code: str
        data: str

        def __init__(self, cueID: str, data: str, sample: str = None, purpouse: str = None, country: str = None,
                     lang: str = None, dial: str = None, code: str = None):
            self.cueID = cueID
            self.sample = sample
            self.purpouse = purpouse
            self.country = country
            self.lang = lang
            self.dial = dial
            self.code = code
            self.data = data

        def __repr__(self):
            return str(self.cueID) + " - " + str(self.data)

        def __str__(self):
            ret = f"\t\t\t\tCue Point ID: {self.cueID}"
            try:
                ret += f"\n\t\t\t\tSample Length: {self.sample}"
                ret += f"\n\t\t\t\tPurpose ID: {self.purpouse}"
                ret += f"\n\t\t\t\tCountry: {self.country}"
                ret += f"\n\t\t\t\tLanguage: {self.lang}"
                ret += f"\n\t\t\t\tDialect: {self.dial}"
                ret += f"\n\t\t\t\tCode Page: {self.code}"
            except Exception:
                pass
            ret += f"\n\t\t\t\tData: {self.data}\n"
            return ret

        pass

        def write(self, file, id):
            try:
                file.write(self.cueID.encode(encoding="utf-8"))
                if id == "itxt":
                    file.write(self.cueID.encode(encoding="utf-8"))
                    file.write(self.sample.encode(encoding="utf-8"))
                    file.write(self.purpouse.encode(encoding="utf-8"))
                    file.write(self.country.encode(encoding="utf-8"))
                    file.write(self.lang.encode(encoding="utf-8"))
                    file.write(self.dial.encode(encoding="utf-8"))
                    file.write(self.code.encode(encoding="utf-8"))

                file.write(self.data.encode(encoding="utf-8"))
            except Exception:
                pass

    data: Contents

    def __init__(self, id: str, size: int, cueID: str, data: list):
        Chunk.__init__(self=self, id=id, size=size, data=None)
        if id != "ltxt":
            self.data = ADTLsubChunk.Contents(cueID, bytes.decode(data[:]))
        else:
            self.data = ADTLsubChunk.Contents(cueID, bytes.decode(data[16:]), bytes.decode(data[:4]),
                                              bytes.decode(data[4:8]), bytes.decode(data[8:10]),
                                              bytes.decode(data[10:12]), bytes.decode(data[12:14]),
                                              bytes.decode(data[14:16]))

    def __repr__(self):
        return Chunk.__repr__(self) + " - " + str(self.data)

    def __str__(self):
        return f"\t\t\t" + Chunk.__str__(self) + "\n" + str(self.data)
    pass

    def write(self, file):
        Chunk.write(self, file)
        self.data.write(file, self.id)


class ADTLChunk(Chunk):
    class Contents:
        labl: ADTLsubChunk          # nazwy znaczników (cue)
        note: ADTLsubChunk          # opisy znaczników (cue)
        ltxt: ADTLsubChunk          # informacje dodatkowe znaczników (cue)
        unrecognized = []           # nierozpoznany

        def __repr__(self):
            list = ""
            try:
                list += str(self.labl)
            except AttributeError:
                pass
            try:
                list += str(self.note)
            except AttributeError:
                pass
            try:
                list += str(self.ltxt)
            except AttributeError:
                pass
            try:
                for unrecognized in self.unrecognized:
                    try:
                        list += "\t\t\tNierozpoznany:\n"
                        list += str(unrecognized)
                    except Exception:
                        pass
            except Exception:
                pass
            return list

        def write(self, file):
            try:
                if 'labl' in tab:
                    self.labl.write(file)
            except AttributeError:
                pass
            try:
                if 'note' in tab:
                    self.note.write(file)
            except AttributeError:
                pass
            try:
                if 'ltxt' in tab:
                    self.ltxt.write(file)
            except AttributeError:
                pass

    data: Contents

    def __init__(self, id: str, size: int, data: list):
        global index
        Chunk.__init__(self=self, id=id, size=size, data=None)
        self.data = ADTLChunk.Contents()
        start = 0
        while start < len(data) - 1:
            subid = bytes.decode(data[start:start + 4])
            if len(subid):
                sizesubid = int.from_bytes(data[start + 4:start + 8], byteorder="little")
                cueID = bytes.decode(data[start + 8:start + 12])
            if subid in self.Contents.__annotations__:
                exec("%s=%s" % (
                    'self.data.' + subid, "ADTLsubChunk(subid, sizesubid, cueID, data[start+12:start+sizesubid+12])"))
                Optional.update({index: subid})
                index += 1
            else:
                self.data.unrecognized.append(ADTLsubChunk(subid, sizesubid, cueID, data[start + 12:start + sizesubid + 12]))
            start = start + sizesubid + 8

        if len(data) > 4 + start:
            self.data.unrecognized.append(ADTLsubChunk(bytes.decode(data[start:start + 4]), len(data[start + 4:]), "",
                                                  data[start + 4:]))

    def __repr__(self):
        return Chunk.__repr__(self) + "\n" + str(self.data)

    def __str__(self):
        return f"\t\t" + Chunk.__str__(self) + "\n" + str(self.data)
    pass

    def write(self, file):
        file.write(self.id.encode(encoding='utf-8'))
        self.data.write(file)


class LISTChunk(Chunk):
    class Contents:
        INFO: INFOChunk             # informacje o utworze
        adtl: ADTLChunk             # informacje o znacznikach w utworze
        unrecognized = []           # nierozpoznany

        def __repr__(self):
            list = ""
            try:
                list += str(self.INFO)
            except AttributeError:
                pass
            try:
                list += str(self.adtl)
            except AttributeError:
                pass
            try:
                for unrecognized in self.unrecognized:
                    try:
                        list += "\t\tNierozpoznany:\n"
                        list += str(unrecognized)
                    except Exception:
                        pass
            except Exception:
                pass
            return list

        pass

        def write(self, file):
            try:
                if 'INFO' in tab:
                    self.INFO.write(file)
            except Exception:
                pass
            try:
                if 'adtl' in tab:
                    self.adtl.write(file)
            except Exception:
                pass

    data: Contents

    def __init__(self, id: str, size: int, data: [bytes, int]):
        global index
        Chunk.__init__(self=self, id=id, size=size, data=None)
        self.data = LISTChunk.Contents()
        start = 0
        while start < data.index(data[-1]):
            subid = bytes.decode(data[start:start + 4])
            if subid == "INFO":
                self.data.INFO = INFOChunk(subid, len(data[start + 4:start + size]), data[start + 4:start + size])
                Optional.update({index: self.data.INFO.id})
                index += 1
            elif subid == "adtl":
                self.data.adtl = ADTLChunk(subid, len(data[start + 4:start + size]), data[start + 4:start + size])
                Optional.update({index: self.data.adtl.id})
                index += 1
            else:
                self.data.unrecognized.append(INFOsubChunk(subid, len(data[start + 4:start + size]), data[start + 4:start + size]))
            start = start + size

        if len(data) > 4 + start:
            self.data.unrecognized.append(INFOsubChunk(bytes.decode(data[start:start + 4]), len(data[start + 4:]), data[start + 4:]))

    def __repr__(self):
        return Chunk.__repr__(self) + "\n" + str(self.data)

    def __str__(self):
        return f"\t" + Chunk.__str__(self) + "\n" + str(self.data)
    pass

    def write(self, file):
        self.size = 0
        if "INFO" in tab:
            for field in tab:
                if tab.index(field) < tab.index("INFO") and field in self.data.INFO.Contents.__annotations__:
                    exec("self.size += self.data.INFO.data.%s.size + 8" % field)
        if self.size > 0:
            self.size += 4
        tmp = self.size
        if "adtl" in tab:
            for field in tab:
                if tab.index(field) < tab.index("adtl") and field in self.data.adtl.Contents.__annotations__:
                    exec("self.size += self.data.adtl.data.%s.size + 8" % field)
        if self.size > tmp:
            self.size += 4
        Chunk.write(self, file)
        self.data.write(file)


class DataChunk(Chunk):
    class Contents:
        samples: list

        def __init__(self, data: list):
            self.samples = data

        def __repr__(self):
            return str(self.samples)

        pass

        @staticmethod
        def bytes_to_channels(fmtChunk: FmtChunk, raw_samples: bytes, size) -> list:
            if int(fmtChunk.data.bits_per_sample / 8) > 0:
                sample_len = int(fmtChunk.data.bits_per_sample / 8)
            else:
                sample_len = 0

            samples = []

            if sample_len > 0:
                for i in range(int(size / sample_len)):
                    sample = raw_samples[i * sample_len:i * sample_len + sample_len]
                    if fmtChunk.data.audio_format == 1:
                        if sample_len == 1:
                            converted_sample = int.from_bytes(sample, byteorder="little", signed=False)
                        else:
                            converted_sample = int.from_bytes(sample, byteorder="little", signed=True)
                    elif fmtChunk.data.audio_format == 3:
                        if sample_len == 4:
                            converted_sample = struct.unpack("f", sample)[0]
                        else:
                            converted_sample = struct.unpack("d", sample)[0]
                    elif fmtChunk.data.audio_format == 6:
                        converted_sample = int.from_bytes(audioop.alaw2lin(sample, sample_len), byteorder="little",
                                                          signed=True)
                    elif fmtChunk.data.audio_format == 7:
                        converted_sample = int.from_bytes(audioop.ulaw2lin(sample, sample_len), byteorder="little",
                                                          signed=True)
                    else:
                        print("Format zapisu danych w pliku nie jest wspierany")
                        raise Exception
                    samples.append(converted_sample)
            else:
                if fmtChunk.data.audio_format == 2:
                    ret = audioop.adpcm2lin(raw_samples, fmtChunk.data.bits_per_sample, None)
                    samples_lin = ret[0]
                    for i in range(int(len(samples_lin) / 8)):
                        sample = samples_lin[i * 8:i * 8 + 8]
                        converted_sample = int.from_bytes(sample, byteorder="little", signed=True)
                        samples.append(converted_sample)
                else:
                    print("Format zapisu danych w pliku nie jest wspierany")
                    raise Exception

            channels = []
            for c in range(fmtChunk.data.num_channels):
                channels.append(samples[c::fmtChunk.data.num_channels])
            return channels

        @staticmethod
        def channels_to_bytes(fmtChunk: FmtChunk, contents) -> bytes:
            combined_channels = [None] * (len(contents.samples) * len(contents.samples[0]))
            for c in range(0, fmtChunk.data.num_channels):
                combined_channels[c::fmtChunk.data.num_channels] = contents.samples[c]

            bytes_sample = b""
            bytes_samples = []

            for sample in combined_channels:
                if fmtChunk.data.bits_per_sample >= 8:
                    sample_len = int(fmtChunk.data.bits_per_sample / 8)
                else:
                    sample_len = int(fmtChunk.data.bits_per_sample / 4)
                if fmtChunk.data.audio_format == 1:
                    if sample_len == 1:
                        bytes_sample = int.to_bytes(sample, byteorder="little", signed=False, length=sample_len)
                    else:
                        bytes_sample = int.to_bytes(sample, byteorder="little", signed=True, length=sample_len)
                elif fmtChunk.data.audio_format == 3:
                    if sample_len == 4:
                        bytes_sample = bytearray(struct.pack("f", sample))
                    else:
                        bytes_sample = bytearray(struct.pack("d", sample))
                elif fmtChunk.data.audio_format == 6:
                    bytes_sample = audioop.lin2alaw(int.to_bytes(sample, byteorder="little",
                                                                 signed=True, length=sample_len), sample_len)
                elif fmtChunk.data.audio_format == 7:
                    bytes_sample = audioop.lin2ulaw(int.to_bytes(sample, byteorder="little",
                                                                 signed=True, length=sample_len), sample_len)
                else:
                    raise Exception
                bytes_samples.append(bytes_sample)
            return b"".join(bytes_samples)

        @staticmethod
        def channels_to_bytes_uncompressed_if_possible(fmtChunk: FmtChunk, contents) -> bytes:
            if fmtChunk.data.audio_format != 6 and fmtChunk.data.audio_format != 7:
                return DataChunk.Contents.channels_to_bytes(fmtChunk, contents)
            else:
                combined_channels = [None] * (len(contents.samples) * len(contents.samples[0]))
                for c in range(0, fmtChunk.data.num_channels):
                    combined_channels[c::fmtChunk.data.num_channels] = contents.samples[c]

                bytes_sample = b""
                bytes_samples = []

                for sample in combined_channels:
                    bytes_sample = int.to_bytes(sample, byteorder="little", signed=False, length=sample.bit_length()//8)
                    bytes_samples.append(bytes_sample)

                fmtChunk.data.audio_format = 1
                fmtChunk.data.bits_per_sample = contents.samples[0][0].bit_length()
                fmtChunk.data.block_align = (fmtChunk.data.bits_per_sample // 8) * fmtChunk.data.num_channels

                return b"".join(bytes_samples)

        def write(self, file, fmtChunk: FmtChunk):
            bytes_to_save = DataChunk.Contents.channels_to_bytes(fmtChunk, self)
            file.write(bytes_to_save)


    data: Contents

    def __init__(self, id: str, size: int, data: Contents):
        Chunk.__init__(self=self, id=id, size=size, data=None)
        self.data = DataChunk.Contents(data)

    def __repr__(self):
        return Chunk.__repr__(self) + "\n" + str(self.data)

    def __str__(self):
        return Chunk.__str__(self) + "\n" + str(self.data)
    pass

    def write(self, file, fmtChunk: FmtChunk, overwrite_data: bytearray = None):
        if overwrite_data is None:
            Chunk.write(self, file)
            self.data.write(file, fmtChunk)
        else:
            self.size = len(overwrite_data)
            Chunk.write(self, file)
            file.write(overwrite_data)


    def update(self, new_byte_data: bytearray):
        self.size = len(new_byte_data)
        self.data.raw_samples = new_byte_data


class ID3Chunk(Chunk):
    class Contents:
        version: int
        TPE1: INFOsubChunk          # wykonawca
        COMM: INFOsubChunk          # tytuł utworu
        TIT2: INFOsubChunk          # tytuł albumu
        TDRC: INFOsubChunk          # gatunek
        TALB: INFOsubChunk          # komentarze
        TRCK: INFOsubChunk          # sciezka
        TCON: INFOsubChunk          # gatunek
        TXXX: INFOsubChunk          # przerwa
        unrecognized = []           # nierozpoznany

        def __repr__(self):
            list = "\t\t\tVersion: " + str(self.version) + "\n"
            try:
                list += str(self.TPE1)
            except AttributeError:
                pass
            try:
                list += str(self.TIT2)
            except AttributeError:
                pass
            try:
                list += str(self.COMM)
            except AttributeError:
                pass
            try:
                list += str(self.TALB)
            except AttributeError:
                pass
            try:
                list += str(self.TDRC)
            except AttributeError:
                pass
            try:
                list += str(self.TRCK)
            except AttributeError:
                pass
            try:
                list += str(self.TCON)
            except AttributeError:
                pass
            try:
                list += str(self.TXXX)
            except AttributeError:
                pass
            try:
                for unrecognized in self.unrecognized:
                    try:
                        list += "\t\t\tNierozpoznany:\n"
                        list += str(unrecognized)
                    except Exception:
                        pass
            except Exception:
                pass
            return list

        def write(self, file):
            try:
                if 'TPE1' in tab:
                    self.TPE1.size -= 2
                    self.TPE1.size = int.from_bytes(self.TPE1.size.to_bytes(4, byteorder="big", signed=True), byteorder="little")
                    self.TPE1.write(file)
            except Exception:
                pass
            try:
                if 'TIT2' in tab:
                    self.TIT2.size -= 2
                    self.TIT2.size = int.from_bytes(self.TIT2.size.to_bytes(4, byteorder="big", signed=True), byteorder="little")
                    self.TIT2.write(file)
            except:
                pass
            try:
                if 'COMM' in tab:
                    self.COMM.size -= 2
                    self.COMM.size = int.from_bytes(self.COMM.size.to_bytes(4, byteorder="big", signed=True), byteorder="little")
                    self.COMM.write(file)
            except:
                pass
            try:
                if 'TALB' in tab:
                    self.TALB.size -= 2
                    self.TALB.size = int.from_bytes(self.TALB.size.to_bytes(4, byteorder="big", signed=True), byteorder="little")
                    self.TALB.write(file)
            except:
                pass
            try:
                if 'TDRC' in tab:
                    self.TDRC.size -= 2
                    self.TDRC.size = int.from_bytes(self.TDRC.size.to_bytes(4, byteorder="big", signed=True), byteorder="little")
                    self.TDRC.write(file)
            except:
                pass
            try:
                if 'TRCK' in tab:
                    self.TRCK.size -= 2
                    self.TRCK.size = int.from_bytes(self.TRCK.size.to_bytes(4, byteorder="big", signed=True), byteorder="little")
                    self.TRCK.write(file)
            except:
                pass
            try:
                if 'TCON' in tab:
                    self.TCON.size -= 2
                    self.TCON.size = int.from_bytes(self.TCON.size.to_bytes(4, byteorder="big", signed=True), byteorder="little")
                    self.TCON.write(file)
            except:
                pass
            try:
                if 'TXXX' in tab:
                    self.TXXX.size -= 2
                    self.TXXX.size = int.from_bytes(self.TXXX.size.to_bytes(4, byteorder="big", signed=True), byteorder="little")
                    self.TXXX.write(file)
            except:
                pass

    data: Contents

    def __init__(self, id: str, size: int, data: list, version: int):
        global index
        Chunk.__init__(self=self, id=id, size=size, data=None)
        self.data = ID3Chunk.Contents()
        self.data.version = version
        start = 0
        while start < len(data) - 1:
            subid = bytes.decode(data[start:start + 4])
            if len(subid):
                sizesubid = int.from_bytes(data[start + 4:start + 8], byteorder="big") + 2
            if subid in self.Contents.__annotations__:
                exec(
                    "%s=%s" % ('self.data.' + subid, "INFOsubChunk(subid, sizesubid, data[start+8:start+sizesubid+8])"))
                Optional.update({index: subid})
                index += 1
            else:
                self.data.unrecognized.append(INFOsubChunk(subid, sizesubid, data[start + 8:start + sizesubid + 8]))
            start = start + sizesubid + 8

        if len(data) > 4 + start:
            self.data.unrecognized.append(INFOsubChunk(bytes.decode(data[start:start + 4]), len(data[start + 4:]), data[start + 4:]))

    def __repr__(self):
        return Chunk.__repr__(self) + "\n" + str(self.data)

    def __str__(self):
        return f"\t\t" + Chunk.__str__(self) + "\n" + str(self.data)
    pass

    def write(self, file):
        self.size = 0
        if "ID3" in tab:
            for field in tab:
                if tab.index(field) < tab.index("ID3") and field in self.Contents.__annotations__:
                    exec("self.size += self.data.%s.size + 8" % field)

        file.write(self.id.encode(encoding='utf-8'))
        file.write(self.data.version.to_bytes(1, byteorder="little", signed=True))
        file.write(self.size.to_bytes(6, byteorder='big', signed=True))
        self.data.write(file)


class id3Chunk(Chunk):
    class Contents:
        ID3: ID3Chunk               # informacje o utworze
        unrecognized = []           # nierozpoznany

        def __repr__(self):
            list = ""
            try:
                list += str(self.ID3)
            except AttributeError:
                pass
            try:
                for unrecognized in self.unrecognized:
                    try:
                        list += "\t\tNierozpoznany:\n"
                        list += str(unrecognized)
                    except Exception:
                        pass
            except Exception:
                pass
            return list

        pass

        def write(self, file):
            try:
                if 'ID3' in tab:
                    self.ID3.write(file)
            except Exception:
                pass

    data: Contents

    def __init__(self, id: str, size: int, data: [bytes, int]):
        global index
        Chunk.__init__(self=self, id=id, size=size, data=None)
        self.data = id3Chunk.Contents()
        start = 0
        while start < data.index(data[-1]):
            subid = bytes.decode(data[start:start + 3])
            if len(subid):
                version = data[start+3]
                subsize = int.from_bytes(data[start + 4:start + 10], byteorder="big")
            if subid == "ID3":
                self.data.ID3 = ID3Chunk(subid, subsize, data[start + 10:start + size], version)
                Optional.update({index: self.data.ID3.id})
                index += 1
            else:
                self.data.unrecognized.append(ID3Chunk(subid, subsize, data[start + 10:start + size], version))
            start = start + size

        if len(data) > 4 + start:
            self.data.unrecognized.append(ID3Chunk(bytes.decode(data[start:start + 3]), len(data[start + 4:]), data[start + 4:], data[start+3]))

    def __repr__(self):
        return Chunk.__repr__(self) + "\n" + str(self.data)

    def __str__(self):
        return f"\t" + Chunk.__str__(self) + "\n" + str(self.data)
    pass

    def write(self, file):
        self.size = 0
        if "ID3" in tab:
            for field in tab:
                if tab.index(field) < tab.index("ID3") and field in self.data.ID3.Contents.__annotations__:
                    exec("self.size += self.data.ID3.data.%s.size + 8" % field)
        self.size += 11
        Chunk.write(self, file)
        self.data.write(file)

