import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    width: 640
    height: 480
    visible: true
    color: "#c8e896"
    title: qsTr("Hello World")

    Image {
        id: image
        x: 223
        y: 24
        width: 194
        height: 129
        source: "../icon_menu.png"
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: image1
        x: 254
        y: 168
        width: 133
        height: 119
        source: "../icon_historique.png"
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: image2
        x: 197
        y: 265
        width: 246
        height: 209
        source: "../icon_recettes.png"
        fillMode: Image.PreserveAspectFit
    }

}
