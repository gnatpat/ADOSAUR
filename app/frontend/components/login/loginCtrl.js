(function () {
  'use strict';
  var adosaur = angular.module('adosaur');
  adosaur.controller('loginCtrl', ['$scope', '$http', '$location', 'Flash',
    function ($scope, $http, $location, Flash) {
      var err = $location.search().err,
        errMsg = "";
      if (err === "1") {
        errMsg = "This username does not exist, please try again";
        Flash.create('danger', errMsg);
      }
      if (err === "2") {
        errMsg = "<strong>Wrong</strong> password, please try again";
        Flash.create('danger', errMsg);
      }
    }]);
}());
