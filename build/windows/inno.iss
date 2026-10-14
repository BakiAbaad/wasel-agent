[Setup]
AppName=Wasel Agent
AppVersion=0.1.0
DefaultDirName={pf}\WaselAgent
DefaultGroupName=WaselAgent
OutputBaseFilename=wasel-agent-setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\run_agent\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{commondesktop}\Wasel Agent"; Filename: "{app}\run_agent.exe"

[Run]
Filename: "{app}\nssm.exe"; Parameters: "install wasel-agent ""{app}\run_agent.exe"""; Flags: runhidden waituntilterminated
Filename: "{app}\nssm.exe"; Parameters: "start wasel-agent"; Flags: runhidden
