(function(){
	angular.module("admin",[])
	.directive('productos', function() {
        return {
          restrict: 'E',
          templateUrl: '/static/directives/productos-main.html',
          controller: 'ProductosController',
        };
    })
    .directive('reportes', function() {
        return {
          restrict: 'E',
          templateUrl: '/static/directives/reportes.html',
          
        };
    })
    .controller('FlowController', function($scope) {
          $scope.flow = 0;
          $scope.changeFlow = function(value) {
             $scope.flow = value;
          }


    })
    .controller('ProductosController', function($scope, $http) {
          $scope.products = [
              {name:"bombillo", reference: "APK1025", price: 20000, image:"/static/images/bulb.jpg"},
              {name:"toilet", reference: "RJK10558", price: 40000, image:"/static/images/bath.jpg"},
              {name:"bombillo", reference: "APK1025", price: 20000, image:"/static/images/bulb.jpg"},
              {name:"toilet", reference: "RJK10558", price: 40000, image:"/static/images/bath.jpg"}
            ]

    })
    .config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  }])
})();