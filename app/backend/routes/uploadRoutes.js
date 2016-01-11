(function () {
  'use strict';
  var formidable = require('formidable');

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
        
        res.redirect('/#/upload?prediction=' + 3);

      }, 5000);

      

      
  	});
  };

}());

