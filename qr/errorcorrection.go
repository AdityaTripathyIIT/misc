package main

import (
  "fmt"
)

var LOG [256]byte
var EXP [256]byte
/*
 Any number in a finite field(modulo a composite number) can be expressed as the a^n where a and n
 are numbers in the finite field. "a" is called a primitive element and is not unique, it has 
 phi(n) options from which we can choose.

 In GF(256) addition is a xor

 multiplications of the numbers x = a^n and y = a^m is a^(n+m % 255)

 We choose a = 2 as it is a valid and easy number to work with
*/
func multiply(a byte, b byte) byte {
  if (a == 0 && b == 0) {
    return 0
  } else {
    return EXP[(LOG[a] + LOG[b]) % 255]
  }
} 

func divide(a byte, b byte) byte {
  if (LOG[a] >= LOG[b]){
    return EXP[(LOG[a] - LOG[b]) % 255]
  } else {
    return EXP[(LOG[b] - LOG[a]) % 255]
  }
}

func multiply_polynomials(polynomial_1 []byte, polynomial_2 []byte)  []byte {
  polynomial_3 := make([]byte, len(polynomial_1) + len(polynomial_2) - 1)
  
  for i := 0; i < len(polynomial_3); i++ {
    polynomial_3[i] = 0
  }

  for i := 0; i < len(polynomial_1); i++ {
    for j := 0; j < len(polynomial_2); j++ {
      //polynomial_3[i + j] ^= multiply(polynomial_1[i],  polynomial_2[j])
      polynomial_3[i + j] += polynomial_1[i] * polynomial_2[j]
    }
  }

  return polynomial_3
}

/*
func get_error_correction_bytes()
*/


func main(){
  /*
  * Initialize the LOG and EXP arrays 
  */

  working_value := byte(1)

  for exponent := byte(0); exponent <= 255; exponent++ {
    if working_value < 128 {
      working_value = working_value << 1
    } else {
      working_value = byte(int((working_value << 1)) ^ 285) //explanation needed
    }
    
    //Explain why (% 255) is needed (check if it works without it)
    LOG[working_value] = exponent % 255
    EXP[exponent % byte(255)] = working_value
    if (exponent == 255) {
      break
    }
  }

  arr1 := []byte{1, 2, 3, 4}
  arr2 := []byte{2, 3, 4, 5}
  fmt.Println(multiply_polynomials(arr1, arr2))

}
