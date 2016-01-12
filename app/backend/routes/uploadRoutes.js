(function () {
  'use strict';
  var formidable = require('formidable'),
      fs         = require('fs');

  module.exports = function (router, models, passport) {

  	router.post('/upload/video', function(req, res) {

  		var form = new formidable.IncomingForm();
      form.uploadDir = '../../tmp';

      form.on('file', function(name, file) {
      });

      form.on('error', function(err) {
        console.log(err);
      });

      form.on('aborted', function() {
        console.log('aborted');
      });

      // TODO: feed the video to the cnn -
      // simulating computation by waiting 5 seconds for now
      setTimeout(function(){
        form.parse(req, function (err, fields, files) {

        });
        var prediction = Math.floor(Math.random() * 3) + 1;
        res.redirect('/#/upload?prediction=' + prediction);

      }, 5000);
  	});

    router.post('/upload/test', function(req, res) {
      // save the video file
      var file = req.body.files.video;

      var fileRootName = file.name.split('.').shift(),
       fileExtension = file.name.split('.').pop(),
       filePathBase =  '../../tmp/',
       fileRootNameWithBase = filePathBase + fileRootName,
       filePath = fileRootNameWithBase + '.' + fileExtension,
       fileID = 2,
       fileBuffer;

       while (fs.existsSync(filePath)) {
           filePath = fileRootNameWithBase + '(' + fileID + ').' + fileExtension;
           fileID += 1;
       }

       file.contents = file.contents.split(',').pop();

       fileBuffer = new Buffer(file.contents, "base64");

       fs.writeFileSync(filePath, fileBuffer);

       //  save the audio file
       var file = req.body.files.audio;

       var fileRootName = file.name.split('.').shift(),
        fileExtension = file.name.split('.').pop(),
        filePathBase =  '../../tmp/',
        fileRootNameWithBase = filePathBase + fileRootName,
        filePath = fileRootNameWithBase + '.' + fileExtension,
        fileID = 2,
        fileBuffer;

        while (fs.existsSync(filePath)) {
            filePath = fileRootNameWithBase + '(' + fileID + ').' + fileExtension;
            fileID += 1;
        }

        file.contents = file.contents.split(',').pop();

        fileBuffer = new Buffer(file.contents, "base64");

        fs.writeFileSync(filePath, fileBuffer);


        // TODO: feed the video and audio files to cnn and get output and save
        // the tests results and notify the doctor
        res.status(200).json({message: "Sent tests results to doctor"});

    });
  };

}());