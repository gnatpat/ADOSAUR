/*node: true*/
(function () {
  'use strict';
  var express = require('express'),
    app = express(),
    server;

  /* Wire-up API routes */
  express.dirname = __dirname;
  require('./routes.js')(app, express);

  server = app.listen(8080, function () {
    var host = server.address().address,
      port = server.address().port;

    console.log('ADOSAUR app listening at http://%s:%s', host, port);
  });


}());
