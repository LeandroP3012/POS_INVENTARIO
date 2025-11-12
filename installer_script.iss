; Script de instalación para Inno Setup
; Sistema POS - Punto de Venta

#define MyAppName "Sistema POS"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Tu Empresa"
#define MyAppURL "https://www.tuempresa.com"
#define MyAppExeName "POS_Sistema.exe"

[Setup]
; Información de la aplicación
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; LicenseFile=LICENSE.txt
; InfoBeforeFile=INSTRUCCIONES_INSTALACION.txt
OutputDir=Output
OutputBaseFilename=POS_Setup
SetupIconFile=assets\images\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Archivos de la aplicación
Source: "dist\POS_Sistema\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\POS_Sistema\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Documentación (si existen)
Source: "dist\POS_Sistema\CONFIGURACION_BD.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme skipifsourcedoesntexist
Source: "INSTRUCCIONES_INSTALACION.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Dirs]
; Crear directorios necesarios
Name: "{app}\logs"; Permissions: users-full
Name: "{app}\backups"; Permissions: users-full
Name: "{app}\tickets"; Permissions: users-full
Name: "{app}\config"; Permissions: users-full

[Icons]
; Iconos del menú inicio
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
; Icono del escritorio
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Ejecutar después de la instalación
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
var
  DBConfigPage: TInputQueryWizardPage;
  DBTestPage: TWizardPage;
  MySQLInstalledPage: TWizardPage;
  LicensePage: TInputQueryWizardPage;
  LicenseValid: Boolean;
  DBTestResultMemo: TNewMemo;
  DBTestButton: TNewButton;
  DBTestRetryButton: TNewButton;
  DBConnectionTested: Boolean;
  DBConnectionSuccess: Boolean;

const
  SECRET_KEY = 'POS_SISTEMA_2025_SECRET';

{ Funciones auxiliares para hash }
function IntToHexCustom(Value: Cardinal; Digits: Integer): String;
var
  HexChars: String;
  I: Integer;
  Temp: Cardinal;
begin
  HexChars := '0123456789ABCDEF';
  Result := '';
  for I := Digits - 1 downto 0 do
  begin
    Temp := (Value shr (I * 4)) and $F;
    Result := Result + HexChars[Temp + 1];
  end;
end;

function SimpleHash(const S: String): String;
var
  I: Integer;
  Hash: Cardinal;
  C: Char;
begin
  Hash := 5381;
  for I := 1 to Length(S) do
  begin
    C := S[I];
    Hash := ((Hash shl 5) + Hash) + Ord(C);
  end;
  Result := IntToHexCustom(Hash, 8);
end;

function GenerateActivationCode(const LicenseKey: String): String;
var
  Data: String;
  Hash1, Hash2, Hash3, Hash4: String;
  FullHash: String;
begin
  Data := LicenseKey + SECRET_KEY;
  
  // Generar múltiples hashes para más caracteres
  Hash1 := SimpleHash(Data);
  Hash2 := SimpleHash(Data + '1');
  Hash3 := SimpleHash(Data + '2');
  Hash4 := SimpleHash(Data + '3');
  
  FullHash := UpperCase(Hash1 + Hash2 + Hash3 + Hash4);
  
  // Formatear como XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
  Result := Copy(FullHash, 1, 4) + '-' +
            Copy(FullHash, 5, 4) + '-' +
            Copy(FullHash, 9, 4) + '-' +
            Copy(FullHash, 13, 4) + '-' +
            Copy(FullHash, 17, 4) + '-' +
            Copy(FullHash, 21, 4) + '-' +
            Copy(FullHash, 25, 4) + '-' +
            Copy(FullHash, 29, 4);
end;

function ValidateLicenseFormat(const LicenseKey: String): Boolean;
var
  I, DashCount, PartLen: Integer;
begin
  Result := False;
  
  // Verificar longitud exacta: XXXX-XXXX-XXXX-XXXX (19 caracteres)
  if Length(LicenseKey) <> 19 then Exit;
  
  // Verificar posiciones de los guiones
  if (LicenseKey[5] <> '-') or (LicenseKey[10] <> '-') or (LicenseKey[15] <> '-') then Exit;
  
  // Verificar que las partes sean de 4 caracteres
  Result := True;
end;

function ValidateLicense(const LicenseKey, ActivationCode: String): Boolean;
var
  ExpectedCode: String;
begin
  Result := False;
  
  if not ValidateLicenseFormat(LicenseKey) then Exit;
  
  ExpectedCode := GenerateActivationCode(LicenseKey);
  
  Result := UpperCase(ActivationCode) = UpperCase(ExpectedCode);
end;

{ Función para probar conexión a MySQL usando Python }
function TestMySQLConnection(Host, Port, User, Password, Database: String): String;
var
  PythonScript: String;
  ScriptFile: String;
  ResultCode: Integer;
  TempDir: String;
  OutputFile: String;
  Output: AnsiString;
  Lines: TArrayOfString;
  I: Integer;
begin
  Result := 'ERROR|No se pudo ejecutar la prueba';
  
  try
    TempDir := ExpandConstant('{tmp}');
    ScriptFile := TempDir + '\test_mysql.py';
    OutputFile := TempDir + '\test_result.txt';
    
    { Eliminar archivos anteriores si existen }
    if FileExists(OutputFile) then
      DeleteFile(OutputFile);
    
    { Crear script Python temporal para probar conexión }
    PythonScript := 
      '# -*- coding: utf-8 -*-' + #13#10 +
      'import sys' + #13#10 +
      'import os' + #13#10 +
      '' + #13#10 +
      'output_file = r"' + OutputFile + '"' + #13#10 +
      '' + #13#10 +
      'try:' + #13#10 +
      '    import mysql.connector' + #13#10 +
      '    ' + #13#10 +
      '    # Intentar conexión' + #13#10 +
      '    conn = mysql.connector.connect(' + #13#10 +
      '        host="' + Host + '",' + #13#10 +
      '        port=' + Port + ',' + #13#10 +
      '        user="' + User + '",' + #13#10 +
      '        password=r"' + Password + '",' + #13#10 +
      '        database="' + Database + '",' + #13#10 +
      '        connect_timeout=5' + #13#10 +
      '    )' + #13#10 +
      '    ' + #13#10 +
      '    # Obtener versión' + #13#10 +
      '    cursor = conn.cursor()' + #13#10 +
      '    cursor.execute("SELECT VERSION()")' + #13#10 +
      '    version = cursor.fetchone()[0]' + #13#10 +
      '    cursor.close()' + #13#10 +
      '    conn.close()' + #13#10 +
      '    ' + #13#10 +
      '    # Escribir resultado' + #13#10 +
      '    with open(output_file, "w", encoding="utf-8") as f:' + #13#10 +
      '        f.write(f"EXITO|Conexion exitosa a MySQL {version}")' + #13#10 +
      '    ' + #13#10 +
      'except ImportError as e:' + #13#10 +
      '    with open(output_file, "w", encoding="utf-8") as f:' + #13#10 +
      '        f.write("ERROR|Libreria mysql-connector-python no instalada. Instale con: pip install mysql-connector-python")' + #13#10 +
      '    ' + #13#10 +
      'except mysql.connector.Error as e:' + #13#10 +
      '    with open(output_file, "w", encoding="utf-8") as f:' + #13#10 +
      '        f.write(f"ERROR|MySQL Error: {str(e)}")' + #13#10 +
      '    ' + #13#10 +
      'except Exception as e:' + #13#10 +
      '    with open(output_file, "w", encoding="utf-8") as f:' + #13#10 +
      '        f.write(f"ERROR|{str(e)}")' + #13#10;
    
    { Guardar script }
    if not SaveStringToFile(ScriptFile, PythonScript, False) then
    begin
      Result := 'ERROR|No se pudo crear el script de prueba';
      Exit;
    end;
    
    { Ejecutar Python directamente sin redirección }
    if not Exec('python', '"' + ScriptFile + '"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
    begin
      Result := 'ERROR|No se pudo ejecutar Python. Verifique que Python 3 este instalado y en PATH';
      Exit;
    end;
    
    { Esperar un momento para que el archivo se escriba }
    Sleep(500);
    
    { Leer resultado del archivo }
    if FileExists(OutputFile) then
    begin
      if LoadStringFromFile(OutputFile, Output) then
      begin
        Result := Trim(String(Output));
        if Result = '' then
          Result := 'ERROR|El archivo de resultado esta vacio';
      end
      else
        Result := 'ERROR|No se pudo leer el archivo de resultado';
    end
    else
      Result := 'ERROR|Python no genero archivo de resultado. Code: ' + IntToStr(ResultCode);
      
    { Limpiar archivos temporales }
    if FileExists(ScriptFile) then
      DeleteFile(ScriptFile);
    if FileExists(OutputFile) then
      DeleteFile(OutputFile);
    
  except
    Result := 'ERROR|Excepcion al ejecutar prueba de conexion';
  end;
end;

{ Manejador del botón "Probar Conexión" }
procedure TestConnectionButtonClick(Sender: TObject);
var
  TestResult: String;
  ResultParts: TArrayOfString;
  Status: String;
  Message: String;
begin
  DBTestResultMemo.Lines.Clear;
  DBTestResultMemo.Lines.Add('🔄 Probando conexión a MySQL...');
  DBTestResultMemo.Lines.Add('');
  DBTestResultMemo.Lines.Add('Host: ' + DBConfigPage.Values[0]);
  DBTestResultMemo.Lines.Add('Puerto: ' + DBConfigPage.Values[1]);
  DBTestResultMemo.Lines.Add('Usuario: ' + DBConfigPage.Values[2]);
  DBTestResultMemo.Lines.Add('Base de datos: ' + DBConfigPage.Values[4]);
  DBTestResultMemo.Lines.Add('');
  DBTestResultMemo.Lines.Add('Ejecutando prueba...');
  
  { Actualizar UI }
  WizardForm.Update;
  
  { Ejecutar prueba }
  TestResult := TestMySQLConnection(
    DBConfigPage.Values[0],  // Host
    DBConfigPage.Values[1],  // Port
    DBConfigPage.Values[2],  // User
    DBConfigPage.Values[3],  // Password
    DBConfigPage.Values[4]   // Database
  );
  
  { Procesar resultado }
  DBTestResultMemo.Lines.Add('');
  DBTestResultMemo.Lines.Add('─────────────────────────────────────');
  DBTestResultMemo.Lines.Add('');
  
  if Pos('EXITO|', TestResult) = 1 then
  begin
    Message := Copy(TestResult, 7, Length(TestResult) - 6);
    DBTestResultMemo.Lines.Add('✅ ' + Message);
    DBTestResultMemo.Lines.Add('');
    DBTestResultMemo.Lines.Add('Puede continuar con la instalación.');
    DBConnectionTested := True;
    DBConnectionSuccess := True;
  end
  else if Pos('ERROR|', TestResult) = 1 then
  begin
    Message := Copy(TestResult, 7, Length(TestResult) - 6);
    DBTestResultMemo.Lines.Add('❌ ERROR: ' + Message);
    DBTestResultMemo.Lines.Add('');
    DBTestResultMemo.Lines.Add('Sugerencias:');
    DBTestResultMemo.Lines.Add('• Verifique que MySQL esté instalado y ejecutándose');
    DBTestResultMemo.Lines.Add('• Revise los datos de conexión (host, puerto, usuario)');
    DBTestResultMemo.Lines.Add('• Asegúrese de que la base de datos existe');
    DBTestResultMemo.Lines.Add('• Verifique que el usuario tenga permisos');
    DBTestResultMemo.Lines.Add('');
    DBTestResultMemo.Lines.Add('Puede reintentar o continuar (configurar después).');
    DBConnectionTested := True;
    DBConnectionSuccess := False;
  end
  else
  begin
    DBTestResultMemo.Lines.Add('⚠️ Resultado inesperado:');
    DBTestResultMemo.Lines.Add(TestResult);
    DBTestResultMemo.Lines.Add('');
    DBTestResultMemo.Lines.Add('Puede continuar e intentar configurar después.');
    DBConnectionTested := True;
    DBConnectionSuccess := False;
  end;
end;

{ Manejador del botón "Reintentar" }
procedure RetryConnectionButtonClick(Sender: TObject);
begin
  { Resetear flags para forzar nueva prueba }
  DBConnectionTested := False;
  DBConnectionSuccess := False;
  DBTestResultMemo.Lines.Clear;
  DBTestResultMemo.Lines.Add('Presione "Probar Conexión" para iniciar la verificación.');
  DBTestResultMemo.Lines.Add('');
  DBTestResultMemo.Lines.Add('IMPORTANTE:');
  DBTestResultMemo.Lines.Add('• Esta prueba requiere Python 3 instalado');
  DBTestResultMemo.Lines.Add('• La librería mysql-connector-python debe estar instalada');
  DBTestResultMemo.Lines.Add('• Puede omitir esta prueba y configurar después');
  
  { Usar BackButtonClick en lugar de cambiar CurPageID directamente }
  WizardForm.BackButton.OnClick(WizardForm.BackButton);
end;

procedure InitializeWizard;
var
  StaticText: TNewStaticText;
  Memo: TNewMemo;
begin
  LicenseValid := False;
  
  { Página de LICENCIA (PRIMERO) }
  LicensePage := CreateInputQueryPage(wpWelcome,
    'Activación de Licencia', 'Ingrese su clave de licencia y código de activación',
    'Para instalar el Sistema POS necesita una licencia válida.');

  LicensePage.Add('Clave de Licencia (XXXX-XXXX-XXXX-XXXX):', False);
  LicensePage.Add('Código de Activación:', False);
  
  { Página de verificación de MySQL }
  MySQLInstalledPage := CreateCustomPage(LicensePage.ID,
    'Requisitos del Sistema', 'Verificación de MySQL Server');

  StaticText := TNewStaticText.Create(MySQLInstalledPage);
  StaticText.Parent := MySQLInstalledPage.Surface;
  StaticText.Caption := 'Este sistema requiere MySQL Server 8.0 o superior instalado.';
  StaticText.AutoSize := True;

  Memo := TNewMemo.Create(MySQLInstalledPage);
  Memo.Parent := MySQLInstalledPage.Surface;
  Memo.Top := StaticText.Top + StaticText.Height + 10;
  Memo.Width := MySQLInstalledPage.SurfaceWidth;
  Memo.Height := ScaleY(150);
  Memo.ReadOnly := True;
  Memo.ScrollBars := ssVertical;
  Memo.Lines.Add('REQUISITOS:');
  Memo.Lines.Add('');
  Memo.Lines.Add('1. MySQL Server 8.0 o superior');
  Memo.Lines.Add('   Descargar desde: https://dev.mysql.com/downloads/mysql/');
  Memo.Lines.Add('');
  Memo.Lines.Add('2. Base de datos creada (pos_db)');
  Memo.Lines.Add('');
  Memo.Lines.Add('3. Usuario con permisos de lectura/escritura');
  Memo.Lines.Add('');
  Memo.Lines.Add('NOTA: Si MySQL no está instalado, puede instalarlo después');
  Memo.Lines.Add('y configurar la aplicación siguiendo las instrucciones en:');
  Memo.Lines.Add('CONFIGURACION_BD.txt');

  { Página de configuración de base de datos }
  DBConfigPage := CreateInputQueryPage(MySQLInstalledPage.ID,
    'Configuración de Base de Datos', 'Ingrese los datos de conexión a MySQL',
    'Puede modificar estos valores después en: config\database.json');

  DBConfigPage.Add('Host (servidor):', False);
  DBConfigPage.Add('Puerto:', False);
  DBConfigPage.Add('Usuario:', False);
  DBConfigPage.Add('Contraseña:', True);
  DBConfigPage.Add('Nombre de BD:', False);

  { Valores predeterminados }
  DBConfigPage.Values[0] := 'localhost';
  DBConfigPage.Values[1] := '3306';
  DBConfigPage.Values[2] := 'root';
  DBConfigPage.Values[3] := '';
  DBConfigPage.Values[4] := 'pos_db';
  
  { Página de PRUEBA de conexión a base de datos }
  DBTestPage := CreateCustomPage(DBConfigPage.ID,
    'Prueba de Conexión', 'Verificar conexión a MySQL');
  
  DBConnectionTested := False;
  DBConnectionSuccess := False;

  StaticText := TNewStaticText.Create(DBTestPage);
  StaticText.Parent := DBTestPage.Surface;
  StaticText.Caption := 'Presione "Probar Conexión" para verificar que MySQL esté accesible.';
  StaticText.AutoSize := True;
  
  { Botón para probar conexión }
  DBTestButton := TNewButton.Create(DBTestPage);
  DBTestButton.Parent := DBTestPage.Surface;
  DBTestButton.Width := ScaleX(150);
  DBTestButton.Height := ScaleY(30);
  DBTestButton.Top := StaticText.Top + StaticText.Height + 10;
  DBTestButton.Left := 0;
  DBTestButton.Caption := 'Probar Conexión';
  DBTestButton.OnClick := @TestConnectionButtonClick;
  
  { Botón para reintentar (volver a configuración) }
  DBTestRetryButton := TNewButton.Create(DBTestPage);
  DBTestRetryButton.Parent := DBTestPage.Surface;
  DBTestRetryButton.Width := ScaleX(150);
  DBTestRetryButton.Height := ScaleY(30);
  DBTestRetryButton.Top := DBTestButton.Top;
  DBTestRetryButton.Left := DBTestButton.Left + DBTestButton.Width + ScaleX(10);
  DBTestRetryButton.Caption := 'Cambiar Configuración';
  DBTestRetryButton.OnClick := @RetryConnectionButtonClick;
  
  { Área de resultados }
  DBTestResultMemo := TNewMemo.Create(DBTestPage);
  DBTestResultMemo.Parent := DBTestPage.Surface;
  DBTestResultMemo.Top := DBTestButton.Top + DBTestButton.Height + 10;
  DBTestResultMemo.Width := DBTestPage.SurfaceWidth;
  DBTestResultMemo.Height := ScaleY(200);
  DBTestResultMemo.ReadOnly := True;
  DBTestResultMemo.ScrollBars := ssVertical;
  DBTestResultMemo.Lines.Add('Presione "Probar Conexión" para iniciar la verificación.');
  DBTestResultMemo.Lines.Add('');
  DBTestResultMemo.Lines.Add('IMPORTANTE:');
  DBTestResultMemo.Lines.Add('• Esta prueba requiere Python 3 instalado');
  DBTestResultMemo.Lines.Add('• La librería mysql-connector-python debe estar instalada');
  DBTestResultMemo.Lines.Add('• Puede omitir esta prueba y configurar después');
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  LicenseKey, ActivationCode: String;
begin
  Result := True;
  
  { Validar LICENCIA }
  if CurPageID = LicensePage.ID then
  begin
    LicenseKey := Trim(LicensePage.Values[0]);
    ActivationCode := Trim(LicensePage.Values[1]);
    
    if (LicenseKey = '') or (ActivationCode = '') then
    begin
      MsgBox('Por favor ingrese la clave de licencia y el código de activación.', mbError, MB_OK);
      Result := False;
      Exit;
    end;
    
    if not ValidateLicense(LicenseKey, ActivationCode) then
    begin
      MsgBox('La licencia o el código de activación son incorrectos.' + #13#10 + #13#10 +
             'Por favor verifique los datos e intente nuevamente.' + #13#10 + #13#10 +
             'Si el problema persiste, contacte a soporte técnico.', mbError, MB_OK);
      Result := False;
      Exit;
    end;
    
    LicenseValid := True;
    MsgBox('✓ Licencia válida' + #13#10 + #13#10 + 'La instalación continuará.', mbInformation, MB_OK);
  end;
  
  { Validar configuración de BD }
  if CurPageID = DBConfigPage.ID then
  begin
    { Validar que los campos no estén vacíos }
    if (DBConfigPage.Values[0] = '') or (DBConfigPage.Values[1] = '') or 
       (DBConfigPage.Values[2] = '') or (DBConfigPage.Values[4] = '') then
    begin
      MsgBox('Por favor complete todos los campos obligatorios.', mbError, MB_OK);
      Result := False;
    end;
  end;
  
  { Manejar página de prueba de conexión }
  if CurPageID = DBTestPage.ID then
  begin
    { Si no se ha probado la conexión, preguntar al usuario }
    if not DBConnectionTested then
    begin
      if MsgBox('No ha probado la conexión a la base de datos.' + #13#10 + #13#10 +
                '¿Desea continuar sin probar la conexión?' + #13#10 +
                '(Podrá configurarla después de la instalación)',
                mbConfirmation, MB_YESNO) = IDYES then
      begin
        Result := True;
      end
      else
      begin
        Result := False;
      end;
    end
    { Si se probó pero falló, advertir al usuario }
    else if not DBConnectionSuccess then
    begin
      if MsgBox('La prueba de conexión falló.' + #13#10 + #13#10 +
                '¿Desea continuar de todas formas?' + #13#10 +
                '(Podrá configurar la base de datos después)',
                mbConfirmation, MB_YESNO) = IDYES then
      begin
        Result := True;
      end
      else
      begin
        Result := False;
      end;
    end
    { Si fue exitosa, continuar }
    else
    begin
      Result := True;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: string;
  LicenseFile: string;
  ConfigContent: TStringList;
begin
  if CurStep = ssPostInstall then
  begin
    { Crear archivo de configuración de base de datos }
    ConfigFile := ExpandConstant('{app}\config\database.json');
    ConfigContent := TStringList.Create;
    try
      ConfigContent.Add('{');
      ConfigContent.Add('    "host": "' + DBConfigPage.Values[0] + '",');
      ConfigContent.Add('    "port": ' + DBConfigPage.Values[1] + ',');
      ConfigContent.Add('    "user": "' + DBConfigPage.Values[2] + '",');
      ConfigContent.Add('    "password": "' + DBConfigPage.Values[3] + '",');
      ConfigContent.Add('    "database": "' + DBConfigPage.Values[4] + '",');
      ConfigContent.Add('    "charset": "utf8mb4"');
      ConfigContent.Add('}');
      
      ConfigContent.SaveToFile(ConfigFile);
    finally
      ConfigContent.Free;
    end;
    
    { Guardar información de licencia }
    if LicenseValid then
    begin
      LicenseFile := ExpandConstant('{app}\config\license.json');
      ConfigContent := TStringList.Create;
      try
        ConfigContent.Add('{');
        ConfigContent.Add('    "license_key": "' + LicensePage.Values[0] + '",');
        ConfigContent.Add('    "activation_code": "' + LicensePage.Values[1] + '",');
        ConfigContent.Add('    "activation_date": "' + GetDateTimeString('yyyy-mm-dd', #0, #0) + '",');
        ConfigContent.Add('    "status": "active"');
        ConfigContent.Add('}');
        
        ConfigContent.SaveToFile(LicenseFile);
      finally
        ConfigContent.Free;
      end;
    end;
  end;
end;

[UninstallDelete]
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\backups"
Type: filesandordirs; Name: "{app}\__pycache__"
