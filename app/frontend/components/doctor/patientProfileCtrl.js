(function () {
  'use strict';
  var adosaur = angular.module('adosaur');
  adosaur.controller('patientProfileCtrl', ['$scope', 'util', '$stateParams',
    function ($scope, util, $stateParams) {
      console.log('IN Patient Profile controller');

      util.getPatient($stateParams.pid, function (res) {
        $scope.patient = res.user;
        console.log($scope.patient._id);
        util.getPatientTests($scope.patient._id, function (data) {
          $scope.tests = data.tests;
          console.log($scope.tests);
        });
      });
    }]);
}());
