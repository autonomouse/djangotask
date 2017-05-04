app.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}]);

app.config(function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: '/static/partials/view.html',
            controller: 'controller',
            controllerAs:'controller'
        })
        .otherwise({
            redirectTo: '/'
        });
  });