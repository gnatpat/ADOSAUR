/*node: true*/
(function () {
  'use strict';
  var express    = require('express'),
    morgan       = require('morgan'),
    bp           = require('body-parser'),
    cookieParser = require('cookie-parser'),
    mongoose     = require('mongoose'), // for the database
    passport     = require('passport'), // for authentification
    session      = require('express-session'), // for authentification
    models       = require('./models/models.js'), /* Setup mongoose models */
    app          = express(),
    server;

  /* Logging http requests*/
  app.use('/api/', morgan('dev'));
  /* to read json */
  app.use(bp.json());
  /* parse application/x-www-form-urlencoded */
  app.use(bp.urlencoded({ extended: false }));
  /* to read cookies */
  app.use(cookieParser());
  /* connect to the mongodb database */
  mongoose.connect('mongodb://debug:adosaur@ds037005.mongolab.com:37005/adosaur');

  /* Session configuration (for authentication) */
  app.use(session({ secret: 'adosaur_secret_123', resave: true, saveUninitialized: true, cookie: { domain: ''}}));

  /* passport authentication configuration */
  require('./config/passport.js')(passport, models);
  app.use(passport.initialize());
  app.use(passport.session());

  /* Wire-up API routes */
  express.dirname = __dirname;
  require('./routes/routes.js')(app, express, models, passport);

  server = app.listen(8080, '127.0.0.1');
  console.log("ADOSAUR started at http://127.0.0.1:8080");
  console.log("Try to be a rainbow in someone's cloud!");
}());
