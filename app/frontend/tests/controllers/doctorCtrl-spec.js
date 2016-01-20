describe("doctorCtrl", function () {
  'use strict';
  var $rootScope,
    $scope,
    controller;

  beforeEach(function () {
    module('adosaur');

    inject(function ($injector) {
      $rootScope = $injector.get($rootScope);
      $scope = $rootScope.$new();
      controller = $injector.get('$controller')("doctorCtrl", {$scope: $scope});
    });
  });

  describe("Initialisation", function () {
    it("Should do something", function () {
      expect($scope.test).toEqual(1);
    });
  });
});
