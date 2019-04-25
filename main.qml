import QtQuick 2.5
import QtQuick.Layouts 1.2
import QtQuick.Dialogs 1.3
import QtQuick.Controls 2.2

ApplicationWindow {
    visible: true
    width: 600
    height: 300
    maximumWidth: 600
    maximumHeight: 300
    minimumWidth: 600
    minimumHeight: 300
    title: "HTA - GUI"
    color: "#AAAAAA"

    ColumnLayout {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 9

        RowLayout {
            Text {
                text: qsTr("SDAS")
            }

            // Input field of the SDAS
            TextField {
                id: sdas
                implicitWidth: 200
            }
        }

        Button {
            height: 40
            Layout.fillWidth: true
            text: qsTr("Browse for working folder")

            Layout.columnSpan: 2

            onClicked: {
                expDialog.visible = true
            }
        }
        FileDialog {
            id: expDialog
            selectFolder: true
            nameFilters: ["DATAPLOT files (*.exp)"]
            title: "Please choose the working folder"
            folder: "file:\\C:\\Users\\dterm\\PycharmProjects\\HTA\\Inno Demo Folder"
            onAccepted: {
                console.log("You chose: " + expDialog.fileUrl)
            }
            onRejected: {
                console.log("Canceled")
            }
        }

        Text {
            id: expFilesText
            text: qsTr("No folder chosen.")
        }
        Connections {
            target: expDialog

            onAccepted: {
                expFilesText.text = "Folder chosen: " + expDialog.fileUrl
            }
        }

        Button {
            height: 40
            Layout.fillWidth: true
            text: qsTr("Select Main File")

            Layout.columnSpan: 2

            onClicked: {
                if(expDialog.fileUrl == "")
                {
                    mainFileFirstError.visible = true
                } else {
                    console.log(expDialog.url)
                    mainDialog.visible = true
                }
            }
        }
        Popup {
            id: mainFileFirstError
            x: 175
            y: 100
            width: 250
            height: 100
            modal: true
            focus: true
            closePolicy: Popup.CloseOnEscape

            ColumnLayout {
                anchors.fill: parent
                Text {
                    anchors.horizontalCenter: parent.center
                    text: qsTr("Please select a working folder first.")
                }
                Button {
                    anchors.verticalCenter: parent.center
                    anchors.horizontalCenter: parent.center
                    height: 40
                    width: 70
                    text: qsTr("Okay")

                    onClicked: {
                        mainFileFirstError.visible = false
                    }
                }
            }
        }
        FileDialog {
            id: mainDialog
            nameFilters: ["DATAPLOT files (*.exp)"]
            title: "Please choose the DATAPLOT file plotting overall chemistry"
            folder: "C:\\Users\\dterm\\PycharmProjects\\HTA\\Inno Demo folder\\"
            onAccepted: {
                console.log("You chose: " + mainDialog.fileUrl)
            }
            onRejected: {
                console.log("Canceled")
            }
        }
        Connections {
            target: expDialog

            onAccepted: {
                mainDialog.folder = expDialog.fileUrl
            }
        }

        Text {
            id: mainFileText
            text: qsTr("No file chosen.")
        }
        Connections {
            target: mainDialog

            onAccepted: {
                mainFileText.text = "File chosen: " + mainDialog.fileUrl
            }
        }


        Button {
            height: 40
            Layout.fillWidth: true
            text: qsTr("Run Computation")

            Layout.columnSpan: 2

            onClicked: {
                gui.run(expDialog.fileUrl, mainDialog.fileUrl, sdas.text)
            }
        }

        Text {
            text: qsTr("")
        }

        // Here we see the result of run
        Text {
            id: runResult
        }

    }

    // Here we take the result of run
    Connections {
        target: gui

        // Run signal handler
        onRunResult: {
            // run was set through arguments=['run']
            runResult.text = run
        }

    }
}

