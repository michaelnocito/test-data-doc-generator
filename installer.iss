[Setup]
AppName=Test Data & Document Generator
AppVersion=1.0.0
AppPublisher=Michael Nocito
DefaultDirName={autopf}\TestDataDocGenerator
DefaultGroupName=Test Data & Document Generator
OutputBaseFilename=TestDataDocGeneratorSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\TestDataDocGenerator.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Test Data & Document Generator"; Filename: "{app}\TestDataDocGenerator.exe"
Name: "{commondesktop}\Test Data & Document Generator"; Filename: "{app}\TestDataDocGenerator.exe"

[Run]
Filename: "{app}\TestDataDocGenerator.exe"; Description: "Launch Test Data & Document Generator"; Flags: nowait postinstall skipifsilent
