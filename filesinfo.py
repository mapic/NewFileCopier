import os
import os.path
import pickle


def collectfilesabspath(dirpath):
    path = os.path.abspath(dirpath)
    return (os.path.join(dirpath, filename) for dirpath, dirs, filenames in os.walk(path) for filename in filenames)


def getinfo(dirpath):
    filespath = collectfilesabspath(dirpath)
    return ((os.path.relpath(filepath, dirpath), FileInfo(filepath)) for filepath in filespath)


def getdata(dirpath):
    return {path: info for path, info in getinfo(dirpath)}


def storedata(data, datafilepath):
    with open(datafilepath, mode='wb') as file:
        pickle.dump(data, file)


def storeinfo(dirpath, datafilepath):
    storedata(getdata(dirpath), datafilepath)


def loadinfo(datafilepath):
    with open(datafilepath, mode='rb') as file:
        return pickle.load(file)


class FileInfo:
    def __init__(self, filepath):
        self.lmt = os.path.getmtime(filepath)

    def __eq__(self, other):
        return self.lmt == other.lmt

    def __repr__(self):
        import time

        return 'Last modify time: %f (%s)' % (self.lmt, time.ctime(self.lmt))


if __name__ == '__main__':
    print('File(s) info in current dir:')
    dat = getdata('.')
    print(dat)
    print()

    datafilename = 'filesinfo_test_data'
    print('Save data of current dir to %s...' % datafilename)
    storedata(dat, datafilename)
    print('Lod data of current dir from %s...' % datafilename)
    ldat = loadinfo(datafilename)
    print('Is data same after load: %s' % (dat == ldat))
    print('Remove test data file %s' % datafilename)
    os.remove(datafilename)
