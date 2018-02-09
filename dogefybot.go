package main

import (
	"fmt"
	"image"
	"image/color"

	"gocv.io/x/gocv"
)

// Cascade classifier parameters
const cc_scale_factor = 1.2
const cc_min_neighbors = 5
const cc_flags = 10 // CASCADE_SCALE_IMAGE | CASCADE_DO_ROUGH_SEARCH

var cc_min_size = image.Pt(20, 20)

// Contrast Limited Adaptive Histogram Equalization
const clahe = true
const clahe_clip = 3.0

var clahe_tile = image.Pt(8, 8)

// main
func main() {
	// Read image
	img := gocv.IMRead("test.jpg", 1)
	defer img.Close()

	// Convert to grayscale
	imgGray := gocv.NewMat()
	defer imgGray.Close()

	gocv.CvtColor(img, imgGray, gocv.ColorBGRToGray)

	/* GoCV doesn't support this yet
	   if clahe {
	           // c = gocv.CreateClahe(clahe_clip, clahe_tile)
	           // imgGray := c.Apply(imgGray)
	   } else {
	           // imgGray := gocv.EqualizeHist(imgGray)
	   }
	*/

	// Initialize the classifier
	classifier := gocv.NewCascadeClassifier()
	defer classifier.Close()

	classifier.Load("haarcascade_frontalface_alt_tree.xml")

	// Classify

	rects := classifier.DetectMultiScaleWithParams(
		imgGray,
		cc_scale_factor,
		cc_min_neighbors,
		cc_flags,
		cc_min_size,
		image.Pt(0, 0),
	)

	// Show the faces
	fmt.Printf("found %d faces\n", len(rects))

	window := gocv.NewWindow("Doges")
	defer window.Close()

	blue := color.RGBA{0, 0, 255, 0}

	for _, r := range rects {
		gocv.Rectangle(img, r, blue, 3)
	}

	window.IMShow(img)
	window.WaitKey(0)
}
