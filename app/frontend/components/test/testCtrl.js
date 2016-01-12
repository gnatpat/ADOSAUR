(function () {
  'use strict';
  var adosaur = angular.module('adosaur');
  adosaur.controller('testCtrl', ['$scope', '$http', function ($scope, $http) {

    var startRecording = document.getElementById('start-recording');
    var stopRecording = document.getElementById('stop-recording');
    var cameraPreview = document.getElementById('camera-preview');

    var recordingClasses = startRecording.className;

    var audio = document.querySelector('audio');

    var isFirefox = !!navigator.mozGetUserMedia;

    var recordAudio, recordVideo;
    startRecording.onclick = function() {

        navigator.getUserMedia({
                audio: true,
                video: true
            }, function(stream) {
                cameraPreview.src = window.URL.createObjectURL(stream);
                console.log(cameraPreview.src)
                cameraPreview.play();

                recordAudio = RecordRTC(stream, {
                    bufferSize: 16384
                });

                if (!isFirefox) {
                    recordVideo = RecordRTC(stream, {
                        type: 'video'
                    });
                }

                recordAudio.startRecording();

                if (!isFirefox) {
                    recordVideo.startRecording();
                }

            }, function(error) {
                alert(JSON.stringify(error));
            });
    };


    stopRecording.onclick = function() {


        $('#sentTest').openModal();


        recordAudio.stopRecording(function() {
            if (isFirefox) onStopRecording();
        });

        if (!isFirefox) {
            recordVideo.stopRecording();
            onStopRecording();
        }

        function onStopRecording() {
            recordAudio.getDataURL(function(audioDataURL) {
                if (!isFirefox) {
                    recordVideo.getDataURL(function(videoDataURL) {
                        postFiles(audioDataURL, videoDataURL);
                    });
                } else postFiles(audioDataURL);
            });
        }
    };

    var fileName;

    function postFiles(audioDataURL, videoDataURL) {
        fileName = getRandomString();
        var files = { };

        files.audio = {
            name: fileName + (isFirefox ? '.webm' : '.wav'),
            type: isFirefox ? 'video/webm' : 'audio/wav',
            contents: audioDataURL
        };

        if (!isFirefox) {
            files.video = {
                name: fileName + '.mp4',
                type: 'video/mp4',
                contents: videoDataURL
            };
        }

        files.isFirefox = isFirefox;

        cameraPreview.src = '';

        var response = $http({
          method: 'POST',
          url: '/api/upload/test',
          data: {files: files}
        });

        response.success(function (data, status, headers, config) {
          console.log('Success');
          $('#thank-you').css('visibility', 'visible');
          $('#exit').css('visibility', 'visible');
        });

        response.error(function (data, status, headers, config) {
          console.log('Fail');
        });

    }

    window.onbeforeunload = function() {
    };

    function getRandomString() {
        if (window.crypto) {
            var a = window.crypto.getRandomValues(new Uint32Array(3)),
                token = '';
            for (var i = 0, l = a.length; i < l; i++) token += a[i].toString(36);
            return token;
        } else {
            return (Math.random() * new Date().getTime()).toString(36).replace( /\./g , '');
        }
    }


  }]);
}());
