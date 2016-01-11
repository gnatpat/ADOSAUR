(function () {
  'use strict';

  var mailer = require('../email.js'); // to send emails

  module.exports = function (router, models, passport) {
    var Test = models.test;

    router.put('/test/send/', function (req, res) {
      console.log(req.body);
      var test = new Test();
      test.doctor  = req.body.doctor;
      test.patient = req.body.patient;
      test.text    = req.body.test.textID;
      test.type    = req.body.test.type;
      test.result  = NaN;

      test.save(function (err, test) {
        if (err) {
          res.status(500).json({error: 'Failed to create test'});
        }
        var link = 'http://127.0.0.1/#/test/' + test._id;
        mailer.sendMail({
          to: req.body.to,
          subject: 'Test',
          text: req.body.test.emailMsg + '   ' + link
        });
        res.status(200).json({meassage: 'Created test and sent email'});
      });
    });
  };
}());
