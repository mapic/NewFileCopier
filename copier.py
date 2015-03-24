import filesinfo
import os
import shutil


def scan(dirpath, datafilepath):
    filesinfo.storeinfo(dirpath, datafilepath)


def startcopy(sourcedir, destnationdir, datafilepath):
    data = filesinfo.loadinfo(datafilepath)
    srcpaths = filesinfo.collectfilesabspath(sourcedir)
    print('\n复制到：%s' % destnationdir)
    for path in srcpaths:
        relpath = os.path.relpath(path, sourcedir)
        if relpath in data and data[relpath] == filesinfo.FileInfo(path):
            continue
        else:
            print(relpath)
            dstpath = os.path.join(destnationdir, relpath)
            os.makedirs(os.path.dirname(dstpath), exist_ok=True)
            shutil.copy(path, dstpath)
