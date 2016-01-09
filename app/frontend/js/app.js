/*global angular, console*/
(function () {
  'use strict';
  var adosaur = angular.module('adosaur', ['ui.router', 'ngFileUpload', 'flash']);

  adosaur.controller('indexCtrl', ['$scope', 'authService', '$http', '$window', '$state',
    function ($scope, authService, $http, $window, $state) {
      authService.getCurrentUser(function (user) {
        console.log(user);
        $scope.user = user;
      }, function (data) {
        console.log('Ajax request failed');
      });

      $scope.logout = function () {
        var rp = $http.get('/api/logout');
        rp.success(function (data, status, headers, config) {
          $state.go('home');
          $window.location.reload();
        });
        rp.error(function (data, status, headers, config) {
          $state.go('home');
          $window.location.reload();
        });
      };
    }]);
}());
