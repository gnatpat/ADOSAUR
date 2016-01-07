/*node: true*/
(function () {
  'use strict';
  var express  = require('express'),
    mongoose   = require('mongoose'), // for the database
    passport   = require('passport'), // for authentification
    session    = require('express-session'), // for authentification
    LocalStrat = require('passport-local'),  // for authentification
    models     = require('./models/models.js'), /* Setup mongoose models */
    app        = express(),
    server;

  /* connect to the mongodb database */
  mongoose.connect('mongodb://debug:adosaur@ds037005.mongolab.com:37005/adosaur');

  /* Session configuration (for authentication) */
  app.use(session({ secret: 'adosaur_secret_123', resave: true, saveUninitialized: true, cookie: { domain: ''}}));

  /* passport authentication configuration */
  app.use(passport.initialize());
  app.use(passport.session());
  passport.use('local', new LocalStrat(
    function (username, password, done) {
      console.log(username);
      models.user.findOne({ 'uid': username }, function (err, user) {
        if (err) { return done(err); }
        if (!user) {
          return done(null, false, { message: 'Incorrect username.' });
        }
        if (!user.validPassword(password)) {
          return done(null, false, { message: 'Incorrect password.' });
        }
        return done(null, user);
      });
    }
  ));

  /* Wire-up API routes */
  express.dirname = __dirname;
  require('./routes/routes.js')(app, express, models, passport);

  server = app.listen(8080, '127.0.0.1');
  console.log("ADOSAUR started at http://127.0.0.1:8080");
  console.log("Enjoy madafaka!!");
}());
