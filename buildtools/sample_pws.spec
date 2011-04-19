a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'F:\\pws\\pws.py'],
             pathex=['F:\\Installer'])
import buildtools
excf = buildtools.get_excludes("F:\\pws")
df = buildtools.get_data_files("F:\\pws")
pyz = PYZ(a.pure - excf)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='buildpws/pws.exe',
          debug=0,
          strip=0,
          upx=0,
          console=0 , icon='F:\\pws\\resources\\pws.ico')
coll = COLLECT( exe,
               a.binaries + df,
               strip=0,
               upx=0,
               name='distpws')
