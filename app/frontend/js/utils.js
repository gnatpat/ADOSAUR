(function () {
  'use strict';
  var app = angular.module('adosaur');

  app.factory('authService', ['$http', function ($http) {
    var
      authService = {},
      currentUser = {};

    authService.getCurrentUser = function (callback, error) {
      var responsePromise = $http.get('/api/users/current');

      responsePromise.success(function (data, status, headers, config) {
        currentUser = data;
        if (callback) {
          callback(currentUser);
        }
      });

      responsePromise.error(function (data, status, headers, config) {
        if (error) {
          error(data);
        }
      });
    };

    return authService;
  }]);
}());
