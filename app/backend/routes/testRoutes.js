(function () {
  'use strict';

  var mailer = require('../email.js'), // to send emails
      ip     = require('ip')

  module.exports = function (router, models, passport) {
    var Test = models.test;

    router.put('/test/send/', function (req, res) {
      console.log(ip.address());
      var test = new Test();
      test.doctor  = req.body.doctor;
      test.patient = req.body.patient;
      test.text    = req.body.test.textID;
      test.type    = req.body.test.type;
      test.result  = 5;

      test.save(function (err, test) {
        if (err) {
          res.status(500).json({error: 'Failed to create test'});
        }
        var link = 'http://' + ip.address() + ':8080/#/test/' + test._id;
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
