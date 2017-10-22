import QtQuick 1.0

Rectangle {
    id: root
    width: 275
    height: 120
	color: "#ffffff"
    objectName: "root"

    /* custom properties */
    property double contentMargin: 0.1*root.height
    property double contentRadius: 3
    property int maxTweetLength: 140
    property int dialogDuration: environment.duration*10
    signal submitTweet(string tweetPostText)
    signal safeQuit()

    Rectangle {
        id: tweetComposer
        radius: root.contentRadius
        width: parent.width - (2*root.contentMargin)
        height: 0.5*parent.height
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: root.contentMargin

        Rectangle {
            id: tweetInfoPanel
            width: parent.width; height:5
            anchors.left: parent.left
            anchors.bottom: parent.bottom

            Text {
                text: environment.last
                anchors.left: parent.left
                anchors.top: parent.top
                font.pointSize: 6.25
            }

            Text {
                id: tweetTextRemainChars
                text: "140"
                anchors.right: parent.right
                anchors.top: parent.top
                font.pointSize: 6.25
            }
        }

        Rectangle {
            id: tweetText
            width:  parent.width
            height: parent.height-tweetInfoPanel.height-(root.contentMargin/2)
            radius: root.contentRadius
            border.color: "#78909C"
            border.width: 1
            color: "transparent"

            Flickable {
                 id: flick

                 width: parent.width;
                 height: parent.height;
                 contentWidth: parent.width
                 contentHeight: parent.height
                 clip: true

                 anchors.topMargin: 4
                 anchors.leftMargin: 4
                 anchors.rightMargin: 4
                 anchors.bottomMargin: 4
                 anchors.top: parent.top
                 anchors.left: parent.left
                 anchors.right: parent.right
                 anchors.bottom: parent.bottom

                 function ensureVisible(r) {
                     if (contentX >= r.x)
                         contentX = r.x;
                     else if (contentX+width <= r.x+r.width)
                         contentX = r.x+r.width-width;
                     if (contentY >= r.y)
                         contentY = r.y;
                     else if (contentY+height <= r.y+r.height)
                         contentY = r.y+r.height-height;
                 }

                 TextEdit {
                     focus: true
                     id: tweetTextContent
                     width: flick.width
                     height: flick.height
                     wrapMode: TextEdit.Wrap
                     font.pointSize: 8

                    function updateCountAndVisible(tweet) {
                        var diff = root.maxTweetLength - tweet.length

                        placeholder.visible = diff === root.maxTweetLength;
                        tweetTextRemainChars.text = diff;
                        
                        if (diff < 0)
                            tweetTextRemainChars.color = "#DD2C00";
                        else {
                            tweetTextRemainChars.color = "#78909C";
                            progress.stop(); progress.reInit();
                        }
                     }

                     onTextChanged: updateCountAndVisible(text)
                     onCursorRectangleChanged: flick.ensureVisible(cursorRectangle)

                     Text {
                        id: placeholder
                        text: String(environment.user) + ", What are you doing ?"
                        font.pointSize: 8
                        color: "#78909C"
                     }
                 }
             }
        }
    }

    Rectangle {
        id: action_panel
        width: parent.width - (2*root.contentMargin)
        height: 0.2*parent.height
        anchors.left: parent.left
        anchors.leftMargin: root.contentMargin
        anchors.top: tweetComposer.bottom
        anchors.topMargin: root.contentMargin

        Rectangle {
            id: tweetButton
            width: 0.28*parent.width
            height: parent.height
            color: "#0084b4"
            anchors.top: parent.top
            anchors.right: parent.right
            radius: root.contentRadius

            Text {
                text: "Tweet"
                color: "#fff"
                font.pointSize: 9
                anchors.centerIn: parent
            }

            MouseArea {
                id: tweetButtonMA
                enabled: true
                anchors.fill: parent
                onClicked: submitTweet(tweetTextContent.text)   
            }

            Action {
                shortcut: "Ctrl+Enter"
                onTriggered: submitTweet(tweetTextContent.text)
            }
        }

        Rectangle {
            id: cancelTweet
            width: tweetButton.width
            height: parent.height
            color: "#78909C"
            anchors.top: parent.top
            anchors.right: tweetButton.left
            anchors.rightMargin: root.contentMargin/2
            radius: root.contentRadius

            Text {
                text: "Cancel"
                color: "#fff"
                font.pointSize: 9
                x: (parent.width-width)/2;
                y: ((parent.height-height)/2);
            }

            MouseArea {
                objectName: "cancelTweet"
                anchors.fill: parent
            }
        }

        Rectangle {
            id: prefsButton
            width: parent.height
            height: parent.height
            color: "#78909C"
            anchors.top: parent.top
            anchors.left: parent.left
            radius: root.contentRadius

            Text {
                text: "⚙"
                color: "#fff"
                font.pointSize: 12
                x: (parent.width-width)/2;
                y: (parent.height-height)/2;
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    overlayBanner.text = "please run glo-conf"
                    overlayBanner.visible = true
                    overlayBanner.color = "#000000"
                }
            }
        }
    }

    Rectangle {
        id: progress
        height: 4
        width: root.width
        color: "#004D40"
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        property int counter: 0        

        Behavior on width {
            NumberAnimation {
                duration: progressTimer.interval
                easing.type: Easing.Linear
            }
        }

        Timer {
            id: progressTimer
            running: true;
            repeat: true
            interval: root.dialogDuration  // total duration in secs into 10
            onTriggered: onTriggerCallback()
        
            function onTriggerCallback() {
                progress.counter += 1
                if (progress.counter > 100)
                    root.safeQuit()
                else
                    progress.width = (1-(progress.counter/100))*root.width
            }
        }

        function reInit() {
            progress.counter = 0
            progress.width = root.width
        }

        function stop() {
            progressTimer.stop()
        }
    }

    Rectangle {
        id: overlayBanner
        width: root.width
        height: root.height-action_panel.y
        anchors.bottom: progress.bottom
        color: "#0084b4"
        visible: false
        property string text: "Login with Twitter!"

        Text {
            color: "#ffffff"
            text: overlayBanner.text
            anchors.centerIn: parent
        }

        MouseArea {
            anchors.fill: parent

            onClicked: {
                overlayBanner.visible = false
            }
        }
    }
}
