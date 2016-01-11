(function () {
  'use strict';

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
    require('./testRoutes.js')(router, models, passport);
    require('./uploadRoutes.js')(router, models, passport);

    /* catches any routes that are not defined */
    router.use(function (req, res) {
      res.status(500).json({
        error: 'Route not found!'
      });
    });

    app.use('/api', router);
  };
}());
