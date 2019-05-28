; Script generated by the HM NIS Edit Script Wizard, then edited manually by David Jablonski.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "HTA"
!define PRODUCT_VERSION "0.2.2"
!define PRODUCT_PUBLISHER "David Jablonski"
!define PRODUCT_WEB_SITE "https://github.com/jablonsk19/HTA"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "Install-HTA.exe"
InstallDir "$PROGRAMFILES\HTA"
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer

  File /r "C:\Users\dterm\PycharmProjects\HTA\HTA\dist\hta\*"

  CreateDirectory "$SMPROGRAMS\HTA"
  CreateShortCut "$SMPROGRAMS\HTA\HTA.lnk" "$INSTDIR\hta.exe"
  CreateShortCut "$DESKTOP\HTA.lnk" "$INSTDIR\hta.exe" "" "$INSTDIR\hta.exe" 0
SectionEnd

Section -AdditionalIcons
  SetOutPath $INSTDIR
  CreateDirectory "$SMPROGRAMS\HTA"
  CreateShortCut "$SMPROGRAMS\HTA\Uninstall.lnk" "$INSTDIR\Uninstall-HTA.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\Uninstall-HTA.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall-HTA.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$SMPROGRAMS\HTA\HTA.lnk"
  Delete "$DESKTOP\HTA.lnk"

  Delete "$SMPROGRAMS\HTA\Uninstall.lnk"

  RMDir /r /REBOOTOK $INSTDIR

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd
