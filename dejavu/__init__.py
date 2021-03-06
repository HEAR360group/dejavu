from dejavu.database import get_database, Database
import dejavu.decoder as decoder
import dejavu.fingerprint as fingerprint
import multiprocessing
import os
import traceback
import sys
import dejavu.shared

class Combinator(object):
    
    SONG_ID = "song_id"
    SONG_NAME = 'song_name'
    CONFIDENCE = 'confidence'
    MATCH_TIME = 'match_time'
    OFFSET = 'offset'
    OFFSET_SECS = 'offset_seconds'
    
    max_sid = 0
    all_songs = []
#    all_hashes = []
    
    def __init__(self, config):
        super(Combinator, self).__init__()

        self.config = config
            
    def add_db(self, dbfile):
        filename, extension = os.path.splitext(os.path.basename(dbfile))
        
        # initialize db
        dejavu.shared.DATABASE_FILE = dbfile
        db_cls = get_database("sqlite")
        #db_cls = get_database(config.get("database_type", None))

        self.db = db_cls(**self.config.get("database", {}))
        self.db.setup()

        # get songs previously indexed
        songs = self.db.get_songs()
        
        for song in songs:
            newsong = {Database.FIELD_SONG_ID: song[Database.FIELD_SONG_ID] + self.max_sid,
                       Database.FIELD_SONGNAME: filename + "_" + song[Database.FIELD_SONGNAME],
                       Database.FIELD_FILE_SHA1: song[Database.FIELD_FILE_SHA1],
                       "hashes": []}
            
            hashes = self.db.get_fingerprints_by_song_id(song[Database.FIELD_SONG_ID])
            newsong["hashes"].extend(hashes)
            
            self.all_songs.append(newsong)
        
        self.max_sid = self.max_sid + len(self.all_songs)
        
#        print("all_songs:%d, all_hashes:%d, max_sid:%d" % (len(self.all_songs), len(self.all_hashes), self.max_sid))
        
    def save_db(self, outpath):
        # initialize db
        dejavu.shared.DATABASE_FILE = outpath
        db_cls = get_database("sqlite")
        #db_cls = get_database(config.get("database_type", None))

        self.db = db_cls(**self.config.get("database", {}))
        self.db.setup()
        
        self.db.empty()
        
        for song in self.all_songs:
            sid = self.db.insert_song(song[Database.FIELD_SONGNAME], song[Database.FIELD_FILE_SHA1])
            self.db.insert_hashes(sid, song["hashes"])
            self.db.set_song_fingerprinted(sid)
            
            print("hashes type:%s" % (type(song["hashes"])))
            print("hashes in %d:%d" % (sid, len(song["hashes"])))
            
        print("all_songs:%d" % (len(self.all_songs)))
        
        return

class Dejavu(object):

    SONG_ID = "song_id"
    SONG_NAME = 'song_name'
    CONFIDENCE = 'confidence'
    MATCH_TIME = 'match_time'
    OFFSET = 'offset'
    OFFSET_SECS = 'offset_seconds'

    def __init__(self, config):
        super(Dejavu, self).__init__()

        self.config = config

        # initialize db
        db_cls = get_database("sqlite")
        #db_cls = get_database(config.get("database_type", None))

        self.db = db_cls(**config.get("database", {}))
        self.db.setup()

        # if we should limit seconds fingerprinted,
        # None|-1 means use entire track
        self.limit = self.config.get("fingerprint_limit", None)
        if self.limit == -1:  # for JSON compatibility
            self.limit = None
        self.get_fingerprinted_songs()
        
    def empty_db(self):
        self.db.empty()

    def get_fingerprinted_songs(self):
        # get songs previously indexed
        self.songs = self.db.get_songs()
        self.songhashes_set = set()  # to know which ones we've computed before
        for song in self.songs:
            song_hash = song[Database.FIELD_FILE_SHA1]
            self.songhashes_set.add(song_hash)

    def fingerprint_directory(self, path, extensions, nprocesses=None):
        # Try to use the maximum amount of processes if not given.
        try:
            nprocesses = nprocesses or multiprocessing.cpu_count()
        except NotImplementedError:
            nprocesses = 1
        else:
            nprocesses = 1 if nprocesses <= 0 else nprocesses

        pool = multiprocessing.Pool(nprocesses)

        filenames_to_fingerprint = []
        for filename, _ in decoder.find_files(path, extensions):

            # don't refingerprint already fingerprinted files
            if decoder.unique_hash(filename) in self.songhashes_set:
                dejavu.shared.UITEXTLOGGER.emit("%s already fingerprinted, continuing..." % filename)
                print("%s already fingerprinted, continuing..." % filename)
                continue

            filenames_to_fingerprint.append(filename)

        # Prepare _fingerprint_worker input
        worker_input = zip(filenames_to_fingerprint,
                           [self.limit] * len(filenames_to_fingerprint))

        # Send off our tasks
        iterator = pool.imap_unordered(_fingerprint_worker,
                                       worker_input)

        # Loop till we have all of them
        while True:
            try:
                song_name, hashes, file_hash = iterator.next()
            except multiprocessing.TimeoutError:
                continue
            except StopIteration:
                break
            except:
                dejavu.shared.UITEXTLOGGER.emit("Failed fingerprinting")
                print("Failed fingerprinting")
                # Print traceback because we can't reraise it here
                traceback.print_exc(file=sys.stdout)
            else:
                dejavu.shared.UITEXTLOGGER.emit ("Saving finger prints to Database for %s" % song_name)
                print("Saving finger prints to Database for %s" % song_name)
                sid = self.db.insert_song(song_name, file_hash)

                self.db.insert_hashes(sid, hashes)
                self.db.set_song_fingerprinted(sid)
                self.get_fingerprinted_songs()
                dejavu.shared.UITEXTLOGGER.emit ("Finished saving finger prints to Database for %s" % song_name)
                print("Finished saving finger prints to Database for %s" % song_name)

        pool.close()
        pool.join()

    def fingerprint_file(self, filepath, song_name=None):
        songname = decoder.path_to_songname(filepath)
        song_hash = decoder.unique_hash(filepath)
        song_name = song_name or songname
        # don't refingerprint already fingerprinted files
        if song_hash in self.songhashes_set:
            dejavu.shared.UITEXTLOGGER.emit("%s already fingerprinted, continuing..." % song_name)
            print ("%s already fingerprinted, continuing..." % song_name)
        else:
            song_name, hashes, file_hash = _fingerprint_worker(
                filepath,
                self.limit,
                song_name=song_name
            )
            dejavu.shared.UITEXTLOGGER.emit("Saving finger prints to Database for %s" % song_name)
            print ("Saving finger prints to Database for %s" % song_name)
            sid = self.db.insert_song(song_name, file_hash)

            self.db.insert_hashes(sid, hashes)
            self.db.set_song_fingerprinted(sid)
            self.get_fingerprinted_songs()
            dejavu.shared.UITEXTLOGGER.emit("Finished saving finger prints to Database for %s" % song_name)
            print ("Finished saving finger prints to Database for %s" % song_name)

    def find_matches(self, samples, Fs=fingerprint.DEFAULT_FS):
        hashes = fingerprint.fingerprint(samples, Fs=Fs)
        return self.db.return_matches(hashes)

    def align_matches(self, matches):
        """
            Finds hash matches that align in time with other matches and finds
            consensus about which hashes are "true" signal from the audio.

            Returns a dictionary with match information.
        """
        # align by diffs
        diff_counter = {}
        largest = 0
        largest_count = 0
        song_id = -1
        for tup in matches:
            sid, diff = tup
            if diff not in diff_counter:
                diff_counter[diff] = {}
            if sid not in diff_counter[diff]:
                diff_counter[diff][sid] = 0
            diff_counter[diff][sid] += 1

            if diff_counter[diff][sid] > largest_count:
                largest = diff
                largest_count = diff_counter[diff][sid]
                song_id = sid

        # extract idenfication
        song = self.db.get_song_by_id(song_id)
        if song:
            # TODO: Clarify what `get_song_by_id` should return.
            songname = song[Dejavu.SONG_NAME]
            #songname = song.get(Dejavu.SONG_NAME, None)
        else:
            return None

        # return match info
        nseconds = round(float(largest) / fingerprint.DEFAULT_FS *
                         fingerprint.DEFAULT_WINDOW_SIZE *
                         fingerprint.DEFAULT_OVERLAP_RATIO, 5)
        song = {
            Dejavu.SONG_ID : song_id,
            Dejavu.SONG_NAME : songname.encode("utf8"),
            Dejavu.CONFIDENCE : largest_count,
            Dejavu.OFFSET : int(largest),
            Dejavu.OFFSET_SECS : nseconds,
            Database.FIELD_FILE_SHA1 : song[Database.FIELD_FILE_SHA1].encode("utf8"),}
        return song

    def recognize(self, recognizer, *options, **kwoptions):
        r = recognizer(self)
        return r.recognize(*options, **kwoptions)


def _fingerprint_worker(filename, limit=None, song_name=None):
    # Pool.imap sends arguments as tuples so we have to unpack
    # them ourself.
    try:
        filename, limit = filename
    except ValueError:
        pass

    songname, extension = os.path.splitext(os.path.basename(filename))
    song_name = song_name or songname
    channels, Fs, file_hash = decoder.read(filename, limit)
    result = set()
    channel_amount = len(channels)

    for channeln, channel in enumerate(channels):
        # TODO: Remove prints or change them into optional logging.
        dejavu.shared.UITEXTLOGGER.emit("Fingerprinting channel %d/%d for %s" % (channeln + 1,
                                                       channel_amount,
                                                       filename))
        print("Fingerprinting channel %d/%d for %s" % (channeln + 1,
                                                       channel_amount,
                                                       filename))
        hashes = fingerprint.fingerprint(channel, Fs=Fs)
        dejavu.shared.UITEXTLOGGER.emit("Finished channel %d/%d for %s" % (channeln + 1, channel_amount,
                                                 filename))
        print("Finished channel %d/%d for %s" % (channeln + 1, channel_amount,
                                                 filename))
        result |= set(hashes)

    return song_name, result, file_hash


def chunkify(lst, n):
    """
    Splits a list into roughly n equal parts.
    http://stackoverflow.com/questions/2130016/splitting-a-list-of-arbitrary-size-into-only-roughly-n-equal-parts
    """
    return [lst[i::n] for i in range(n)]
