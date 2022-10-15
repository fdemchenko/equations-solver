from typing import Union
from validator import Validator

class Polynomial:
    '''
        Polynomial with power 10
    '''
    polynomial_power: int = 10
    superscript_digits: list[str] = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']

    def __init__(self, coefficients: list[Union[int, float]] = None) -> None:
        '''
            Polynomial constructor. Set all coefficients to zero if input list is empty
            else takes first 11 numbers from input list. If given list length less than 11
            takes all list's elements and optionally zeros
        '''
        if coefficients:
            if not all(map(Validator.validate_float_number, coefficients)):
                self.coefficients = [0] * (self.polynomial_power + 1)
                raise TypeError('Invald type of coefficients')
            
            self.coefficients = list(map(float, coefficients[:self.polynomial_power + 1]))
            self.coefficients += [0] * (self.polynomial_power + 1 - len(coefficients))
        else:
            self.coefficients = [0] * (self.polynomial_power + 1)

    def __str__(self) -> str:
        '''
            String representation of polynomial
        '''
        string_representation: str = ''

        for index, coeff in enumerate(reversed(self.coefficients)):
            power = self.polynomial_power - index

            if power == 0 and coeff:
                if not string_representation:
                    if coeff < 0:
                        string_representation += f'-{abs(coeff)}'
                    else:
                        string_representation += f'{abs(coeff)}'
                else:
                    sign = '-' if coeff < 0 else '+'
                    string_representation += f' {sign} {abs(coeff)}'
            elif power == 10 and coeff:
                if coeff < 0:
                    string_representation += f'-{abs(coeff)}x{self.superscript_digits[1]}{self.superscript_digits[0]}'
                else:
                    string_representation += f'{abs(coeff)}x{self.superscript_digits[1]}{self.superscript_digits[0]}'
            elif power == 1 and coeff:
                if not string_representation:
                    if coeff < 0:
                        string_representation += f'-{abs(coeff)}x'
                    else:
                        string_representation += f'{abs(coeff)}x'
                else:
                    sign = '-' if coeff < 0 else '+'
                    string_representation += f' {sign} {abs(coeff)}x'
            elif coeff:
                if not string_representation:
                    if coeff < 0:
                        string_representation += f'-{abs(coeff)}x{self.superscript_digits[power]}'
                    else:
                        string_representation += f'{abs(coeff)}x{self.superscript_digits[power]}'
                else:
                    sign = '-' if coeff < 0 else '+'
                    string_representation += f' {sign} {abs(coeff)}x{self.superscript_digits[power]}'
        if not string_representation:
            string_representation += '0'

        return string_representation
                
    def get_value(self, x: Union[int ,float]) -> float:
        '''
            This method compute value of polynomial in given point
        '''
        if not Validator.validate_float_number(x):
            raise TypeError('Invald type of independent variable')
        return sum([coeff * x ** index for index, coeff in enumerate(self.coefficients)])

    @staticmethod
    def find_derivative(polynomial: 'Polynomial') -> 'Polynomial':
        '''
            This method evaluates derivative of given polynomial
        '''
        derivative_polynomial = Polynomial()
        for index, coef in enumerate(polynomial.coefficients):
            if index == 0:
                continue
            derivative_polynomial.coefficients[index - 1] = coef * index
        return derivative_polynomial


