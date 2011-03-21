# last edited 2010.02.24
import sys
import os
from subprocess import Popen, PIPE

extToProcess = [
   '.iso',
   '.mdf',
   '.bin',
   '.img',
   '.nrg',
   '.bwi',
   '.mdx',
]

def getExePath():
   try:
      from win32api import RegOpenKey, RegQueryValue
      from win32con import HKEY_LOCAL_MACHINE
      key = RegOpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\EasyBoot Systems\UltraISO\5.0')
      path = RegQueryValue(key, None)
   except:
      guesses = [
            r'C:\Program Files\UltraISO',
            r'C:\Program Files (x86)\UltraISO',
      ]
      for folder in guesses:
         if os.path.isdir(folder):
            path = folder
            break

   return os.path.join(path, 'UltraISO.exe')

def iso2isz(inp, out=None):
   inp = os.path.abspath(inp)
   ext = os.path.splitext(inp)[1]
   out = out or os.path.splitext(inp)[0] + '.isz'
   # ultraiso insists that input files end in .iso
   # so rename if necessary
   if ext.lower() != '.iso':
      tempname = os.path.splitext(inp)[0] + '.iso'
      os.rename(inp, tempname)
      inp = tempname
   cmd = [
      getExePath(),
      '-in', inp,
      '-out', out,
      '-optimize',
      '-compress', '6', # 1-6, 6 is max compression
      #'-md5',
   ]
   Popen(cmd).wait()
   origName = os.path.splitext(inp)[0] + ext
   # undo rename if it was done
   if inp != origName:
      os.rename(inp, origName)

def main(argv=None):
   argv = argv or sys.argv
   args = argv[1:]

   # Zero args: do every iso in current directory
   if len(args) == 0:
      for f in os.listdir(os.getcwd()):
         if os.path.splitext(f)[1].lower() in extToProcess:
            iso2isz(f)
   # One arg: convert the given iso to .isz
   elif len(args) == 1:
      iso2isz(args[0])
   # Two args: convert source to destination path
   elif len(args) == 2:
      iso2isz(*args)
   else:  
      print 'Too many args!'

if __name__ == '__main__':
   sys.exit(main())

