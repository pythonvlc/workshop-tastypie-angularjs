'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
  'myApp.filters',
  'myApp.services',
  'myApp.directives',
  'myApp.controllers',
  'restangular'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {templateUrl: 'partials/partial1.html', controller: 'MyCtrl1'});
  $routeProvider.when('/characters/new', {templateUrl: 'partials/partial3.html', controller: 'New'});
  $routeProvider.when('/characters/:characterId', {
  	templateUrl: 'partials/partial2.html', 
  	controller: 'MyCtrl2',
    resolve: {
      character: function(Restangular, $route){
        return Restangular.one('characters', $route.current.params.characterId).get();
      }
    }
  });

  $routeProvider.otherwise({redirectTo: '/view1'});
}]).

config(['RestangularProvider', function(RestangularProvider) {
	RestangularProvider.setBaseUrl('http://127.0.0.1:8000/api/v1');
	RestangularProvider.setDefaultRequestParams({format:"json"});
    RestangularProvider.setRestangularFields({
      selfLink: "self.resource_uri"
    });

	RestangularProvider.setResponseExtractor(function(response, operation, what, url) {
	console.log(response);
	console.log(url);
	var newResponse;
	if (operation === "getList") {
	    newResponse = response.objects;
	    newResponse.metadata = response.meta;
	} else {
	    newResponse = response;
	}
	return newResponse;
	});

}]);
