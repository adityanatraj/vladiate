import io
import boto
from urlparse import urlparse
from StringIO import StringIO


class VladInput(object):
    ''' A generic input class '''

    def __init__(self):
        raise NotImplementedError

    def open(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class LocalFile(VladInput):
    ''' Read from a local file path '''

    def __init__(self, filename):
        self.filename = filename

    def open(self):
        return open(self.filename, 'r')

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.filename)


class S3File(VladInput):
    ''' Read from a file in S3 '''

    def __init__(self, path=None, bucket=None, key=None):
        if path and not any((bucket, key)):
            self.path = path
            parse_result = urlparse(path)
            self.bucket = parse_result.netloc
            self.key = parse_result.path
        elif all((bucket, key)):
            self.bucket = bucket
            self.key = key
            self.path = "s3://{}{}"
        else:
            raise ValueError(
                "Either 'path' argument or 'bucket' and 'key' argument must be set.")

    def open(self):
        s3 = boto.connect_s3()
        bucket = s3.get_bucket(self.bucket)
        key = bucket.new_key(self.key)
        contents = key.get_contents_as_string()
        ret = io.BytesIO(bytes(contents))
        return ret

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.path)


class String(VladInput):
    ''' Read a file from a string '''

    def __init__(self, string_input=None, string_io=None):
        self.string_io = string_io if string_io else StringIO(string_input)

    def open(self):
        return self.string_io

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, '...')
