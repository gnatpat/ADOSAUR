(function () {
  var express = require('express'),
      formidable = require('formidable'),
      app = express(),
      server;

  /* Wire-up API routes */
  express.dirname = __dirname;
  require('./routes.js')(app, express);

  var server = app.listen(8080, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('ADOSAUR app listening at http://%s:%s', host, port);
    app.post('/upload', function(req, res) {
      // parse a file upload
      var form = new formidable.IncomingForm();
      form.uploadDir = 'tmp';


      form.parse(req, function(err, fields, files) {
        console.log("Evaluating BDI for " + files.file.path);
        var depressed = evaluateBDI(files.file.path)
        res.writeHead(200, {'content-type': 'text/plain'});
        res.end("" + depressed);
      });

      return;
    });
  });

  function evaluateBDI(filePath) {
    return 0;
  }
}());
