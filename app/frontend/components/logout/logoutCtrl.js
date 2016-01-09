/*global angular, console */
(function () {
  'use strict';

  var app = angular.module('adosaur');

  app.controller('logoutCtrl', ['$scope', '$http', '$window', function ($scope, $http, $window) {
    var responsePromise = $http.get('/api/logout');

    responsePromise.success(function (data, status, headers, config) {
      $window.location.href = '/';
    });

    responsePromise.error(function (data, status, headers, config) {
      console.log('Ajax request failed');
    });

  }]);
}());
