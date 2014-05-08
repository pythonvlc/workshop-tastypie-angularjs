'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
  .controller('MyCtrl1', ['$scope', 'Restangular', function($scope, Restangular) {
		Restangular.all('characters').getList().then(function(characters) {
	 		$scope.characters = characters;
		});

  }])
  .controller('MyCtrl2', ['$scope','character', function($scope, character) {
		$scope.character = character;
  }])
  .controller('New', ['$scope', 'Restangular',function($scope, Restangular) {
		
    $scope.addCharacter = function(){
        var character = {
            name: $scope.formCharacterName
        };
        Restangular.all('characters').post(character).then(function(result){
            console.log("saved", result);
        });

        $scope.formCharacterName = '';
    }
  }]);
