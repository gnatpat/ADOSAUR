(function () {
  'use strict';
  var formidable = require('formidable'),
    fs         = require('fs'),
    mailer     = require('../email.js'),
    child_process = require('child_process'),
    exec = child_process.exec,
    dlevels = {
      "0": "Minimal depression",
      "1": "Mild depression",
      "2": "Moderate depression",
      "3": "Severe depression"
    };

  // function to majority vote the results obtained from the audio and video CNN
  function majorityVote(audioResult, videoResult) {
      // initiliaze the result array and parse the outputs of audio and video
      var resultArr = [0,0,0,0];
      var audioArr = audioResult.split('{')[1].split('}')[0].split(',');
      var videoArr = videoResult.split('{')[1].split('}')[0].split(',');

      console.log(audioArr)
      console.log(videoArr)

      // build the result array from the audio results
      var arrayLength = audioArr.length;
      for (var i = 0; i < arrayLength; i++) {
        var splitElem = audioArr[i].split(':');
        var index = parseInt(splitElem[0]);
        var result = parseInt(splitElem[1]);
        resultArr[index] = resultArr[index] + result;
      }

      // build the result array from the video results
      var arrayLength = videoArr.length;
      for (var i = 0; i < arrayLength; i++) {
        var splitElem = videoArr[i].split(':');
        var index = parseInt(splitElem[0]);
        var result = parseInt(splitElem[1]);
        resultArr[index] = resultArr[index] + result;
      }

      console.log(resultArr)
      return resultArr;
  }

  module.exports = function (router, models, passport) {
    var Test = models.test;

    router.post('/upload/video', function (req, res) {

      var form = new formidable.IncomingForm();
      form.uploadDir = '../../tmp';

      form.on('error', function (err) {
        console.log(err);
      });

      form.on('aborted', function () {
        console.log('aborted');
      });


      // handle the incoming form data
      form.parse(req, function (err, fields, files) {
          // get the uploaded video path and initiliaze audio path
          var videoFilePath = files.video.path;
          var audioFilePath = '../../tmp/audio.wav'

          // extract the audio from the video as wav
          exec('avconv -i ' + videoFilePath + ' -ar 16000 -ac 1 ' + audioFilePath, function(err,stdout,stderr) {
              // run the python script to make a prediction on the video and audio files
              exec('python ../../cnn/predict.py ' + videoFilePath + ' ' + audioFilePath, function(err,stdout,stderr) {
              if (err) {
                console.log('Child process exited with error code', err.code);
                return
              }
              // get the results returned from the python script
              var results = stdout.split('\n')
              var audioResult = results[0].replace(/\s+/g, '');
              var videoResult = results[1].replace(/\s+/g, '');

              // majority vote the results
              var resultArr = majorityVote(audioResult, videoResult);

              // return the corresponding predicted depression level
              var prediction = resultArr.indexOf(Math.max.apply(Math, resultArr));
              res.redirect('/#/upload?prediction=' + prediction);
              });
          });
      });
    });

    router.post('/upload/test/:testID', function (req, res) {
      // save the video file
      var file = req.body.files.video,
        testID = req.params.testID,
        docEmail = req.body.docEmail,
        patient = req.body.patient;

      var fileRootName = file.name.split('.').shift(),
       fileExtension = file.name.split('.').pop(),
       filePathBase =  '../../tmp/',
       fileRootNameWithBase = filePathBase + fileRootName,
       videoFilePath = fileRootNameWithBase + '.' + fileExtension,
       fileID = 2,
       fileBuffer;

       while (fs.existsSync(videoFilePath)) {
           videoFilePath = fileRootNameWithBase + '(' + fileID + ').' + fileExtension;
           fileID += 1;
       }

       file.contents = file.contents.split(',').pop();

       fileBuffer = new Buffer(file.contents, "base64");

       fs.writeFileSync(videoFilePath, fileBuffer);

       //  save the audio file
       var file = req.body.files.audio;

       var fileRootName = file.name.split('.').shift(),
        fileExtension = file.name.split('.').pop(),
        filePathBase =  '../../tmp/',
        fileRootNameWithBase = filePathBase + fileRootName,
        audioFilePath = fileRootNameWithBase + '.' + fileExtension,
        fileID = 2,
        fileBuffer;

        while (fs.existsSync(audioFilePath)) {
            audioFilePath = fileRootNameWithBase + '(' + fileID + ').' + fileExtension;
            fileID += 1;
        }

        file.contents = file.contents.split(',').pop();

        fileBuffer = new Buffer(file.contents, "base64");

        fs.writeFileSync(audioFilePath, fileBuffer);

        // initiliase the paths for the video and audio files
        var newVideoFilePath = '../../tmp/video.mp4'
        var newAudioFilePath = '../../tmp/audio.wav'

        // convert the video and audio files to mp4 and wav respectively
        exec('avconv -i ' + videoFilePath + ' -vf scale=640:480 ' + newVideoFilePath, function(err,stdout,stderr) {
          exec('avconv -i ' + audioFilePath + ' -ar 16000 -ac 1 ' + newAudioFilePath, function(err, stdout, stderr) {
              // run the python script to make a prediction on the video and audio files
              exec('python ../../cnn/predict.py ' + newVideoFilePath + ' ' + newAudioFilePath, function(err,stdout,stderr) {
                if (err) {
                  console.log('Child process exited with error code', err.code);
                  console.log(stderr)
                  return
                }
                // get the results returned from the python script
                var results = stdout.split('\n')

                var audioResult = results[0].replace(/\s+/g, '');
                var videoResult = results[1].replace(/\s+/g, '');

                // majority vote the results
                var resultArr = majorityVote(audioResult, videoResult);

                // get the predicted depression level
                var prediction = resultArr.indexOf(Math.max.apply(Math, resultArr));

                // update the corresponding test result
                Test.findByIdAndUpdate(testID, {$set: {"result": prediction} }, function (err) {
                  if (err) {
                    res.status(500).json({error: "Failed to update test result"});
                  }
                });

                // send an email to the doctor with result
                mailer.sendMail({
                  to: docEmail,
                  subject: 'Test results',
                  text: "Patient " + patient.first_name + " " + patient.last_name +
                  " finished his test. His estimated depression level is: " + prediction + " " + dlevels[prediction]
                });

                res.status(200).json({message: "Sent tests results to doctor"});
                });
            });
          });

    });
  };

}());
