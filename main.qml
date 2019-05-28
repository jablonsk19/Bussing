import QtQuick 2.5
import QtQuick.Layouts 1.2
import QtQuick.Dialogs 1.3
import QtQuick.Controls 2.2

ApplicationWindow {
    visible: true
    width: 600
    height: 638
    maximumWidth: 600
    maximumHeight: 638
    minimumWidth: 600
    minimumHeight: 638
    title: "HTA - GUI"

    //color: "#AAAAAA"

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#AAAACC" }
            GradientStop { position: 1.0; color: "#6666AA" }
        }
    }

    ColumnLayout {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 9

        Image {
            source: "./HTA Logo.png"
        }

        RowLayout {
            Text {
                font.pointSize: 10
                text: qsTr("SDAS (m)")
            }

            // Input field of the SDAS
            TextField {
                font.pointSize: 10
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
                expDialog.open()
            }
        }
        FileDialog {
            id: expDialog
            selectFolder: true
            nameFilters: ["DATAPLOT files (*.exp)"]
            title: "Please choose the working folder"
            folder: "file:\\C:\\"
            onAccepted: {
                console.log("You chose: " + expDialog.fileUrl)
            }
            onRejected: {
                console.log("Canceled")
            }
        }

        Text {
            font.pointSize: 10
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
                    mainFileFirstError.open()
                } else {
                    console.log(expDialog.url)
                    mainDialog.open()
                }
            }
        }
        Popup {
            id: mainFileFirstError
            x: 150
            y: 100
            width: 300
            height: 100
            modal: true
            focus: true
            closePolicy: Popup.CloseOnEscape

            ColumnLayout {
                anchors.fill: parent
                Text {
                    font.pointSize: 10
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
            font.pointSize: 10
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


        // Here we see the result of run
        Text {
            font.pointSize: 10
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

