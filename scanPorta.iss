[Setup]
AppName=scanPorta
AppVersion=1.0
DefaultDirName={pf}\scanPorta
DefaultGroupName=scanPorta
OutputBaseFilename=scanPortaSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=icone.ico
DisableDirPage=no
DisableProgramGroupPage=no
WizardStyle=modern

[Files]
Source: "dist\scanPorta.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icone.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\scanPorta"; Filename: "{app}\scanPorta.exe"; IconFilename: "{app}\icone.ico"
Name: "{commondesktop}\scanPorta"; Filename: "{app}\scanPorta.exe"; IconFilename: "{app}\icone.ico"
