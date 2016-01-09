(function () {
  'use strict';
  var formidable = require('formidable'),
    evaluateBDI  = require('../utils.js').evaluateBDI;

  // api routes go here
  module.exports = function (app, express, models, passport) {
    // serve static
    app.use(express.static(express.dirname + '/../frontend'));
    /* gets a router instance */
    var router = express.Router();

    router.get('/', function (req, res) {
      res.status(200).json({
        message: 'ADOSAUR api running',
        data: 'Test data'
      });
    });

    // Import other routes into same file
    require('./loginRoutes.js')(router, models, passport);
    require('./userRoutes.js')(router, models, passport);
    require('./textRoutes.js')(router, models, passport);
    require('./recordRoutes.js')(router, models, passport);
    app.post('/upload', function (req, res) {
      // parse a file upload
      var form = new formidable.IncomingForm();
      form.uploadDir = '../../tmp';

      form.parse(req, function (err, fields, files) {
        console.log("Evaluating BDI for " + files.file.path);
        evaluateBDI(files.file.path, function (result) {
          res.writeHead(200, {'content-type': 'text/json'});
          console.log("Sending " + result);
          res.end(JSON.stringify({"data": result}));
        });
      });

      return;
    });

    /* catches any routes that are not defined */
    router.use(function (req, res) {
      res.status(500).json({
        error: 'Route not found!'
      });
    });

    app.use('/api', router);
  };
}());
