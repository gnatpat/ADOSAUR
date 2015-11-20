(function () {
  // api routes go here
  module.exports = function (app, express) {

    // serve static
    app.use(express.static(express.dirname + '/../Frontend'));
    /* gets a router instance */
    var router = express.Router();

    router.get('/', function (req, res) {
      res.status(200).json({
        message: 'ADOSAUR api running',
        data: 'Test data'
      });
    });

    /* catches any routes that are not defined */
    router.use(function (req, res) {
      res.status(500).json({
        error: 'Route not found!'
      });
    });

    app.use('/api', router);
  }
}());
