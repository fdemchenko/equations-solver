from typing import Dict, Union
from polynomial import Polynomial

class Solver:
    @staticmethod
    def bisection_method_solver(
            left_end: Union[int, float], rigth_end: Union[int, float], 
            eps: float, polynomial: Polynomial, max_iterations: int = 1000
        ) -> Dict:


        if eps <= 0:
            raise ValueError('Invalid value for epsilon! It must be greater than zero')
            
        results = {
            'root' : None,
            'approximate roots' : [],
            'iterations count' : None
        }
        
        if polynomial.get_value(left_end) * polynomial.get_value(rigth_end) >= 0:
            return results

        iterations_count = 1
        
        approximate_root = (left_end + rigth_end) / 2
        results['approximate roots'].append(approximate_root)
        while abs(polynomial.get_value(approximate_root)) >= eps and iterations_count < max_iterations:
            if polynomial.get_value(left_end) * polynomial.get_value(approximate_root) < 0:
                rigth_end = approximate_root
            elif polynomial.get_value(rigth_end) * polynomial.get_value(approximate_root) < 0:
                left_end = approximate_root
            else:
                raise RuntimeError('Impossible!')

            approximate_root = (left_end + rigth_end) / 2
            results['approximate roots'].append(approximate_root)
            iterations_count += 1
            
        results['root'] = approximate_root
        results['iterations_count'] = iterations_count

        return results

    @staticmethod
    def newton_method_solver(x0: Union[float, int], eps: float, polynomial: Polynomial, max_iterations: int = 1000) -> Dict:  
        x, x_prev, iterations_count = x0, x0 + 2 * eps, 0
        polynomial_derivative = Polynomial.find_derivative(polynomial)

        results = {
            'root' : None,
            'approximate_roots' : [],
            'iterations_count' : None
        }

        if eps <= 0:
            raise ValueError('Invalid value for epsilon! It must be greater than zero')

        while abs(x - x_prev) >= eps and iterations_count < max_iterations:
            try:
                x, x_prev = x - polynomial.get_value(x) / polynomial_derivative.get_value(x), x
                results['approximate_roots'].append(x)
                iterations_count += 1
            except ZeroDivisionError:
                return results

        results['iterations_count'] = iterations_count
        results['root'] = x

        return results

    @staticmethod
    def secants_method_solver(x0: Union[float, int], eps: float, polynomial: Polynomial, max_iterations: int = 1000) -> Dict:
        x, x_prev, iterations_count = x0, x0 + 2 * eps, 0
	
        if eps <= 0:
            raise ValueError('Invalid value for epsilon! It must be greater than zero')

        results = {
            'root' : None,
            'approximate_roots' : [],
            'iterations_count' : None
        }

        while abs(x - x_prev) >= eps and iterations_count < max_iterations:
            try:
                x, x_prev = x - polynomial.get_value(x) / (polynomial.get_value(x) - polynomial.get_value(x_prev)) * (x - x_prev), x
                results['approximate_roots'].append(x)
                iterations_count += 1
            except ZeroDivisionError:
                return results

        results['iterations_count'] = iterations_count
        results['root'] = x

        return results
