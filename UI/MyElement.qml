import QtQuick 2.15
Rectangle {
    width:777 
    height:1700
    color: "#00000000"
    border.color: "#00000000"
    Image {
        source:"MyElement_images/pasted_layer_copy.png"
        id:pasted_layer_copy
        x:3 ; y:1007
        width:777 
        height:678 
    }
    Image {
        source:"MyElement_images/pasted_layer.png"
        id:pasted_layer
        x:3 ; y:287
        width:777 
        height:678 
    }
    Image {
        source:"MyElement_images/background.png"
        id:background
        x:0 ; y:0
        width:767 
        height:242 
    }
    Text {
        text:'LU 25/10' 
        font.pixelSize:120 
        color:Qt.rgba(0, 0, 0, 1)
        id:date
        x:116 ; y:24
        width:562 
        height:208 
    }
    Text {
        text:'None' 
        font.pixelSize:120 
        color:Qt.rgba(0, 0, 0, 1)
        id:dahl_de_lentilles
        x:112 ; y:742
        width:562 
        height:208 
    }
    Text {
        text:'None' 
        font.pixelSize:120 
        color:Qt.rgba(0, 0, 0, 1)
        id:tajine_vegan
        x:112 ; y:1464
        width:562 
        height:208 
    }
    Image {
        source:"MyElement_images/image1.png"
        id:image1
        x:122 ; y:300
        width:548 
        height:442 
    }
    Image {
        source:"MyElement_images/image2.png"
        id:image2
        x:124 ; y:1024
        width:540 
        height:442 
    }
}
