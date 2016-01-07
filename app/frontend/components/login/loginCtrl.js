(function () {
  'use strict';
  var adosaur = angular.module('adosaur');
  adosaur.controller('loginCtrl', ['$scope', '$http', function ($scope, $http) {

    // var rp = $http({
    //   method: 'PUT',
    //   url: '/api/user/new',
    //   data: {uid: "sc8013", pwd: "adosaur", email: "sc8013@ic.ac.uk", doctor: true}
    // });
    // rp.success(function (data, status, headers, config) {
    //   console.log('success');
    //   console.log(data);
    // });
    // rp.error(function (data, status, headers, config) {
    //   console.log('Ajax request failed for PUT users');
    // });
  }]);
}());
