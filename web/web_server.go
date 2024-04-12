package main

import (
	"errors"
	"io"
	"log"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

func search_image(c *gin.Context) {
	form, err := c.MultipartForm()
	if err != nil {
		c.String(http.StatusBadRequest, "get form err: %s", err.Error())
		return
	}
	file := form.File["images"][0]

	log.Printf(file.Filename)
	filename, err := saveImage(c, file, IMAGEPATH)
	if err != nil {
		c.String(http.StatusBadRequest, "search file %s err: %s", file.Filename, err)
		return
	}

	res, err := http.Get("http://127.0.0.1:12345/search/" + filename)
	if err != nil {
		c.String(http.StatusInternalServerError, "search file %s err:%s", err)
		return
	}
	body, err := io.ReadAll(res.Body)
	if err != nil {
		c.String(http.StatusInternalServerError, "search file %s err:%s", err)
		return
	}
	c.String(http.StatusOK, string(body))

}

func upload_image(c *gin.Context) {
	form, err := c.MultipartForm()
	if err != nil {
		c.String(http.StatusBadRequest, "get form err: %s", err.Error())
		return
	}
	files := form.File["images"]

	for _, file := range files {
		log.Printf(file.Filename)
		filename, err := saveImage(c, file, IMAGEPATH)
		if err != nil {
			c.String(http.StatusBadRequest, "upload file %s err: %s", file.Filename, err.Error())
			continue
		}

		if !processImage(filename) {
			c.String(http.StatusBadRequest, "process %s file err", file.Filename)
			os.Remove(IMAGEPATH + filename)
			continue
		}
	}
}

func isImage(ext string) bool {
	switch ext {
	case ".jpg":
		return true
	case ".jpeg":
		return true
	case ".png":
		return true
	default:
		return false
	}
}

func processImage(filename string) bool {
	res, err := http.Get("http://127.0.0.1:12345/process/" + filename)
	if err != nil {
		return false
	}

	if res.StatusCode != http.StatusOK {
		return false
	}

	return true
}

func saveImage(ctx *gin.Context, file *multipart.FileHeader, path string) (string, error) {
	ext := filepath.Ext(file.Filename)
	if !isImage(ext) {
		return "", errors.New("file extension error")
	}
	filename := uuid.NewString() + ext
	return filename, ctx.SaveUploadedFile(file, path+filename)
}
