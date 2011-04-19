; -- pws.iss --
; PATCH .95b

[Setup]
AppName=Pro Wrestling Superstar
AppId=Pro Wrestling Superstar
AppVerName=Pro Wrestling Superstar version .95b Patch
DefaultDirName={pf}\Pro Wrestling Superstar
;DefaultGroupName=Pro Wrestling Superstar
CreateUninstallRegKey=no
UpdateUninstallLogAppName=no

[Files]
Source: "data\strategyPinChart.py"; DestDir: "{app}\data"
Source: "data\globalConstants.py"; DestDir: "{app}\data"
Source: "gui\jowstgui.py"; DestDir: "{app}\gui"
Source: "gui\tourngui.py"; DestDir: "{app}\gui"
Source: "gui\brackets.py"; DestDir: "{app}\gui"
Source: "lib\util.py"; DestDir: "{app}\lib"
Source: "lib\spw.py"; DestDir: "{app}\lib"
Source: "lib\dblib.py"; DestDir: "{app}\lib"

[Icons]
;Name: "{group}\Pro Wrestling Superstar"; Filename: "{app}\pws.exe"
