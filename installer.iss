; ============================================================
;  Personnel System — Inno Setup Script
; ============================================================

[Setup]
AppName=نظام ملفات الموظفين
AppVersion=1.0
AppPublisher=شركتك
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
DefaultDirName={autopf}\PersonnelSystem
DefaultGroupName=نظام ملفات الموظفين
DisableProgramGroupPage=no
OutputDir=installer_output
OutputBaseFilename=PersonnelSystem_Setup_v1.0
WizardStyle=modern
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=admin
MinVersion=10.0
Uninstallable=yes
UninstallDisplayName=نظام ملفات الموظفين
UninstallDisplayIcon={app}\company_logo.ico
SetupIconFile=dist\PersonnelSystem\company_logo.ico

[Languages]
Name: "arabic"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "إنشاء اختصار على سطح المكتب"; Flags: unchecked
Name: "startupicon"; Description: "تشغيل البرنامج عند بدء Windows"; Flags: unchecked

[Files]
Source: "dist\PersonnelSystem\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]
Name: "{commonappdata}\PersonnelSystem"; Permissions: users-full
Name: "{commonappdata}\PersonnelSystem\employee_files"; Permissions: users-full

[Icons]
Name: "{group}\نظام ملفات الموظفين"; Filename: "{app}\PersonnelSystem.exe"; IconFilename: "{app}\company_logo.ico"
Name: "{group}\إلغاء التثبيت"; Filename: "{uninstallexe}"
Name: "{autodesktop}\نظام ملفات الموظفين"; Filename: "{app}\PersonnelSystem.exe"; IconFilename: "{app}\company_logo.ico"; Tasks: desktopicon
Name: "{autostartup}\نظام ملفات الموظفين"; Filename: "{app}\PersonnelSystem.exe"; IconFilename: "{app}\company_logo.ico"; Tasks: startupicon

[Run]
Filename: "{app}\PersonnelSystem.exe"; Description: "تشغيل البرنامج الآن"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\__pycache__"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  DataDir, ReadmePath: String;
  Lines: TArrayOfString;
begin
  if CurStep = ssPostInstall then
  begin
    DataDir    := ExpandConstant('{commonappdata}\PersonnelSystem');
    ReadmePath := DataDir + '\README.txt';
    SetArrayLength(Lines, 6);
    Lines[0] := 'نظام ملفات الموظفين — مجلد البيانات';
    Lines[1] := '=====================================';
    Lines[2] := 'personnel.db   — قاعدة البيانات المشفرة';
    Lines[3] := 'personnel.key  — مفتاح التشفير (احتفظ به في مكان آمن)';
    Lines[4] := 'employee_files — مستندات وصور الموظفين';
    Lines[5] := '';
    SaveStringsToFile(ReadmePath, Lines, False);
  end;
end;
