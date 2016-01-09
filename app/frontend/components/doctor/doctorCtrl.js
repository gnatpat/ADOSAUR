(function () {
  'use strict';
  var adosaur = angular.module('adosaur');
  adosaur.controller('doctorCtrl', ['$scope', '$stateParams', '$http',
    function ($scope, $stateParams, $http) {
      $scope.uid = $stateParams.uid;

      var rp = $http.get('/api/user/' + $scope.uid);
      rp.success(function (data, status, headers, config) {
        console.log('GOT USER!', data.user);
        $scope.patients = data.user.patients;
        $scope.texts = data.user.texts;
      });
      rp.error(function (data, status, headers, config) {
        console.log('an error occured');
      });
    }]);
}());
