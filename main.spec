# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
         ('..\\a_table\\images', 'images'),
         ('..\\a_table\\Mes_Fiches', 'Mes_Fiches'),
         ('..\\a_table\\MesRecettes.csv', '.'),
         ('..\\a_table\\Historique.csv', '.'),
]

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          Tree('..\\a_table\\UI\\', prefix='UI\\'),
          a.zipfiles,
          a.datas,  
          [],
          name='A_Table',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='..\\a_table\\UI\\images\\donut.ico')
#coll = COLLECT(exe,
#               a.binaries,
#               a.zipfiles,
#               a.datas,
#               added_files,
#               strip=False,
#               upx=True,
#               name='A_Table')