import glob, os
"""Add a call to get_excludes to the spec file from the installer.
   This function will exclude all of the pws modules from the build,
   and will allow you to package the pws packages with
   the executable instead of having them built into the executable.

   Add the call to the spec file after the Installer has done its
   analysis."""
    
def get_excludes(path):
    excludeThese = [("pwsconfig", '', '')]
    for pkg in ("data", "db", "gui", "lib", "Matches", "Wrestlers"):
        excludeThese.append((pkg, '', ''))
        pkgMods = get_package_modules(path, pkg)
        excludeThese += pkgMods

    return excludeThese

def get_package_modules(path, pkg, retpath=0):
    files = glob.glob(os.path.join(path, pkg, "*.py"))
    mods = []
    for file in files:
        modname = os.path.basename(file)
        if not retpath:
            mods.append((pkg+'.'+modname[:-3], '', ''))
        else:
            mods.append((os.path.join(pkg, modname), file, 'DATA'))

    return mods
    
def get_data_files(path):
    datafiles = [('README.txt', os.path.join(path, 'README.txt'), 'DATA'),
                 ('license.txt', os.path.join(path, 'license.txt'), 'DATA'),
                 ('pwsconfig.py', os.path.join(path, 'pwsconfig.py'), 'DATA'),
                 (os.path.join('log', 'README.Logging.txt'),
                  os.path.join(path, 'log', 'README.Logging.txt'), 'DATA'),
                 (os.path.join('db', 'dataRegistry.py'),
                  os.path.join(path, 'db', 'dataRegistry.py'), 'DATA')
                 ]
    datafiles += getFiles(os.path.join(path, "resources"))
    
    docfiles = []
    absdocpath = os.path.join(path, 'doc')
    doclist = os.listdir(absdocpath)
    doclist.remove("CVS")
    # The following should be replaced with some sort of file tree walk...
    for docfile in doclist:
        if os.path.isfile(os.path.join(absdocpath, docfile)):
            docfiles.append((os.path.join('doc', docfile), os.path.join(absdocpath, docfile), 'DATA'))
        else:
            absSubdirPath = os.path.join(absdocpath, docfile)
            subdirFiles = os.listdir(absSubdirPath)
            subdirFiles.remove("CVS")
            for dirfile in subdirFiles:
                docfiles.append((os.path.join('doc', docfile ,dirfile),
                                 os.path.join(absSubdirPath, dirfile), 'DATA'))

    datafiles += docfiles    

    # Get package files
    for pkg in ("data", "db", "gui", "lib", "Matches", "Wrestlers"):
        pkgfiles = get_package_modules(path, pkg, 1)
        datafiles += pkgfiles

    return datafiles

def getFiles(path):
    dirfiles = []
    relpath = os.path.split(path)[-1]
    files = os.listdir(path)
    files.remove("CVS")
    for file in files:
        dirfiles.append((os.path.join(relpath, file), os.path.join(path, file),
                         'DATA'))

    return dirfiles
