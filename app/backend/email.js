(function () {
  'use strict';
  var nodemailer = require('nodemailer'),
    transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: 'adosaur.noreply@gmail.com',
        pass: 'Adosaur123'
      }
    }, {
      // default values for sendMail method
      from: 'adosaur.noreply@gmail.com',
      headers: {
        'My-Awesome-Header': '123'
      }
    });

  // toy example
  // transporter.sendMail({
  //   to: 'tom.bartissol@gmail.com',
  //   subject: 'hello',
  //   text: 'hello world!'
  // });

  module.exports = transporter;
}());
