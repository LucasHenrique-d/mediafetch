#define MyAppName "MediaFetch"
#define MyAppVersion "2.2.0"
#define MyAppPublisher "Luczeraaa"
#define MyAppExeName "MediaFetch.exe"

[Setup]

AppId={{A4C1B9F7-5E7A-4A38-BB9E-91E9D8E6C742}

AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\MediaFetch
DefaultGroupName={#MyAppName}

OutputDir=installer
OutputBaseFilename=MediaFetch-Setup-{#MyAppVersion}

SetupIconFile=assets\icon.ico

Compression=lzma
SolidCompression=yes

WizardStyle=modern

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DisableProgramGroupPage=yes

UninstallDisplayIcon={app}\{#MyAppExeName}

PrivilegesRequired=admin

[Files]

Source: "dist\MediaFetch.exe"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]

Name: "{autoprograms}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"

Name: "{autodesktop}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"

[Run]

Filename: "{app}\{#MyAppExeName}"; \
    Description: "Executar {#MyAppName}"; \
    Flags: nowait postinstall skipifsilent