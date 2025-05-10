package main

import (
  "fmt"
)

func RK4(initPoint [2]float64, xlim [2]float64, rhsFunc func(float64, float64)float64, numPoints int) []float64{
  
  points := make([]float64, 2 * numPoints)
  x_0 = initPoint[0]
  y_0 = initPoint[1]

  h := (xlim[1] - xlim[2]) / numPoints
  for i in range numPoints{
    points.append(x_0)
    points.append(y_0)
    
    k_1 = rhsFunc(x_0, y_0)
    k_2 = rhsFunc(x_0 + 0.5 * h, y_0 + 0.5 * h * k_1)
    k_3 = rhsFunc(x_0 + 0.5 * h, y_0 + 0.5 * h * k_2)
    k_4 = rhsFunc(x_0 + h, y_0 + h * k_3)

    y_0 += h * (k_1 + 2 * k_2 + 2 * k_3 + k_4)/6 
    x_0 += h
  }
  
  return points
}
