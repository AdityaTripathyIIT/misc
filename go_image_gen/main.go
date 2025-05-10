package main

import (
  "image"
  "image/color"
  "image/png"
  "log"
  "fmt"
  "os"
  "math"
  "strconv"
)

type imageGenErr struct {
  where string
}

func (e *imageGenErr) Error() string{
  return fmt.Sprintf("at %s\n", e.where)
}

func maskGenerator(mask_num byte, imageContainer *image.RGBA) error{
  if mask_num > 7 {
    return &imageGenErr{
      "maskGenerator - invalid mask num",
    }
  } else {
    switch mask_num {
    case 0 :
      for i := range (imageContainer.Bounds()).Dx() {
        for j := range (imageContainer.Bounds()).Dy() {
          if (i + j) % 2 == 0 {
            imageContainer.Set(i, j, color.RGBA{0, 0, 0, 255})
          } else {
            imageContainer.Set(i, j, color.RGBA{255, 255, 255, 255})
          }
        }
      }
    case 1 :
      for i := range (imageContainer.Bounds()).Dx() {
        for j := range (imageContainer.Bounds()).Dy() {
          if (j) % 2 == 0 {
            imageContainer.Set(i, j, color.RGBA{0, 0, 0, 255})
          } else {
            imageContainer.Set(i, j, color.RGBA{255, 255, 255, 255})
          }
        }
      }
    case 2 :
      for i := range (imageContainer.Bounds()).Dx() {
        for j := range (imageContainer.Bounds()).Dy() {
          if (i) % 3 == 0 {
            imageContainer.Set(i, j, color.RGBA{0, 0, 0, 255})
          } else {
            imageContainer.Set(i, j, color.RGBA{255, 255, 255, 255})
          }
        }
      }
    case 7 :
      for i := range (imageContainer.Bounds()).Dx() {
        for j := range (imageContainer.Bounds()).Dy() {
          if ((i + j ) % 2  + i * (j % 3)) % 2 == 0 {
            imageContainer.Set(i, j, color.RGBA{0, 0, 0, 255})
          } else {
            imageContainer.Set(i, j, color.RGBA{255, 255, 255, 255})
          }
        }
      }
    case 3 :
      for i := range (imageContainer.Bounds()).Dx() {
        for j := range (imageContainer.Bounds()).Dy() {
          if ((i + j ) % 3) == 0 {
            imageContainer.Set(i, j, color.RGBA{0, 0, 0, 255})
          } else {
            imageContainer.Set(i, j, color.RGBA{255, 255, 255, 255})
          }
        }
      }
    case 4 :
      for i := range (imageContainer.Bounds()).Dx() {
        for j := range (imageContainer.Bounds()).Dy() {
          if int32((math.Floor(float64(j) / 2))  + (math.Floor(float64(i) / 3))) % 2 == 0 {
            imageContainer.Set(i, j, color.RGBA{0, 0, 0, 255})
          } else {
            imageContainer.Set(i, j, color.RGBA{255, 255, 255, 255})
          }
        }
      }
    case 5 :
      for i := range (imageContainer.Bounds()).Dx() {
        for j := range (imageContainer.Bounds()).Dy() {
          if ((i * j) % 2 + i * (j % 3)) == 0 {
            imageContainer.Set(i, j, color.RGBA{0, 0, 0, 255})
          } else {
            imageContainer.Set(i, j, color.RGBA{255, 255, 255, 255})
          }
        }
      }
    case 6 :
      for i := range (imageContainer.Bounds()).Dx() {
        for j := range (imageContainer.Bounds()).Dy() {
          if ((i * j) % 2  + i * (j % 3)) % 2 == 0 {
            imageContainer.Set(i, j, color.RGBA{0, 0, 0, 255})
          } else {
            imageContainer.Set(i, j, color.RGBA{255, 255, 255, 255})
          }
        }
      }
    }
  }
  return nil
}


func main(){
  width, height := 100, 100
  base := image.NewRGBA(image.Rect(0, 0, width, height))

  for i := range 8{
    err := maskGenerator(byte(i), base)
    if err != nil {
      log.Fatal(err)
      return 
    }

    file, err := os.Create("mask_" + strconv.Itoa(i) + ".png")

    if err != nil {
      log.Fatal(err)
      return 
    }

    if err := png.Encode(file, base); err != nil {
      file.Close()
      log.Fatal(err)
    }

    if err := file.Close(); err != nil {
      log.Fatal(err)
    } 

  }
}
