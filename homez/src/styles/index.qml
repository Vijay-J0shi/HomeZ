import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.DeepPurple
    visibility: Qt.WindowFullScreen
    title: "HomeZ"
    Item {
        anchors.fill: parent

        Loader {
            id: sidebarLoader
            sourceComponent: {
                // Load the sidebar component only when the width is greater than 324
                if (parent.width > 324)
                    return sidebarComponent;
                else
                    return null;
            }

            onStatusChanged: {
                if (status === Loader.Ready) {
                    // Adjust the width of the main content when the sidebar is hidden
                    mainContent.width = parent.width;
                }
            }
        }

        Rectangle {
            id: mainContent
            width: parent.width
            height: parent.height
            color: "#0e1217"

            // Main content goes here
            Text {
                anchors.centerIn: parent
                text: "Sidebar"
            }
        }

        Component {
            id: sidebarComponent

            Rectangle {
                width: parent.width * 0.2
                height: parent.height
                color: "lightblue"

                // Sidebar content goes here
                Text {
                    anchors.centerIn: parent
                    text: "Sidebar"
                }
            }
        }

        onWidthChanged: {
            // Reload the sidebar when the window width changes
            sidebarLoader.sourceComponent = (width > 324) ? sidebarComponent : null;
        }
    }

       
}

